@echo off
powershell.exe -File "C:\path\to\your\git_auto_commit.ps1" -RepoPath "C:\path\to\your\repo" >> "C:\path\to\your\logfile.log" 2>&1
echo %date% %time% >> "C:\path\to\your\logfile.log"
echo Git auto commit script executed. >> "C:\path\to\your\logfile.log"
