# SwiftMacro

<p>
  <img src="assets/logo-64.png" alt="SwiftMacro logo" width="64" />
</p>

Công cụ desktop cho Windows: **ghi macro chuột + phím và phát lại**, kèm **Auto Click** kiểu GS AutoClicker. Giao diện tiếng Việt, điều khiển chủ yếu bằng phím tắt toàn cục.

[![CI](https://github.com/YOUR-GITHUB-USER/SwiftMacro/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR-GITHUB-USER/SwiftMacro/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/YOUR-GITHUB-USER/SwiftMacro)](https://github.com/YOUR-GITHUB-USER/SwiftMacro/releases)
![Windows](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)

> **Bản quyền:** mã nguồn công khai để minh bạch, mọi quyền được bảo lưu — xem [LICENSE](LICENSE). Chưa được phép thì không dùng/sửa/phân phối lại.

## Tính năng

- **Macro:** ghi thao tác chuột + bàn phím, phát lại theo số vòng lặp hoặc liên tục đến khi dừng.
- **Auto Click:** khoảng nghỉ giờ/phút/giây/ms, chuột trái/phải/giữa, click đơn/đúp, lặp N lần hoặc đến khi dừng, click tại vị trí hiện tại hoặc tọa độ cố định.
- **Phím tắt toàn cục:** F9 ghi/dừng, F10 phát/dừng, F8 auto click start/stop — tùy chỉnh được, có cảnh báo khi trùng phím.
- **Lưu/tải kịch bản** định dạng `.swiftmacro` (JSON).
- Gọn nhẹ: chỉ dùng `tkinter` + `keyboard`, `mouse`, `Pillow`. Không yêu cầu quyền admin.

## Phím tắt mặc định

| Phím | Tác dụng              |
|------|-----------------------|
| F9   | Bắt đầu / dừng ghi    |
| F10  | Phát / dừng phát lại  |
| F8   | Auto Click start/stop |

Ghi và phát loại trừ lẫn nhau: đang ghi thì không phát được và ngược lại.

## Cài đặt & chạy từ mã nguồn

Yêu cầu: **Windows** + **Python 3.10 trở lên**.

```bat
git clone https://github.com/YOUR-GITHUB-USER/SwiftMacro.git
cd SwiftMacro
pip install -r requirements.txt
python swiftmacro.py
```

## Tải bản dựng sẵn (khuyến nghị cho người dùng cuối)

Vào trang [Releases](https://github.com/YOUR-GITHUB-USER/SwiftMacro/releases), tải file `SwiftMacro-<phiên bản>-win64.exe` và chạy — không cần cài Python.

## Tự build file EXE

```bat
pip install -r requirements.txt
pip install pyinstaller
pyinstaller SwiftMacro.spec
```

File EXE nằm trong `dist/SwiftMacro/`.

## Cấu trúc project

```
swiftmacro.py      → launcher mỏng, gọi swift.app:main
swift/
  config.py        → tên app, phiên bản, hotkey và giá trị mặc định
  theme.py         → palette, icon pixel, style nút
  macro_engine.py  → ghi + phát lại macro (không dính tkinter)
  auto_engine.py   → auto click kiểu GS AutoClicker (không dính tkinter)
  panels.py        → 3 panel UI: Macro, AutoClick, Hotkeys
  app.py           → MacroApp: chrome cửa sổ + lắp ráp + đọc/ghi file
assets/            → logo các kích thước + icon .ico
```

Chi tiết sản phẩm xem [PRODUCT.md](PRODUCT.md), quyết định thiết kế xem [DESIGN.md](DESIGN.md).

## Đóng góp

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) trước khi gửi pull request.

## Bảo mật

Phát hiện lỗ hổng? Đừng mở issue công khai — xem [SECURITY.md](SECURITY.md).

## Changelog

Xem [CHANGELOG.md](CHANGELOG.md).
