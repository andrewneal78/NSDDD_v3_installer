' NSDDD v3 — Windows launcher
' Double-click this file to start the search interface.
' Uses pythonw so no console window appears.
Set WshShell = CreateObject("WScript.Shell")
ScriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = ScriptDir
WshShell.Run "pythonw launch.py --detach", 0, False
