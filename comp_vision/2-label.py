import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8n model
model = YOLO("yolov8n.pt")

# Start webcam
cap = cv2.VideoCapture('/dev/video2')  # Change if using different device

while True:
    ret, frame = cap.read()
    if not ret:
        break

    original = frame.copy()
    height, width = frame.shape[:2]

    # Inference
    results = model(frame)[0]

    # Create a mask to track obstacles
    obstacle_mask = np.zeros((height, width), dtype=np.uint8)

    # Draw bounding boxes
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Mark obstacle area on mask
        obstacle_mask[y1:y2, x1:x2] = 255

        # Draw red for person, green for others
        color = (0, 0, 255) if label == "person" else (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # --- PATH IDENTIFICATION (Safe Zone Estimation) ---
    scan_y = height - 80  # Start scanning near the bottom
    row = obstacle_mask[scan_y]
    threshold = 20  # pixels

    start = None
    for x in range(width):
        if row[x] == 0:
            if start is None:
                start = x
        else:
            if start is not None:
                if x - start > threshold:
                    cv2.rectangle(frame, (start, scan_y - 40), (x, scan_y), (255, 255, 0), 2)
                start = None

    # Optional: show where the scan row is
    cv2.line(frame, (0, scan_y), (width, scan_y), (200, 200, 200), 1)

    # Show final output
    cv2.imshow("YOLOv8 with Path Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
