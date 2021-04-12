from django.db import IntegrityError
from .models import Coin
import requests
import datetime
import time


def load_coin():
    """Called by ready() function inside apps.py when server is sarted.
    In case there is no data, the function loads data from the last 365 days."""

    # Set the date now = yesterday ; past = 365 days ago plus 200 days to permit calculate 200_sma
    now = datetime.date.today() - datetime.timedelta(days=1)
    past = now - datetime.timedelta(days=365 + 200)

    # Convert date to timestamp
    now, past = date2timestamps(now, past)

    return insert_data(past, now)


def update_coin():
    """Called by ready() function inside apps.py when server is sarted.
    Every day will update the database for the last day candle not existing in register."""

    # First it arranges the timestamp attribute in a descending way and
    # takes the first item, this is the most recent day in the database.
    last_obj = Coin.objects.all().order_by("-timestamp")[0]

    # Convert timestamp to date and increment 200 days to allow sma200 calc.
    past = datetime.date.fromtimestamp(last_obj.timestamp)
    past = past - datetime.timedelta(days=200)

    # Set the date now = yesterday ; past = 365 days ago plus 200 days to permit calculate 200_sma
    now = datetime.date.today() - datetime.timedelta(days=1)

    # Convert date to timestamp
    now, past = date2timestamps(now, past)

    return insert_data(past, now)


def date2timestamps(now, past):
    """Convert date format "%Y-%m-%d" to timestamps"""
    now = int(time.mktime(datetime.datetime.strptime(str(now), "%Y-%m-%d").timetuple()))
    past = int(time.mktime(datetime.datetime.strptime(str(past), "%Y-%m-%d").timetuple()))
    return now, past


def insert_data(past, now):
    """Function responsible for populating/update the database"""

    # Set default cryptocurrencies that will be treat
    cryptos = ["BRLBTC", "BRLETH"]

    for crypto in cryptos:

        candles = request_data(crypto, past, now)

        # If the API is unavailable candles will receive None.
        # In this case, I do not need to proceed with data entry.
        if candles is not None:
            daily_candles = candles["candles"]

            for i, day in enumerate(daily_candles):
                # We have to ignore the first 200 days of the loop. The 200 days will be used only
                # for the purposes of calculating the 200 mms of the first day.
                if i > 199:
                    try:
                        coin = Coin()
                        coin.timestamp = day['timestamp']
                        coin.pair = crypto
                        # Silicing items for simple movin average calculate
                        coin.mms_20 = sma_calc(daily_candles[i-19:i + 1], 20)
                        coin.mms_50 = sma_calc(daily_candles[i-49:i + 1], 50)
                        coin.mms_200 = sma_calc(daily_candles[i-199:i + 1], 200)
                        coin.save()
                    # Exception will be raise when a duplicate register try to save in DataBase
                    # We don't make anything, just don't save it.
                    except IntegrityError:
                        pass


def day_missing():
    """The function examines the database and issues an alert
    if any day is missing from the records of the last 365 days"""

    cryptos = ['BRLBTC', 'BRLETH']

    for crypto in cryptos:
        # Organizes the timestamp from the oldest to the newest and assigns it to a variable.
        coin = Coin.objects.filter(pair=crypto).order_by("timestamp")
        last_date = ""
        for k, v in enumerate(coin):

            day_coin = v.timestamp
            day_coin = datetime.date.fromtimestamp(day_coin)

            # In the first loop, last day receveive current date loop less 1 day
            if k == 0:
                last_date = day_coin - datetime.timedelta(days=1)

            # Checks database consistency
            if day_coin != last_date + datetime.timedelta(days=1):
                # If the date in the current loop isn't consecutive to
                # the date in the previous loop, there is a record gap.
                print(f"Between data {last_date} and {day_coin} in the crypto {crypto}, there are missing records.")

            last_date = last_date + datetime.timedelta(days=1)


def request_data(coin, past, now):
    """
    Receive and treats BTC/ETH Candles data from Mercado Bitcoin Candles API
    """
    url = f'https://mobile.mercadobitcoin.com.br/v4/{coin}/candle?from={past}&to={now}&precision=1d'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        print(f"\nThe Bitcoin Market candles API for {coin} crypto is not available to load/update the database.")
        return None
    else:
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
