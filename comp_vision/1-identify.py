import cv2
import torch
from ultralytics import YOLO

# Load YOLOv8n pretrained model
model = YOLO('yolov8n.pt')  # You can replace with a custom path if needed

# Initialize webcam
cap = cv2.VideoCapture('/dev/video2')# Use 1 or 2 if 0 doesn't work

# ID tracking counter
object_counter = 0
tracked_objects = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame)[0]

    # Draw boxes
    for i, box in enumerate(results.boxes):
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Assign unique ID based on position hash
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        obj_hash = hash(center)

        if obj_hash not in tracked_objects:
            tracked_objects[obj_hash] = object_counter
            object_counter += 1

        obj_id = tracked_objects[obj_hash]

        # Draw rectangle and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{label} #{obj_id} ({conf:.2f})"
        cv2.putText(frame, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("YOLOv8 Webcam Detection", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
