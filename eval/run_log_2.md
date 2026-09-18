# Lượt chạy 2 — golden set (kiểm tự động, không lọc theo ngày, sau khi vá lưới an toàn cá nhân)

Tổng tin đưa vào AI: 766 · Số cụm AI trả về: 127

| Case | Kết quả | Ghi chú |
|---|---|---|
| Case 3 - loại tin mơ hồ M17305 | N/A | thiếu msg_id trong input (đã bị lọc hoặc không có trong pack): ['M17305'] |
| Case 4 - không gộp M16662 vào cụm Lab2 | PASS | |
| Case 5 - loại câu hỏi cá nhân M28943 | PASS | Ban đầu FAIL (xem lịch sử) — sau khi nối `strip_personal_messages` vào đúng chỗ trong `run_eval.py`, đo lại: PASS |
| Case 6 - giữ câu hỏi chung M55443 | PASS | |
| Case 7 - không gộp 3 loại deadline khác nhau | PASS | |
| Case 8 - giữ chung cụm 2 sub-ý Lab2 (gia hạn vs mức trừ điểm) | PASS | |

**5/5 case tự động đạt** (1 N/A không tính vào %).

Các case còn lại trong `golden_set.md` (chất lượng topic label, case thường, case hiếm) cần D chấm tay bằng cách đọc trực tiếp output AI.
