from datetime import datetime

import pycountry
import requests
from celery import shared_task
from django.db.models.functions import TruncMinute

from currency.models import Currency, CurrencyRate
from utils.fix_currency_code import fix_currency_code


@shared_task
def fetch_currency_rates() -> None:
    # Task celery to retrieve currencies and exchange rates via API
    # Works every 5 minutes (crontab(minute='*/5'))
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for rate in data:
            rate = fix_currency_code(rate)
            currency_name_1 = pycountry.currencies.get(
                numeric=str(rate['currencyCodeA'])
            ).alpha_3
            currency_name_2 = pycountry.currencies.get(
                numeric=str(rate['currencyCodeB'])
            ).alpha_3
            currency_1 = Currency.objects.get_or_create(
                name=currency_name_1
            )[0]
            currency_2 = Currency.objects.get_or_create(
                name=currency_name_2
            )[0]
            if currency_1.is_active is True and currency_2.is_active is True:
                CurrencyRate.objects.create(
                    currency_1=currency_1,
                    currency_2=currency_2,
                    date=TruncMinute(datetime.now()),
                    rate_buy=rate.get('rateBuy'),
                    rate_sell=rate.get('rateSell'),
                    rate_cross=rate.get('rateCross')
                )
