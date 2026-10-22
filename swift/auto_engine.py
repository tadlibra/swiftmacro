"""AutoClick engine kiểu GS AutoClicker. Không phụ thuộc tkinter."""

import threading
import time

import mouse

BUTTONS = {"Trái": "left", "Phải": "right", "Giữa": "middle"}


def interval_ms(h, m, s, ms):
    return max(0, h) * 3600000 + max(0, m) * 60000 + max(0, s) * 1000 + max(0, ms)


def capture_position():
    """Chặn tới khi đọc được vị trí chuột (gọi trong thread riêng)."""
    return mouse.get_position()


class AutoClicker:
    def __init__(self):
        self.running = False
        self.stop_flag = threading.Event()
        self.count = 0

    def start(self, cfg, on_count=None, on_done=None):
        """cfg: {interval_ms, button, double, target|None, pos: None|(x, y)}."""
        self.running = True
        self.stop_flag.clear()
        self.count = 0
        threading.Thread(target=self._loop,
                         args=(cfg, on_count, on_done),
                         daemon=True).start()

    def stop(self):
        self.stop_flag.set()

    def _loop(self, cfg, on_count, on_done):
        try:
            interval = cfg["interval_ms"] / 1000.0
            btn = cfg["button"]
            dbl = cfg["double"]
            target = cfg["target"]
            pos = cfg["pos"]
            n = 0
            while not self.stop_flag.is_set():
                if pos is not None:
                    try:
                        mouse.move(*pos)
                    except Exception:
                        pass
                try:
                    if dbl:
                        mouse.double_click(btn)
                    else:
                        mouse.click(btn)
                except Exception:
                    pass
                n += 1
                self.count = n
                if on_count:
                    try:
                        on_count(n)
                    except Exception:
                        pass
                if target is not None and n >= target:
                    break
                end = time.time() + interval
                while time.time() < end:
                    if self.stop_flag.is_set():
                        return
                    time.sleep(0.005)
        finally:
            self.running = False
            if on_done:
                try:
                    on_done(self.count)
                except Exception:
                    pass
