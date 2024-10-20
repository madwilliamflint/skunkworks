@echo off
REM Fetch and sync the master branch
git checkout master
git pull origin master
echo Synced master with origin
