import datetime
import time

from config import (
    ACTIVE_DAYS,
    START_HOUR,
    START_MINUTE,
    END_HOUR,
    END_MINUTE,
)


class Scheduler:
    def __init__(self):
        pass

    def is_active(self):
        now = datetime.datetime.now()

        # Check day
        if now.weekday() not in ACTIVE_DAYS:
            return False

        now_time = now.time()

        start_time = datetime.time(hour=START_HOUR, minute=START_MINUTE)

        end_time = datetime.time(hour=END_HOUR, minute=END_MINUTE)

        # CASE 1: same-day window

        if start_time < end_time:

            return start_time <= now_time <= end_time

        # CASE 2: overnight window

        else:

            return now_time >= start_time or now_time <= end_time

    def wait_until_active(self, sleep_interval):
        while not self.is_active():
            time.sleep(sleep_interval)