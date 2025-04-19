@echo off
cd /d c:\Documents\code\yolo

echo Building Songsterr Detector executable...
pyinstaller --onefile ^
            --noconsole ^
            --name SongsterrDetector ^
            --add-data "my_model/train/weights/best.pt;my_model/train/weights/" ^
            --icon=NONE ^
            songsterr_wrapper.py

echo Executable created in dist folder
echo You can now create a shortcut to c:\Documents\code\yolo\dist\SongsterrDetector.exe
pause