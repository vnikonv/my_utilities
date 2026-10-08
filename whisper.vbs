Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Input file path
input = WScript.Arguments(0)

' Language argument
If WScript.Arguments.Count > 1 Then
    lang = WScript.Arguments(1)
Else
    lang = "en"
End If

' Input folder
inputFolder = FSO.GetParentFolderName(input)

' Input filename without extension
baseName = FSO.GetBaseName(input)

' Windows temporary folder
tempFolder = WshShell.ExpandEnvironmentStrings("%TEMP%")

' Temporary WAV file
wav = FSO.BuildPath(tempFolder, baseName & ".whisper-temp.wav")

' Convert input audio to 16 kHz, mono, 16-bit PCM WAV
ffmpeg = "ffmpeg -i """ & input & """ -ar 16000 -ac 1 -c:a pcm_s16le """ & wav & """"
WshShell.Run ffmpeg, 0, True

' Transcribe with Whisper
whisper = "whisper-cli -m ""E:\LLMS\whisper.cpp\models\ggml-large-v3.bin"" -f """ & wav & """ -l " & lang & " --no-timestamps --output-txt --output-file """ & FSO.BuildPath(inputFolder, baseName) & """"
WshShell.Run whisper, 0, True

' Delete temporary WAV
If FSO.FileExists(wav) Then
    FSO.DeleteFile wav, True
End If
