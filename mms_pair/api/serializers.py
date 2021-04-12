from rest_framework import serializers
from mms_pair.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['timestamp', 'mms_20', 'mms_50', 'mms_200']


class CoinMms20Serializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['timestamp', 'mms_20']


class CoinMms50Serializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['timestamp', 'mms_50']


class CoinMms200Serializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['timestamp', 'mms_200']
