@echo off
REM Merge a branch into master and push
SET /p BRANCH_NAME=Enter the branch name to merge into master: 
git checkout master
git pull origin master
git merge %BRANCH_NAME%
git push origin master
echo Merged %BRANCH_NAME% into master and pushed
