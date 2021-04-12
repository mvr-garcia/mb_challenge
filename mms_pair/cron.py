from django_cron import CronJobBase, Schedule
from .engine import update_coin


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 12 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        update_coin()
