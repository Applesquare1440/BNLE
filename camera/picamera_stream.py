from picamera2 import Picamera2
import threading
import numpy as np
import cv2
import time
from libcamera import Transform

from config import FRAME_WIDTH, FRAME_HEIGHT


class CameraStream:
    def __init__(self):
        self.picam2 = Picamera2()

        config = self.picam2.create_preview_configuration(

            main={
                "size": (FRAME_WIDTH, FRAME_HEIGHT),   # output size (e.g. 320x240)
                "format": "BGR888"
            },
            raw={
                "size": (1640, 1232)  # FULL SENSOR for IMX219
            },
            transform=Transform(hflip=1, vflip=1),
            buffer_count=2
        )

        self.picam2.configure(config)
        self.picam2.start()

        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            frame = self.picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            with self.lock:
                self.frame = frame

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        self.thread.join()
        self.picam2.stop()
