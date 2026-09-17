# AI SPEC — Bản tin ngày gộp cụm ngữ nghĩa cho TA · Nhóm Robotica · Zone [CẦN ĐIỀN]
Hướng: [x] B — Trợ lý Học viên
Loại: [x] Tối ưu tính năng có sẵn (B2 — bản tin ngày)

## §1. User & Job
- Job executor + workflow: TA/Learning Coach đọc bản tin cuối ngày do bot "Trợ lý" tự đăng trên Discord, để biết học viên đang vướng vấn đề gì cần can thiệp.
- Core JTBD: *Khi đọc bản tin cuối ngày, TA muốn biết đúng số học viên đang gặp mỗi vấn đề, để quyết định vấn đề nào cần ưu tiên trả lời trước.*
- Problem statement (không chữ AI): Bản tin liệt kê từng câu hỏi thành một gạch đầu dòng riêng, kể cả khi nhiều dòng thực chất là cùng một vấn đề do một người hỏi lại nhiều lần hoặc nhiều người diễn đạt khác nhau — khiến TA đọc nhầm số lượng người bị ảnh hưởng và không biết vấn đề nào đã có hướng giải quyết.
- Evidence (chuẩn B — mining):
  - Đêm 12→13/9, 3 học viên khác nhau (`D3115`, `D6014`, `D7496`) hỏi cùng chủ đề "nộp Lab2 muộn/gia hạn" trong 79 phút (00:08–01:27); `D6014` hỏi 2 lần liên tiếp cùng phút 00:15 (`M20574`, `M75012`). Bot báo cáo thành 4 gạch đầu dòng riêng trong "Học viên đang hỏi gì" (nguồn: `k4_daily_reports.md`, K4-L3-4 14/9), đếm `D6014` như 2 vấn đề khác nhau; câu trả lời gợi ý của `D7593` (`M24366`) bị tách sang mục "Thảo luận học tập" thay vì gắn liền.
  - [CẦN ĐIỀN] Mở rộng đếm trên toàn bộ `k4_messages.csv` + cả 4 bản tin trong `k4_daily_reports.md`: bao nhiêu % gạch đầu dòng trong "Học viên đang hỏi gì" là có thể gộp được với ít nhất 1 dòng khác (mục tiêu ≥5 case nguyên văn, không chỉ 1 case Lab2). Người phụ trách: A (Nguyễn Thái Lương).
  - [CẦN ĐIỀN] Khảo sát/phỏng vấn TA hoặc học viên từng đọc bản tin (nếu kịp làm chuẩn A).

## §2. Impact & quyết định chọn
- [CẦN ĐIỀN] Bảng impact ≥3 ứng viên — hiện mới có 1 (gộp cụm). Cần thêm ≥2 ứng viên khác đã cân nhắc (vd: cảnh báo học viên stuck chủ động, tóm tắt chủ đề nóng theo kênh...) kèm số liệu bao nhiêu người × tần suất × tốn gì mỗi lần.
- Ứng viên ĐÃ LOẠI + vì sao: [CẦN ĐIỀN]
- Ứng viên CHỌN: Gộp cụm ngữ nghĩa câu hỏi trùng ý — vì sao (bằng số): [CẦN ĐIỀN, dựa trên % gộp được ở §1]

## §3. Giải pháp tương tự đã nghiên cứu
- [CẦN ĐIỀN] Mỗi thành viên dùng thử 1 sản phẩm gần giống (vd: Slack thread summarization, Discord AI mod bot, Notion AI) — flow / đáng học / đáng né / mình khác gì.

## §4. Thiết kế
- Lát cắt MỘT CÂU: Một TA đọc bản tin cuối ngày · AI gom các câu hỏi trùng ý thành một dòng đếm theo số học viên duy nhất kèm link nguồn · TA biết đúng có bao nhiêu học viên thực sự đang vướng một vấn đề.
- Non-goals (≥3 thứ KHÔNG build): [CẦN ĐIỀN — gợi ý: không tự động trả lời thay TA; không tự gửi tin nhắn cho học viên; không nêu tên/định danh học viên trong bản tin công khai]
- Mức prototype nhắm tới: [ ] Sketch [x] Mock (đang ở flow.md) — phần thật: lọc + hiển thị; phần mock: AI call (CP3 sẽ thay bằng thật)
- Automation: [x] Conditional — tự gộp khi chắc chắn cùng chủ đề; không tự gộp khi mơ hồ, giữ tách + gắn cờ "cần TA xác nhận". Lý do (cost-of-error): gộp lố 2 vấn đề khác nhau (vd 2 deadline khác nhau) khiến TA trả lời sai thông tin cho đúng người — sai thì đắt, nên chọn conditional thay vì automate.
- §4b. Nguyên tắc đã áp dụng (≥4 — cần điền vị trí cụ thể):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | G10 — Thu hẹp phạm vi khi nghi ngờ | [CẦN ĐIỀN — vị trí trong flow.md bước [3] nhánh "không chắc"] |
  | [CẦN ĐIỀN thêm ≥3 nguyên tắc, xem further-reading/hax-guidelines.md] | |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)
| Lớp | Tình huống cụ thể | Hành vi mong muốn | Nguyên tắc áp |
|---|---|---|---|
| ④ Đặc thù domain | Hai deadline khác nhau (Lab2 vs Lab3) bị gộp chung 1 cụm | Không gộp, tách riêng, gắn cờ cần xác nhận | G10 |
| ① Nguồn sự thật | AI suy diễn "vấn đề đã xử lý" dù chưa có ai xác nhận | Giữ nguyên trạng thái "chưa xác nhận", không tự kết luận | G11 |
| ③ Ngoài phạm vi | Tin của bot (`is_bot=True`) bị đếm là câu hỏi học viên | Lọc bỏ trước khi gộp cụm | — |
| [CẦN ĐIỀN — còn thiếu ≥5 kịch bản, mỗi lớp ①②③④ cần ≥2 case, xem 02-guide.md §2.5] | | | |

## §6. Bốn đường đi của trải nghiệm
- Happy path: Nhiều học viên hỏi rõ cùng 1 chủ đề → gộp thành 1 dòng có số đếm + link (xem flow.md mock trước/sau)
- Low-confidence (②): Hai câu hỏi có thể cùng/khác chủ đề → không gộp liều, gắn cờ "cần TA xác nhận" (xem flow.md bước [3])
- Failure/không căn cứ (①): [CẦN ĐIỀN]
- Correction (user sửa): [CẦN ĐIỀN — nút "tách cụm" trong flow.md bước [6], chưa build]
- Khi bị đòi ngoài phạm vi (③): [CẦN ĐIỀN]
- Case đặc thù domain (④): [CẦN ĐIỀN — case 2 deadline khác nhau bị gộp sai]

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được: [CẦN ĐIỀN]
- Golden set (≥20 case, file trong eval/): [CẦN ĐIỀN — chưa xây]
- Quality bar: "Đạt khi ≥ ___% qua bộ, và ___" — [CẦN ĐIỀN, chốt trước 21:00 18/9 tại CP4]
- Kết quả các lượt chạy: [CẦN ĐIỀN sau CP3]

## §8. Phân công & kế hoạch
- Phân công có tên:
  - Nguyễn Thái Lương (2A202602932) — A: mining evidence, đếm + mã tin
  - Trần Cao Quốc Định (2A202602939) — B: spec, đội trưởng nộp form
  - Nguyễn Xuân Trường (2A202602761) — C: build, gọi AI thật
  - Nguyễn Mạnh Tiến (2A202602506) — D: golden set, đo lường
- Willing users (≥2 tên): Mai Tiến Huy (học viên K4), Lê Việt Hoàng (học viên K4), Hoàng Ngọc Đức (học viên K4)
- Multi-prototype (nếu làm): [CẦN ĐIỀN, không bắt buộc]

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| [Điền sau khi có validation ở CP5] | | |
