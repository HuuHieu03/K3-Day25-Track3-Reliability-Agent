---
version: "1.0.0"
date: "2026-08-27"
type: "doc"
status: "COMPLETED"
author: "AI Agent"
target_component: "Logs Directory"
tags: ["logs", "readme"]
summary: "Thư mục lưu trữ toàn bộ kết quả chạy test, benchmark và chaos simulation thực tế."
---

# 📋 THƯ MỤC NHẬT KÝ KIỂM THỬ (LOGS)

Thư mục này lưu trữ:
- Toàn bộ kết quả thực thi lệnh test thực tế (`pytest`, `make test`).
- Log chạy mô phỏng Chaos và Benchmark (`make run-chaos`).
- Log kiểm tra static analysis / typecheck (`mypy`, `ruff`).

## File mẫu
- `TEMPLATE_log.md`: Mẫu chuẩn cho tài liệu ghi log kiểm thử.
