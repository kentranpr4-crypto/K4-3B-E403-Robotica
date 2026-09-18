"""Chạy golden set qua AI thật và tự chấm các case kiểm tra được bằng cấu trúc
(msg_id nằm đúng/sai cụm). Cần GEMINI_API_KEY thật.

Chạy: cd eval && GEMINI_API_KEY=xxx python3 run_eval.py

Lưu ý: KHÔNG lọc theo 1 ngày cụ thể — golden set có message trải trên cả 3 ngày
của pack (12-14/9). Lọc cứng 1 ngày sẽ làm model chưa từng thấy message của case
thuộc ngày khác, dẫn tới báo FAIL sai (model không có lỗi, chỉ là chưa được đưa dữ liệu).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codebase"))

from cluster_report import (
    load_messages,
    filter_candidate_questions,
    build_prompt,
    call_gemini,
    parse_model_json,
    strip_personal_messages,
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "discord-pack", "k4_messages.csv")
DAY = None  # None = chạy trên cả pack, không lọc theo ngày


def msg_cluster(parsed, msg_id):
    for c in parsed.get("clusters", []):
        if msg_id in c["msg_ids"]:
            return c
    return None


def verdict(candidates, parsed, required_msg_ids, check_fn):
    """Trả về PASS/FAIL/N-A. N-A khi msg_id cần cho case này không hề có trong
    dữ liệu đưa vào AI (bị lọc rác/bot, hoặc không thuộc phạm vi ngày) — lúc đó
    không thể kết luận model đúng/sai vì nó chưa từng thấy message đó."""
    candidate_ids = {r["msg_id"] for r in candidates}
    missing = [m for m in required_msg_ids if m not in candidate_ids]
    if missing:
        return "N/A", f"thiếu msg_id trong input (đã bị lọc hoặc không có trong pack): {missing}"
    return ("PASS" if check_fn() else "FAIL"), ""


def run():
    rows = load_messages(CSV_PATH)
    candidates = filter_candidate_questions(rows, day=DAY)
    id_to_row = {r["msg_id"]: r for r in rows}
    prompt = build_prompt(candidates)
    raw = call_gemini(prompt)
    parsed = parse_model_json(raw)
    parsed["clusters"] = strip_personal_messages(parsed.get("clusters", []), id_to_row)  # lưới an toàn thứ 2

    results = []

    v, note = verdict(candidates, parsed, ["M17305"],
                       lambda: msg_cluster(parsed, "M17305") is None)
    results.append(("Case 3 - loại tin mơ hồ M17305", v, note))

    c_lab2 = msg_cluster(parsed, "M88027")
    c_video = msg_cluster(parsed, "M16662")
    v, note = verdict(candidates, parsed, ["M88027", "M16662"],
                       lambda: c_lab2 is None or c_video is None or c_lab2 is not c_video)
    results.append(("Case 4 - không gộp M16662 vào cụm Lab2", v, note))

    v, note = verdict(candidates, parsed, ["M28943"],
                       lambda: msg_cluster(parsed, "M28943") is None)
    results.append(("Case 5 - loại câu hỏi cá nhân M28943", v, note))

    v, note = verdict(candidates, parsed, ["M55443"],
                       lambda: msg_cluster(parsed, "M55443") is not None)
    results.append(("Case 6 - giữ câu hỏi chung M55443", v, note))

    c_team = msg_cluster(parsed, "M19124")
    v, note = verdict(
        candidates, parsed, ["M88027", "M19124", "M16662"],
        lambda: len({id(c) for c in [c_lab2, c_team, c_video] if c is not None})
        == len([c for c in [c_lab2, c_team, c_video] if c is not None]),
    )
    results.append(("Case 7 - không gộp 3 loại deadline khác nhau", v, note))

    v, note = verdict(
        candidates, parsed, ["M88027", "M75012"],
        lambda: msg_cluster(parsed, "M88027") is not None
        and msg_cluster(parsed, "M88027") is msg_cluster(parsed, "M75012"),
    )
    results.append(("Case 8 - giữ chung cụm 2 sub-ý Lab2 (gia hạn vs mức trừ điểm)", v, note))

    print(f"Tổng {len(candidates)} tin đưa vào AI, model trả về {len(parsed.get('clusters', []))} cụm.\n")
    tally = {"PASS": 0, "FAIL": 0, "N/A": 0}
    for name, v, note in results:
        extra = f"  ({note})" if note else ""
        print(f"{v:4}  {name}{extra}")
        tally[v] += 1
    scored = tally["PASS"] + tally["FAIL"]
    print(f"\n{tally['PASS']}/{scored} case có thể chấm tự động đạt "
          f"({tally['N/A']} case N/A vì thiếu dữ liệu — không tính vào %)")

    with open(os.path.join(os.path.dirname(__file__), "run_log_2.md"), "w", encoding="utf-8") as f:
        f.write("# Lượt chạy 2 — golden set (kiểm tự động, không lọc theo ngày)\n\n")
        f.write(f"Tổng tin đưa vào AI: {len(candidates)} · Số cụm AI trả về: {len(parsed.get('clusters', []))}\n\n")
        f.write("| Case | Kết quả | Ghi chú |\n|---|---|---|\n")
        for name, v, note in results:
            f.write(f"| {name} | {v} | {note} |\n")
        f.write(f"\n**{tally['PASS']}/{scored} case tự động đạt** ({tally['N/A']} N/A không tính vào %).\n")
        f.write("\nCác case còn lại trong `golden_set.md` (chất lượng topic label, case thường, case hiếm) cần D chấm tay bằng cách đọc trực tiếp output AI.\n")


if __name__ == "__main__":
    run()
