import time
import math

from config import TARGET_LOCK_TIME, HOLD_TIME, LOST_TIMEOUT, SCAN_MIN, SCAN_MAX, SCAN_SPEED


class StateMachine:
    def __init__(self):
        self.state = "IDLE"
        self.state_time = time.time()
        self.target = None
        self.scan_direction = 1
        self.scan_angle = 90

    def update(self, detections, target_visible):
        now = time.time()

        if self.state == "IDLE":
            if detections:
                self.state = "TRACKING"
                self.state_time = now
            return "SCAN"

        elif self.state == "TRACKING":
            if not target_visible:
                self.state = "LOST"
                self.state_time = now
            elif now - self.state_time > TARGET_LOCK_TIME:
                self.state = "HOLD"
                self.state_time = now
            return "TRACK"

        elif self.state == "HOLD":
            if now - self.state_time > HOLD_TIME:
                self.state = "TRACKING"
                self.state_time = now
            return "HOLD"

        elif self.state == "LOST":
            if now - self.state_time > LOST_TIMEOUT:
                self.state = "IDLE"
                self.state_time = now
            return "LOST"

    def scan(self):
        self.scan_angle += self.scan_direction * SCAN_SPEED

        if self.scan_angle > SCAN_MAX or self.scan_angle < SCAN_MIN:
            self.scan_direction *= -1

        return self.scan_angle