"""Configuration Manager for AI Remote Desktop."""

import os
from pathlib import Path
from typing import Optional


class AppConfig:
    def __init__(self):
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.desk_id: str = os.getenv("DESK_ID", "982 411 723")
        self.secret_key: str = os.getenv("SECRET_KEY", "antigravity-secret-key-2026")
        self.default_vlm_provider: str = os.getenv("DEFAULT_VLM_PROVIDER", "gemini")
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
        self.safety_mode: str = os.getenv("SAFETY_MODE", "interactive")
        self.fps: int = int(os.getenv("STREAM_FPS", "30"))


config = AppConfig()
