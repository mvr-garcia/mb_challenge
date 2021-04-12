from django.test import TestCase
from .models import Coin
from .engine import sma_calc


class CoinModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Test Dictionary Creation
        test_data = []
        for i in range(201):
            test_data.append({'close': i + 1})

        for i, v in enumerate(test_data):
            if i > 199:
                Coin.objects.create(timestamp=1234567891,
                                    pair='BRLBTC',
                                    mms_20=sma_calc(test_data[i-19:i + 1], 20),
                                    mms_50=sma_calc(test_data[i-49:i + 1], 50),
                                    mms_200=sma_calc(test_data[i-199:i + 1], 200))

    def test_mms20_content(self):
        coin = Coin.objects.last()
        expected_object_name = coin.mms_20
        self.assertEqual(expected_object_name, 191.5)

    def test_mms50_content(self):
        coin = Coin.objects.last()
        expected_object_name = coin.mms_50
        self.assertEqual(expected_object_name, 176.5)

    def test_mms200_content(self):
        coin = Coin.objects.last()
        expected_object_name = coin.mms_200
        self.assertEqual(expected_object_name, 101.5)
