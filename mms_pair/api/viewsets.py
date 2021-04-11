from rest_framework import generics
from mms_pair.models import Coin
from . import serializers


class CoinListView(generics.ListAPIView):
    serializer_class = serializers.CoinSerializer
    queryset = Coin.objects.all()
