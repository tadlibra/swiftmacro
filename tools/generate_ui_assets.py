from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "assets" / "ui"
ICON_DIR = UI_DIR / "icons"
TEXTURE_DIR = UI_DIR / "textures"
BUTTON_DIR = UI_DIR / "buttons"
SCALE = 3
CELL = 16 * SCALE
INK = (59, 47, 30, 255)
GOLD = (247, 215, 116, 255)
GOLD_LIGHT = (255, 238, 157, 255)
GREEN = (47, 168, 79, 255)
GREEN_LIGHT = (143, 214, 164, 255)
RED = (185, 28, 28, 255)
WHITE = (255, 255, 255, 255)
BLUE = (37, 99, 235, 255)
CREAM = (255, 246, 217, 255)


def px(draw, box, color):
    draw.rectangle(tuple(value * SCALE for value in box), fill=color)


def make_icon(name):
    image = Image.new("RGBA", (16 * SCALE, 16 * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if name == "folder":
        px(draw, (1, 4, 14, 14), INK); px(draw, (2, 6, 13, 13), GOLD)
        px(draw, (2, 3, 7, 6), INK); px(draw, (3, 4, 7, 5), GOLD_LIGHT)
        px(draw, (4, 7, 13, 8), GOLD_LIGHT)
    elif name == "disk":
        px(draw, (2, 1, 13, 14), INK); px(draw, (3, 2, 12, 13), GREEN)
        px(draw, (4, 2, 10, 5), CREAM); px(draw, (5, 3, 9, 4), (76, 121, 154, 255))
        px(draw, (4, 8, 11, 13), INK); px(draw, (5, 9, 10, 12), CREAM)
    elif name == "record":
        draw.ellipse((SCALE, SCALE, 15*SCALE, 15*SCALE), fill=INK)
        draw.ellipse((2*SCALE, 2*SCALE, 14*SCALE, 14*SCALE), fill=RED)
        draw.ellipse((4*SCALE, 3*SCALE, 8*SCALE, 6*SCALE), fill=(241, 119, 104, 255))
    elif name == "play":
        # Tam giác trắng đặc, không viền INK: get_icon() tint mọi pixel
        # tối thành fg nên viền INK sẽ bị nuốt → chỉ dùng trắng tinh.
        draw.polygon([(4*SCALE, 2*SCALE), (12*SCALE, 8*SCALE),
                      (4*SCALE, 14*SCALE)], fill=WHITE)
    elif name == "gear":
        # Vẽ trực tiếp ở 16x16 cho nét pixel rõ: 8 răng + vành INK,
        # lỗ giữa khoét trong suốt (thay vì tô GOLD) để nổi trên mọi màu nút.
        small = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(small)
        d.rectangle((6, 0, 9, 15), fill=INK)    # răng dọc
        d.rectangle((0, 6, 15, 9), fill=INK)    # răng ngang
        d.rectangle((3, 3, 5, 5), fill=INK)
        d.rectangle((10, 3, 12, 5), fill=INK)
        d.rectangle((3, 10, 5, 12), fill=INK)
        d.rectangle((10, 10, 12, 12), fill=INK)
        d.ellipse((2, 2, 13, 13), fill=INK)     # vành
        d.ellipse((5, 5, 10, 10), fill=(0, 0, 0, 0))  # khoét lỗ
        image.alpha_composite(
            small.resize((16 * SCALE, 16 * SCALE), Image.Resampling.NEAREST))
    elif name == "trash":
        px(draw, (4, 4, 11, 14), INK); px(draw, (5, 6, 10, 13), CREAM)
        px(draw, (3, 3, 12, 4), INK); px(draw, (6, 1, 9, 2), INK)
        px(draw, (5, 2, 10, 3), INK)
        for x in (6, 8, 10): px(draw, (x, 7, x, 12), (138, 109, 31, 255))
    elif name in ("info", "help"):
        color = BLUE if name == "info" else (27, 145, 202, 255)
        draw.ellipse((SCALE, SCALE, 15*SCALE, 15*SCALE), fill=INK)
        draw.ellipse((2*SCALE, 2*SCALE, 14*SCALE, 14*SCALE), fill=color)
        px(draw, (7, 4, 8, 5), CREAM)
        if name == "info": px(draw, (7, 7, 8, 12), CREAM)
        else:
            px(draw, (6, 7, 9, 7), CREAM); px(draw, (9, 7, 10, 8), CREAM)
            px(draw, (8, 8, 9, 9), CREAM); px(draw, (7, 9, 8, 10), CREAM)
            px(draw, (7, 12, 8, 12), CREAM)
    elif name == "warning":
        draw.polygon([(8*SCALE, SCALE), (15*SCALE, 14*SCALE), (SCALE, 14*SCALE)], fill=INK)
        draw.polygon([(8*SCALE, 3*SCALE), (13*SCALE, 13*SCALE), (3*SCALE, 13*SCALE)], fill=GOLD)
        px(draw, (7, 6, 8, 10), INK); px(draw, (7, 11, 8, 12), INK)
    elif name == "link":
        draw.arc((SCALE, 2*SCALE, 10*SCALE, 11*SCALE), 300, 130, fill=INK, width=2*SCALE)
        draw.arc((6*SCALE, 5*SCALE, 15*SCALE, 14*SCALE), 120, 310, fill=BLUE, width=2*SCALE)
        px(draw, (5, 7, 10, 8), INK)
    elif name == "plus":
        px(draw, (6, 2, 9, 13), INK); px(draw, (2, 6, 13, 9), INK)
        px(draw, (7, 3, 8, 12), GREEN); px(draw, (3, 7, 12, 8), GREEN)
    elif name == "list":
        for y in (3, 7, 11):
            px(draw, (2, y, 4, y+2), GREEN); px(draw, (6, y, 14, y+1), INK)
    elif name == "check":
        px(draw, (2, 8, 5, 10), GREEN); px(draw, (4, 10, 6, 12), GREEN)
        px(draw, (6, 7, 8, 9), GREEN); px(draw, (8, 5, 10, 7), GREEN)
        px(draw, (10, 3, 13, 5), GREEN)
    elif name == "close":
        for i in range(4, 12):
            px(draw, (i, i, i+1, i+1), RED); px(draw, (15-i, i, 16-i, i+1), RED)
    elif name == "cube":
        draw.polygon([(8*SCALE, SCALE), (15*SCALE, 5*SCALE), (8*SCALE, 9*SCALE), (SCALE, 5*SCALE)], fill=(145, 218, 69, 255), outline=INK)
        draw.polygon([(SCALE, 5*SCALE), (8*SCALE, 9*SCALE), (8*SCALE, 15*SCALE), (SCALE, 11*SCALE)], fill=(107, 68, 35, 255), outline=INK)
        draw.polygon([(8*SCALE, 9*SCALE), (15*SCALE, 5*SCALE), (15*SCALE, 11*SCALE), (8*SCALE, 15*SCALE)], fill=(126, 80, 38, 255), outline=INK)
    elif name == "cursor":
        draw.polygon([(2*SCALE, SCALE), (13*SCALE, 10*SCALE), (8*SCALE, 10*SCALE), (10*SCALE, 15*SCALE), (7*SCALE, 15*SCALE), (5*SCALE, 10*SCALE), (2*SCALE, 13*SCALE)], fill=GOLD, outline=INK)
    else:
        raise KeyError(name)
    return image


def make_texture(name):
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if name == "grass":
        px(draw, (0, 0, 15, 5), (94, 187, 43, 255))
        for box in ((1,0,3,1),(6,2,8,3),(11,0,14,1),(4,4,5,5),(13,3,15,4)):
            px(draw, box, (143, 214, 74, 255))
        px(draw, (0, 6, 15, 15), (107, 68, 35, 255))
        for box in ((2,8,4,9),(9,7,11,8),(5,12,7,13),(13,14,15,15)):
            px(draw, box, (138, 90, 43, 255))
        for box in ((7,9,8,10),(1,14,2,15),(12,11,13,12)):
            px(draw, box, (70, 44, 22, 255))
    elif name == "soil":
        px(draw, (0,0,15,15), (107,68,35,255))
        for box in ((2,2,5,3),(10,1,13,2),(6,8,9,9),(1,13,4,14)):
            px(draw, box, (138,90,43,255))
        for box in ((7,4,8,5),(13,10,15,11),(3,7,4,8),(10,14,11,15)):
            px(draw, box, (70,44,22,255))
    elif name == "stone":
        px(draw, (0,0,15,15), (130,139,117,255))
        for box in ((2,2,6,3),(10,1,13,2),(7,8,11,9),(1,12,4,13)):
            px(draw, box, (177,184,162,255))
        for box in ((8,4,9,5),(13,11,14,12),(4,8,5,9)):
            px(draw, box, (84,91,73,255))
    elif name == "wood":
        px(draw, (0,0,15,15), (151,101,51,255))
        for y in (3, 8, 13): px(draw, (0,y,15,y), (91,57,31,255))
        for box in ((2,1,5,2),(9,5,13,6),(4,10,7,11),(11,14,14,15)):
            px(draw, box, (191,143,78,255))
    elif name == "leaves":
        px(draw, (0,0,15,15), (65,151,47,255))
        for box in ((1,1,4,3),(9,2,13,4),(5,7,8,9),(1,12,5,14),(11,11,14,14)):
            px(draw, box, (113,196,63,255))
        for box in ((6,1,7,2),(2,8,3,9),(10,7,12,8),(7,13,8,14)):
            px(draw, box, (43,111,39,255))
    return image


def make_button(state):
    face = Image.new("RGBA", (48, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(face)
    colors = {
        "normal": ((138,109,31,255), (255,224,138,255), (247,215,116,255)),
        "hover": ((138,109,31,255), (255,238,157,255), (255,228,112,255)),
        "pressed": ((59,47,30,255), (138,109,31,255), (232,195,74,255)),
        "disabled": ((157,151,132,255), (223,218,201,255), (238,235,224,255)),
    }
    border, highlight, fill = colors[state]
    draw.rectangle((0,0,47,23), fill=border)
    draw.rectangle((2,2,45,21), fill=highlight)
    draw.rectangle((4,4,43,19), fill=(0,0,0,0))
    if state == "pressed":
        draw.line((4,3,43,3), fill=(198,165,65,255), width=1)
    else:
        draw.line((4,2,43,2), fill=(255,249,198,255), width=1)
    return face


def save_atlas_and_crops():
    names = ["folder", "disk", "record", "play", "gear", "trash", "info", "warning",
             "help", "link", "plus", "list", "check", "close", "cube", "cursor"]
    atlas = Image.new("RGBA", (CELL * 4, CELL * 4), (255, 246, 217, 255))
    for index, name in enumerate(names):
        x, y = (index % 4) * CELL, (index // 4) * CELL
        icon = make_icon(name).resize((16, 16), Image.Resampling.NEAREST)
        atlas_icon = icon.resize((CELL, CELL), Image.Resampling.NEAREST)
        atlas.alpha_composite(atlas_icon, (x, y))
        ICON_DIR.mkdir(parents=True, exist_ok=True)
        icon.save(ICON_DIR / f"{name}.png", optimize=True)
    atlas.save(UI_DIR / "icon_atlas.png", optimize=True)

    texture_names = ["grass", "soil", "stone", "wood", "leaves"]
    texture_atlas = Image.new("RGBA", (CELL * len(texture_names), CELL), (0,0,0,0))
    for index, name in enumerate(texture_names):
        texture = make_texture(name).resize((CELL, CELL), Image.Resampling.NEAREST)
        texture_atlas.alpha_composite(texture, (CELL * index, 0))
        TEXTURE_DIR.mkdir(parents=True, exist_ok=True)
        texture.save(TEXTURE_DIR / f"{name}.png", optimize=True)
    texture_atlas.save(UI_DIR / "texture_atlas.png", optimize=True)

    button_states = ["normal", "hover", "pressed", "disabled"]
    button_atlas = Image.new("RGBA", (CELL * len(button_states), 24 * SCALE), (0,0,0,0))
    for index, state in enumerate(button_states):
        button = make_button(state).resize((48*SCALE, 24*SCALE), Image.Resampling.NEAREST)
        button_atlas.alpha_composite(button, (index * 48*SCALE, 0))
        BUTTON_DIR.mkdir(parents=True, exist_ok=True)
        button.save(BUTTON_DIR / f"{state}.png", optimize=True)
    button_atlas.save(UI_DIR / "button_states.png", optimize=True)

    # Contact sheet mirrors the sample's asset-library presentation.
    swatch = Image.new("RGBA", (640, 420), CREAM)
    draw = ImageDraw.Draw(swatch)
    draw.rectangle((0, 0, 639, 419), outline=INK, width=3)
    for index, name in enumerate(names):
        x, y = 20 + (index % 8) * 76, 20 + (index // 8) * 76
        draw.rectangle((x, y, x+55, y+55), fill=GOLD, outline=INK, width=2)
        icon = make_icon(name).resize((42,42), Image.Resampling.NEAREST)
        swatch.alpha_composite(icon, (x+7,y+7))
    for index, name in enumerate(texture_names):
        texture = make_texture(name).resize((64,64), Image.Resampling.NEAREST)
        swatch.alpha_composite(texture, (20+index*90, 190))
    for index, state in enumerate(button_states):
        button = make_button(state).resize((96,48), Image.Resampling.NEAREST)
        swatch.alpha_composite(button, (20+index*145, 300))
    swatch.save(UI_DIR / "asset_catalog.png", optimize=True)

    (UI_DIR / "README.md").write_text(
        "# SwiftMacro UI assets\n\n"
        "Generated pixel-art PNGs inspired by the supplied UI reference sheet.\n"
        "Run `python tools/generate_ui_assets.py` to rebuild the atlases and crops.\n\n"
        "- `icons/`: standalone transparent pixel icons\n"
        "- `textures/`: repeating Minecraft-inspired material tiles\n"
        "- `buttons/`: normal, hover, pressed and disabled button faces\n"
        "- `*_atlas.png`: source atlases; `asset_catalog.png` is a preview sheet\n",
        encoding="utf-8")


if __name__ == "__main__":
    save_atlas_and_crops()
