# Đóng góp cho SwiftMacro

Cảm ơn bạn đã quan tâm! Vài quy ước để giữ project gọn và ổn định:

## Quy trình

1. Fork repo và tạo nhánh từ `main`: `git checkout -b feat/ten-tinh-nang`.
2. Chỉ sửa đúng phạm vi của issue/tính năng — không dồn nhiều việc vào một PR.
3. Mô tả PR rõ ràng: làm gì, vì sao, cách kiểm thử thủ công trên Windows.
4. Chờ review trước khi merge. Nhánh `main` luôn ở trạng thái chạy được.

## Quy ước code

- Theo đúng cấu trúc hiện tại: engine (`macro_engine.py`, `auto_engine.py`) **không** import tkinter; UI nằm ở `panels.py` / `app.py`.
- Giữ tiếng Việt trực tiếp, dễ hiểu trong UI; thông báo lỗi phải nêu rõ vấn đề **và** cách khắc phục.
- Không thêm dependency mới nếu chưa thảo luận qua issue.

## Báo lỗi

Dùng mẫu [bug report](../../issues/new?template=bug_report.yml): mô tả bước tái hiện, hành vi mong đợi, hành vi thực tế, phiên bản Windows + Python.
