"""Các panel UI: Macro, AutoClick, Hotkeys. Không chứa logic engine."""

import threading
import tkinter as tk
from tkinter import messagebox, ttk

import keyboard

from . import theme


def capture_key(root, var, btn):
    """Bấm vào ô rồi nhấn phím thật → điền vào ô (chạy thread riêng)."""
    if str(btn["state"]) == "disabled":
        return
    old = var.get()
    var.set("Nhấn phím…")
    btn.config(state="disabled")

    def _read():
        try:
            key = keyboard.read_key(suppress=False)
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Capture", str(e)))
            root.after(0, lambda: (var.set(old),
                                   btn.config(state="normal")))
            return
        root.after(0, lambda: (var.set(key.strip().upper()),
                               btn.config(state="normal")))

    threading.Thread(target=_read, daemon=True).start()


class MacroPanel(ttk.Frame):
    """Thẻ Macro: trạng thái + bảng Steps + thanh tiến trình pixel."""

    def __init__(self, parent, on_clear):
        super().__init__(parent, padding=10, style="Card.TFrame")
        self.record_hotkey = "F9"
        self.status_var = tk.StringVar(value="Ready. No macro loaded.")
        ttk.Label(self, textvariable=self.status_var, style="Card.TLabel",
                  font=("Segoe UI", 11, "bold"), wraplength=580,
                  justify="left").pack(anchor="w")

        stat = ttk.Frame(self, style="Card.TFrame")
        stat.pack(fill="x", pady=(6, 2))
        self.detail_var = tk.StringVar(value="Events: 0")
        ttk.Label(stat, textvariable=self.detail_var, style="Card.TLabel",
                  font=("Segoe UI", 10, "bold")).pack(side="left")
        self.dur_var = tk.StringVar(value="Duration: 0.0s")
        ttk.Label(stat, textvariable=self.dur_var, style="Card.TLabel").pack(
            side="left", padx=14)
        self.hot_var = tk.StringVar(value="")
        ttk.Label(stat, textvariable=self.hot_var, style="Muted.TLabel").pack(side="right")

        self.pbar = theme.SegmentBar(self)
        self.pbar.pack(fill="x", pady=(6, 8))

        list_head = ttk.Frame(self, style="Card.TFrame")
        list_head.pack(fill="x")
        ttk.Label(list_head, text="Steps đã ghi", style="Card.TLabel",
                  font=("Segoe UI", 10, "bold")).pack(side="left")
        clear_btn = theme.pixel_button(
            list_head, "Clear", "#F7D774", "#3B2F1E", on_clear,
            icon=theme.get_icon("trash", "#3B2F1E", scale=1))
        clear_btn.pack(side="right")

        cols = ("time", "kind", "detail")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=11)
        for c, w, a in (("time", 80, "center"), ("kind", 90, "center"), ("detail", 380, "w")):
            self.tree.heading(c, text={"time": "Thời gian", "kind": "Loại",
                                       "detail": "Chi tiết"}[c])
            self.tree.column(c, width=w, anchor=a, stretch=(c == "detail"))
        vs = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vs.set)
        self.tree.pack(side="left", fill="both", expand=True, pady=(4, 0))
        vs.pack(side="right", fill="y", pady=(4, 0))

    def refresh_tree(self, events):
        try:
            self.tree.delete(*self.tree.get_children())
            if not events:
                self.tree.insert("", "end", values=("—", "trống",
                    f"Chưa có bước nào — bấm Record ({self.record_hotkey}) "
                    "để bắt đầu ghi."))
                return
            for e in events[-200:]:
                k = e.get("kind", "")
                if k == "move":
                    d = f"move → ({e.get('x')},{e.get('y')})"
                elif k == "mouse":
                    d = f"{e.get('button')} {e.get('type')}"
                elif k == "wheel":
                    d = f"delta {e.get('delta')}"
                elif k == "key":
                    d = f"{e.get('name')} {e.get('type')}"
                else:
                    d = str(e)
                self.tree.insert("", "end", values=(f"{e.get('t', 0):.2f}s", k, d))
        except Exception:
            pass

    def set_record_hotkey(self, hotkey):
        self.record_hotkey = hotkey.upper()

    def set_hotkeys_hint(self, text):
        self.hot_var.set(text)


class AutoClickPanel(ttk.Frame):
    """Thẻ Auto Click kiểu GS AutoClicker."""

    def __init__(self, parent, on_toggle, on_pick):
        super().__init__(parent, padding=10, style="Card.TFrame")
        # tk vars dùng default root (đã tồn tại lúc panel được tạo)
        self.ac_h = tk.IntVar(value=0)
        self.ac_m = tk.IntVar(value=0)
        self.ac_s = tk.IntVar(value=0)
        self.ac_ms = tk.IntVar(value=100)
        self.ac_button = tk.StringVar(value="Trái")
        self.ac_type = tk.StringVar(value="Đơn")
        self.ac_rep = tk.StringVar(value="stop")
        self.ac_n = tk.IntVar(value=10)
        self.ac_pos = tk.StringVar(value="cur")
        self.ac_x = tk.IntVar(value=0)
        self.ac_y = tk.IntVar(value=0)
        self.count_var = tk.StringVar(value="Chưa chạy")

        head = ttk.Frame(self, style="Card.TFrame")
        head.pack(fill="x")
        ttk.Label(head, text="Auto Click", style="Card.TLabel",
                  font=("Courier New", 11, "bold")).pack(side="left")
        ttk.Label(head, textvariable=self.count_var,
                  style="Muted.TLabel").pack(side="left", padx=10)
        self.btn_ac = theme.pixel_button(
            head, "Start", "#2FA84F", "#FFFFFF", on_toggle,
            icon=theme.get_icon("play", "#FFFFFF"))
        self.btn_ac.pack(side="right")
        self.hotkey_label = ttk.Label(head, text="phím F8", style="Muted.TLabel")
        self.hotkey_label.pack(side="right", padx=(0, 8))

        g1 = ttk.Frame(self, style="Card.TFrame")
        g1.pack(fill="x", pady=(8, 0))
        ttk.Label(g1, text="Mỗi:", style="Card.TLabel").pack(side="left")
        for var, unit in ((self.ac_h, "giờ"), (self.ac_m, "phút"),
                          (self.ac_s, "giây"), (self.ac_ms, "ms")):
            ttk.Spinbox(g1, from_=0, to=9999, width=5,
                        textvariable=var).pack(side="left", padx=(4, 0))
            ttk.Label(g1, text=unit, style="Muted.TLabel").pack(side="left")
        ttk.Label(g1, text="Chuột:", style="Card.TLabel").pack(side="left",
                                                               padx=(10, 0))
        ttk.Combobox(g1, textvariable=self.ac_button, width=7, state="readonly",
                     values=["Trái", "Phải", "Giữa"]).pack(side="left", padx=4)
        ttk.Label(g1, text="Kiểu:", style="Card.TLabel").pack(side="left")
        ttk.Combobox(g1, textvariable=self.ac_type, width=7, state="readonly",
                     values=["Đơn", "Đúp"]).pack(side="left", padx=4)

        g2 = ttk.Frame(self, style="Card.TFrame")
        g2.pack(fill="x", pady=(6, 0))
        ttk.Label(g2, text="Lặp:", style="Card.TLabel").pack(side="left")
        ttk.Radiobutton(g2, text="Đến khi dừng", variable=self.ac_rep,
                        value="stop").pack(side="left", padx=4)
        ttk.Radiobutton(g2, text="Số lần:", variable=self.ac_rep,
                        value="n").pack(side="left")
        ttk.Spinbox(g2, from_=1, to=999999, width=7,
                    textvariable=self.ac_n).pack(side="left", padx=4)
        ttk.Label(g2, text="Vị trí:", style="Card.TLabel").pack(side="left",
                                                                padx=(10, 0))
        ttk.Radiobutton(g2, text="Chuột hiện tại", variable=self.ac_pos,
                        value="cur").pack(side="left", padx=4)
        ttk.Radiobutton(g2, text="Cố định", variable=self.ac_pos,
                        value="fixed").pack(side="left")
        ttk.Entry(g2, textvariable=self.ac_x, width=6).pack(side="left", padx=2)
        ttk.Entry(g2, textvariable=self.ac_y, width=6).pack(side="left", padx=2)
        self.btn_pick = theme.pixel_button(g2, "Lấy vị trí", "#F7D774",
                                             "#3B2F1E", on_pick)
        self.btn_pick.pack(side="left", padx=4)

    def set_running(self, running):
        self.btn_ac.inner.configure(text="Stop" if running else "Start")

    def set_pick_busy(self, busy):
        try:
            self.btn_ac.inner.configure(state="disabled" if busy else "normal")
        except Exception:
            pass

    def set_click_hotkey(self, hotkey):
        self.hotkey_label.configure(text=f"phím {hotkey}")

    def paint_count(self, n):
        self.count_var.set(f"Đã click: {n}")

    def set_hint(self, text):
        self.count_var.set(text)


class HotkeyPanel(ttk.Frame):
    """Dropdown chỉnh phím tắt (không popup riêng)."""

    def __init__(self, parent, root, on_save, on_reset):
        super().__init__(parent, padding=12, style="Card.TFrame")
        self._root = root
        ttk.Label(self, text="Phím tắt", style="Card.TLabel",
                  font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(self,
                  text="Bấm vào ô rồi nhấn phím thật. "
                       "Kết hợp được: ctrl+shift+r, alt+f9. Các phím phải khác nhau.",
                  style="Muted.TLabel", wraplength=580,
                  justify="left").grid(row=1, column=0, columnspan=4, sticky="w",
                                        pady=(2, 8))
        self.vars = {}
        self.cap_btns = {}
        for i, (label, key) in enumerate((("Record:", "rec"), ("Play:", "play"),
                                          ("Click:", "click"))):
            ttk.Label(self, text=label, style="Card.TLabel").grid(
                row=2 + i, column=0, sticky="e", pady=6)
            var = tk.StringVar(value="")
            self.vars[key] = var
            cap = theme.pixel_button(self, "", "#FFFFFF", "#3B2F1E",
                                     lambda: None)
            cap.grid(row=2 + i, column=1, sticky="w", padx=6, pady=6)
            cap.inner.configure(
                textvariable=var,
                command=lambda v=var, b=cap.inner: capture_key(self._root, v, b))
            self.cap_btns[key] = cap.inner

        from tkinter import BooleanVar, IntVar
        self.cont_var = BooleanVar(value=False)
        ttk.Checkbutton(self, text="Lặp liên tục (chạy tới khi bấm Stop)",
                        variable=self.cont_var).grid(row=5, column=0, columnspan=3,
                                                     sticky="w")
        hf = ttk.Frame(self, style="Card.TFrame")
        hf.grid(row=6, column=0, columnspan=4, sticky="ew", pady=(8, 0))
        ttk.Label(hf, text="Số vòng lặp:", style="Card.TLabel").pack(side="left")
        self.loops_var = IntVar(value=1)
        ttk.Spinbox(hf, from_=1, to=9999, width=8,
                    textvariable=self.loops_var).pack(side="left", padx=6)
        self.btn_reset_hk = theme.pixel_button(hf, "Reset F9/F10", "#F7D774",
                                               "#3B2F1E", on_reset,
                                               icon=theme.get_icon("gear", "#3B2F1E",
                                                                   scale=1))
        self.btn_reset_hk.pack(side="right", padx=4)
        self.btn_save_hk = theme.pixel_button(hf, "Lưu", "#2FA84F", "#FFFFFF",
                                              on_save)
        self.btn_save_hk.pack(side="right", padx=4)

    def load(self, rec, play, click, cont, loops):
        self.vars["rec"].set(str(rec).strip().upper())
        self.vars["play"].set(str(play).strip().upper())
        self.vars["click"].set(str(click).strip().upper())
        self.cont_var.set(cont)
        self.loops_var.set(loops)
        try:
            self.btn_reset_hk.inner.configure(
                text=f"Reset {rec.strip().upper()}/"
                     f"{play.strip().upper()}")
        except Exception:
            pass

    def reset_defaults(self, rec="F9", play="F10", click="F8"):
        self.vars["rec"].set(rec)
        self.vars["play"].set(play)
        self.vars["click"].set(click)
        self.cont_var.set(False)
        self.loops_var.set(1)

    def collect(self):
        """→ (rec, play, click, cont, loops). Raise ValueError nếu thiếu/trùng."""
        rh = self.vars["rec"].get().strip().upper()
        ph = self.vars["play"].get().strip().upper()
        ch = self.vars["click"].get().strip().upper()
        if not rh or not ph or not ch:
            raise ValueError("Phím không được để trống.")
        if len({rh.lower(), ph.lower(), ch.lower()}) < 3:
            raise ValueError("Ba phím phải khác nhau.")
        try:
            loops = max(1, int(self.loops_var.get()))
        except Exception:
            loops = 1
        return rh, ph, ch, bool(self.cont_var.get()), loops
