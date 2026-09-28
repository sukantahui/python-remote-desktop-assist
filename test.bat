@echo off
cd /d "%~dp0"
echo ===================================================================
echo   Running Test Suite with Pytest...
echo ===================================================================
.\.venv\Scripts\pytest.exe -v %*
