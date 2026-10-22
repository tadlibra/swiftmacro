# PRODUCT.md — SwiftMacro

## Product truth

- **What:** Windows desktop tool that records mouse + keyboard macros and replays
  them (loops / continuous until stopped).
- **Audience:** Vietnamese gamers and power users automating repetitive in-game /
  in-app tasks. Intermediate skill, Vietnamese UI preferred.
- **Scene:** Runs *alongside* a game or app — window is small, often in background;
  user drives it mostly via global hotkeys (F9 record, F10 play), not mouse.
- **Job:** Record once → replay reliably, controlled by global hotkeys. Auto Click
  riêng cho nhu cầu click lặp (kiểu GS AutoClicker): khoảng nghỉ giờ/phút/giây/ms,
  chuột trái/phải/giữa, đơn/đúp, lặp đến khi dừng hoặc N lần, vị trí hiện tại hoặc
  tọa độ cố định, phím F8 Start/Stop.
- **Constraints:**
  - tkinter + `keyboard`, `mouse`, `Pillow` only. No admin rights assumed.
  - Global hotkeys must never collide silently; record/play are mutually exclusive.
  - Window must stay usable at 620px wide, resizable, nothing clipped.
- **Voice:** Direct Vietnamese, no marketing. Controls name their action;
  errors name the problem and the recovery.
- **Proof:** User screenshots of v2.0 (header/footer mismatch, button inconsistency,
  clipped color panel, popup settings) drove the v2.1 redesign.

## Standing commitments

- Light Restrained visual world (matches Windows light chrome). No dark hero blocks.
- Text-only controls; state shown by drawn lamp + color fill, never emoji glyphs.
- Settings stay inline (dropdown panel), never a modal popup.
