"""Cấu hình chung: tên app, phiên bản, phím và giá trị mặc định."""

import os
import sys

APP_NAME = "SwiftMacro"
APP_VERSION = "2.0"
FILE_EXT = ".swiftmacro"

DEFAULT_RECORD_HOTKEY = "F9"
DEFAULT_PLAY_HOTKEY = "F10"
DEFAULT_CLICK_HOTKEY = "F8"

DEFAULT_INTERVAL = {"h": 0, "m": 0, "s": 0, "ms": 100}
DEFAULT_REPEAT_COUNT = 10

MOVE_THROTTLE_S = 0.015
RECORD_ARM_DELAY_S = 0.4
TICK_MS = 100
WINDOW_GEO = "700x940"
WINDOW_MIN = (640, 720)

TITLE_BG = "#F2B632"
DARK_INK = "#3B2F1E"


def _base_dir():
    """Thư mục gốc chứa assets: thư mục project khi chạy source,
    thư mục tạm _MEIPASS khi chạy file EXE đã đóng gói."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ASSETS_DIR = os.path.join(_base_dir(), "assets")
LOGO_PNG = os.path.join(ASSETS_DIR, "logo-64.png")
