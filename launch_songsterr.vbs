Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "c:\Documents\code\yolo"
WshShell.Run "pythonw.exe c:\Documents\code\yolo\songsterr_app.py", 0, False