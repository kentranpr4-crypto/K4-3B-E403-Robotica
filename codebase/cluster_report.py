"""Gộp cụm ngữ nghĩa các câu hỏi trùng ý cho bản tin ngày TA (Track B2).

Chạy: GEMINI_API_KEY=xxx python3 cluster_report.py <path_to_k4_messages.csv> [YYYY-MM-DD]
Lấy key free tại https://aistudio.google.com/apikey
"""
import csv
import json
import os
import re
import sys

JUNK_RE = re.compile(r"^[\W\d]{0,3}$")
AUTHOR_LEAK_RE = re.compile(r"\bD\d{3,6}\b")

# Lưới an toàn THỨ 2 cho câu hỏi cá nhân, độc lập với prompt — vì đây là lớp lỗi
# nghiêm trọng nhất (lộ thông tin cá nhân), không được phép chỉ dựa vào AI tự giác
# tuân theo instruction. Thực tế đo được: M28943 ("...điểm danh của mình...") đã
# lọt vào cụm công khai dù prompt đã yêu cầu loại trừ (xem eval/run_log_2.md).
PERSONAL_MARKER_RE = re.compile(
    r"(của\s+(tôi|mình|em|bạn ấy)\b.{0,20}(điểm danh|lịch sử|log|tài khoản|hồ sơ)"
    r"|(điểm danh|lịch sử|log|tài khoản|hồ sơ).{0,20}của\s+(tôi|mình|em|bạn ấy)\b)",
    re.IGNORECASE,
)

CATEGORIES = [
    "Nộp bài & deadline",
    "Thông tin chung & logistics",
    "Kiến thức học thuật",
    "Kỹ thuật & công cụ",
    "Khác",
]

CLUSTER_PROMPT = """Bạn là trợ lý tổng hợp bản tin ngày cho TA một khoá học online.

Nhiệm vụ: đọc danh sách tin nhắn học viên bên dưới, GOM các tin cùng một vấn đề cụ thể thành một cụm,
và gắn cho mỗi cụm đúng MỘT danh mục trong danh sách sau: {categories}.

QUY TẮC BẮT BUỘC:
1. Chỉ gộp khi CHẮC CHẮN cùng một vấn đề cụ thể. Nếu hai tin có thể là hai vấn đề khác nhau dù dùng từ giống nhau (ví dụ hai deadline khác nhau, hai loại lỗi khác nhau) — KHÔNG gộp, tách riêng và đánh dấu "uncertain": true cho từng cụm đó.
2. KHÔNG tự kết luận một vấn đề "đã được xử lý" trừ khi chính trong danh sách tin nhắn này có một tin trả lời rõ ràng cho đúng vấn đề đó.
3. KHÔNG gộp câu hỏi mang tính cá nhân (tra cứu thông tin riêng của một người, ví dụ điểm danh/lịch sử của riêng bạn đó) vào cụm công khai — liệt các msg_id này vào "dropped_msg_ids" với lý do "personal", không tính vào số đếm công khai.
4. "category" chỉ được chọn đúng 1 trong danh sách đã cho, không tự bịa danh mục mới.
5. KHÔNG tự chấm mức độ khẩn cấp/ưu tiên — việc đó hệ thống tính riêng từ dữ liệu thật, bạn chỉ cần trả về category và danh sách msg_ids.
6. Chỉ trả lời bằng JSON đúng schema dưới đây, không thêm chữ nào khác ngoài JSON.

Schema:
{{"clusters": [{{"topic": "tên chủ đề ngắn gọn", "category": "một trong danh sách danh mục", "msg_ids": ["M#####", ...], "uncertain": false}}], "dropped_msg_ids": ["M#####"]}}

Tin nhắn cần xử lý (định dạng "msg_id: nội dung"):
{messages_block}
"""


def load_messages(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_candidate_questions(rows, day=None):
    """Loại tin của bot và tin rác trước khi đưa cho AI — giảm chi phí và tránh lớp lỗi
    'tin của bot bị đếm là câu hỏi' (hard test track B2)."""
    out = []
    for r in rows:
        if r["is_bot"] == "True":
            continue
        content = r["content"].strip()
        if len(content) < 4 or JUNK_RE.match(content):
            continue
        if day and not r["created_at_vn"].startswith(day):
            continue
        out.append(r)
    return out


def strip_identifiers(text):
    """Lưới an toàn cuối: xoá mọi mã D#### còn sót trong text công khai."""
    return AUTHOR_LEAK_RE.sub("[ẩn danh]", text)


def build_prompt(rows):
    lines = [f"{r['msg_id']}: {r['content'][:300]}" for r in rows]
    return CLUSTER_PROMPT.format(
        categories=", ".join(CATEGORIES),
        messages_block="\n".join(lines),
    )


def call_gemini(prompt, model_name="gemini-1.5-flash"):
    import google.generativeai as genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Thiếu GEMINI_API_KEY — export GEMINI_API_KEY=... trước khi chạy")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt)
    return resp.text


def parse_model_json(raw_text):
    cleaned = raw_text.strip().strip("`")
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:]
    return json.loads(cleaned)


def recompute_unique_author_count(cluster, id_to_row):
    """KHÔNG tin số đếm do model tự khai — luôn tính lại từ dữ liệu gốc.
    Đây là lưới an toàn chặn lớp lỗi 'đếm nhầm người thành đếm tin nhắn'."""
    authors = {id_to_row[mid]["author"] for mid in cluster["msg_ids"] if mid in id_to_row}
    return len(authors)


def compute_priority(cluster, unique_author_count):
    """Mức ưu tiên tính bằng code từ số liệu thật — KHÔNG để AI tự chấm khẩn cấp,
    vì đó là kết luận có hậu quả (TA xử lý cái gì trước) mà không có căn cứ kiểm chứng
    được nếu để AI tự bịa (đúng lớp lỗi ① nguồn sự thật).

    Quy tắc (giải thích được — G11):
    - Cao: >=5 học viên bất kể danh mục, HOẶC >=3 học viên và thuộc "Nộp bài & deadline"
      (sai deadline gây hậu quả điểm số trực tiếp — cost-of-error cao).
    - Trung bình: >=2 học viên, hoặc 1 học viên nhưng thuộc "Nộp bài & deadline".
    - Thấp: còn lại.
    """
    category = cluster.get("category", "Khác")
    if unique_author_count >= 5 or (unique_author_count >= 3 and category == "Nộp bài & deadline"):
        return "Cao"
    if unique_author_count >= 2 or category == "Nộp bài & deadline":
        return "Trung bình"
    return "Thấp"


PRIORITY_ICON = {"Cao": "🔴", "Trung bình": "🟡", "Thấp": "🟢"}


def format_report_line(cluster, id_to_row):
    n = recompute_unique_author_count(cluster, id_to_row)
    category = cluster.get("category", "Khác")
    if category not in CATEGORIES:
        category = "Khác"  # lưới an toàn: model bịa danh mục ngoài danh sách thì gạt về "Khác"
    priority = compute_priority(cluster, n)
    tag = " (cần TA xác nhận)" if cluster.get("uncertain") else ""
    sources = ", ".join(cluster["msg_ids"])
    icon = PRIORITY_ICON[priority]
    line = (
        f"- {icon} [{category}] {n} học viên đang hỏi về \"{cluster['topic']}\""
        f"{tag} — ưu tiên: {priority} (nguồn: {sources})"
    )
    return strip_identifiers(line)


def strip_personal_messages(clusters, id_to_row):
    """Lưới an toàn thứ 2: nếu AI lỡ không loại câu hỏi cá nhân theo đúng chỉ dẫn
    trong prompt, code tự rà lại nội dung gốc bằng heuristic từ khoá và loại khỏi
    cụm công khai. Cụm rỗng sau khi loại thì bỏ luôn cụm đó."""
    cleaned = []
    for c in clusters:
        kept_ids = [
            mid for mid in c["msg_ids"]
            if not (mid in id_to_row and PERSONAL_MARKER_RE.search(id_to_row[mid]["content"]))
        ]
        if kept_ids:
            cleaned.append({**c, "msg_ids": kept_ids})
    return cleaned


def build_report(csv_path, day=None):
    rows = load_messages(csv_path)
    candidates = filter_candidate_questions(rows, day=day)
    id_to_row = {r["msg_id"]: r for r in rows}

    prompt = build_prompt(candidates)
    raw = call_gemini(prompt)
    parsed = parse_model_json(raw)
    parsed["clusters"] = strip_personal_messages(parsed.get("clusters", []), id_to_row)

    lines = ["Học viên đang hỏi gì"]
    for cluster in parsed.get("clusters", []):
        lines.append(format_report_line(cluster, id_to_row))
    return "\n".join(lines), parsed


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "../data/discord-pack/k4_messages.csv"
    day = sys.argv[2] if len(sys.argv) > 2 else None
    report, raw_parsed = build_report(csv_path, day=day)
    print(report)
