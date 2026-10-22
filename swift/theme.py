"""Pixel theme: palette, bitmap glyphs, icon/grass factories, pixel widgets."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageTk

UI_ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "ui"

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
    "gear": [
        "...#####...",
        "..##...##..",
        ".##..#..##.",
        "##...#...##",
        "##.#####.##",
        "##.#####.##",
        "##.#####.##",
        "##...#...##",
        ".##..#..##.",
        "..##...##..",
        "...#####..."],
    "info": [
        "...#####...",
        "..#######..",
        ".#########.",
        "###########",
        "####.######",
        "#####.#####",
        "####...####",
        "####...####",
        "####...####",
        "###########",
        ".#########."],
    "warning": [
        ".....#.....",
        "....###....",
        "....###....",
        "...#####...",
        "...#####...",
        "..#######..",
        "..###.###..",
        ".#########.",
        ".#########.",
        "###########",
        "....###...."],
    "help": [
        "...#####...",
        "..#######..",
        ".#########.",
        "###########",
        "#####.#####",
        "####..#####",
        "####.######",
        "#####.#####",
        "###########",
        ".#########.",
        "...#####..."],
    "plus": [
        ".....#.....",
        ".....#.....",
        ".....#.....",
        "###########",
        "###########",
        "###########",
        ".....#.....",
        ".....#.....",
        ".....#.....",
        ".....#.....",
        ".....#....."],
    "link": [
        "...###.....",
        "..#...#....",
        ".#.....#...",
        ".#....##...",
        "..#..##....",
        "...##..#...",
        "...##...#..",
        "....#....#.",
        ".....#...#.",
        "......###..",
        "..........."],
    "list": [
        "###########",
        "##..#######",
        "###########",
        "##..#######",
        "###########",
        "##..#######",
        "###########",
        "##..#######",
        "###########",
        "##..#######",
        "###########"],
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
_texture_cache = {}
_button_cache = {}
_button_src = {}
_live_buttons = []

TEXTURES = {
    "grass": [
        "GGGGGGGG", "GGgGGGGG", "GGGGGGGG", "GGGGGGGG",
        "DDDDDDDD", "DDdDDDDD", "DDDDDDDD", "DDDdDDDD"],
    "soil": [
        "DDDDDDDD", "DDdDDDDD", "DDDDDDDD", "DDDdDDDD",
        "DDDDDDDD", "DddDDDDD", "DDDDDDDD", "DDDDdDDD"],
    "stone": [
        "SSSSSSSS", "SSsSSSSS", "SSSSSSSS", "SSSSsSSS",
        "SSSSSSSS", "SsSSSSSS", "SSSSSSSS", "SSSSSSsS"],
    "wood": [
        "WWWWWWWW", "WwWWWWWW", "WWWWWWWW", "WWWWwWWW",
        "WWWWWWWW", "WwWWWWWW", "WWWWWWWW", "WWWWWWwW"],
    "leaves": [
        "GGGGGGGG", "GGgGGGGG", "GGGGGGGG", "GGGGgGGG",
        "GGGGGGGG", "GgGGGGGG", "GGGGGGGG", "GGGGGGgG"],
}


def get_icon(name, fg="#3B2F1E", scale=2):
    """Load a transparent pixel-art PNG sprite and scale it with nearest-neighbor."""
    try:
        key = (name, fg, scale)
        if key in _icon_cache:
            return _icon_cache[key]
        image = Image.open(UI_ASSET_DIR / "icons" / f"{name}.png").convert("RGBA")
        if fg.lower() != "#3b2f1e":
            source = image.load()
            rgb = tuple(int(fg[index:index + 2], 16) for index in (1, 3, 5))
            for y in range(image.height):
                for x in range(image.width):
                    red, green, blue, alpha = source[x, y]
                    if alpha and red < 100 and green < 100 and blue < 100:
                        source[x, y] = (*rgb, alpha)
        image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        tkimg = ImageTk.PhotoImage(image)
        _icon_cache[key] = tkimg
        return tkimg
    except Exception:
        return None


def get_grass(w=800, h=18):
    """Dải cỏ-đất pixel cho footer. Hỏng PIL → None."""
    try:
        if "bar" in _grass_cache:
            return _grass_cache["bar"]
        from PIL import Image, ImageTk
        greens = [(94, 187, 43), (77, 166, 38), (111, 209, 58), (62, 142, 31)]
        browns = [(107, 68, 35), (122, 82, 48), (93, 58, 30), (138, 90, 43)]
        img = Image.new("RGB", (w, h), (107, 68, 35))
        px = img.load()
        for x in range(w):
            edge = 5 + ((x // 4 * 7) % 3)
            for y in range(h):
                if y < edge:
                    px[x, y] = greens[((x // 4) * 3 + (y // 2) * 5) % 4]
                else:
                    px[x, y] = browns[((x // 4) * 5 + (y // 2) * 3) % 4]
        tkimg = ImageTk.PhotoImage(img)
        _grass_cache["bar"] = tkimg
        return tkimg
    except Exception:
        return None


def get_texture(name, scale=3):
    """Load and cache a repeating PNG tile used for pixel-art surfaces."""
    try:
        key = (name, scale)
        if key in _texture_cache:
            return _texture_cache[key]
        image = Image.open(UI_ASSET_DIR / "textures" / f"{name}.png").convert("RGBA")
        image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        texture = ImageTk.PhotoImage(image)
        _texture_cache[key] = texture
        return texture
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


def _button_skin(state, width, height):
    try:
        key = (state, width, height)
        if key not in _button_cache:
            if state not in _button_src:
                source = Image.open(
                    UI_ASSET_DIR / "buttons" / f"{state}.png").convert("RGBA")
                _button_src[state] = source.resize((48, 24), Image.Resampling.NEAREST)
            source = _button_src[state]
            inset = 2
            corner = inset * 2
            center_width = max(1, width - corner * 2)
            center_height = max(1, height - corner * 2)
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

            patches = (
                (source.crop((0, 0, inset, inset)), (0, 0, corner, corner)),
                (source.crop((source.width-inset, 0, source.width, inset)),
                 (width-corner, 0, width, corner)),
                (source.crop((0, source.height-inset, inset, source.height)),
                 (0, height-corner, corner, height)),
                (source.crop((source.width-inset, source.height-inset,
                              source.width, source.height)),
                 (width-corner, height-corner, width, height)),
                (source.crop((inset, 0, source.width-inset, inset)),
                 (corner, 0, width-corner, corner)),
                (source.crop((inset, source.height-inset,
                              source.width-inset, source.height)),
                 (corner, height-corner, width-corner, height)),
                (source.crop((0, inset, inset, source.height-inset)),
                 (0, corner, corner, height-corner)),
                (source.crop((source.width-inset, inset, source.width,
                              source.height-inset)),
                 (width-corner, corner, width, height-corner)),
                (source.crop((inset, inset, source.width-inset,
                              source.height-inset)),
                 (corner, corner, width-corner, height-corner)),
            )
            for patch, bounds in patches:
                x0, y0, x1, y1 = bounds
                if x1 > x0 and y1 > y0:
                    patch = patch.resize((x1-x0, y1-y0), Image.Resampling.NEAREST)
                    image.alpha_composite(patch, (x0, y0))
            _button_cache[key] = ImageTk.PhotoImage(image)
        return _button_cache[key]
    except Exception:
        return None


def pixel_button(parent, text, bg, fg, command, ghost=False, icon=None):
    """Pixel button with a nine-slice PNG frame and a live Tk button center."""
    outer = tk.Canvas(parent, width=144, height=48, bg=bg,
                      bd=0, highlightthickness=0)
    skin_item = outer.create_image(0, 0, anchor="nw")
    button_host = tk.Frame(outer, bg=bg, bd=0, highlightthickness=0)
    button_host.place(x=4, y=4, width=max(1, outer.winfo_width()-8),
                      height=max(1, outer.winfo_height()-8))
    b = tk.Button(button_host, text=text, image=icon, compound="left",
                  bg=bg, fg=fg, font=("Segoe UI", 10, "bold"),
                  bd=0, relief="flat", padx=8, pady=6, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  disabledforeground="#8A877D",
                  highlightthickness=0, takefocus=0, command=command)
    b.pack(fill="both", expand=True)

    skin_state = ["normal"]
    last_size = [0, 0]
    pending = [None]

    def set_skin(state):
        skin_state[0] = state
        width, height = max(1, outer.winfo_width()), max(1, outer.winfo_height())
        if (width, height) == (last_size[0], last_size[1]) \
                and hasattr(outer, "_skin_image"):
            return  # cùng kích thước → dùng skin đã vẽ, không ghép lại
        last_size[0], last_size[1] = width, height
        image = _button_skin(state, width, height)
        if image is not None:
            outer.itemconfigure(skin_item, image=image)
            outer._skin_image = image
        button_host.place(x=4, y=4, width=max(1, width-8),
                  height=max(1, height-8))

    def schedule_skin():
        # Debounce: Windows bắn chùm <Configure> khi restore/minimize —
        # chỉ vẽ lại một lần sau khi yên 60ms.
        if pending[0] is not None:
            try:
                outer.after_cancel(pending[0])
            except Exception:
                pass
        pending[0] = outer.after(60, lambda: set_skin(skin_state[0]))

    b.bind("<Enter>", lambda e: set_skin("hover")
           if str(b["state"]) != "disabled" else None)
    b.bind("<Leave>", lambda e: set_skin(
        "disabled" if str(b["state"]) == "disabled" else "normal"))
    b.bind("<ButtonPress-1>", lambda e: set_skin("pressed")
           if str(b["state"]) != "disabled" else None)
    b.bind("<ButtonRelease-1>", lambda e: set_skin("hover")
           if str(b["state"]) != "disabled" else None)

    outer.bind("<Configure>", lambda e: schedule_skin())
    set_skin("normal")
    outer.inner = b
    outer.set_skin = set_skin
    _live_buttons.append(outer)
    return outer


def repaint_all_buttons():
    """Vẽ lại toàn bộ pixel button (gọi khi cửa sổ hiện lại sau ẩn/minimize)."""
    for btn in list(_live_buttons):
        try:
            if btn.winfo_exists():
                btn.set_skin("normal" if str(btn.inner["state"]) != "disabled"
                             else "disabled")
        except Exception:
            pass


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
    s.configure("Vertical.TScrollbar", background="#8A6D1F",
                troughcolor="#FFF6D9", bordercolor="#3B2F1E",
                arrowcolor="#3B2F1E", relief="flat", width=16)
    s.map("Vertical.TScrollbar",
          background=[("active", "#F7D774"), ("pressed", "#2FA84F")])
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
