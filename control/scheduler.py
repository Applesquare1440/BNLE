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

        start = now.replace(
            hour=START_HOUR,
            minute=START_MINUTE,
            second=0,
            microsecond=0,
        )

        end = now.replace(
            hour=END_HOUR,
            minute=END_MINUTE,
            second=0,
            microsecond=0,
        )

        return start <= now <= end

    def wait_until_active(self, sleep_interval):
        while not self.is_active():
            time.sleep(sleep_interval)