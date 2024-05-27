import datetime

from django.db.models import OuterRef, Subquery, QuerySet
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import request, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Currency, CurrencyRate
from .serializers import (
    CurrencySerializer,
    CurrencyRateSerializer,
    AddToActiveRequestSerializer,
    SwitchMonitoringRequestSerializer
)
from utils.message_response import APIErrorMessage, APIDetailMessage
from utils.utils import create_instance, save_serializer_and_response


class LastRatesAPIView(APIView):
    # get a list of currencies with the current exchange rate
    @staticmethod
    def get(request_data: request.Request) -> Response:
        subquery = CurrencyRate.objects.filter(
            currency_1=OuterRef('currency_1'),
            currency_2=OuterRef('currency_2')
        ).order_by('-date')

        queryset = CurrencyRate.objects.filter(
            pk=Subquery(subquery.values('pk')[:1]),
            currency_1__is_monitoring=True,
            currency_2__is_monitoring=True
        ).select_related('currency_1', 'currency_2')

        serializer = CurrencyRateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrencyListToAddAPIView(APIView):
    # get a list of currencies that can be added for tracking
    @staticmethod
    def get(request_data: request.Request) -> Response:
        queryset = Currency.objects.filter(is_active=False)

        serializer = CurrencySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToActiveCurrencyView(APIView):
    # add a new currency to track
    @staticmethod
    @swagger_auto_schema(
        request_body=AddToActiveRequestSerializer,
        responses={200: CurrencySerializer(many=True)}
    )
    def put(request_data: request.Request) -> Response:
        instance = create_instance(request_data)

        if 'is_active' not in request_data.data:
            return Response({
                'error': APIErrorMessage.MESSAGE_ERROR_IS_ACTIVE_REQUIRED
            })
        elif instance.is_active is True:
            return Response({
                'error': APIErrorMessage.MESSAGE_ERROR_CURRENCY_ALREADY_ACTIVE
            })
        elif 'is_monitoring' in request_data.data:
            return Response({
                'error': APIErrorMessage.MESSAGE_ERROR_MONITORING_NOT_ALLOWED
            })

        return save_serializer_and_response(
            request_data,
            instance
        )


class SwitchMonitoringCurrencyView(APIView):
    # switching on/off a currency from monitoring
    @staticmethod
    @swagger_auto_schema(
        request_body=SwitchMonitoringRequestSerializer,
        responses={200: CurrencySerializer(many=True)}
    )
    def put(request_data: request.Request) -> Response:
        instance = create_instance(request_data)

        if 'is_monitoring' not in request_data.data:
            return Response({
                'error': APIErrorMessage.MESSAGE_ERROR_IS_MONITORING_REQUIRED
            })
        elif 'is_active' in request_data.data:
            return Response({
                'error': APIErrorMessage.MESSAGE_ERROR_ACTIVE_NOT_ALLOWED
            })
        elif instance.is_active is False:
            return Response({
                'error': APIErrorMessage.MESSAGE_ERROR_CURRENCY_NOT_ACTIVE
            })

        try:
            request_data.data._mutable = True
            request_data.data['is_active'] = True
        except AttributeError:
            pass

        return save_serializer_and_response(
            request_data,
            instance
        )


class CurrencyRateAtTimeView(generics.RetrieveAPIView):
    # get exchange rate history for a specific currency / period of time
    serializer_class = CurrencyRateSerializer

    def get_queryset(self) -> QuerySet:
        currency_1_name = self.request.query_params.get('currency_1')
        currency_2_name = self.request.query_params.get('currency_2')
        timestamp = self.request.query_params.get('timestamp')

        if not (currency_1_name and currency_2_name and timestamp):
            return CurrencyRate.objects.none()

        try:
            timestamp = int(timestamp)
            target_datetime = timezone.make_aware(
                datetime.datetime.fromtimestamp(timestamp)
            )
        except (ValueError, OSError):
            return CurrencyRate.objects.none()

        queryset = CurrencyRate.objects.filter(
            currency_1__name=currency_1_name,
            currency_2__name=currency_2_name,
            date__lte=target_datetime
        ).order_by('-date')

        if len(queryset) == 0:
            queryset = CurrencyRate.objects.filter(
                currency_1__name=currency_2_name,
                currency_2__name=currency_1_name,
                date__lte=target_datetime
            ).order_by('-date')

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'currency_1',
                openapi.IN_QUERY,
                description="Name of the first currency",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'currency_2',
                openapi.IN_QUERY,
                description="Name of the second currency",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'timestamp',
                openapi.IN_QUERY,
                description="Unix time",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(
            self,
            request_data: request.Request,
            *args,
            **kwargs
    ) -> Response:
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                "detail": APIDetailMessage.MESSAGE_NO_DATA_CRITERIA
            }, status=status.HTTP_404_NOT_FOUND)
        instance = queryset.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
