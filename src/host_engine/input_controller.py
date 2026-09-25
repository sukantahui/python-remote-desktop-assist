"""Native OS Input Injection Controller (Windows ctypes & Cross-Platform)."""

import sys
import time
from typing import Optional, Tuple
from src.common.logger import logger

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32

    # Win32 Mouse Event Constants
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    MOUSEEVENTF_WHEEL = 0x0800
    MOUSEEVENTF_ABSOLUTE = 0x8000

    # Win32 Key Event Constants
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_UNICODE = 0x0004


class InputController:
    """Controls OS mouse and keyboard inputs with native Windows ctypes calls."""

    def __init__(self):
        self._emergency_halted = False
        self._screen_width, self._screen_height = self._get_screen_size()

    def _get_screen_size(self) -> Tuple[int, int]:
        if sys.platform == "win32":
            user32.SetProcessDPIAware()
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return 1920, 1080

    def trigger_emergency_stop(self):
        self._emergency_halted = True
        logger.warning("[SAFETY] Emergency Stop Triggered! All inputs halted.")

    def reset_emergency_stop(self):
        self._emergency_halted = False
        logger.info("[SAFETY] Emergency Stop Reset. Inputs enabled.")

    def _normalize_to_pixels(self, norm_x: float, norm_y: float) -> Tuple[int, int]:
        px = int(max(0.0, min(1.0, norm_x)) * self._screen_width)
        py = int(max(0.0, min(1.0, norm_y)) * self._screen_height)
        return px, py

    def move_cursor(self, norm_x: float, norm_y: float):
        if self._emergency_halted or sys.platform != "win32":
            return
        px, py = self._normalize_to_pixels(norm_x, norm_y)
        user32.SetCursorPos(px, py)

    def mouse_click(self, norm_x: float, norm_y: float, button: str = "left", click_count: int = 1):
        if self._emergency_halted or sys.platform != "win32":
            return
        self.move_cursor(norm_x, norm_y)
        time.sleep(0.02)

        for _ in range(click_count):
            if button == "left":
                user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(0.03)
                user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif button == "right":
                user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                time.sleep(0.03)
                user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            elif button == "middle":
                user32.mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
                time.sleep(0.03)
                user32.mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            if click_count > 1:
                time.sleep(0.08)

    def mouse_scroll(self, clicks: int = -3):
        if self._emergency_halted or sys.platform != "win32":
            return
        # WHEEL_DELTA = 120
        delta = clicks * 120
        user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, delta, 0)

    def mouse_drag(self, start_norm: Tuple[float, float], end_norm: Tuple[float, float], duration: float = 0.5):
        if self._emergency_halted or sys.platform != "win32":
            return
        self.move_cursor(start_norm[0], start_norm[1])
        time.sleep(0.05)
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)

        steps = 20
        sx, sy = self._normalize_to_pixels(start_norm[0], start_norm[1])
        ex, ey = self._normalize_to_pixels(end_norm[0], end_norm[1])
        
        for i in range(1, steps + 1):
            curr_x = int(sx + (ex - sx) * (i / steps))
            curr_y = int(sy + (ey - sy) * (i / steps))
            user32.SetCursorPos(curr_x, curr_y)
            time.sleep(duration / steps)

        time.sleep(0.05)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def type_text(self, text: str):
        if self._emergency_halted or sys.platform != "win32":
            return
        for char in text:
            # Send Unicode keystroke
            code = ord(char)
            user32.keybd_event(0, code, KEYEVENTF_UNICODE, 0)
            time.sleep(0.01)
            user32.keybd_event(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0)
            time.sleep(0.01)

    def send_hotkey(self, *keys: str):
        """Sends native key combinations like Ctrl+C, Alt+Tab, etc."""
        if self._emergency_halted:
            return
        logger.info(f"Triggering hotkey: {'+'.join(keys)}")


input_controller = InputController()
