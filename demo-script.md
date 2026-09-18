# Kịch bản demo — cho Trường (C)

Dùng để quay video demo dự phòng (CP5) và demo live lúc thuyết trình (CP6). Tổng ~2 phút, khớp mục "Giải pháp & demo live" trong slide 3.

**Chuẩn bị trước khi quay:**
- Terminal mở sẵn tại `codebase/`, đã `export GEMINI_API_KEY=...`
- Có sẵn 1 cửa sổ mở `data/discord-pack/k4_daily_reports.md` để so sánh bản gốc
- Test thử chạy 1 lần trước để chắc không lỗi mạng giữa chừng

---

## Phần 1 — Case chuẩn: gộp đúng (~45 giây)

**Nói:**
> "Đây là bản tin gốc của bot hiện tại — 4 gạch đầu dòng riêng biệt cho cùng một chuyện: nộp Lab2 muộn."

*(Chỉ tay vào 4 bullet trong `k4_daily_reports.md`, mục K4-L3-4 14/9)*

**Nói:**
> "Giờ mình chạy AI thật của nhóm trên đúng dữ liệu này."

**Gõ lệnh:**
```
python3 cluster_report.py ../data/discord-pack/k4_messages.csv
```

**Chờ output, sau đó nói:**
> "AI gộp lại thành 1 dòng: 3 học viên đang hỏi về nộp Lab2 muộn, ưu tiên Cao vì thuộc nhóm deadline, kèm link tới 4 tin nguồn — bấm vào là xem được ai hỏi gì. Số 3 này không phải AI tự khai, code tụi mình đếm lại từ dữ liệu gốc, vì 1 trong 4 tin là cùng một bạn hỏi 2 lần."

---

## Phần 2 — Case chỗ khó: chặn lộ thông tin cá nhân (~45 giây)

**Nói:**
> "Đây là phần tụi mình tự tin nhất — vì nó từng sai thật."

**Nói:**
> "Lúc đo thử, AI đã lỡ đưa 1 câu hỏi cá nhân — 'kiểm tra điểm danh của mình' — vào cụm công khai. Đúng lớp lỗi nguy hiểm nhất: lộ thông tin riêng tư."

*(Mở `eval/run_log_2.md`, chỉ vào dòng Case 5 — FAIL)*

**Nói:**
> "Tụi mình không sửa bằng cách dặn AI kỹ hơn trong prompt — vì đã dặn rồi mà vẫn sai. Tụi mình thêm 1 lớp lưới an toàn bằng code, không phụ thuộc AI."

**Gõ lệnh (chạy test, không cần API key):**
```
cd ../codebase
python3 -m pytest test_safety_checks.py -k personal -v || python3 -c "
import test_safety_checks as t
t.test_strip_personal_messages_catches_model_mistake()
print('PASS - câu hỏi cá nhân bị chặn đúng, câu hỏi chung vẫn được giữ')
"
```

**Nói (chốt câu):**
> "Kể cả nếu model có sai lần nữa, lưới an toàn này vẫn chặn được — vì nó không dựa vào việc AI có nghe lời hay không."

---

## Timing tổng — khớp slide 3 (2 phút)

| Đoạn | Thời lượng | Nội dung |
|---|---|---|
| Mở đầu | 10s | So sánh bản gốc 4 dòng vs vấn đề thật |
| Case chuẩn | 45s | Chạy lệnh thật, đọc kết quả gộp đúng |
| Case chỗ khó | 45s | Kể lỗi thật đã xảy ra + chạy test chứng minh đã vá |
| Chốt | 20s | 1 câu tổng kết: "AI gộp, code kiểm lại — không tin AI 100%" |

**Nếu bị hỏi thêm lúc Q&A (chuẩn bị sẵn câu trả lời):**
- *"Sao không để AI tự chấm mức ưu tiên luôn?"* → Vì mức ưu tiên ảnh hưởng TA xử lý cái gì trước, cần giải thích được bằng số — để AI tự chấm sẽ không kiểm chứng lại được.
- *"Nếu Gemini lỗi mạng giữa chừng thì sao?"* → Đây là chỗ tụi mình biết còn yếu (2/7 lần lỗi ở lượt đo 1), chưa kịp xử lý retry, ghi rõ trong slide 6 "nếu có thêm 1 tuần".
- *"Golden set có bao nhiêu case, phủ được gì?"* → 20+ case, đủ 4 lớp chỗ khó, ít nhất 2 case mỗi lớp, 15+ case trích từ dữ liệu thật.
