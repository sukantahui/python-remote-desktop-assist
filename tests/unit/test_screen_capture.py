"""Unit tests for Screen Capture Engine."""

from src.host_engine.screen_capture import ScreenCaptureEngine


def test_screen_capture_resolution():
    engine = ScreenCaptureEngine()
    width, height = engine.get_screen_resolution()
    assert isinstance(width, int) and width > 0
    assert isinstance(height, int) and height > 0


def test_screen_capture_jpeg():
    engine = ScreenCaptureEngine()
    frame = engine.capture_jpeg(quality=50)
    assert isinstance(frame, bytes)
    assert len(frame) > 0
    # Valid JPEG magic bytes start with \xff\xd8
    assert frame.startswith(b"\xff\xd8")
