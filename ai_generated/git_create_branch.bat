@echo off
REM Create and push a new branch
SET /p BRANCH_NAME=Enter the new branch name: 
git checkout -b %BRANCH_NAME%
git push -u origin %BRANCH_NAME%
echo Created and pushed branch %BRANCH_NAME%
