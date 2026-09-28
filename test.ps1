# ===================================================================
#   Run Test Suite (PowerShell)
# ===================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

& ".\.venv\Scripts\pytest.exe" -v $args
