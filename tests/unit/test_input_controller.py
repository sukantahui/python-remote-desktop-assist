"""Unit tests for Input Controller and safety mechanisms."""

from src.host_engine.input_controller import InputController


def test_input_controller_normalization():
    controller = InputController()
    width, height = controller._screen_width, controller._screen_height
    
    px, py = controller._normalize_to_pixels(0.5, 0.5)
    assert px == int(0.5 * width)
    assert py == int(0.5 * height)

    px_min, py_min = controller._normalize_to_pixels(-0.2, -0.5)
    assert px_min == 0
    assert py_min == 0

    px_max, py_max = controller._normalize_to_pixels(1.5, 2.0)
    assert px_max == width
    assert py_max == height


def test_emergency_stop_toggle():
    controller = InputController()
    assert controller._emergency_halted is False
    
    controller.trigger_emergency_stop()
    assert controller._emergency_halted is True
    
    controller.reset_emergency_stop()
    assert controller._emergency_halted is False
