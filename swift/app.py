"""MacroApp: lắp chrome + panels + engines thành app hoàn chỉnh."""

import json
import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import keyboard

from . import theme
from .auto_engine import BUTTONS as AC_BUTTONS
from .auto_engine import AutoClicker, capture_position, interval_ms
from .config import (APP_NAME, APP_VERSION, DEFAULT_CLICK_HOTKEY,
                     DEFAULT_PLAY_HOTKEY, DEFAULT_RECORD_HOTKEY, FILE_EXT,
                     LOGO_PNG, RECORD_ARM_DELAY_S, TICK_MS, TITLE_BG, DARK_INK,
                     WINDOW_GEO, WINDOW_MIN)
from .macro_engine import MacroRecorder
from .panels import AutoClickPanel, HotkeyPanel, MacroPanel


class MacroApp:
    BAR_BG = TITLE_BG
    DARK_INK = DARK_INK

    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry(WINDOW_GEO)
        self.root.minsize(*WINDOW_MIN)
        self.root.resizable(True, True)
        self.root.configure(bg=theme.THEME["bg"])
        try:
            self.logo_img = tk.PhotoImage(file=LOGO_PNG).subsample(3, 3)
            self.root.iconphoto(True, self.logo_img)
        except Exception:
            self.logo_img = None

        # macro settings
        self.record_hotkey = DEFAULT_RECORD_HOTKEY
        self.play_hotkey = DEFAULT_PLAY_HOTKEY
        self.continuous = False
        self.loops = 1
        self.file_path = None
        # autoclick settings
        self.ac_hotkey = DEFAULT_CLICK_HOTKEY

        self.recorder = MacroRecorder()
        self.autoclicker = AutoClicker()

        theme.apply_style(self.root, TITLE_BG, DARK_INK)
        self._build_ui()
        self._register_hotkeys()

    # ---------- build UI ----------
    def _build_ui(self):
        # ---- custom titlebar: thay thanh Windows → chỉ còn 1 header ----
        self.root.overrideredirect(True)
        self._fix_taskbar()
        titlebar = tk.Frame(self.root, bg=self.BAR_BG, padx=8, pady=6,
                            highlightthickness=0, bd=0)
        titlebar.pack(fill="x")
        if self.logo_img:
            _lg = tk.Label(titlebar, image=self.logo_img, bg=self.BAR_BG, bd=0)
            _lg.pack(side="left", padx=(0, 8))
            _lg.bind("<ButtonPress-1>", self._drag_start)
            _lg.bind("<B1-Motion>", self._drag_move)
        self.title_label = tk.Label(titlebar, text="SwiftMacro 2.0", bg=self.BAR_BG,
                                   fg=self.DARK_INK, font=("Courier New", 13, "bold"),
                                   anchor="w", bd=0)
        self.title_label.pack(side="left", fill="x", expand=True)
        lamp_box = tk.Frame(titlebar, bg=self.BAR_BG)
        lamp_box.pack(side="left", padx=(0, 6))
        self.lamp = tk.Canvas(lamp_box, width=12, height=12, bg=self.BAR_BG,
                              highlightthickness=0, bd=0)
        self.lamp.pack(side="left", padx=(0, 6))
        self.lamp_dot = self.lamp.create_oval(1, 1, 11, 11,
                                              fill="#16A34A", outline="#16A34A")
        self.state_word = tk.Label(lamp_box, text="Sẵn sàng", fg="#16A34A",
                                   bg=self.BAR_BG, font=("Segoe UI", 10, "bold"), bd=0)
        self.state_word.pack(side="left")
        # pack side=right theo thứ tự này → hiển thị trái-sang: – ▢ ✕
        for _kind, _fn in (("close", self._close_app), ("max", self._max_win),
                           ("min", self._min_win)):
            _wb = theme.pixel_button(
                titlebar, "", "#F7D774", self.DARK_INK, _fn,
                icon=theme.win_icon("close" if _kind == "close" else _kind,
                                     "#3B2F1E"))
            _wb.pack(side="right", padx=2)
        titlebar.bind("<ButtonPress-1>", self._drag_start)
        titlebar.bind("<B1-Motion>", self._drag_move)
        self.title_label.bind("<ButtonPress-1>", self._drag_start)
        self.title_label.bind("<B1-Motion>", self._drag_move)
        lamp_box.bind("<ButtonPress-1>", self._drag_start)
        lamp_box.bind("<B1-Motion>", self._drag_move)
        self.root.bind("<Alt-F4>", lambda e: self._close_app())
        self._zoomed = False
        self._norm_geo = None
        _grip = tk.Canvas(self.root, width=18, height=18, bg="#F2B632",
                          highlightthickness=0, bd=0, cursor="size_nw_se")
        for _i in range(3):
            _o = 4 + _i * 4
            _grip.create_line(_o, 17, 17, _o, fill="#3B2F1E", width=2)
        _grip.place(relx=1.0, rely=1.0, anchor="se")
        _grip.bind("<ButtonPress-1>", self._grip_start)
        _grip.bind("<B1-Motion>", self._grip_move)
        self.root.bind("<Map>", lambda e: self.root.after(30, self._repaint))

        # ---- toolbar pixel: 5 nút cùng cỡ, icon pixel + text ----
        bar = tk.Frame(self.root, bg=theme.THEME["bg"], padx=10, pady=10)
        bar.pack(fill="x")
        self._bar = bar
        for i in range(5):
            bar.columnconfigure(i, weight=1, uniform="tb")
        GOLD, GINK = "#F7D774", "#3B2F1E"
        self.btn_open = theme.pixel_button(
            bar, "Open", GOLD, GINK, self.open_file,
            icon=theme.get_icon("folder", "#3B2F1E"))
        self.btn_open.grid(row=0, column=0, sticky="nsew", padx=3)
        self.btn_save = theme.pixel_button(
            bar, "Save", GOLD, GINK, self.save_file,
            icon=theme.get_icon("disk", "#3B2F1E"))
        self.btn_save.grid(row=0, column=1, sticky="nsew", padx=3)
        self.btn_record = theme.pixel_button(
            bar, "Record", "#B91C1C", "#FFFFFF", self.toggle_record,
            icon=theme.get_icon("record", "#FFFFFF"))
        self.btn_record.grid(row=0, column=2, sticky="nsew", padx=3)
        self.btn_play = theme.pixel_button(
            bar, "Play", "#2FA84F", "#FFFFFF", self.toggle_play,
            icon=theme.get_icon("play", "#FFFFFF"))
        self.btn_play.grid(row=0, column=3, sticky="nsew", padx=3)
        self.btn_settings = theme.pixel_button(
            bar, "Hotkeys  ▾", GOLD, GINK, self.toggle_hotkey_panel,
            icon=theme.get_icon("sliders", "#3B2F1E"))
        self.btn_settings.grid(row=0, column=4, sticky="nsew", padx=3)

        # ---- guide strip ----
        hintbar = tk.Frame(self.root, bg="#E4F3C2", padx=12, pady=6,
                           highlightthickness=1, highlightbackground="#7A9A4A", bd=0)
        hintbar.pack(fill="x", padx=10, pady=(0, 2))
        self.hint_short = tk.Label(
            hintbar, bg="#E4F3C2", fg="#1D4ED8", justify="left",
            font=("Segoe UI", 9),
            text="Record → thao tác → Record lần nữa để dừng → Play để chạy lại.  "
                 "Chi tiết ▸")
        self.hint_short.pack(side="left", fill="x", expand=True)
        self.hint_full = tk.Label(
            hintbar, bg="#E4F3C2", fg="#2F4A12", justify="left", wraplength=560,
            font=("Segoe UI", 9),
            text="1) Bấm Record (hoặc F9) → thao tác chuột/phím cần lặp.\n"
                 "2) Bấm Record lần nữa để dừng → xem lại Steps, bấm Clear nếu ghi sai.\n"
                 "3) Bấm Play (hoặc F10) để chạy lại; chỉnh vòng lặp trong Hotkeys ▾.")
        self._hint_open = False

        def _toggle_hint(e=None):
            self._hint_open = not self._hint_open
            if self._hint_open:
                self.hint_full.pack(fill="x", pady=(2, 0))
                self.hint_short.configure(text="Record → thao tác → Stop → Play.  Thu gọn ▾")
            else:
                self.hint_full.pack_forget()
                self.hint_short.configure(
                    text="Record → thao tác → Record lần nữa để dừng → Play để chạy lại.  "
                         "Chi tiết ▸")
        self.hint_short.bind("<Button-1>", _toggle_hint)
        self.hint_short.configure(cursor="hand2")

        # ---- dropdown Hotkeys (không mở popup mới) ----
        self.hot_panel = HotkeyPanel(self.root, self.root,
                                     self._save_hotkeys, self._reset_hotkeys)
        # (chưa pack — toggle_hotkey_panel sẽ pack/forget)

        # ---- Auto Click kiểu GS AutoClicker ----
        self.ac_panel = AutoClickPanel(self.root, self.toggle_autoclick,
                                       self.pick_ac_position)
        self.ac_panel.pack(fill="x", padx=10, pady=(0, 6))
        self.ac_panel.set_click_hotkey(self.ac_hotkey)

        body = ttk.Frame(self.root, padding=(10, 6, 10, 10))
        body.pack(fill="both", expand=True)
        self.macro_panel = MacroPanel(body, self.clear_events)
        self.macro_panel.pack(fill="both", expand=True)

        # ---- grass strip footer (trang trí; trạng thái nằm ở thẻ Macro) ----
        _grass = theme.get_grass()
        if _grass is not None:
            _gl = tk.Label(self.root, image=_grass, bd=0,
                           highlightthickness=0)
            _gl.image = _grass
            _gl.pack(fill="x", side="bottom")
        self._center_on_cursor_monitor()
        self._refresh()

    # ---------- custom window chrome ----------
    def _fix_taskbar(self):
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW, WS_EX_TOOLWINDOW = 0x40000, 0x80
            st = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
                                                (st | WS_EX_APPWINDOW) & ~WS_EX_TOOLWINDOW)
        except Exception:
            pass

    def _drag_start(self, e):
        self._dx = e.x_root - self.root.winfo_x()
        self._dy = e.y_root - self.root.winfo_y()

    def _drag_move(self, e):
        self.root.geometry(f"+{e.x_root - self._dx}+{e.y_root - self._dy}")

    def _min_win(self):
        try:
            self.root.iconify()
        except Exception:
            pass

    def _monitor_workarea(self):
        """Workarea (trừ taskbar) của monitor đang chứa cửa sổ. None nếu lỗi."""
        try:
            import ctypes
            from ctypes import wintypes

            class _RECT(ctypes.Structure):
                _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG),
                             ("right", wintypes.LONG), ("bottom", wintypes.LONG)]

            class _MONITORINFO(ctypes.Structure):
                _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", _RECT),
                             ("rcWork", _RECT), ("dwFlags", wintypes.DWORD)]

            user32 = ctypes.windll.user32
            hwnd = user32.GetParent(self.root.winfo_id())
            hmon = user32.MonitorFromWindow(hwnd, 2)  # MONITOR_DEFAULTTONEAREST
            mi = _MONITORINFO()
            mi.cbSize = ctypes.sizeof(_MONITORINFO)
            if user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                r = mi.rcWork
                return (r.left, r.top, r.right, r.bottom)
        except Exception:
            pass
        return None

    def _center_on_cursor_monitor(self):
        """Mở app giữa monitor đang có chuột (không hard-code monitor chính)."""
        try:
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            hmon = user32.MonitorFromPoint(pt, 2)

            class _RECT(ctypes.Structure):
                _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG),
                             ("right", wintypes.LONG), ("bottom", wintypes.LONG)]

            class _MONITORINFO(ctypes.Structure):
                _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", _RECT),
                             ("rcWork", _RECT), ("dwFlags", wintypes.DWORD)]

            mi = _MONITORINFO()
            mi.cbSize = ctypes.sizeof(_MONITORINFO)
            if not user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                return
            w, h = (int(v) for v in WINDOW_GEO.split("x"))
            rw = mi.rcWork.right - mi.rcWork.left
            rh = mi.rcWork.bottom - mi.rcWork.top
            x = mi.rcWork.left + max(0, (rw - w) // 2)
            y = mi.rcWork.top + max(0, (rh - h) // 2)
            self.root.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def _max_win(self):
        try:
            if not self._zoomed:
                self._norm_geo = self.root.geometry()
                area = self._monitor_workarea()
                if area:
                    l, t, r, b = area
                    self.root.geometry(f"{r - l}x{b - t}+{l}+{t}")
                else:
                    self.root.geometry(f"{self.root.winfo_screenwidth()}x"
                                        f"{self.root.winfo_screenheight()}+0+0")
                self._zoomed = True
            else:
                if self._norm_geo:
                    self.root.geometry(self._norm_geo)
                self._zoomed = False
            self.root.update_idletasks()
            self.macro_panel.pbar.refresh()
        except Exception:
            pass

    def _grip_start(self, e):
        self._gx, self._gy = e.x_root, e.y_root
        self._gw, self._gh = self.root.winfo_width(), self.root.winfo_height()

    def _grip_move(self, e):
        w = max(WINDOW_MIN[0], self._gw + e.x_root - self._gx)
        h = max(WINDOW_MIN[1], self._gh + e.y_root - self._gy)
        self.root.geometry(f"{w}x{h}")

    def _set_title_file(self, path):
        base = os.path.basename(path) if path else ""
        self.title_label.config(
            text=f"SwiftMacro 2.0  —  {base}" if base else "SwiftMacro 2.0")

    def _close_app(self):
        if self.recorder.recording or self.recorder.playing or self.autoclicker.running:
            try:
                ok = messagebox.askokcancel(
                    "Thoát?", "Đang chạy — thoát sẽ dừng hết. Thoát luôn?")
            except Exception:
                ok = True
            if not ok:
                return
        try:
            self.recorder.request_stop()
            self.autoclicker.stop()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def _repaint(self):
        try:
            self.root.update_idletasks()
            self.macro_panel.pbar.refresh()
            self._refresh()
        except Exception:
            pass

    # ---------- hotkey dropdown ----------
    def toggle_hotkey_panel(self):
        if self.hot_panel.winfo_ismapped():
            self.hot_panel.pack_forget()
            self.btn_settings.inner.configure(text="Hotkeys  ▾")
        else:
            self.hot_panel.load(self.record_hotkey, self.play_hotkey,
                                self.ac_hotkey, self.continuous, self.loops)
            self.hot_panel.pack(fill="x", padx=10, pady=(0, 6), after=self._bar)
            self.btn_settings.inner.configure(text="Hotkeys  ▴")

    def _save_hotkeys(self):
        try:
            rh, ph, ch, cont, loops = self.hot_panel.collect()
        except ValueError as e:
            messagebox.showwarning("Hotkeys", str(e))
            return
        self.record_hotkey, self.play_hotkey, self.ac_hotkey = rh, ph, ch
        self.continuous = cont
        self.loops = loops
        self.ac_panel.set_click_hotkey(ch)
        self._register_hotkeys()
        self.toggle_hotkey_panel()
        self._refresh(f"Hotkeys: rec={self.record_hotkey} play={self.play_hotkey} "
                      f"click={self.ac_hotkey} "
                      f"loops={'inf' if self.continuous else self.loops}")

    def _reset_hotkeys(self):
        self.hot_panel.reset_defaults(DEFAULT_RECORD_HOTKEY,
                                      DEFAULT_PLAY_HOTKEY,
                                      DEFAULT_CLICK_HOTKEY)

    # ---------- state lamp ----------
    def _set_dot(self, mode):
        modes = {"ready": ("Sẵn sàng", "#16A34A"), "rec": ("Đang ghi", "#B91C1C"),
                 "play": ("Đang chạy", "#2563EB"),
                 "click": ("Auto click", "#2FA84F")}
        word, col = modes.get(mode, modes["ready"])
        try:
            self.lamp.itemconfig(self.lamp_dot, fill=col, outline=col)
            self.state_word.config(text=word, fg=col)
        except Exception:
            pass

    # ---------- refresh ----------
    def clear_events(self):
        if self.recorder.recording or self.recorder.playing:
            return
        self.recorder.events = []
        self.macro_panel.pbar.set(0.0)
        self._refresh("Cleared. Ready to record.")

    def _refresh(self, msg=None):
        n = len(self.recorder.events)
        dur = self.recorder.events[-1]["t"] if self.recorder.events else 0.0
        self.macro_panel.detail_var.set(f"Events: {n}")
        self.macro_panel.dur_var.set(f"Duration: {dur:.1f}s")
        self.macro_panel.set_hotkeys_hint(
            f"rec={self.record_hotkey} play={self.play_hotkey} "
            f"click={self.ac_hotkey}")
        if msg is not None:
            self.macro_panel.status_var.set(msg)
        self.btn_record.inner.config(text="Stop" if self.recorder.recording else "Record")
        self.btn_play.inner.config(text="Stop" if self.recorder.playing else "Play")
        if not self.recorder.recording and not self.recorder.playing \
                and not self.autoclicker.running:
            self._set_dot("ready")
        self.macro_panel.refresh_tree(self.recorder.events)

    # ---------- file ----------
    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[(f"{APP_NAME} macro", f"*{FILE_EXT}"),
                       ("TinyTasks macro", "*.tinytask"), ("JSON", "*.json")],
            defaultextension=FILE_EXT,
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.recorder.events = data.get("events", [])
            s = data.get("settings", {})
            self.record_hotkey = s.get("record_hotkey", self.record_hotkey)
            self.play_hotkey = s.get("play_hotkey", self.play_hotkey)
            self.continuous = s.get("continuous", self.continuous)
            self.loops = s.get("loops", self.loops)
            a = data.get("autoclick", {})
            if a:
                p = self.ac_panel
                p.ac_h.set(a.get("h", p.ac_h.get()))
                p.ac_m.set(a.get("m", p.ac_m.get()))
                p.ac_s.set(a.get("s", p.ac_s.get()))
                p.ac_ms.set(a.get("ms", p.ac_ms.get()))
                p.ac_button.set(a.get("button", p.ac_button.get()))
                p.ac_type.set(a.get("type", p.ac_type.get()))
                p.ac_rep.set(a.get("rep", p.ac_rep.get()))
                p.ac_n.set(a.get("n", p.ac_n.get()))
                p.ac_pos.set(a.get("pos", p.ac_pos.get()))
                p.ac_x.set(a.get("x", p.ac_x.get()))
                p.ac_y.set(a.get("y", p.ac_y.get()))
                self.ac_hotkey = a.get("hotkey", self.ac_hotkey)
                p.set_click_hotkey(self.ac_hotkey)
            self.file_path = path
            self._set_title_file(path)
            self._register_hotkeys()
            self._refresh(f"Loaded {path} ({len(self.recorder.events)} events)")
        except Exception as e:
            messagebox.showerror("Open failed", str(e))

    def save_file(self):
        path = self.file_path or ""
        if not path:
            path = filedialog.asksaveasfilename(
                filetypes=[(f"{APP_NAME} macro", f"*{FILE_EXT}")],
                defaultextension=FILE_EXT,
            )
        if not path:
            return
        try:
            p = self.ac_panel
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"events": self.recorder.events,
                           "settings": {"record_hotkey": self.record_hotkey,
                                        "play_hotkey": self.play_hotkey,
                                        "continuous": self.continuous,
                                        "loops": self.loops},
                           "app": APP_NAME, "version": APP_VERSION,
                           "autoclick": {"h": int(p.ac_h.get()),
                                         "m": int(p.ac_m.get()),
                                         "s": int(p.ac_s.get()),
                                         "ms": int(p.ac_ms.get()),
                                         "button": p.ac_button.get(),
                                         "type": p.ac_type.get(),
                                         "rep": p.ac_rep.get(),
                                         "n": int(p.ac_n.get()),
                                         "pos": p.ac_pos.get(),
                                         "x": int(p.ac_x.get()),
                                         "y": int(p.ac_y.get()),
                                         "hotkey": self.ac_hotkey}}, f)
            self.file_path = path
            self._set_title_file(path)
            self._refresh(f"Saved to {path}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))

    # ---------- record / playback ----------
    def toggle_record(self):
        if self.recorder.playing or self.autoclicker.running:
            return
        if self.recorder.recording:
            self.stop_record()
        else:
            self.start_record()

    def start_record(self):
        self.recorder.start_record(
            on_count=lambda n: self.root.after(
                0, lambda: self.macro_panel.detail_var.set(f"Events: {n}")))
        self._set_dot("rec")
        self._refresh("Recording... press Record again to stop.")
        self._tick_id = self.root.after(TICK_MS, self._tick)

    def _tick(self):
        if not self.recorder.recording:
            return
        elapsed = max(0.0, time.time() - self.recorder.record_start
                      - RECORD_ARM_DELAY_S)
        self.macro_panel.dur_var.set(f"Duration: {elapsed:.1f}s")
        self.macro_panel.detail_var.set(f"Events: {len(self.recorder.events)}")
        self.macro_panel.status_var.set(
            f"Recording... {elapsed:.1f}s • {len(self.recorder.events)} events")
        self._tick_id = self.root.after(TICK_MS, self._tick)

    def stop_record(self):
        n = self.recorder.stop_record()
        try:
            if getattr(self, "_tick_id", None):
                self.root.after_cancel(self._tick_id)
                self._tick_id = None
        except Exception:
            pass
        self._refresh(f"Recorded {n} events.")

    def toggle_play(self):
        if self.recorder.recording or self.autoclicker.running:
            return
        if self.recorder.playing:
            self.recorder.request_stop()
        else:
            self.start_play()

    def start_play(self):
        if not self.recorder.events:
            messagebox.showinfo("Nothing to play", "Record or open a macro first.")
            return
        self._set_dot("play")
        self._refresh("Playing... press Play again to stop.")
        self.recorder.start_play(
            {"continuous": self.continuous, "loops": self.loops},
            on_progress=lambda i, t: self.root.after(
                0, lambda: self.macro_panel.pbar.set(i / max(1, t))),
            on_done=lambda: self.root.after(0, self._play_done))

    def _play_done(self):
        self.macro_panel.pbar.set(1.0)
        self._refresh("Done.")

    # ---------- auto click ----------
    def toggle_autoclick(self):
        if self.recorder.recording or self.recorder.playing:
            return
        if self.autoclicker.running:
            self.autoclicker.stop()
        else:
            self.start_autoclick()

    def _read_ac_ints(self):
        p = self.ac_panel
        try:
            return (int(p.ac_h.get()), int(p.ac_m.get()),
                    int(p.ac_s.get()), int(p.ac_ms.get()),
                    int(p.ac_n.get()), int(p.ac_x.get()), int(p.ac_y.get()))
        except Exception:
            raise ValueError("Số giờ/phút/giây/ms, số lần và X/Y phải là số.")

    def start_autoclick(self):
        try:
            h, m, s, ms, n, x, y = self._read_ac_ints()
        except ValueError as e:
            messagebox.showwarning("Auto Click", str(e))
            return
        if interval_ms(h, m, s, ms) < 1:
            messagebox.showwarning("Auto Click",
                                   "Khoảng nghỉ phải lớn hơn 0 (vd 100 mili giây).")
            return
        p = self.ac_panel
        target = max(1, n) if p.ac_rep.get() == "n" else None
        pos = (x, y) if p.ac_pos.get() == "fixed" else None
        btn = AC_BUTTONS.get(p.ac_button.get(), "left")
        dbl = p.ac_type.get() == "Đúp"
        self.ac_panel.set_hint("Chưa chạy")
        self.ac_panel.set_running(True)
        self._set_dot("click")
        self.macro_panel.status_var.set("Auto Click đang chạy… bấm Stop hoặc F8 để dừng.")
        self.autoclicker.start(
            {"interval_ms": interval_ms(h, m, s, ms), "button": btn,
             "double": dbl, "target": target, "pos": pos},
            on_count=lambda c: self.root.after(0, lambda: p.paint_count(c)),
            on_done=lambda c: self.root.after(0, lambda: self._ac_finished(c)))

    def _ac_finished(self, count):
        self.ac_panel.set_running(False)
        self._refresh(f"Auto Click xong: {count} lần click.")

    def pick_ac_position(self):
        p = self.ac_panel
        p.set_pick_busy(True)
        p.set_hint("Lia chuột tới điểm cần click… (3s)")

        def _job():
            time.sleep(3)
            try:
                x, y = capture_position()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lấy vị trí", str(e)))
                self.root.after(0, lambda: p.set_pick_busy(False))
                return

            def _set():
                p.ac_x.set(x)
                p.ac_y.set(y)
                p.ac_pos.set("fixed")
                p.set_hint(f"Đã ghim vị trí ({x}, {y})")
                p.set_pick_busy(False)
            self.root.after(0, _set)

        threading.Thread(target=_job, daemon=True).start()

    # ---------- hotkeys ----------
    def _register_hotkeys(self):
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        try:
            if self.record_hotkey:
                keyboard.add_hotkey(self.record_hotkey, self.toggle_record)
            if self.play_hotkey:
                keyboard.add_hotkey(self.play_hotkey, self.toggle_play)
            if self.ac_hotkey:
                keyboard.add_hotkey(self.ac_hotkey, self.toggle_autoclick)
        except Exception as e:
            messagebox.showwarning("Hotkey error", f"Cannot bind hotkey: {e}")


def main():
    root = tk.Tk()
    MacroApp(root)
    root.mainloop()
