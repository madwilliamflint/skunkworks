@echo off
REM Delete a local and remote branch
SET /p BRANCH_NAME=Enter the branch name to delete: 
git branch -d %BRANCH_NAME%
git push origin --delete %BRANCH_NAME%
echo Deleted branch %BRANCH_NAME% locally and remotely
