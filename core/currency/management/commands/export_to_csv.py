import csv
from django.core.management.base import BaseCommand
from django.db.models import OuterRef, Subquery

from currency.models import CurrencyRate


class Command(BaseCommand):
    # create csv file with a list of currencies and current exchange rate
    help = 'Export currency rates to CSV file'

    def handle(self, *args, **kwargs) -> None:
        with open('currency_rates.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Currency_1',
                'Currency_2',
                'Date',
                'Rate Buy',
                'Rate Sell',
                'Rate Cross'
            ])
            subquery = CurrencyRate.objects.filter(
                currency_1=OuterRef('currency_1'),
                currency_2=OuterRef('currency_2')
            ).order_by('-date')
            queryset = CurrencyRate.objects.filter(
                pk=Subquery(subquery.values('pk')[:1]),
                currency_1__is_monitoring=True,
                currency_2__is_monitoring=True
            ).select_related('currency_1', 'currency_2')
            for rate in queryset:
                writer.writerow([
                    rate.currency_1.name,
                    rate.currency_2.name,
                    rate.date,
                    rate.rate_buy,
                    rate.rate_sell,
                    rate.rate_cross
                ])
