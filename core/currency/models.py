from django.db import models


class Currency(models.Model):
    # Currency model
    name = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=False)
    is_monitoring = models.BooleanField(default=False)


class CurrencyRate(models.Model):
    # CurrencyRate model
    currency_1 = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='currency'
    )
    currency_2 = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    rate_buy = models.FloatField(null=True, blank=True)
    rate_sell = models.FloatField(null=True, blank=True)
    rate_cross = models.FloatField(null=True, blank=True)
