# ===================================================================
#   Launch Antigravity AI Remote Desktop Assistant (PowerShell)
# ===================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "[!] Virtual environment not found. Running setup.ps1 first..." -ForegroundColor Yellow
    & ".\setup.ps1"
}

Write-Host "Launching Antigravity AI Remote Desktop..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" "src\main.py" $args
