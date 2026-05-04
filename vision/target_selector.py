import time
import math

from config import W_RECENCY, W_SIZE, W_CENTER, TARGET_LOCK_TIME


class Target:
    def __init__(self, bbox, target_id):
        self.bbox = bbox
        self.id = target_id
        self.last_seen = time.time()
        self.last_selected = 0

    def update(self, bbox):
        self.bbox = bbox
        self.last_seen = time.time()


class TargetSelector:
    def __init__(self, frame_width):
        self.targets = {}
        self.next_id = 0
        self.frame_center = frame_width / 2

        self.current_target_id = None
        self.lock_time = 0

    def _bbox_center(self, bbox):
        x, y, w, h = bbox
        return x + w / 2

    def _distance(self, b1, b2):
        c1 = self._bbox_center(b1)
        c2 = self._bbox_center(b2)
        return abs(c1 - c2)

    def update_targets(self, detections):
        now = time.time()

        # Match detections to existing targets (simple nearest match)
        assigned = set()

        for det in detections:
            best_id = None
            best_dist = 50  # threshold in pixels

            for tid, target in self.targets.items():
                dist = self._distance(det, target.bbox)
                if dist < best_dist:
                    best_dist = dist
                    best_id = tid

            if best_id is not None:
                self.targets[best_id].update(det)
                assigned.add(best_id)
            else:
                self.targets[self.next_id] = Target(det, self.next_id)
                assigned.add(self.next_id)
                self.next_id += 1

        # Remove stale targets
        to_remove = []
        for tid, target in self.targets.items():
            if now - target.last_seen > 2.0:
                to_remove.append(tid)

        for tid in to_remove:
            del self.targets[tid]

    def _compute_score(self, target):
        now = time.time()

        x, y, w, h = target.bbox

        size = w * h

        center_x = x + w / 2
        dist = abs(center_x - self.frame_center) / self.frame_center
        centrality = 1.0 - dist

        recency = now - target.last_selected

        score = (
            W_RECENCY * recency +
            W_SIZE * size +
            W_CENTER * centrality
        )

        return score

    def select_target(self):
        now = time.time()

        # keep current target if within lock time
        if self.current_target_id is not None:
            if self.current_target_id in self.targets:
                if now - self.lock_time < TARGET_LOCK_TIME:
                    return self.targets[self.current_target_id].bbox
            else:
                # lost target
                self.current_target_id = None

        # select new target
        best_id = None
        best_score = -1

        for tid, target in self.targets.items():
            score = self._compute_score(target)

            if score > best_score:
                best_score = score
                best_id = tid

        if best_id is not None:
            self.current_target_id = best_id
            self.targets[best_id].last_selected = now
            self.lock_time = now
            return self.targets[best_id].bbox

        return None