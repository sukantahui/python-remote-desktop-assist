"""Main application entry point for AI Remote Desktop Assistant."""

import argparse
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.common.config import config
from src.common.logger import logger


def print_banner(desk_id: str = "982 411 723", port: int = 8000):
    lan_url = f"http://{config.local_ip}:{port}"
    local_url = f"http://localhost:{port}"
    banner = f"""
===================================================================
   ANTIGRAVITY AI REMOTE DESKTOP (AnyDesk-Style Python Engine)
===================================================================
   * Device Desk ID : \033[92m{desk_id}\033[0m
   * Local Machine  : \033[96m{local_url}\033[0m
   * Other Machines : \033[93m{lan_url}\033[0m (Open on phone/laptop on same Wi-Fi)
   * AI Copilot     : \033[92mReady (Multimodal 'Computer Use')\033[0m
   * Safety Guard   : \033[94m{config.safety_mode.capitalize()} Mode\033[0m
   * Emergency Stop : \033[91mEsc + Esc or Web UI Killswitch\033[0m
===================================================================
"""
    print(banner)


def open_browser_delayed(url: str, delay: float = 1.2):
    def _open():
        time.sleep(delay)
        webbrowser.open(url)
    threading.Thread(target=_open, daemon=True).start()


def main():
    parser = argparse.ArgumentParser(description="Antigravity AI Remote Desktop Assistant")
    parser.add_argument("--host", type=str, default=config.host, help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=config.port, help="Port to listen on (default: 8000)")
    parser.add_argument("--desk-id", type=str, default=config.desk_id, help="Custom 9-digit Desk ID")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open browser")
    parser.add_argument("--connect", type=str, help="Target Desk ID or IP to connect to immediately")
    args = parser.parse_args()

    desk_id = args.desk_id or config.desk_id
    print_banner(desk_id=desk_id, port=args.port)

    url = f"http://localhost:{args.port}"
    if not args.no_browser:
        logger.info(f"Opening Remote Desktop Controller in default browser: {url}")
        open_browser_delayed(url)

    # Launch server using uvicorn if available, or fallback
    try:
        import uvicorn
        logger.info(f"Starting ASGI Server with Uvicorn on {args.host}:{args.port} (LAN: http://{config.local_ip}:{args.port})...")
        uvicorn.run("src.server.app:app", host=args.host, port=args.port, log_level="info", reload=False)
    except ImportError:
        logger.warning("Uvicorn not found in current environment. Please install dependencies:")
        print(f"\n   \033[92mpip install -r requirements.txt\033[0m\n")
        print(f"Then run:\n   \033[96mpython src/main.py\033[0m\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
