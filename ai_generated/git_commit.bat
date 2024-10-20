
@echo off
REM call c:\users\mpwilson\bin\git_commit.bat

powershell.exe -File "c:\users\mpwilson\bin\git_auto_commit.ps1" -RepoPath "c:\users\mpwilson\srctree\python\skunkworks" >>"C:\users\mpwilson\log\gitcommit.log" 2>&1
echo %date% %time% >> "C:\users\mpwilson\log\gitcommit.log"
echo Git auto commit script executed. >> "C:\users\mpwilson\log\gitcommit.log"