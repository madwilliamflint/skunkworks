@echo off

REM ############################################

.\test_envelope.py


REM ############################################

REM Ping timeout trick to sleep.
@ping 127.0.0.1 -n 3 >nul
