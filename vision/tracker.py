import cv2
from config import LOST_TIMEOUT


class TrackerWrapper:
    def __init__(self):
        self.tracker = None
        self.bbox = None
        self.use_csrt = False

    def init(self, frame, bbox):
        try:
            self.tracker = cv2.TrackerKCF_create()
            self.tracker.init(frame, tuple(bbox))
            self.bbox = bbox
            self.use_csrt = False
        except:
            self.tracker = cv2.TrackerCSRT_create()
            self.tracker.init(frame, tuple(bbox))
            self.bbox = bbox
            self.use_csrt = True

    def update(self, frame):
        if self.tracker is None:
            return False, None

        success, bbox = self.tracker.update(frame)

        if not success and not self.use_csrt:
            # fallback
            try:
                self.tracker = cv2.TrackerCSRT_create()
                self.tracker.init(frame, tuple(self.bbox))
                self.use_csrt = True
                success, bbox = self.tracker.update(frame)
            except:
                return False, None

        if success:
            self.bbox = bbox
            return True, bbox

        return False, None