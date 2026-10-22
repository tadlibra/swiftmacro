"""Macro engine: ghi + phát lại chuột/phím. Không phụ thuộc tkinter.

Callbacks được gọi từ thread hook/phát lại — phía UI phải tự điều phối
về main thread (``root.after``).
"""

import threading
import time

import keyboard
import mouse

from .config import MOVE_THROTTLE_S, RECORD_ARM_DELAY_S


class MacroRecorder:
    def __init__(self):
        self.events = []
        self.recording = False
        self.playing = False
        self.stop_flag = threading.Event()
        self.record_start = 0
        self._last_move = 0

    # ---------- recording ----------
    def start_record(self, on_count=None):
        def _wrap(fn):
            def _cb(e):
                fn(e)
                if on_count is not None:
                    try:
                        on_count(len(self.events))
                    except Exception:
                        pass
            return _cb

        self.events = []
        self.recording = True
        self.record_start = time.time() + RECORD_ARM_DELAY_S
        self._mouse_cb = _wrap(self._on_mouse)
        self._key_cb = _wrap(self._on_keyboard)
        mouse.hook(self._mouse_cb)
        keyboard.hook(self._key_cb)

    def stop_record(self):
        for fn, h in ((mouse.unhook, getattr(self, "_mouse_cb", None)),
                      (keyboard.unhook, getattr(self, "_key_cb", None))):
            try:
                if h is not None:
                    fn(h)
            except Exception:
                pass
        self.recording = False
        if self.events:
            t0 = self.events[0]["t"]
            for e in self.events:
                e["t"] -= t0
        return len(self.events)

    def _stamp(self):
        return time.time() - self.record_start

    def _on_mouse(self, e):
        if not self.recording or time.time() < self.record_start:
            return
        if isinstance(e, mouse.MoveEvent):
            now = time.time()
            if now - self._last_move < MOVE_THROTTLE_S:
                return
            self._last_move = now
            self.events.append({"t": self._stamp(), "kind": "move", "x": e.x, "y": e.y})
        elif isinstance(e, mouse.ButtonEvent):
            self.events.append({"t": self._stamp(), "kind": "mouse",
                                "button": e.button, "type": e.event_type})
        elif isinstance(e, mouse.WheelEvent):
            self.events.append({"t": self._stamp(), "kind": "wheel", "delta": e.delta})

    def _on_keyboard(self, e):
        if not self.recording or time.time() < self.record_start:
            return
        if e.event_type not in ("down", "up"):
            return
        self.events.append({"t": self._stamp(), "kind": "key",
                            "name": e.name, "type": e.event_type})

    # ---------- playback ----------
    def start_play(self, settings, on_progress=None, on_done=None):
        """settings: {"continuous": bool, "loops": int}."""
        self.playing = True
        self.stop_flag.clear()
        threading.Thread(target=self._play_loop,
                         args=(settings, on_progress, on_done),
                         daemon=True).start()

    def request_stop(self):
        self.stop_flag.set()

    def _play_loop(self, settings, on_progress, on_done):
        try:
            run = 0
            total = len(self.events)
            while not self.stop_flag.is_set():
                self._play_once(
                    lambda i: on_progress(i, total) if on_progress else None)
                run += 1
                if not settings.get("continuous") and run >= max(1, settings.get("loops", 1)):
                    break
        finally:
            self.playing = False
            if on_done:
                try:
                    on_done()
                except Exception:
                    pass

    def _play_once(self, on_step=None):
        prev = 0
        for i, e in enumerate(self.events):
            if self.stop_flag.is_set():
                break
            delay = e["t"] - prev
            if delay > 0:
                end = time.time() + delay
                while time.time() < end:
                    if self.stop_flag.is_set():
                        return
                    time.sleep(0.005)
            prev = e["t"]
            if on_step:
                on_step(i + 1)
            kind = e["kind"]
            try:
                if kind == "move":
                    mouse.move(e["x"], e["y"])
                elif kind == "mouse":
                    if e["type"] == "down":
                        mouse.press(e["button"])
                    elif e["type"] == "double":
                        mouse.double_click(e["button"])
                    else:
                        mouse.release(e["button"])
                elif kind == "wheel":
                    mouse.wheel(e["delta"])
                elif kind == "key":
                    if e["type"] == "down":
                        keyboard.press(e["name"])
                    else:
                        keyboard.release(e["name"])
            except Exception:
                pass
