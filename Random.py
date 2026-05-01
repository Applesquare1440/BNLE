import board
import busio
import adafruit_pca9685
import time
import random
from adafruit_servokit import ServoKit

# =======================
# CONFIGURATION RANGES
# =======================
ANGLE_MIN = 20
ANGLE_MAX = 160

SPEED_MIN = 0.01   # fastest movement
SPEED_MAX = 0.2    # slowest movement

MODE_DURATION_MIN = 2    # seconds
MODE_DURATION_MAX = 8

STEP_MIN = 1
STEP_MAX = 5

IDLE_CHANCE = 0.3   # chance to stay idle during idling mode

# =======================
# SETUP
# =======================
kit = ServoKit(channels=16)

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 60

current_angle = 90
kit.servo[0].angle = current_angle

# =======================
# MODES
# =======================

def sweep(duration):
    """Smooth left-right sweeping"""
    global current_angle
    end_time = time.time() + duration

    direction = random.choice([-1, 1])
    step = random.randint(STEP_MIN, STEP_MAX)

    while time.time() < end_time:
        speed = random.uniform(SPEED_MIN, SPEED_MAX)

        current_angle += direction * step

        if current_angle >= ANGLE_MAX or current_angle <= ANGLE_MIN:
            direction *= -1

        kit.servo[0].angle = current_angle
        time.sleep(speed)


def tracking(duration):
    """Simulates following something (biased random walk)"""
    global current_angle
    end_time = time.time() + duration

    while time.time() < end_time:
        speed = random.uniform(SPEED_MIN, SPEED_MAX)

        # bias movement toward a random "target"
        target = random.randint(ANGLE_MIN, ANGLE_MAX)

        if current_angle < target:
            current_angle += random.randint(1, 3)
        else:
            current_angle -= random.randint(1, 3)

        current_angle = max(ANGLE_MIN, min(ANGLE_MAX, current_angle))

        kit.servo[0].angle = current_angle
        time.sleep(speed)


def idling(duration):
    """Mostly still, occasional small movement"""
    global current_angle
    end_time = time.time() + duration

    while time.time() < end_time:
        if random.random() > IDLE_CHANCE:
            # small twitch
            delta = random.randint(-2, 2)
            current_angle += delta
            current_angle = max(ANGLE_MIN, min(ANGLE_MAX, current_angle))

            kit.servo[0].angle = current_angle

        time.sleep(random.uniform(0.2, 0.8))


def jitter(duration):
    """Erratic random motion"""
    global current_angle
    end_time = time.time() + duration

    while time.time() < end_time:
        speed = random.uniform(SPEED_MIN, SPEED_MAX)

        current_angle = random.randint(ANGLE_MIN, ANGLE_MAX)

        kit.servo[0].angle = current_angle
        time.sleep(speed)


# =======================
# MAIN LOOP
# =======================

modes = [sweep, tracking, idling, jitter]

while True:
    mode = random.choice(modes)
    duration = random.uniform(MODE_DURATION_MIN, MODE_DURATION_MAX)

    mode(duration)
