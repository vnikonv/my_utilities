' Silently extracts all images from \word\media inside a DOCX archive

Option Explicit

Dim fso, shell
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

Dim docxPath
docxPath = WScript.Arguments(0)  ' full path to the selected .docx file

Dim parentFolder, baseName
parentFolder = fso.GetParentFolderName(docxPath)        ' folder containing the document
baseName = fso.GetBaseName(docxPath)                    ' filename without extension

Dim outputFolder
outputFolder = parentFolder & "\" & baseName            ' target folder name

If Not fso.FolderExists(outputFolder) Then
    fso.CreateFolder(outputFolder)                      ' create target folder if not exists
End If

' Path to 7-Zip executable
Dim sevenZip
sevenZip = """C:\Global\7-Zip\7z.exe"""

' Build extraction command
Dim cmd
cmd = sevenZip & " e """ & docxPath & """ word/media/* -o""" & outputFolder & """ -y"

' Run extractor silently and wait until it finishes
shell.Run cmd, 0, True