import cv2
import numpy as np
import pyautogui
import mss
import time
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO(r'C:\Documents\code\yolo\my_model\train\weights\best.pt')  # Change this to your trained model path
  # Change this to your trained model path

# Define the target class name (from your trained model labels)
TARGET_CLASS_NAME = "songsterrBox"

def capture_screen():
     with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])  # Capture full screen
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert for OpenCV

while True:
    frame = capture_screen()  # Capture the screen

    frame_resized = cv2.resize(frame, (384, 288))  # Resize image before passing to model
    results = model(frame_resized)


    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # Get detected class ID
            conf = float(box.conf[0])  # Get confidence score
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box

          
            if result.names[class_id] == TARGET_CLASS_NAME and conf > 0.1:
                print(f"Detected {TARGET_CLASS_NAME} with confidence {conf}")
                
                # Get current mouse position
                mouse_x, mouse_y = pyautogui.position()
                 
                # Click at the current mouse position
                pyautogui.click(1000, 500)
                print(f"Clicked at {1000}, {500}")

    time.sleep(1)  # Adjust interval as needed
