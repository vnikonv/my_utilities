Set WshShell = CreateObject("WScript.Shell")

cmd = "cmd /c cd /d D:\__pictures\ && python D:\__projects\utilities\jpeg2png_silent.py -yrl -w 16"

WshShell.Run cmd, 0, False
