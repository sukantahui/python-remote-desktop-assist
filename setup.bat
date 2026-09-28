@echo off
@setlocal

echo ===================================================================
echo   ANTIGRAVITY AI REMOTE DESKTOP - AUTOMATED SETUP (WINDOWS)
echo ===================================================================

cd /d "%~dp0"

:: 1. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH. Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

:: 2. Create Virtual Environment
if not exist ".venv" goto CREATE_VENV
echo [2/4] Virtual environment already exists.
goto INSTALL_DEPS

:CREATE_VENV
echo [2/4] Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

:INSTALL_DEPS
:: 3. Install Dependencies
echo [3/4] Installing / updating dependencies in virtual environment...
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps

:: 4. Setup .env configuration
echo [4/4] Configuring environment (.env)...
if not exist ".env" (
    copy .env.example .env
    echo [OK] Created .env from .env.example
) else (
    echo [OK] Existing .env file found.
)

echo ===================================================================
echo   SETUP COMPLETE! Everything is ready.
echo ===================================================================
echo   To launch the application:
echo      Double-click run.bat   OR   run: python src/main.py
echo ===================================================================
pause
