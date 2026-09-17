"""Test các lưới an toàn KHÔNG cần gọi AI thật — chạy được ngay, không cần API key.
Phần gộp cụm ngữ nghĩa (cần gọi Gemini) đo riêng trong eval/, sau khi có GEMINI_API_KEY.

Chạy: python3 -m pytest test_safety_checks.py -v
"""
from cluster_report import (
    filter_candidate_questions,
    strip_identifiers,
    recompute_unique_author_count,
)

ROWS = [
    {"msg_id": "M88027", "author": "D3115", "is_bot": "False", "created_at_vn": "2026-09-13 00:08",
     "content": "cho em hỏi Lab2 có được extend thời gian submit thêm không v ạ? Em lỡ nộp muộn 1 phút không submit bài được ạ"},
    {"msg_id": "M20574", "author": "D6014", "is_bot": "False", "created_at_vn": "2026-09-13 00:15",
     "content": "[@BOT] muộn sau 23h59"},
    {"msg_id": "M75012", "author": "D6014", "is_bot": "False", "created_at_vn": "2026-09-13 00:15",
     "content": "[@BOT] nộp lab muộn trừ bao nhiêu điểm"},
    {"msg_id": "M40677", "author": "D7496", "is_bot": "False", "created_at_vn": "2026-09-13 01:27",
     "content": "[@BOT] tôi nộp codelab trên vlearn đúng giờ deadline nhưng commit trên máy bị lỗi thì có tính đúng hạn không?"},
    {"msg_id": "M24366", "author": "D7593", "is_bot": "False", "created_at_vn": "2026-09-13 00:21",
     "content": "[HV] với [HV] chịu khó vào chỗ vlearn-support gửi ticket nhé"},
    {"msg_id": "M_BOT1", "author": "BOT", "is_bot": "True", "created_at_vn": "2026-09-13 00:20",
     "content": "Cảm ơn bạn đã hỏi, mình sẽ chuyển cho TA hỗ trợ nhé"},
    {"msg_id": "M17305", "author": "D6014", "is_bot": "False", "created_at_vn": "2026-09-13 00:16",
     "content": "1"},
    {"msg_id": "M08376", "author": "D6243", "is_bot": "False", "created_at_vn": "2026-09-13 08:55",
     "content": "."},
]
ID_TO_ROW = {r["msg_id"]: r for r in ROWS}


def test_filters_out_bot_messages():
    out = filter_candidate_questions(ROWS)
    ids = {r["msg_id"] for r in out}
    assert "M_BOT1" not in ids


def test_filters_out_junk_messages():
    out = filter_candidate_questions(ROWS)
    ids = {r["msg_id"] for r in out}
    assert "M17305" not in ids
    assert "M08376" not in ids


def test_keeps_real_questions():
    out = filter_candidate_questions(ROWS)
    ids = {r["msg_id"] for r in out}
    for mid in ["M88027", "M20574", "M75012", "M40677", "M24366"]:
        assert mid in ids


def test_recompute_counts_dedups_repeat_asker():
    # D6014 hỏi 2 lần (M20574, M75012) -> phải tính là 1 người, không phải 2
    cluster = {"topic": "nộp Lab2 muộn", "msg_ids": ["M88027", "M20574", "M75012", "M40677"]}
    n = recompute_unique_author_count(cluster, ID_TO_ROW)
    assert n == 3, f"Kỳ vọng 3 học viên duy nhất (D3115,D6014,D7496), model/code trả về {n}"


def test_strip_identifiers_removes_author_codes():
    leaked = "3 học viên D3115, D6014, D7496 đang hỏi về nộp Lab2 muộn"
    cleaned = strip_identifiers(leaked)
    assert "D3115" not in cleaned
    assert "D6014" not in cleaned
    assert "D7496" not in cleaned
