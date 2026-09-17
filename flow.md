# CP2 — Sơ đồ luồng: Bản tin ngày gộp cụm cho TA

## Luồng chính (TA journey)

```
[0] Cuối ngày, bot quét toàn bộ tin nhắn public trong ngày
        |
        v
[1] Lọc bỏ: tin của bot (is_bot=True), tin không phải câu hỏi
    (chào hỏi, lời khuyên/trả lời của học viên khác, tin rỗng)
        |
        v
[2] AI gom các câu hỏi còn lại theo chủ đề ngữ nghĩa
    -> mỗi cụm giữ: chủ đề, số tác giả DUY NHẤT, danh sách msg_id nguồn
        |
        v
[3] Với mỗi cụm, AI tự hỏi "có chắc cùng chủ đề không?"
        |
        +-- CHẮC (happy path) --------> xuất 1 dòng:
        |                               "N học viên đang hỏi về X" + link nguồn
        |
        +-- KHÔNG CHẮC (low-confidence) -> KHÔNG gộp liều,
                                            tách riêng + gắn nhãn
                                            "có thể liên quan - cần TA xác nhận"
        |
        v
[4] Bot đăng bản tin lên kênh (giữ nguyên format hiện tại,
    chỉ đổi phần "Học viên đang hỏi gì")
        |
        v
[5] TA đọc bản tin -> thấy dòng đã gộp -> bấm link xem tin gốc
    -> biết ngay 1 vấn đề có bao nhiêu người thật đang vướng
        |
        v
[6] (Correction, làm ở bản sau) TA thấy cụm gộp sai
    -> có nút "tách cụm này" để báo AI gộp nhầm
```

## Mock trước/sau — dùng case thật đã có trong `canvas.md`

**TRƯỚC (bot hiện tại — trích `data/discord-pack/k4_daily_reports.md`, K4-L3-4 14/9):**

```
Học viên đang hỏi gì
• Học viên hỏi có được gia hạn thời gian nộp Lab2 vì lỡ nộp muộn 1 phút... — [HV]
• Học viên thắc mắc về việc nộp lab muộn sẽ bị trừ bao nhiêu điểm... — [HV]
• Học viên hỏi về quy định nộp lab muộn sau 23h59... — [HV]
• Học viên hỏi nếu nộp codelab đúng hạn nhưng commit lỗi... — [HV]
```
-> TA đọc thấy **4 vấn đề khác nhau**, không biết đây thực chất là 3 người hỏi về 1 chủ đề.

**SAU (bản gộp cụm đề xuất):**

```
Học viên đang hỏi gì
• 3 học viên đang hỏi về "nộp Lab2 muộn / gia hạn deadline"
  (nguồn: M88027, M20574, M75012, M40677)
```
-> TA thấy ngay: 1 vấn đề, 3 người, bấm vào nguồn để xử lý theo đúng số người thật.

## Trạng thái build hiện tại

Sketch — mock tĩnh bằng dữ liệu thật, chưa gọi AI. CP3 sẽ thay bước [2]-[3] bằng lời gọi AI thật (Gemini) chạy trên dữ liệu `k4_messages.csv`.
