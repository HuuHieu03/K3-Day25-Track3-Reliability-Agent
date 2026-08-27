---
version: "1.0.0"
date: "2026-08-27"
type: "doc"
status: "COMPLETED"
author: "AI Agent"
target_component: "Workspace Guide"
tags: ["workspace", "readme", "guide"]
summary: "Tổng quan về cấu trúc, quy ước đặt tên và cách sử dụng không gian làm việc chuẩn my_workspace/."
---

# 📂 MY WORKSPACE - HỆ THỐNG QUẢN LÝ DỰ ÁN & TIẾN ĐỘ CHUẨN

Không gian làm việc `my_workspace/` được thiết kế để theo dõi tiến độ, lưu trữ tài liệu phân tích kỹ thuật, kế hoạch thực thi, nhật ký kiểm thử và lịch sử bàn giao phiên làm việc cho bài Lab **Day 25 Track 3: Reliability Agent**.

---

## 🗂️ Cấu trúc thư mục

```
my_workspace/
├── rules.md                   # Bộ quy chuẩn hành vi cốt lõi của AI Agent
├── README.md                  # Hướng dẫn tổng quan về workspace
├── docs/                      # Tài liệu phân tích kỹ thuật, kiến trúc, khái niệm
│   ├── README.md              # Giới thiệu thư mục docs
│   ├── TEMPLATE_docs.md       # Mẫu tài liệu kỹ thuật
│   └── reports/               # Báo cáo tổng kết, đánh giá bài Lab
│       ├── README.md          # Giới thiệu thư mục reports
│       └── TEMPLATE_report.md # Mẫu báo cáo kỹ thuật / tổng kết
├── plans/                     # Kế hoạch thực thi chi tiết theo từng phiên/giai đoạn
│   ├── README.md              # Giới thiệu thư mục plans
│   └── TEMPLATE_plan.md       # Mẫu kế hoạch thực thi
├── progress/                  # Theo dõi tiến độ chi tiết từng task và checklist
│   ├── README.md              # Giới thiệu thư mục progress
│   └── TEMPLATE_progress.md   # Mẫu bảng theo dõi tiến độ
├── logs/                      # Nhật ký chạy test, chaos simulation, benchmark thực tế
│   ├── README.md              # Giới thiệu thư mục logs
│   └── TEMPLATE_log.md        # Mẫu ghi nhận log kiểm thử
└── history/                   # Tóm tắt các phiên làm việc và bàn giao ngữ cảnh
    ├── README.md              # Giới thiệu thư mục history
    └── TEMPLATE_history.md    # Mẫu tóm tắt bàn giao phiên làm việc
```

---

## 📝 Quy chuẩn YAML Frontmatter bắt buộc

Mọi tệp tài liệu trong `my_workspace/` phải chứa YAML header ở đầu tệp:

```yaml
---
version: "1.0.0"
date: "YYYY-MM-DD"
type: "plan | progress | log | history | doc | report"
status: "PLANNED | IN_PROGRESS | COMPLETED | FAILED"
author: "AI Agent"
target_component: "Tên module hoặc bài Lab"
tags: ["tag1", "tag2"]
summary: "Tóm tắt ngắn gọn 1-2 câu."
---
```

## 🏷️ Quy tắc đặt tên tệp
- Định dạng chuẩn: `v<version>_<YYYY-MM-DD>_<tên_ngắn_gọn>.md`
- Ví dụ:
  - `v1.0.0_2026-08-27_execution_plan.md`
  - `v1.0.0_2026-08-27_task_progress.md`
  - `v1.0.0_2026-08-27_baseline_test_run.md`
