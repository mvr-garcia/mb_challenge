import requests


def request_data(coin, past, now):
    """
    Receive and treats BTC/ETH Candles data from Mercado Bitcoin Candles API
    """
    url = f'https://mobile.mercadobitcoin.com.br/v4/{coin}/candle?from={past}&to={now}&precision=1d'
    response = requests.get(url)
    candles = response.json()

    return candles


def sma_calc(candle_list, period_qty):
    """
    Calculate the SMA 20 period.
    """
    period_sum = 0.0
    for candle in candle_list:
        period_sum += candle["close"]

    result = period_sum / period_qty

    return result
