Set WshShell = CreateObject("WScript.Shell")

' Input file path
input = WScript.Arguments(0)

' Output file path (same folder, filename without extension)
output = Left(input, InStrRev(input, ".") - 1)

' Language argument (second argument)
If WScript.Arguments.Count > 1 Then
    lang = WScript.Arguments(1)
Else
    lang = "eng" ' default to English if not specified
End If

' Construct the Tesseract command
cmd = "tesseract """ & input & """ """ & output & """ -l " & lang

' Run hidden (0 = hidden window)
WshShell.Run cmd, 0, True
