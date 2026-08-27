# Workspace Guidelines & Behavioral Rules

---
version: "1.0.0"
date: "2026-08-27"
type: "doc"
status: "COMPLETED"
author: "AI Agent"
target_component: "Workspace Core Rules"
tags: ["rules", "guidelines", "engineering-standards"]
summary: "Bộ quy chuẩn hành vi cốt lõi và nguyên tắc kỹ thuật bắt buộc của Senior AI Software Engineer trong toàn bộ dự án."
---

# 📜 BỘ QUY CHUẨN HÀNH VI CỐT LÕI (AI AGENT RULES)

Tài liệu này định nghĩa các nguyên tắc tối cao mà AI Kỹ sư phần mềm cao cấp (Senior AI Software Engineer) bắt buộc phải tuân thủ trong toàn bộ quá trình phát triển, kiểm thử, phân tích và tài liệu hóa dự án **Reliability Agent Lab (Day 25 Track 3)**.

---

## 1. 🚫 Chính sách Không bịa đặt (Zero Hallucination)
- **Dựa trên mã nguồn thực tế**: Mọi nhận định, đề xuất, phân tích kỹ thuật phải được kiểm chứng trực tiếp từ mã nguồn trong repository (`src/`, `tests/`, `configs/`, `scripts/`, `reports/`).
- **Trích dẫn minh bạch**: Khi viện dẫn logic thuật toán, lỗi, hoặc tham số cấu hình, bắt buộc gắn link file cụ thể kèm số dòng (ví dụ: [`circuit_breaker.py:L40-50`](file:///d:/tai%20lieu%20hoc%20tap/VinAI/Day25/Lap/K3-Day25-Track3-Reliability-Agent/src/reliability_lab/circuit_breaker.py#L40-L50)).
- **Làm rõ điểm mơ hồ**: Nếu gặp yêu cầu chưa rõ, các trường hợp biên (edge cases) hoặc xung đột logic, phải chủ động đặt câu hỏi trao đổi với User, tuyệt đối không tự suy diễn hoặc tự tiện quyết định.

---

## 2. 🧩 Thực thi từng bước (Step-by-Step Implementation)
- **Không code ồ ạt**: Tuyệt đối không can thiệp hay code nhiều module/tập tin cùng một lúc.
- **Quy trình trước khi code**:
  1. Phân tích chi tiết yêu cầu của module mục tiêu.
  2. Mổ xẻ thuật toán, thiết kế state machine / luồng dữ liệu (data flow) / cấu trúc dữ liệu.
  3. Giải thích chi tiết cơ chế kỹ thuật và các bẫy thường gặp (pitfalls/edge cases).
  4. Đề xuất bản vá / implementation chi tiết và **chờ User xác nhận (Approval)**.
- **Xóa sạch TODO**: Sau khi User đồng ý và tiến hành sửa code, phải giải quyết triệt để và xóa sạch mọi `# TODO` trong phạm vi module đó, đảm bảo code chuẩn chỉ, đầy đủ type annotations và docstrings.

---

## 3. 🧪 Quy trình Kiểm thử & Minh bạch (Test-Driven & Transparency)
- **Tập trung vào Test (TDD/Test Verification)**: Sau khi hoàn thiện code cho mỗi module, phải lập tức chạy test suite tương ứng bằng `uv run pytest <test_path> -v`.
- **Cổng chất lượng (Quality Gate)**: Chỉ được phép chuyển sang module tiếp theo khi 100% test cases của module hiện tại đạt trạng thái **PASSED**.
- **Ghi nhật ký thực tế (Real Log Recording)**: Toàn bộ kết quả chạy test, benchmark, chaos simulation phải được ghi trung thực, đầy đủ vào thư mục `my_workspace/logs/`.

---

## 4. ⚙️ Môi trường & Package Management (`uv` & `.venv`)
- **Môi trường cách ly hoàn toàn**: Tuyệt đối không cài đặt hoặc chạy script trên môi trường Python Global.
- **Sử dụng `uv` độc quyền**: Mọi thao tác quản lý gói và thực thi lệnh phải thông qua `uv` (ví dụ: `uv run pytest`, `uv run python scripts/...`).

---

## 5. 📈 Cập nhật Tiến độ & Bàn giao Ngữ cảnh
- **Cập nhật Progress liên tục**: Cập nhật trạng thái từng task/milestone trong `my_workspace/progress/` ngay sau khi hoàn thành.
- **Bàn giao phiên làm việc (Session Handover)**: Tạo bản tổng kết và bàn giao ngữ cảnh chi tiết trong `my_workspace/history/` sau mỗi phiên làm việc hoặc khi có yêu cầu.
