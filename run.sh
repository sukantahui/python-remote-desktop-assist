#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f ".venv/bin/python" ]; then
    echo "[!] Virtual environment not found. Running setup.sh first..."
    bash setup.sh
fi

echo "Starting Antigravity AI Remote Desktop..."
./.venv/bin/python src/main.py "$@"
