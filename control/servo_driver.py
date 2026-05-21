import board
import busio
from adafruit_servokit import ServoKit
import time

from config import SERVO_MIN, SERVO_MAX, SERVO_CENTER


class ServoDriver:
    def __init__(self, channel=0):
        self.kit = ServoKit(channels=16)
        self.angle = SERVO_CENTER
        self.channel = channel

        # Safe startup
        self.set_angle(SERVO_CENTER)
        time.sleep(0.5)

    def clamp(self, angle):
        return max(SERVO_MIN, min(SERVO_MAX, angle))

    def set_angle(self, angle):
        angle = self.clamp(angle)
        self.angle = angle
        self.kit.servo[self.channel].angle = angle
        time.sleep(0.1)

    def get_angle(self):
        return self.angle