import cv2
import numpy as np

from config import MODEL_PATH, CONF_THRESHOLD, NMS_THRESHOLD


class YOLODetector:
    def __init__(self):
        self.net = cv2.dnn.readNetFromONNX(MODEL_PATH)

    def detect(self, frame):
        h, w = frame.shape[:2]
        
        #export to YOLOv8n image of 640 640
        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (640, 640), swapRB=True, crop=False
        )
        self.net.setInput(blob)
        
        #Predict
        outputs = self.net.forward()
        
        #Remove batch dimension: (1, 84, 8400) -> (84, 8400)
        outputs = outputs[0]  # shape: (84, N) or (N, 84)

        # Ensure correct shape
        if outputs.shape[0] < outputs.shape[1]:
            outputs = outputs.T  # make (N, 84)

        boxes = []
        confidences = []
        
        x_factor = w / 640
        y_factor = h / 640

        #outputs = self.net.forward()[0]

        """for det in outputs:
            scores = det[4:]"""

        for row in outputs:
            # YOLOv8: first 4 = bbox, rest = class scores
            #cx, cy, bw, bh = row[:4]
            scores = row[4:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if class_id != 0 or confidence < CONF_THRESHOLD:
                continue
            cx, cy, bw, bh = row[:4]
            print("RAW:", cx, cy, bw, bh)

            # Convert to pixel coords
            x = int((cx - bw / 2) * x_factor)
            y = int((cy - bh / 2) * y_factor)
            bw = int(bw * x_factor)
            bh = int(bh * y_factor)
            
            print("Converted:", cx, cy, bw, bh)
            
            boxes.append([x, y, bw, bh])
            confidences.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)

        results = []
        
        if len(indices) > 0:
            for i in indices.flatten():
                results.append(boxes[i])

        return results
