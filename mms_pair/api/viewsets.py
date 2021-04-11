from rest_framework import generics
from mms_pair.models import Coin
from . import serializers
import datetime
import time


class CoinListView(generics.ListAPIView):
    serializer_class = serializers.CoinSerializer
    queryset = Coin.objects.all()


class CryptoListView(generics.ListAPIView):
    serializer_class = serializers.CoinSerializer

    def get_queryset(self):
        """This view should return a list of all the crypto in specific timestamp range."""
        pair = self.kwargs['crypto']


        past = self.kwargs['past']

        # If now timestamps aren't passed, now will be equal yesterday's timestamps
        if 'now' not in self.kwargs.keys():
            now = datetime.date.today() - datetime.timedelta(days=1)
            now = int(time.mktime(datetime.datetime.strptime(str(now), "%Y-%m-%d").timetuple()))
        else:
            now = self.kwargs['now']

        return Coin.objects.filter(pair=pair.upper(), timestamp__range=(past, now))
