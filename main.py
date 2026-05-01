import time
import cv2

from vision.target_selector import TargetSelector
from camera.picamera_stream import CameraStream
from vision.detector import YOLODetector
from vision.tracker import TrackerWrapper
from control.controller import Controller
from control.servo_driver import ServoDriver
from behavior.state_machine import StateMachine
from config import FRAME_WIDTH, FRAME_HEIGHT, DETECTION_INTERVAL


def main():
    cam = CameraStream()
    detector = YOLODetector()
    tracker = TrackerWrapper()
    servo = ServoDriver()
    controller = Controller(FRAME_WIDTH)
    state = StateMachine()
    selector = TargetSelector(FRAME_WIDTH)

    fps = 0
    frame_counter = 0
    fps_timer = time.time()
    
    frame_id = 0
    bbox = None

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                continue

            #DEBUG
            cv2.line(frame, (FRAME_WIDTH // 2, 0), (FRAME_WIDTH // 2, FRAME_HEIGHT), (0, 255, 255), 1)

            detections = []

            # Detection step
            if frame_id % DETECTION_INTERVAL == 0:
                print("RUNNING DETECTION FRAME", frame_id)
                detections = detector.detect(frame)
                for (x, y, w, h) in detections:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                selector.update_targets(detections)

                selected_bbox = selector.select_target()

                if selected_bbox is not None:
                    bbox = selected_bbox
                    tracker.init(frame, bbox)

            # Tracking step
            success, tracked_box = tracker.update(frame)
            if not success:
                # try to reacquire from selector
                selected_bbox = selector.select_target()
                if selected_bbox is not None:
                    tracker.init(frame, selected_bbox)
                    success = True
                    tracked_box = selected_bbox

            target_visible = success

            mode = state.update(detections, target_visible)

            current_angle = servo.get_angle()

            if mode == "SCAN":
                angle = state.scan()

            elif mode == "TRACK" and success:
                x, y, w, h = map(int, tracked_box)
                target_x = x + w // 2
                angle = controller.update(target_x, current_angle)

                #DEBUG
                cv2.circle(frame, (target_x, FRAME_HEIGHT//2), 4, (0,0,255), -1)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            else:
                angle = current_angle
            
            servo.set_angle(angle)
            
            #DEBUG  
            print(f"Angle: {angle:.2f}")

            # ===== DEBUG OVERLAY =====
            info1 = f"FPS: {fps}"
            info2 = f"Mode: {mode}"
            info3 = f"Detections: {len(detections)}"
            info4 = f"Angle: {angle:.2f}"

            cv2.putText(frame, info1, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.putText(frame, info2, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.putText(frame, info3, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
            cv2.putText(frame, info4, (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == 27:
                break
            frame_counter += 1

            if time.time() - fps_timer >= 1.0:
                fps = frame_counter
                frame_counter = 0
                fps_timer = time.time()
                
            frame_id += 1

    finally:
        cam.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
