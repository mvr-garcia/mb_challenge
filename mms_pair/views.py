from django.shortcuts import render
from .helpers import request_data, sma_calc
from .models import Coin
from django.db import IntegrityError
import datetime
import time


def load_coin():
    """Called by ready() function inside apps.py when server is sarted.
    In case there is no data, the function loads data from the last 365 days."""

    # Set the date now = yesterday ; past = 365 days ago plus 200 days to permit calculate 200_sma
    now = datetime.date.today() - datetime.timedelta(days=1)
    past = now - datetime.timedelta(days=365 + 200)

    # Convert date to timestamp
    now = int(time.mktime(datetime.datetime.strptime(str(now), "%Y-%m-%d").timetuple()))
    past = int(time.mktime(datetime.datetime.strptime(str(past), "%Y-%m-%d").timetuple()))

    return insert_data(past, now)


def update_coin():
    """Called by ready() function inside apps.py when server is sarted.
    Every day will update the database for the last day candle not existing in register."""

    # First it arranges the timestamp attribute in a descending way and
    # takes the first item, this is the most recent day in the database.
    last_obj = Coin.objects.all().order_by("-timestamp")[0]
    print(last_obj.timestamp)

    # Convert timestamp to date and increment 200 days to allow sma200 calc.
    past = datetime.date.fromtimestamp(last_obj.timestamp)
    past = past - datetime.timedelta(days=200)

    # Set the date now = yesterday ; past = 365 days ago plus 200 days to permit calculate 200_sma
    now = datetime.date.today() - datetime.timedelta(days=1)

    # Convert date to timestamp
    now = int(time.mktime(datetime.datetime.strptime(str(now), "%Y-%m-%d").timetuple()))
    past = int(time.mktime(datetime.datetime.strptime(str(past), "%Y-%m-%d").timetuple()))

    return insert_data(past, now)


def insert_data(past, now):
    """Function responsible for populating/update the database"""

    # Set default cryptocurrencies that will be treat
    cryptos = ["BRLBTC", "BRLETH"]

    for crypto in cryptos:

        candles = request_data(crypto, past, now)
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


def verify_db():
    coins = Coin.objects.all().count()

    # If database is empty, call the load_coin function
    if coins == 0:
        load_coin()
    # Else, call the update_coin function to update the database to the latest available date
    else:
        update_coin()


def index(request):
    """"""
    verify_db()

    pair = Coin.objects.filter(pair="BRLBTC").order_by("-timestamp")
    context = {'pair': pair}

    return render(request, 'mms_pair/index.html', context)
