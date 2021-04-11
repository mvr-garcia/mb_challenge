from rest_framework import serializers
from mms_pair.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['timestamp', 'mms_20', 'mms_50', 'mms_200']
