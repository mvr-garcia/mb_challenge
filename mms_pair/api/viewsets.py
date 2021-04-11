from rest_framework import generics
from mms_pair.models import Coin
from . import serializers


class CoinListView(generics.ListAPIView):
    serializer_class = serializers.CoinSerializer
    queryset = Coin.objects.all()


class CryptoListView(generics.ListAPIView):
    serializer_class = serializers.CoinSerializer

    def get_queryset(self):
        """This view should return a list of all the crypto in specific timestamp range."""
        pair = self.kwargs['crypto']
        past = self.kwargs['past']
        now = self.kwargs['now']
        return Coin.objects.filter(pair=pair.upper(), timestamp__range=(past, now))
