from django.shortcuts import render
from .models import Coin


def index(request):
    """"""
    pair = Coin.objects.filter(pair="BRLBTC").order_by("-timestamp")
    context = {'pair': pair}

    return render(request, 'mms_pair/index.html', context)
