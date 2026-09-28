# ===================================================================
#   ANTIGRAVITY AI REMOTE DESKTOP - AUTOMATED SETUP (POWERSHELL)
# ===================================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "   ANTIGRAVITY AI REMOTE DESKTOP - AUTOMATED SETUP (POWERSHELL)" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan

# 1. Check Python
try {
    $pythonVersion = python --version
    Write-Host "[1/4] Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# 2. Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "[2/4] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "[2/4] Virtual environment (.venv) already exists." -ForegroundColor Green
}

# 3. Dependencies
Write-Host "[3/4] Installing dependencies in .venv..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\pip.exe" install -r requirements.txt
& ".\.venv\Scripts\pip.exe" install -e . --no-deps

# 4. .env File
Write-Host "[4/4] Configuring .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Created .env from .env.example" -ForegroundColor Green
} else {
    Write-Host "[OK] Existing .env file found." -ForegroundColor Green
}

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "   SETUP COMPLETE! Everything is ready." -ForegroundColor Green
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "   To launch the application:" -ForegroundColor White
Write-Host "      .\run.ps1   OR   .\.venv\Scripts\python.exe src\main.py" -ForegroundColor Yellow
Write-Host "===================================================================" -ForegroundColor Cyan
