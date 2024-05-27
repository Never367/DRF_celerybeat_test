from typing import Union


def fix_currency_code(
    rate: dict[str, Union[int, float, str]]
) -> dict[str, Union[int, float, str]]:
    # Fixing currency code from API
    rate['currencyCodeA'] = str(rate['currencyCodeA'])
    rate['currencyCodeB'] = str(rate['currencyCodeB'])

    if (
            len(rate['currencyCodeA']) < 3 or
            len(rate['currencyCodeB']) < 3
    ):
        if len(rate['currencyCodeA']) == 2:
            rate['currencyCodeA'] = f'0{rate["currencyCodeA"]}'
        if len(rate['currencyCodeB']) == 2:
            rate['currencyCodeB'] = f'0{rate["currencyCodeB"]}'
        if len(rate['currencyCodeA']) == 1:
            rate['currencyCodeA'] = f'00{rate["currencyCodeA"]}'
        if len(rate['currencyCodeB']) == 1:
            rate['currencyCodeB'] = f'00{rate["currencyCodeB"]}'
    return rate
