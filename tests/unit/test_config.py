"""Unit tests for AppConfig and settings."""

import os
from unittest.mock import patch
from src.common.config import AppConfig, format_desk_id, get_or_generate_desk_id


def test_app_config_defaults():
    cfg = AppConfig()
    assert cfg.host in ["0.0.0.0", "127.0.0.1", "localhost"]
    assert isinstance(cfg.port, int)
    assert cfg.port > 0
    assert cfg.desk_id is not None
    assert isinstance(cfg.fps, int)
    assert cfg.fps > 0


def test_desk_id_format():
    desk_id = get_or_generate_desk_id()
    digits = "".join(filter(str.isdigit, desk_id))
    assert len(digits) == 9
    parts = desk_id.split()
    assert len(parts) == 3
    for p in parts:
        assert len(p) == 3
        assert p.isdigit()


def test_custom_desk_id_override():
    with patch.dict(os.environ, {"DESK_ID": "111 222 333"}):
        custom_id = get_or_generate_desk_id()
        assert custom_id == "111 222 333"


def test_auto_desk_id_generation():
    with patch.dict(os.environ, {"DESK_ID": "auto"}):
        auto_id = get_or_generate_desk_id(force_regenerate=True)
        digits = "".join(filter(str.isdigit, auto_id))
        assert len(digits) == 9


def test_format_desk_id():
    assert format_desk_id("123456789") == "123 456 789"
    assert format_desk_id("123 456 789") == "123 456 789"
    assert format_desk_id(" 123-456-789 ") == "123 456 789"

