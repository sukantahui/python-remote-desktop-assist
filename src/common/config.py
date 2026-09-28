"""Configuration Manager and Network Discovery for AI Remote Desktop."""

import hashlib
import os
import platform
import socket
import uuid
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


def get_machine_fingerprint() -> str:
    """Collects stable hardware and OS identifiers to create a unique machine fingerprint."""
    components = [
        str(uuid.getnode()),
        socket.gethostname(),
        platform.node(),
        platform.machine(),
    ]
    
    # Windows: read cryptographic MachineGuid
    if platform.system() == "Windows":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography") as key:
                guid, _ = winreg.QueryValueEx(key, "MachineGuid")
                if guid:
                    components.append(str(guid))
        except Exception:
            pass
    # Linux: read system machine-id
    elif platform.system() == "Linux":
        for mid_path in [Path("/etc/machine-id"), Path("/var/lib/dbus/machine-id")]:
            if mid_path.exists():
                try:
                    components.append(mid_path.read_text(encoding="utf-8").strip())
                    break
                except Exception:
                    pass

    return "_".join(components)


def format_desk_id(raw_id: str) -> str:
    """Formats a 9-digit string into standard AnyDesk format 'XXX XXX XXX'."""
    digits = "".join(filter(str.isdigit, raw_id))
    if len(digits) == 9:
        return f"{digits[0:3]} {digits[3:6]} {digits[6:9]}"
    return raw_id.strip()


def get_or_generate_desk_id(force_regenerate: bool = False) -> str:
    """
    Returns a unique, persistent 9-digit AnyDesk-style Device ID (e.g. '465 145 922').
    
    Priority:
    1. Explicit custom DESK_ID from environment (unless set to 'auto', empty, or legacy template placeholder).
    2. Cached persistent ID file in user home directory (~/.antigravity_desk_id).
    3. Deterministically computed 9-digit ID from the host's unique hardware fingerprint.
    """
    custom_id = os.getenv("DESK_ID", "").strip()
    # If the user explicitly provided a unique custom ID other than the default template placeholders
    if custom_id and custom_id.lower() not in ("auto", "generate", "default", "none", "", "982 411 723", "982411723"):
        return format_desk_id(custom_id)

    id_file = Path.home() / ".antigravity_desk_id"
    if not force_regenerate and id_file.exists():
        try:
            cached_id = id_file.read_text(encoding="utf-8").strip()
            digits = "".join(filter(str.isdigit, cached_id))
            if len(digits) == 9:
                return format_desk_id(cached_id)
        except Exception:
            pass

    # Deterministically derive a 9-digit ID from the machine fingerprint
    fingerprint = get_machine_fingerprint()
    hash_hex = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()
    hash_int = int(hash_hex[:8], 16)
    
    # Map into 9-digit range (100 000 000 to 999 999 999)
    desk_num = 100000000 + (hash_int % 900000000)
    desk_id_str = format_desk_id(str(desk_num))

    # Persist locally so it remains constant across all runs
    try:
        id_file.write_text(desk_id_str, encoding="utf-8")
    except Exception:
        pass

    return desk_id_str


class AppConfig:
    def __init__(self):
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.desk_id: str = get_or_generate_desk_id()
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

