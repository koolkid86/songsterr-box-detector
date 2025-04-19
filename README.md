# Songsterr Box Detector

A desktop application that uses YOLO object detection to identify and click on Songsterr boxes automatically. This tool helps automate interactions with the Songsterr website by detecting specific UI elements.

## Features

- Real-time detection of Songsterr boxes using YOLO object detection
- Configurable confidence threshold for detection
- Customizable click coordinates
- Adjustable detection interval
- Live preview of detection results
- Enable/disable automatic clicking

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone this repository:
    git clone https://github.com/YOUR_USERNAME/songsterr-box-detector.git cd songsterr-box-detector

2. Install the required dependencies:
    pip install -r requirements.txt

3. Download the trained model (if not included in the repository):
    Place the model file in `my_model/train/weights/best.pt`

### Using the Application

1. Launch the application
2. Adjust the confidence threshold as needed (higher values = more precise detection)
3. Set the X and Y coordinates where you want the application to click when a box is detected
4. Set the detection interval (how frequently the app checks for boxes)
5. Check/uncheck "Enable Clicking" to control whether the app should automatically click
6. Click "Start Detection" to begin monitoring
7. The preview area will show what the detector is seeing with boxes highlighted
8. Click "Stop Detection" when finished

## Building an Executable (Windows)

To create a standalone executable:

1. Install PyInstaller:
    pip install pyinstaller

2. Build the executable:
    pyinstaller --onefile --noconsole --name SongsterrDetector --add-data "my_model/train/weights/best.pt;my_model/train/weights/" songsterr_app.py

3. Find the executable in the `dist` folder

## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses the [Ultralytics YOLO](https://github.com/ultralytics/yolo) for object detection
- Built with PyQt5 for the user interface