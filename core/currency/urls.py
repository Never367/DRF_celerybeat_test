from django.urls import path
from .views import (
    LastRatesAPIView,
    CurrencyListToAddAPIView,
    SwitchMonitoringCurrencyView,
    AddToActiveCurrencyView,
    CurrencyRateAtTimeView,
)

# url for api
urlpatterns = [
    path(
        'add-currency-to-active/',
        AddToActiveCurrencyView.as_view(),
        name='add-currency-to-active'
    ),
    path(
        'last_rates/',
        LastRatesAPIView.as_view(),
        name='last_rates'
    ),
    path(
        'switch-monitoring-currency/',
        SwitchMonitoringCurrencyView.as_view(),
        name='switch-monitoring-currency'
    ),
    path(
        'currency-rate-at-time/',
        CurrencyRateAtTimeView.as_view(),
        name='currency-rate-at-time'
    ),
    path(
        'get_currency_list_to_add/',
        CurrencyListToAddAPIView.as_view(),
        name='get_currency_list_to_add'
    ),
]
