from rest_framework import generics
from rest_framework.exceptions import NotAcceptable
from mms_pair.models import Coin
from . import serializers
import datetime
import time


class CoinListView(generics.ListAPIView):
    serializer_class = serializers.CoinSerializer
    queryset = Coin.objects.all()


class CryptoListView(generics.ListAPIView):

    def get_serializer_class(self):

        # If the resquest don't pass the range, API return all 3 mms
        if 'mms' not in self.kwargs.keys():
            return serializers.CoinSerializer

        # If the request has the mms attribute, it checks whether
        # it is valid and passes the corresponding serializer.
        mms = self.kwargs['mms']
        if mms == 20:
            return serializers.CoinMms20Serializer
        elif mms == 50:
            return serializers.CoinMms50Serializer
        elif mms == 200:
            return serializers.CoinMms200Serializer
        # If it is an invalid mms, raise an exception.
        raise NotAcceptable("Request range Movin average isn't allowed. Choose between 20, 50, 200 range.")

    def get_queryset(self):
        """This view should return a list of all the crypto in specific timestamp range."""
        pair = self.kwargs['crypto']

        # Pair name validate
        if pair.upper() not in ['BRLBTC', 'BRLETH']:
            raise NotAcceptable("Request crypto isn't allowed. Choose between BRLBTC and BRLETH")

        # Checks if the request start date is less than 365 days.
        # First: Finds the 365 day timestamps.
        past = datetime.date.today() - datetime.timedelta(days=365 + 1)
        past = int(time.mktime(datetime.datetime.strptime(str(past), "%Y-%m-%d").timetuple()))

        # Second: If past is less then request start date, request isn't allowed
        if self.kwargs['past'] < past:
            raise NotAcceptable("Request start date less than 365 days isn't allowed")
        else:
            past = self.kwargs['past']

        # If 'now' timestamps aren't passed, 'now' will be equal yesterday's timestamps
        if 'now' not in self.kwargs.keys():
            now = datetime.date.today() - datetime.timedelta(days=1)
            now = int(time.mktime(datetime.datetime.strptime(str(now), "%Y-%m-%d").timetuple()))
        else:
            now = self.kwargs['now']

        return Coin.objects.filter(pair=pair.upper(), timestamp__range=(past, now))
