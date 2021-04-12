from django.shortcuts import render
from .engine import load_coin, update_coin
from .models import Coin


def index(request):
    """The home page for MMS Pair App"""

    # If the client-side forgets to run the command manage.py checkdb,
    # this check ensures that the data will be updated on the home page.
    coins = Coin.objects.all().count()

    # If database is empty, call the load_coin function
    if coins == 0:
        load_coin()
    # Else, call the update_coin function to update the database to the latest available date
    else:
        update_coin()

    pair = Coin.objects.filter(pair='BRLBTC').order_by("-timestamp")
    context = {'pair': pair}

    return render(request, 'mms_pair/index.html', context)
