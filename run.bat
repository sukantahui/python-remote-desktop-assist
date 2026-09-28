@echo off
cd /d "%~dp0"

echo ===================================================================
echo   Starting Antigravity AI Remote Desktop Assistant...
echo ===================================================================

if not exist ".venv\Scripts\python.exe" goto RUN_SETUP

:LAUNCH_APP
.\.venv\Scripts\python.exe src\main.py %*
goto END

:RUN_SETUP
echo [!] Virtual environment not found. Running setup first...
call setup.bat
.\.venv\Scripts\python.exe src\main.py %*

:END
