from typing import Any

from rest_framework import serializers
from .models import Currency, CurrencyRate


class CurrencySerializer(serializers.ModelSerializer):
    # Serialization of currency data
    class Meta:
        model = Currency
        fields = '__all__'

    def update(
            self,
            instance: Currency,
            validated_data: dict[str, Any]
    ) -> Currency:
        # Update currency data
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get(
            'is_active',
            instance.is_active
        )
        instance.is_monitoring = validated_data.get(
            'is_monitoring',
            instance.is_monitoring
        )
        instance.save()
        return instance


class CurrencyRateSerializer(serializers.ModelSerializer):
    # Serialization of currency_rate data
    currency_1 = CurrencySerializer()
    currency_2 = CurrencySerializer()

    class Meta:
        model = CurrencyRate
        fields = [
            'id',
            'date',
            'rate_buy',
            'rate_sell',
            'rate_cross',
            'currency_1',
            'currency_2'
        ]


class AddToActiveRequestSerializer(serializers.Serializer):
    # Serialization of add_to_active_request data
    name = serializers.CharField(required=True, max_length=100)
    is_active = serializers.BooleanField(required=True)


class SwitchMonitoringRequestSerializer(serializers.Serializer):
    # Serialization of switch_monitoring_request data
    name = serializers.CharField(required=True, max_length=100)
    is_monitoring = serializers.BooleanField(required=True)
