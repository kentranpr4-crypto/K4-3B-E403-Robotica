# Outline slide 6 trang (CP5) — B dựng PDF từ đây

Luật: mỗi slide phải có ≥1 con số / quote có nguồn.

## Slide 1 — User & Job (45")
- Job executor: TA/Learning Coach đọc bản tin cuối ngày trên Discord
- Con số pain: "3 học viên khác nhau hỏi cùng 1 vấn đề trong 79 phút, nhưng bot báo cáo thành 4 dòng riêng — đếm 1 người (D6014) thành 2 vấn đề"
- Nguồn: `k4_daily_reports.md` K4-L3-4 14/9 + `k4_messages.csv`

## Slide 2 — Vì sao chọn tính năng này (45")
- Bảng impact rút gọn (từ spec.md §2): 35 học viên/60 tin liên quan deadline·nộp·hạn (trong 779 tin không-bot) — lớn nhất trong 3 ứng viên đã cân nhắc
- Ứng viên loại 1 dòng: B1 (trả lời logistics) trùng hướng nhóm khác · C (chủ động nhắn học viên) rủi ro an toàn cao

## Slide 3 — Giải pháp & demo live (2')
- Lát cắt 1 câu (spec.md §4)
- Automation: Conditional — vì gộp lố 2 deadline khác nhau gây hậu quả điểm số thật (cost-of-error)
- **Demo trực tiếp:** 1 case chuẩn (cụm Lab2 gộp đúng 3 người) + 1 case chỗ khó (3 loại "deadline" khác nhau không bị gộp nhầm — case §5 lớp ④)

## Slide 4 — Kết quả đo (45")
- Lượt 0 (lưới an toàn, chạy thật): 5/5 test PASS — lọc bot, lọc rác, đếm đúng người, che định danh
- Lượt 1 (AI gộp cụm thật): [CẦN ĐIỀN sau khi C chạy `codebase/cluster_report.py` với API key thật — % qua golden set 19-20 case]
- Đối chiếu quality bar đã chốt ở CP4: [CẦN ĐIỀN]

## Slide 5 — User thật nói gì (45")
- ≥2 quote nguyên văn từ `validation/README.md` (tên/vai) — [CẦN ĐIỀN sau khi test 5 người thật]
- Nếu chưa kịp validation: thay bằng kết quả golden set đạt/không đạt quality bar

## Slide 6 — Nếu có thêm 1 tuần (30")
- Build nút "tách cụm" cho TA tự sửa khi AI gộp sai (G9, đang để dành ở flow.md bước [6])
- Mở rộng golden set lên 30+ case bằng promptfoo
- Bài học lớn nhất: [CẦN ĐIỀN sau demo]
