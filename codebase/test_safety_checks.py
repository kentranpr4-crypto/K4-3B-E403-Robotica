"""Test các lưới an toàn KHÔNG cần gọi AI thật — chạy được ngay, không cần API key.
Phần gộp cụm ngữ nghĩa (cần gọi Gemini) đo riêng trong eval/, sau khi có GEMINI_API_KEY.

Chạy: python3 -m pytest test_safety_checks.py -v
"""
from cluster_report import (
    filter_candidate_questions,
    strip_identifiers,
    recompute_unique_author_count,
    compute_priority,
    strip_personal_messages,
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


def test_priority_high_for_deadline_cluster_with_3_students():
    # Cụm Lab2: 3 học viên duy nhất, danh mục "Nộp bài & deadline" -> phải là Cao
    cluster = {"category": "Nộp bài & deadline"}
    assert compute_priority(cluster, unique_author_count=3) == "Cao"


def test_priority_medium_for_single_deadline_question():
    cluster = {"category": "Nộp bài & deadline"}
    assert compute_priority(cluster, unique_author_count=1) == "Trung bình"


def test_priority_low_for_single_non_deadline_question():
    cluster = {"category": "Kiến thức học thuật"}
    assert compute_priority(cluster, unique_author_count=1) == "Thấp"


def test_strip_personal_messages_catches_model_mistake():
    # Case thật đo được ở eval/run_log_2.md: model lỡ đưa M28943 (câu hỏi cá nhân
    # về điểm danh của chính người hỏi) vào cụm công khai dù prompt đã cấm.
    id_to_row = {
        "M28943": {"content": "mail về IT về kiểm tra các lượt điểm danh của mình ạ"},
        "M55443": {"content": "check điểm danh như nào"},  # câu hỏi chung -> phải giữ
    }
    clusters = [{"topic": "điểm danh", "msg_ids": ["M28943", "M55443"]}]
    cleaned = strip_personal_messages(clusters, id_to_row)
    assert cleaned[0]["msg_ids"] == ["M55443"], "Phải loại M28943 (cá nhân) và giữ M55443 (câu hỏi chung)"


def test_strip_personal_messages_drops_empty_cluster():
    id_to_row = {"M28943": {"content": "kiểm tra điểm danh của mình giúp em với"}}
    clusters = [{"topic": "điểm danh cá nhân", "msg_ids": ["M28943"]}]
    cleaned = strip_personal_messages(clusters, id_to_row)
    assert cleaned == [], "Cụm chỉ toàn tin cá nhân thì phải bị loại hết, không còn cụm rỗng"


def test_strip_identifiers_removes_author_codes():
    leaked = "3 học viên D3115, D6014, D7496 đang hỏi về nộp Lab2 muộn"
    cleaned = strip_identifiers(leaked)
    assert "D3115" not in cleaned
    assert "D6014" not in cleaned
    assert "D7496" not in cleaned
