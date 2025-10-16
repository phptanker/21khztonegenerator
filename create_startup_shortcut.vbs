' VBScript to create a startup shortcut for the DAC Keep-Alive program
' Run this script to automatically add the program to Windows startup

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the current directory
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Define paths
exePath = currentDir & "\dist\DACKeepAlive.exe"
pythonPath = currentDir & "\tone_generator.py"

' Check which file exists
If fso.FileExists(exePath) Then
    targetPath = exePath
    targetName = "DACKeepAlive.exe"
ElseIf fso.FileExists(pythonPath) Then
    ' If using Python script, create a shortcut that runs it with pythonw
    targetPath = "pythonw.exe"
    targetName = "tone_generator.py"
    arguments = Chr(34) & pythonPath & Chr(34)
Else
    MsgBox "Error: Could not find DACKeepAlive.exe or tone_generator.py", vbCritical, "File Not Found"
    WScript.Quit
End If

' Get startup folder path
startupFolder = WshShell.SpecialFolders("Startup")

' Create shortcut
shortcutPath = startupFolder & "\DACKeepAlive.lnk"
Set shortcut = WshShell.CreateShortcut(shortcutPath)

If fso.FileExists(exePath) Then
    shortcut.TargetPath = targetPath
    shortcut.WorkingDirectory = currentDir & "\dist"
Else
    shortcut.TargetPath = targetPath
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = currentDir
End If

shortcut.Description = "DAC Keep-Alive Tone Generator"
shortcut.Save

MsgBox "Startup shortcut created successfully!" & vbCrLf & vbCrLf & _
       "Location: " & shortcutPath & vbCrLf & vbCrLf & _
       "The program will now start automatically when Windows boots.", _
       vbInformation, "Success"
