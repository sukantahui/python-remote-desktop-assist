#!/usr/bin/env bash
set -e

echo "==================================================================="
echo "  ANTIGRAVITY AI REMOTE DESKTOP - SETUP (LINUX / MACOS)"
echo "==================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    exit 1
fi

echo "[1/4] Found Python: $(python3 --version)"

# 2. Virtual Environment
if [ ! -d ".venv" ]; then
    echo "[2/4] Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "[2/4] Virtual environment (.venv) already exists."
fi

# 3. Dependencies
echo "[3/4] Installing dependencies in .venv..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps

# 4. .env File
echo "[4/4] Configuring .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "[OK] Created .env from .env.example"
else
    echo "[OK] Existing .env file found."
fi

echo "==================================================================="
echo "  SETUP COMPLETE! Everything is ready."
echo "==================================================================="
echo "  To launch the application:"
echo "     ./run.sh   OR   python3 src/main.py"
echo "==================================================================="
