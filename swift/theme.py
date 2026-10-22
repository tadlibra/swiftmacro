"""Pixel theme: palette, bitmap glyphs, icon/grass factories, pixel widgets."""

import tkinter as tk
from tkinter import ttk

THEME = {
    "bg": "#A9DC76",      # grass ground
    "card": "#FFF6D9",    # cream panels
    "line": "#E3D199",
    "ink": "#3B2F1E",      # dark bark text
    "muted": "#5C6B3C",
    "accent": "#2FA84F",
    "danger": "#B91C1C",
    "ok": "#2FA84F",
    "warn": "#B45309",
    "gold": "#F7D774",
    "gold_banner": "#F2B632",
}

GLYPHS = {
    "folder": [
        "...........",
        ".######....",
        ".########..",
        ".#########.",
        "###########",
        "###########",
        "###########",
        "###########",
        "###########",
        "###########",
        "..........."],
    "disk": [
        "###########",
        "###########",
        "###.....###",
        "###.....###",
        "###.....###",
        "###########",
        "###########",
        "####...####",
        "####...####",
        "####...####",
        "###########"],
    "record": [
        ".....#.....",
        "...#####...",
        "..#######..",
        ".#########.",
        ".#########.",
        "###########",
        ".#########.",
        ".#########.",
        "..#######..",
        "...#####...",
        ".....#....."],
    "play": [
        "#..........",
        "####.......",
        "######.....",
        "########...",
        "##########.",
        "###########",
        "##########.",
        "########...",
        "######.....",
        "####.......",
        "#.........."],
    "sliders": [
        "...........",
        "..##.......",
        "..##.......",
        "..##..###..",
        "..##..###..",
        "..##.......",
        "..###..##..",
        "..###..##..",
        "..##.......",
        "..##.......",
        "..........."],
    "trash": [
        ".....#.....",
        "....###....",
        ".....#.....",
        ".#########.",
        ".#.......#.",
        ".#.......#.",
        ".#...#...#.",
        ".#...#...#.",
        ".#...#...#.",
        ".#.......#.",
        ".#########."],
    "cube": [
        "GGGGGGGGGGG",
        "GGGGGGGGGGG",
        "GGGGGGGGGGG",
        "DDDDDDDDDDD",
        "DDdDDDDDdDD",
        "DDDDDDDDDDD",
        "DDDdDDDdDDD",
        "DDDDDDDDDDD",
        "DDdDDDDdDDD",
        "DDDDDDDDDDD",
        "DDDDDDDDDDD"],
}

_icon_cache = {}
_grass_cache = {}


def get_icon(name, fg="#3B2F1E", scale=2):
    """Pixel icon vẽ lúc chạy bằng PIL, phóng NEAREST. Hỏng PIL → None."""
    try:
        key = (name, fg, scale)
        if key in _icon_cache:
            return _icon_cache[key]
        from PIL import Image, ImageTk
        rows = GLYPHS[name]
        h, w = len(rows), len(rows[0])
        pal = {"G": (94, 187, 43), "D": (107, 68, 35), "d": (70, 44, 22)}
        fr, fgg, fb = int(fg[1:3], 16), int(fg[3:5], 16), int(fg[5:7], 16)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        px = img.load()
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == "#":
                    px[x, y] = (fr, fgg, fb, 255)
                elif ch in pal:
                    px[x, y] = pal[ch] + (255,)
        img = img.resize((w * scale, h * scale), Image.NEAREST)
        tkimg = ImageTk.PhotoImage(img)
        _icon_cache[key] = tkimg
        return tkimg
    except Exception:
        return None


def get_grass(w=800, h=18):
    """Dải cỏ-đất nhiễu pixel cho footer. Hỏng PIL → None."""
    try:
        if "bar" in _grass_cache:
            return _grass_cache["bar"]
        from PIL import Image, ImageTk
        greens = [(94, 187, 43), (77, 166, 38), (111, 209, 58), (62, 142, 31)]
        browns = [(107, 68, 35), (122, 82, 48), (93, 58, 30), (138, 90, 43)]
        img = Image.new("RGB", (w, h), (107, 68, 35))
        px = img.load()
        for x in range(w):
            edge = 5 + ((x * 7) % 3)
            for y in range(h):
                if y < edge:
                    px[x, y] = greens[(x * 3 + y * 5) % 4]
                else:
                    px[x, y] = browns[(x * 5 + y * 3) % 4]
        tkimg = ImageTk.PhotoImage(img)
        _grass_cache["bar"] = tkimg
        return tkimg
    except Exception:
        return None


_win_cache = {}


def win_icon(kind, fg="#3B2F1E", bg="#F7D774", size=22):
    """Icon pixel cho nút –, ▢, ✕: vẽ trên lưới 11x11 rồi phóng NEAREST."""
    try:
        key = (kind, fg, size)
        if key in _win_cache:
            return _win_cache[key]
        from PIL import Image, ImageDraw, ImageTk
        base = 11
        fr = (int(fg[1:3], 16), int(fg[3:5], 16), int(fg[5:7], 16), 255)
        img = Image.new("RGBA", (base, base), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        if kind == "min":
            d.rectangle([1, 4, 9, 6], fill=fr)
        elif kind == "max":
            d.rectangle([1, 1, 9, 9], outline=fr, width=2)
        else:  # close
            d.line([2, 2, 8, 8], fill=fr, width=2)
            d.line([2, 8, 8, 2], fill=fr, width=2)
            d.point([(2, 2), (8, 8), (2, 8), (8, 2)], fill=fr)
        img = img.resize((size, size), Image.NEAREST)
        tkimg = ImageTk.PhotoImage(img)
        _win_cache[key] = tkimg
        return tkimg
    except Exception:
        return None


def pixel_button(parent, text, bg, fg, command, ghost=False, icon=None):
    """Nút pixel: viền đậm + mép sáng trên + mặt phẳng, không đổi màu hover.

    Trả về khung ngoài; nút thật nằm ở ``outer.inner``.
    """
    light = {"#B91C1C": "#E88A7D", "#2FA84F": "#8FD6A4"}.get(bg, "#FFE08A")
    dark = {"#B91C1C": "#7F1D1D", "#2FA84F": "#1E6F35"}.get(bg, "#8A6D1F")
    outer = tk.Frame(parent, bg=dark, padx=2, pady=2, bd=0, highlightthickness=0)
    top = tk.Frame(outer, bg=light, bd=0, highlightthickness=0)
    top.pack(fill="both", expand=True)
    b = tk.Button(top, text=text, image=icon, compound="left",
                  bg=bg, fg=fg, font=("Segoe UI", 10, "bold"),
                  bd=0, relief="flat", padx=8, pady=6, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  highlightthickness=0, takefocus=0, command=command)
    b.pack(fill="both", expand=True, pady=(2, 0))
    normal = bg
    pressed = {"#B91C1C": "#991B1B", "#2FA84F": "#257A3E"}.get(bg, "#E8C34A")
    b.bind("<ButtonPress-1>", lambda e, w=b, p=pressed: w.configure(bg=p))
    b.bind("<ButtonRelease-1>", lambda e, w=b, n=normal: w.configure(bg=n))
    outer.inner = b
    return outer


class SegmentBar(tk.Canvas):
    """Thanh tiến trình dạng khối pixel vẽ trên canvas."""

    def __init__(self, parent, height=18, **kw):
        super().__init__(parent, height=height, bg="#3A2E18",
                         highlightthickness=0, bd=0, **kw)
        self.frac = 0.0
        self.bind("<Configure>", lambda e: self.draw(self.frac))

    def set(self, frac):
        self.draw(frac)

    def refresh(self):
        self.draw(self.frac)

    def draw(self, frac):
        try:
            self.frac = max(0.0, min(1.0, frac))
            w = self.winfo_width() or 560
            self.delete("all")
            self.create_rectangle(0, 0, w, 18, fill="#3A2E18", outline="#241C0E")
            n = max(8, w // 16)
            bw = (w - 4) / n
            for i in range(n):
                if i / n >= self.frac:
                    break
                x0 = 2 + i * bw
                self.create_rectangle(x0 + 1, 3, x0 + bw - 1, 15,
                                      fill="#5EBB2B", outline="#2F6B12")
                self.create_line(x0 + 2, 4, x0 + bw - 2, 4, fill="#A5E075", width=2)
        except Exception:
            pass


def apply_style(root, title_bg, dark_ink):
    """Dựng toàn bộ ttk style của app (gọi một lần khi khởi động)."""
    s = ttk.Style(root)
    try:
        s.theme_use("clam")
    except Exception:
        pass
    s.configure("TFrame", background=THEME["bg"])
    s.configure("Card.TFrame", background=THEME["card"])
    s.configure("TLabel", background=THEME["bg"], foreground=THEME["ink"],
                font=("Segoe UI", 10))
    s.configure("Card.TLabel", background=THEME["card"], foreground=THEME["ink"])
    s.configure("Muted.TLabel", background=THEME["card"], foreground=THEME["muted"],
                font=("Segoe UI", 9))
    s.configure("Title.TLabel", background=title_bg, foreground=dark_ink,
                font=("Courier New", 14, "bold"))
    s.configure("TButton", focusthickness=0, focuscolor="none")
    try:
        s.map("TButton", focuscolor=[("active", "none"), ("focus", "none")])
    except Exception:
        pass
    root.option_add("*TButton.takeFocus", "0")
    s.configure("TCheckbutton", background=THEME["card"], font=("Segoe UI", 10))
    s.configure("TRadiobutton", background=THEME["card"], font=("Segoe UI", 10))
    # form controls theo chuẩn pixel chung: nền trắng, viền nâu (kể cả AutoClick)
    try:
        for _w in ("TEntry", "TCombobox", "TSpinbox"):
            s.configure(_w, fieldbackground="#FFFFFF", foreground="#3B2F1E",
                        bordercolor="#8A6D1F", lightcolor="#FFE08A",
                        darkcolor="#8A6D1F", arrowcolor="#3B2F1E", padding=3)
    except Exception:
        pass
    # đầu bảng phẳng (không nút 3D từng cột, không đổi màu khi hover)
    s.configure("Treeview.Heading", background="#F5D76E",
                foreground="#3B2F1E", relief="flat", borderwidth=0,
                font=("Courier New", 10, "bold"))
    s.map("Treeview.Heading",
          background=[("active", "#F5D76E")],
          relief=[("active", "flat")])
    s.configure("Treeview", rowheight=24, background="#FFF6D9",
                fieldbackground="#FFF6D9", foreground="#3B2F1E",
                font=("Segoe UI", 10))
    s.map("Treeview", background=[("selected", "#2FA84F")],
          foreground=[("selected", "#FFFFFF")])
