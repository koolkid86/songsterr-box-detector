import sys
import cv2
import numpy as np
import pyautogui
import mss
import time
from ultralytics import YOLO
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QSlider, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

class SongsterrDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the trained YOLO model
        self.model = YOLO(r'C:\Documents\code\yolo\my_model\train\weights\best.pt')
        
        # Define the target class name
        self.TARGET_CLASS_NAME = "songsterrBox"
        
        # App state
        self.running = False
        self.confidence_threshold = 0.1
        self.click_enabled = True
        self.click_x = 1000
        self.click_y = 500
        self.interval = 1.0  # seconds
        
        self.init_ui()
        
        # Timer for detection loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.detection_loop)
        
    def init_ui(self):
        # Main window setup
        self.setWindowTitle('Songsterr Box Detector')
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Preview area
        self.preview_label = QLabel("Preview will appear here when running")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("border: 1px solid #ccc;")
        main_layout.addWidget(self.preview_label)
        
        # Controls section
        controls_layout = QVBoxLayout()
        
        # Confidence threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Confidence Threshold:"))
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(int(self.confidence_threshold * 100))
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        threshold_layout.addWidget(self.threshold_slider)
        self.threshold_value_label = QLabel(f"{self.confidence_threshold:.2f}")
        threshold_layout.addWidget(self.threshold_value_label)
        controls_layout.addLayout(threshold_layout)
        
        # Click coordinates
        click_layout = QHBoxLayout()
        click_layout.addWidget(QLabel("Click at coordinates:"))
        click_layout.addWidget(QLabel("X:"))
        self.click_x_slider = QSlider(Qt.Horizontal)
        self.click_x_slider.setMinimum(0)
        self.click_x_slider.setMaximum(1920)  # Assuming max screen width
        self.click_x_slider.setValue(self.click_x)
        self.click_x_slider.valueChanged.connect(self.update_click_x)
        click_layout.addWidget(self.click_x_slider)
        self.click_x_label = QLabel(f"{self.click_x}")
        click_layout.addWidget(self.click_x_label)
        
        click_layout.addWidget(QLabel("Y:"))
        self.click_y_slider = QSlider(Qt.Horizontal)
        self.click_y_slider.setMinimum(0)
        self.click_y_slider.setMaximum(1080)  # Assuming max screen height
        self.click_y_slider.setValue(self.click_y)
        self.click_y_slider.valueChanged.connect(self.update_click_y)
        click_layout.addWidget(self.click_y_slider)
        self.click_y_label = QLabel(f"{self.click_y}")
        click_layout.addWidget(self.click_y_label)
        
        controls_layout.addLayout(click_layout)
        
        # Interval setting
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Detection Interval (seconds):"))
        self.interval_slider = QSlider(Qt.Horizontal)
        self.interval_slider.setMinimum(1)
        self.interval_slider.setMaximum(50)
        self.interval_slider.setValue(int(self.interval * 10))
        self.interval_slider.valueChanged.connect(self.update_interval)
        interval_layout.addWidget(self.interval_slider)
        self.interval_label = QLabel(f"{self.interval:.1f}")
        interval_layout.addWidget(self.interval_label)
        controls_layout.addLayout(interval_layout)
        
        # Enable/disable clicking
        click_checkbox_layout = QHBoxLayout()
        self.click_checkbox = QCheckBox("Enable Clicking")
        self.click_checkbox.setChecked(self.click_enabled)
        self.click_checkbox.stateChanged.connect(self.toggle_clicking)
        click_checkbox_layout.addWidget(self.click_checkbox)
        controls_layout.addLayout(click_checkbox_layout)
        
        main_layout.addLayout(controls_layout)
        
        # Start/Stop button
        button_layout = QHBoxLayout()
        self.start_stop_button = QPushButton("Start Detection")
        self.start_stop_button.clicked.connect(self.toggle_detection)
        button_layout.addWidget(self.start_stop_button)
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        self.setCentralWidget(central_widget)
    
    def update_threshold(self, value):
        self.confidence_threshold = value / 100.0
        self.threshold_value_label.setText(f"{self.confidence_threshold:.2f}")
    
    def update_click_x(self, value):
        self.click_x = value
        self.click_x_label.setText(f"{value}")
    
    def update_click_y(self, value):
        self.click_y = value
        self.click_y_label.setText(f"{value}")
    
    def update_interval(self, value):
        self.interval = value / 10.0
        self.interval_label.setText(f"{self.interval:.1f}")
        if self.running:
            self.timer.setInterval(int(self.interval * 1000))
    
    def toggle_clicking(self, state):
        self.click_enabled = (state == Qt.Checked)
    
    def toggle_detection(self):
        if not self.running:
            self.running = True
            self.start_stop_button.setText("Stop Detection")
            self.status_label.setText("Running detection...")
            self.timer.start(int(self.interval * 1000))
        else:
            self.running = False
            self.start_stop_button.setText("Start Detection")
            self.status_label.setText("Detection stopped")
            self.timer.stop()
    
    def capture_screen(self):
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])  # Capture full screen
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert for OpenCV
    
    def detection_loop(self):
        try:
            # Capture screen
            frame = self.capture_screen()
            
            # Create a copy for display
            display_frame = frame.copy()
            
            # Resize for model
            frame_resized = cv2.resize(frame, (384, 288))
            
            # Run detection
            results = self.model(frame_resized)
            
            detection_found = False
            
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Scale bounding box to original frame size
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    h, w = frame.shape[:2]
                    h_r, w_r = frame_resized.shape[:2]
                    x1 = int(x1 * w / w_r)
                    y1 = int(y1 * h / h_r)
                    x2 = int(x2 * w / w_r)
                    y2 = int(y2 * h / h_r)
                    
                    if result.names[class_id] == self.TARGET_CLASS_NAME and conf > self.confidence_threshold:
                        detection_found = True
                        # Draw bounding box on display frame
                        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(display_frame, f"{conf:.2f}", (x1, y1-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Perform click if enabled
                        if self.click_enabled:
                            pyautogui.click(self.click_x, self.click_y)
                            self.status_label.setText(f"Detected! Clicked at ({self.click_x}, {self.click_y})")
            
            if not detection_found:
                self.status_label.setText("Running detection... No targets found")
            
            # Update preview
            h, w, c = display_frame.shape
            bytes_per_line = 3 * w
            # Resize for display if too large
            if w > 580:  # Slightly less than window width
                scale = 580 / w
                display_frame = cv2.resize(display_frame, (int(w * scale), int(h * scale)))
                h, w, c = display_frame.shape
                bytes_per_line = 3 * w
            
            q_img = QImage(display_frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.preview_label.setPixmap(QPixmap.fromImage(q_img))
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            print(f"Error in detection loop: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = SongsterrDetectorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()