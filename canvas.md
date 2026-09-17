# Canvas 7 dòng (CP1)

| # | Dòng | Nội dung |
|---|---|---|
| 1 | Track + đề | B · B2 — Bản tin ngày cho TA: gom nhóm ngữ nghĩa các câu hỏi trùng ý |
| 2 | Job executor | TA/Learning Coach đọc bản tin cuối ngày trên Discord để biết học viên đang vướng vấn đề gì cần can thiệp |
| 3 | Pain | TA đọc bản tin "Học viên đang hỏi gì" thấy nhiều gạch đầu dòng tưởng là nhiều vấn đề/nhiều người khác nhau, trong khi thực chất chỉ vài học viên hỏi đi hỏi lại hoặc diễn đạt khác nhau về cùng một vấn đề, nên đánh giá sai độ nóng và không biết vấn đề đã có ai trả lời gợi ý chưa |
| 4 | Bằng chứng đầu | Đêm 12→13/9, 3 học viên khác nhau (`D3115`, `D6014`, `D7496`) hỏi cùng chủ đề "nộp Lab2 muộn" trong 79 phút (00:08–01:27), trong đó `D6014` hỏi 2 lần liên tiếp cùng phút 00:15 (`M20574`, `M75012`). Bot báo cáo (`k4_daily_reports.md`, K4-L3-4 14/9) thành 4 gạch đầu dòng riêng trong "Học viên đang hỏi gì", đếm `D6014` như 2 vấn đề khác nhau, và tách câu trả lời gợi ý của `D7593` (`M24366`) sang mục khác thay vì gắn liền |
| 5 | Lát cắt MỘT CÂU | Một TA đọc bản tin cuối ngày · AI gom các câu hỏi trùng ý thành một dòng đếm theo **số học viên duy nhất** kèm link tin nguồn · TA biết đúng có bao nhiêu người thực sự đang vướng một vấn đề và đã được ai trả lời chưa |
| 6 | AI tự làm đến đâu | *Có điều kiện (Conditional):* tự gộp khi hai tin cùng chủ đề rõ ràng; **không tự gộp** khi có thể là hai vấn đề khác nhau (vd hai deadline khác nhau) — giữ tách và gắn cờ "cần TA xác nhận". Lý do: gộp lố khiến TA trả lời sai thông tin cho đúng người, hậu quả domain thật. **Willing users:** Mai Tiến Huy (học viên K4), Lê Việt Hoàng (học viên K4), Hoàng Ngọc Đức (học viên K4) |
| 7 | Phân công | Nguyễn Thái Lương (2A202602932) — A: mining evidence, đếm + mã tin · Trần Cao Quốc Định (2A202602939) — B: spec, đội trưởng nộp form · Nguyễn Xuân Trường (2A202602761) — C: build, gọi AI thật · Nguyễn Mạnh Tiến (2A202602506) — D: golden set, đo lường |
