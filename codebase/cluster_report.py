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

CLUSTER_PROMPT = """Bạn là trợ lý tổng hợp bản tin ngày cho TA một khoá học online.

Nhiệm vụ: đọc danh sách tin nhắn học viên bên dưới, GOM các tin cùng một vấn đề cụ thể thành một cụm.

QUY TẮC BẮT BUỘC:
1. Chỉ gộp khi CHẮC CHẮN cùng một vấn đề cụ thể. Nếu hai tin có thể là hai vấn đề khác nhau dù dùng từ giống nhau (ví dụ hai deadline khác nhau, hai loại lỗi khác nhau) — KHÔNG gộp, tách riêng và đánh dấu "uncertain": true cho từng cụm đó.
2. KHÔNG tự kết luận một vấn đề "đã được xử lý" trừ khi chính trong danh sách tin nhắn này có một tin trả lời rõ ràng cho đúng vấn đề đó.
3. KHÔNG gộp câu hỏi mang tính cá nhân (tra cứu thông tin riêng của một người, ví dụ điểm danh/lịch sử của riêng bạn đó) vào cụm công khai — liệt các msg_id này vào "dropped_msg_ids" với lý do "personal", không tính vào số đếm công khai.
4. Chỉ trả lời bằng JSON đúng schema dưới đây, không thêm chữ nào khác ngoài JSON.

Schema:
{{"clusters": [{{"topic": "tên chủ đề ngắn gọn", "msg_ids": ["M#####", ...], "uncertain": false}}], "dropped_msg_ids": ["M#####"]}}

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
    return CLUSTER_PROMPT.format(messages_block="\n".join(lines))


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

def format_report_line(cluster, id_to_row):
    n = recompute_unique_author_count(cluster, id_to_row)
    tag = " (cần TA xác nhận)" if cluster.get("uncertain") else ""
    sources = ", ".join(cluster["msg_ids"])
    line = f"- {n} học viên đang hỏi về \"{cluster['topic']}\"{tag} (nguồn: {sources})"
    return strip_identifiers(line)


def build_report(csv_path, day=None):
    rows = load_messages(csv_path)
    candidates = filter_candidate_questions(rows, day=day)
    id_to_row = {r["msg_id"]: r for r in rows}

    prompt = build_prompt(candidates)
    raw = call_gemini(prompt)
    parsed = parse_model_json(raw)

    lines = ["Học viên đang hỏi gì"]
    for cluster in parsed.get("clusters", []):
        lines.append(format_report_line(cluster, id_to_row))
    return "\n".join(lines), parsed


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "../data/discord-pack/k4_messages.csv"
    day = sys.argv[2] if len(sys.argv) > 2 else None
    report, raw_parsed = build_report(csv_path, day=day)
    print(report)
