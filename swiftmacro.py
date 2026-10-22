"""SwiftMacro launcher. Toàn bộ app nằm trong package `swift/`:

- swift/config.py       → tên app, phím/hotkey mặc định
- swift/theme.py         → palette, icon pixel, nút bevel, SegmentBar
- swift/macro_engine.py  → ghi + phát lại macro (không dính tkinter)
- swift/auto_engine.py   → auto click kiểu GS AutoClicker
- swift/panels.py        → 3 panel UI: Macro, AutoClick, Hotkeys
- swift/app.py           → MacroApp: chrome cửa sổ + lắp ráp + file IO
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swift.app import main

if __name__ == "__main__":
    main()
