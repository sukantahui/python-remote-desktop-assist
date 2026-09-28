"""Unit tests for AppConfig and settings."""

from src.common.config import AppConfig


def test_app_config_defaults():
    cfg = AppConfig()
    assert cfg.host in ["0.0.0.0", "127.0.0.1", "localhost"]
    assert isinstance(cfg.port, int)
    assert cfg.port > 0
    assert cfg.desk_id is not None
    assert isinstance(cfg.fps, int)
    assert cfg.fps > 0
