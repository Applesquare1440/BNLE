from config import CP, MAX_STEP, DEAD_ZONE, SMOOTHING_ALPHA, GEAR_RATIO


class Controller:
    def __init__(self, frame_width):
        self.frame_center = frame_width / 2
        # self.prev_angle = 90

    def update(self, target_x, current_angle):
        error = (target_x - self.frame_center) / self.frame_center

        if abs(error) < DEAD_ZONE:
            return current_angle

        delta = CP * error * GEAR_RATIO
        delta = max(-MAX_STEP, min(MAX_STEP, delta))

        #DEBUG
        print(f"Delta: {delta:.2f}")

        if abs(delta) < 0.3:
            return current_angle

        new_angle = current_angle + delta

        # smoothing
        smoothed = SMOOTHING_ALPHA * current_angle + (1 - SMOOTHING_ALPHA) * new_angle

        # self.prev_angle = smoothed
        return smoothed
