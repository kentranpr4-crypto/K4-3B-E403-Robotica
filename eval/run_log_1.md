# Lượt chạy 1 — CP3 (thử tay bởi C, 18/9)

**Đã thử:** 7 lần · **Đạt:** 5/7 (~71%)

**Chuẩn "đạt" dùng cho lượt này:** Gọi Gemini thật, kết quả gộp đúng ngữ nghĩa các câu hỏi trùng ý, hiển thị đầy đủ thông tin (chủ đề, số học viên, nguồn tin).

**2 lần chưa đạt — nguyên nhân:**
1. Lỗi khi gọi API (chưa xác định rõ nguyên nhân cụ thể — nghi ngờ định dạng request hoặc rate limit của free tier).
2. Code chưa quy định rõ schema output cần hiển thị, nên model thiếu trường khi trả về.

**Việc cần làm tiếp trước CP4:**
- Bắt lỗi rõ ràng khi gọi API thất bại (retry hoặc thông báo lỗi rõ thay vì im lặng) — liên quan G1 (làm rõ hệ thống làm được gì).
- Ép schema output chặt hơn trong prompt (`CLUSTER_PROMPT` trong `codebase/cluster_report.py` đã có schema JSON — kiểm tra lại có đang bị model bỏ sót trường không).
- Chạy tiếp qua `eval/golden_set.md` (19 case) bằng `eval/run_eval.py` để có số đo đầy đủ hơn cho CP4, không chỉ dừng ở 7 lần thử tay.
