# DESIGN.md — SwiftMacro v2.1 (impeccable, Operate, code-led)

## Cấu trúc code (không dồn 1 file)

- `swiftmacro.py` — launcher mỏng (19 dòng).
- `swift/config.py` — tên app, phím mặc định.
- `swift/theme.py` — palette, glyph pixel, icon/grass, nút bevel, SegmentBar.
- `swift/macro_engine.py` — ghi + phát lại, không dính tkinter.
- `swift/auto_engine.py` — auto click GS-style, không dính tkinter.
- `swift/panels.py` — 3 panel UI: Macro, AutoClick, Hotkeys.
- `swift/app.py` — MacroApp: chrome cửa sổ + lắp ráp + file IO.

## Direction contract

- **THESIS:** The window is a lab-bench instrument, not a page. One glance gives
  state (idle / recording / playing / watching); one row of five equal controls;
  one dense step ledger. Refuses the category default: dark hero header, slogan
  subtitle, emoji icon buttons, nested cards, blue info banner.
- **OWN-WORLD:** Light neutral ground `#F1F5F9`, white instrument surface, hairline
  `#E2E8F0` rules. Ink `#0F172A`, muted `#64748B`. One signal blue `#2563EB`
  reserved for progress + selection; red `#DC2626` = recording, green `#16A34A` =
  playing. Single family Segoe UI (13 title / 10 body / 9 small). State lamp is a
  drawn canvas dot, never a text glyph.
- **STORY:** User opens, presses Record (or F9), does the task, presses Stop, sees
  every step listed with timestamps, presses Play (or F10). Nothing is hidden
  in dialogs.
- **FIRST VIEWPORT:** Custom gold titlebar thay thanh Windows
  (overrideredirect + WS_EX_APPWINDOW giữ nút taskbar): logo, tên file hiện tại,
  lamp+state, nút thu/phóng/đóng, kéo thả, resize góc. Không còn 2 header.
  Five equal pixel buttons with drawn pixel icons. One-line guide strip.
  Auto Click card (GS-style: interval, button, type, repeat, position, F8).
  Ledger fills remaining space. Decorative grass strip at the bottom, no text
  (status lives in the Macro card).
- **FORM:** Code-led Operate rebuild (no image generation for tkinter; skill
  routes Operate surfaces code-led). Keeps the user-approved structure from v2.0
  feedback; replaces the visual world, not the layout.
- **FINISH:** Unreviewed and undocumented is unfinished; this build ends with the
  finish review, the verdict, DESIGN.md, and every shipping raster carrying its
  provenance.

## Tokens

| Role    | Value     | Use                                  |
|---------|-----------|--------------------------------------|
| ground  | `#A9DC76` | grass window background              |
| surface | `#FFF6D9` | cream cards                          |
| banner  | `#F2B632` | gold header + footer                 |
| gold    | `#F7D774` | gold buttons, dark outline           |
| ink     | `#3B2F1E` | primary text (bark brown)            |
| muted   | `#5C6B3C` | secondary text                       |
| accent  | `#2FA84F` | progress blocks, play, selection     |
| danger  | `#B91C1C` | record state only                    |

Type: Segoe UI only. Title 13 bold / section 10 bold / body 10 / small 9.
Buttons: 1px `raised` Win32-style, uniform padding, hover lighten, sunken on press.
No focus dotted ring (global hotkeys are the keyboard interface).
Empty ledger shows a teaching row, never a blank table.
