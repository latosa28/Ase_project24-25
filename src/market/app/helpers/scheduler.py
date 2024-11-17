from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app, Flask

from helpers.auction_helper import check_expired_auctions


class SchedulerHelper:

    def __init__(self, app: Flask):
        self.app = app

    def check_expired_auctions(self):
        with self.app.app_context():
            check_expired_auctions()

    def start_scheduler(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.check_expired_auctions,
            "interval",
            seconds=int(self.app.config["auction_end"]["job_frequency_second"]),
        )
        scheduler.start()
