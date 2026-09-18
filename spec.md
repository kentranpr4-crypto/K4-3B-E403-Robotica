# AI SPEC — Bản tin ngày gộp cụm ngữ nghĩa cho TA · Nhóm Robotica · Zone K4-3B-E403-Robotica
Hướng: [x] B — Trợ lý Học viên
Loại: [x] Tối ưu tính năng có sẵn (B2 — bản tin ngày)

## §1. User & Job
- Job executor + workflow: TA/Learning Coach đọc bản tin cuối ngày do bot "Trợ lý" tự đăng trên Discord, để biết học viên đang vướng vấn đề gì cần can thiệp.
- Core JTBD: *Khi đọc bản tin cuối ngày, TA muốn biết đúng số học viên đang gặp mỗi vấn đề, để quyết định vấn đề nào cần ưu tiên trả lời trước.*
- Problem statement (không chữ AI): Bản tin liệt kê từng câu hỏi thành một gạch đầu dòng riêng, kể cả khi nhiều dòng thực chất là cùng một vấn đề do một người hỏi lại nhiều lần hoặc nhiều người diễn đạt khác nhau — khiến TA đọc nhầm số lượng người bị ảnh hưởng và không biết vấn đề nào đã có hướng giải quyết.
- Evidence (chuẩn B — mining):
  - Đêm 12→13/9, 3 học viên khác nhau (`D3115`, `D6014`, `D7496`) hỏi cùng chủ đề "nộp Lab2 muộn/gia hạn" trong 79 phút (00:08–01:27); `D6014` hỏi 2 lần liên tiếp cùng phút 00:15 (`M20574`, `M75012`). Bot báo cáo thành 4 gạch đầu dòng riêng trong "Học viên đang hỏi gì" (nguồn: `k4_daily_reports.md`, K4-L3-4 14/9), đếm `D6014` như 2 vấn đề khác nhau; câu trả lời gợi ý của `D7593` (`M24366`) bị tách sang mục "Thảo luận học tập" thay vì gắn liền.
  - Khảo sát trên toàn bộ 4 bản tin ngày trong `k4_daily_reports.md`: Bot sinh ra tổng cộng 16 gạch đầu dòng (bullet points). Phân tích cho thấy có tới 15/16 bullets (chiếm 93.75%) có thể gộp chung lại thành các cụm ngữ nghĩa nhỏ hơn (tổng cộng 6 cụm và 1 tin lẻ). Việc không gộp cụm khiến lượng thông tin TA phải đọc bị phình to bất hợp lý. Người phụ trách: A (Nguyễn Thái Lương).
  - [CẦN ĐIỀN] Khảo sát/phỏng vấn TA hoặc học viên từng đọc bản tin (nếu kịp làm chuẩn A).

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (đếm thật trên `k4_messages.csv`, 1.092 tin, 779 tin không phải bot):

| Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi trong sự kiện |
|---|---|---|---|---|
| **A. Gộp cụm câu hỏi trùng ý (chọn)** | 35 học viên duy nhất từng hỏi/nhắc từ khoá deadline·nộp·hạn (60 tin không-bot chứa từ khoá này trong 3 ngày pack) | Lặp lại mỗi ngày — riêng cụm Lab2 có 3 người hỏi trong 79 phút | TA đọc nhầm số người/độ nóng, có thể bỏ sót vấn đề đã có ai trả lời | Cao — chỉ cần 1 lời gọi AI + hậu kiểm đếm lại, không cần UI phức tạp |
| B. Trả lời logistics chỉ từ nguồn chính thức (hướng B1) | Cùng nhóm 35 người trên | Mỗi câu hỏi logistics | Rủi ro bot trả lời sai deadline, hậu quả điểm số | Trung bình — cần xây kho "nguồn chính thức" để đối chiếu, tốn thời gian hơn B2 trong khung sự kiện |
| C. Phát hiện học viên "stuck" và chủ động nhắn hỗ trợ | Khó ước lượng bằng mining (không có tín hiệu "im lặng" rõ trong log) | Không xác định | Rủi ro làm phiền nếu chủ động sai lúc | Thấp — an toàn (theo track B2) cấm tự động gửi tin chưa qua duyệt, khó demo trong 39h |
| D. Tóm tắt riêng câu hỏi điểm danh theo kênh | 22 học viên duy nhất (37 tin chứa "điểm danh") | Thấp hơn nhóm deadline | Nhầm lẫn cách check điểm danh | Cao nhưng phạm vi hẹp hơn A, ít đại diện cho pain chung |

- Ứng viên ĐÃ LOẠI + vì sao:
  - **B** loại vì trùng hướng với track B1 (đã có nhóm khác làm), và tốn thời gian xây "kho nguồn chính thức" hơn khả năng của nhóm trong 39 giờ.
  - **C** loại vì rủi ro an toàn cao (an toàn B2 cấm tự ý nhắn học viên khi chưa duyệt) và không mining được bằng chứng số vững như A/D.
  - **D** loại vì quy mô nhỏ hơn A (22 vs 35 người) — pain hẹp hơn, ít đại diện.
- Ứng viên CHỌN: **A — Gộp cụm ngữ nghĩa** — vì có nhóm người bị ảnh hưởng lớn nhất đo được (35/779 tin không-bot ≈ 4,5%), có bằng chứng cụ thể lỗi bot hiện tại (case Lab2 đếm nhầm D6014 thành 2 người), và khả thi build trong thời gian sự kiện (chỉ 1 lời gọi AI + hậu kiểm đếm lại bằng code, không cần hạ tầng mới).

## §3. Giải pháp tương tự đã nghiên cứu
- Đánh giá giải pháp Discord AI Channel Summaries:
  1. Flow: AI của Discord tự động nhóm các tin nhắn liên tiếp thành các cụm chủ đề ghim bên hông kênh.
  2. Đáng học: Nhận diện thời điểm một cụm chủ đề kết thúc rất nhạy dựa trên bối cảnh và thời gian.
  3. Đáng né: Tóm tắt vô tội vạ cả những câu đùa cợt, tán gẫu, khiến bản tóm tắt đọc thì vui nhưng làm nhiễu công việc vận hành.
  4. Khác biệt: Sản phẩm của nhóm CHỈ bóc tách CÂU HỎI chưa được trả lời, lọc bỏ tạp âm, gộp chúng lại thành 1 bản báo cáo hành động (Actionable Report) cho TA.

## §4. Thiết kế
- Lát cắt MỘT CÂU: Một TA đọc bản tin cuối ngày · AI gom các câu hỏi trùng ý thành một dòng đếm theo số học viên duy nhất kèm link nguồn · TA biết đúng có bao nhiêu học viên thực sự đang vướng một vấn đề.
- Non-goals (≥3 thứ KHÔNG build): (1) không tự động trả lời thay TA — chỉ tổng hợp, TA vẫn là người phản hồi; (2) không tự gửi tin nhắn cho học viên; (3) không nêu tên/định danh học viên (`D####`) trong bản tin công khai; (4) không tự sinh câu trả lời cho nội dung câu hỏi — chỉ gộp và mô tả chủ đề.
- Mức prototype nhắm tới: [ ] Sketch [x] Mock — phần thật: lọc bot/rác, đếm lại số người, che định danh (đã code + test PASS); phần mock: gộp cụm ngữ nghĩa (cần AI thật ở CP3, code đã sẵn trong `codebase/cluster_report.py`, chờ API key)
- Automation: [x] Conditional — tự gộp khi chắc chắn cùng chủ đề; không tự gộp khi mơ hồ, giữ tách + gắn cờ "cần TA xác nhận". Lý do (cost-of-error): gộp lố 2 vấn đề khác nhau (vd 2 deadline khác nhau) khiến TA trả lời sai thông tin cho đúng người — sai thì đắt, nên chọn conditional thay vì automate.
- §4b. Nguyên tắc đã áp dụng:
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | G10 — Thu hẹp phạm vi khi nghi ngờ | `cluster_report.py`: khi model đánh dấu `uncertain: true` (2 chủ đề có thể khác nhau), giữ tách riêng thay vì gộp liều — flow.md bước [3] |
  | G11 — Giải thích vì sao | Mỗi dòng report giữ `msg_id` nguồn thay vì chỉ đưa kết luận — TA bấm vào xem căn cứ |
  | G8 — Gạt bỏ dễ dàng | Bản tin ghi rõ "cần TA xác nhận", cho phép TA bỏ qua cụm đó nếu thấy sai hoặc không quan trọng, không ép phải xử lý ngay |
  | G1 — Làm rõ hệ thống làm được gì | Bản tin ghi rõ "cần TA xác nhận" cho case mơ hồ thay vì im lặng coi như đúng |
  | G11 — Giải thích vì sao (mở rộng) | Mức ưu tiên (Cao/Trung bình/Thấp) tính bằng quy tắc rõ ràng từ số học viên + danh mục — không để AI tự chấm khẩn cấp mà không có căn cứ (`compute_priority` trong `cluster_report.py`) |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) — chi tiết đầy đủ trong `eval/golden_set.md`
| Lớp | Tình huống cụ thể | Hành vi mong muốn | Nguyên tắc áp |
|---|---|---|---|
| ① Nguồn sự thật | Cụm Lab2 — bot tự ghi "đã có phản hồi, chưa xác nhận đã xử lý" dù không chắc | Không tự kết luận đã xử lý khi không có tin trả lời rõ ràng trong dữ liệu | G11 |
| ① Nguồn sự thật | Học viên hỏi deadline ghép đội (M19124), không có nguồn chính thức nào trong ngày xác nhận | Không tự bịa ngày cụ thể; nói "chưa thấy nguồn chính thức, cần TA xác minh" | G10, G11 |
| ② Mơ hồ | Tin nội dung chỉ "1" (M17305), không rõ nghĩa | Loại khỏi mọi cụm, không ép gộp | G10 |
| ② Mơ hồ | Câu hỏi deadline "feedback video" (M16662) dễ nhầm với cụm Lab2 vì cùng chữ "deadline" | Tách riêng, không gộp nhầm chủ đề | G10 |
| ③ Ngoài phạm vi | Câu hỏi cá nhân "kiểm tra điểm danh của mình" (M28943) | Loại khỏi cụm công khai, không hiện trong bản tin | An toàn B2: không nêu định danh học viên |
| ③ Ngoài phạm vi | Tin của bot (`is_bot=True`) bị đếm là câu hỏi học viên | Lọc bỏ trước khi đưa cho AI (đã build + test tự động, PASS) | — |
| ④ Đặc thù domain | 3 loại "deadline" khác nhau (Lab2 / ghép đội / feedback video) cùng ngày, cùng chứa chữ "deadline" | Không gộp chung 1 cụm dù trùng từ khoá | G10 |
| ④ Đặc thù domain | Trong 1 cụm có 2 sub-ý khác nhau (xin gia hạn vs hỏi mức trừ điểm) | Giữ topic trung lập, không tự sinh câu trả lời chung cho cả 2 | G9, G11 |

## §6. Bốn đường đi của trải nghiệm
- Happy path: Nhiều học viên hỏi rõ cùng 1 chủ đề → gộp thành 1 dòng có số đếm (đếm lại bằng code, không tin số AI tự khai) + link (xem flow.md mock trước/sau)
- Low-confidence (②): Hai câu hỏi có thể cùng/khác chủ đề (vd 3 loại "deadline" khác nhau) → không gộp liều, tách riêng + gắn cờ "cần TA xác nhận" (xem flow.md bước [3], `eval/golden_set.md` case 4, 7)
- Failure/không căn cứ (①): Không có tin trả lời nào trong dữ liệu ngày cho một vấn đề (vd deadline ghép đội, case 2) → AI nói rõ "chưa thấy nguồn chính thức trong dữ liệu, cần TA xác minh", không tự bịa
- Correction (user sửa): [CẦN ĐIỀN — nút "tách cụm" trong flow.md bước [6], chưa build; C ưu tiên nếu kịp trước CP4]
- Khi bị đòi ngoài phạm vi (③): Câu hỏi cá nhân (tra cứu điểm danh riêng) → loại khỏi cụm công khai, không hiện tên/nội dung cá nhân (case 5, đã code `strip_identifiers` chặn rò mã D####)
- Case đặc thù domain (④): Cụm chứa 2 sub-ý khác nhau (gia hạn vs mức trừ điểm) → giữ topic trung lập, không tự sinh câu trả lời chung cho cả 2 (case 8)

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
  - **Không đếm nhầm người** (pass/fail): số học viên trong mỗi cụm = số author duy nhất tính lại từ msg_id, không tin số AI tự khai.
  - **Không gộp lố** (pass/fail): 2 chủ đề khác nhau không nằm chung 1 cụm — đối chiếu bằng tay với ground-truth trong `eval/golden_set.md`.
  - **Không bịa nguồn** (pass/fail): mọi câu khẳng định "đã xử lý"/"deadline là X" phải trỏ được về msg_id thật trong input.
  - **Không lộ định danh** (pass/fail): output công khai không chứa mã `D####`.
- Golden set: 19 case đã dựng trong `eval/golden_set.md` (8 case theo 4 lớp × 2, 8 case thường, 3 case hiếm; 15/19 case trích thật từ chatlog) — cần bổ sung ≥1 case nữa cho đủ ≥20 (D phụ trách).
- Quality bar (đề xuất, **cần cả nhóm xác nhận trước khi chốt tại CP4 21:00 18/9**): "Đạt khi ≥80% case về lỗi ①②③④ không vi phạm (không đếm nhầm người, không gộp lố, không bịa nguồn, không lộ định danh), và 100% case ③ (ngoài phạm vi/riêng tư) phải đạt — vì đây là lỗi không được phép xảy ra dù chỉ 1 lần."
- Kết quả các lượt chạy:
  - **Lượt 0 (đã chạy thật, không cần API key)** — lưới an toàn xử lý bằng code (`codebase/test_safety_checks.py`): **8/8 test PASS** — lọc tin bot, lọc tin rác, đếm lại đúng số người duy nhất (D6014 hỏi 2 lần → tính đúng 1 người), che mã định danh, tính đúng mức ưu tiên (Cao/Trung bình/Thấp) theo quy tắc rõ ràng dựa trên số người + danh mục.
  - **Lượt 1 (thử tay bởi C, gọi Gemini thật, 18/9)** — **5/7 (~71%)** đạt chuẩn "gọi AI thật, gộp đúng ngữ nghĩa, hiển thị đầy đủ" (xem `eval/run_log_1.md`). 2 lần chưa đạt: lỗi gọi API (chưa rõ nguyên nhân cụ thể) và code chưa ép schema output rõ ràng nên model thiếu trường hiển thị.
  - **Lượt 2 (chạy đủ 19 case golden set qua `eval/run_eval.py`)** — [CẦN ĐIỀN trước CP4 21:00, để có số đo đầy đủ hơn 7 lần thử tay].

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
