from typing import Union

from rest_framework import request, status
from rest_framework.response import Response

from currency.models import Currency
from currency.serializers import CurrencySerializer
from utils.message_response import APIErrorMessage, APISuccessMessage


def create_instance(
        request_data: request.Request
) -> Union[Response, Currency]:
    # Instance creation
    try:
        instance = Currency.objects.get(
            name=request_data.data.get('name')
        )
    except Currency.DoesNotExist:
        return Response({
            'error': APIErrorMessage.MESSAGE_ERROR_NOT_EXIST
        })
    return instance


def save_serializer_and_response(
        request_data: request.Request,
        instance: Currency
) -> Response:
    # Saving the serializer, checking for validity and server response
    serializer = CurrencySerializer(
        data=request_data.data,
        instance=instance
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        APISuccessMessage.MESSAGE_SUCCESS_CURRENCY_CHANGED,
        status=status.HTTP_200_OK
    )
