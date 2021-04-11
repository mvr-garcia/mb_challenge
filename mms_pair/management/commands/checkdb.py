from django.core.management.base import BaseCommand
from mms_pair.models import Coin
from mms_pair.engine import load_coin, update_coin


class Command(BaseCommand):

    def handle(self, *args, **options):
        coins = Coin.objects.all().count()

        # If database is empty, call the load_coin function
        if coins == 0:
            load_coin()
        # Else, call the update_coin function to update the database to the latest available date
        else:
            update_coin()

        return self.stdout.write(self.style.SUCCESS('Coin database successfully updated'))
