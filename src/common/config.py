"""Configuration Manager and Network Discovery for AI Remote Desktop."""

import os
import socket
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    # Load .env from project root
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass


def get_local_ip() -> str:
    """Discovers the machine's primary local LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


class AppConfig:
    def __init__(self):
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.desk_id: str = os.getenv("DESK_ID", "982 411 723")
        self.secret_key: str = os.getenv("SECRET_KEY", "antigravity-secret-key-2026")
        self.unattended_password: str = os.getenv("UNATTENDED_ACCESS_PASSWORD", "")
        self.rendezvous_server: str = os.getenv("RENDEZVOUS_SERVER", "")
        self.default_vlm_provider: str = os.getenv("DEFAULT_VLM_PROVIDER", "gemini")
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
        self.safety_mode: str = os.getenv("SAFETY_MODE", "interactive")
        self.fps: int = int(os.getenv("STREAM_FPS", "30"))
        self.local_ip: str = get_local_ip()
        self.hostname: str = socket.gethostname()

    @property
    def lan_url(self) -> str:
        return f"http://{self.local_ip}:{self.port}"


config = AppConfig()
