"""Chạy golden set qua AI thật và tự chấm các case kiểm tra được bằng cấu trúc
(msg_id nằm đúng/sai cụm). Cần GEMINI_API_KEY thật.

Chạy: cd eval && GEMINI_API_KEY=xxx python3 run_eval.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codebase"))

from cluster_report import load_messages, filter_candidate_questions, build_prompt, call_gemini, parse_model_json

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "discord-pack", "k4_messages.csv")
DAY = "2026-09-13"


def msg_cluster(parsed, msg_id):
    for c in parsed.get("clusters", []):
        if msg_id in c["msg_ids"]:
            return c
    return None


def run():
    rows = load_messages(CSV_PATH)
    candidates = filter_candidate_questions(rows, day=DAY)
    prompt = build_prompt(candidates)
    raw = call_gemini(prompt)
    parsed = parse_model_json(raw)

    results = []

    # Case 3: M17305 ("1") không được nằm trong cụm nào
    results.append(("Case 3 - loại tin mơ hồ M17305", msg_cluster(parsed, "M17305") is None))

    # Case 4: M16662 không được gộp chung cụm với M88027 (Lab2)
    c_lab2 = msg_cluster(parsed, "M88027")
    c_video = msg_cluster(parsed, "M16662")
    results.append(("Case 4 - không gộp M16662 vào cụm Lab2", c_lab2 is None or c_video is None or c_lab2 is not c_video))

    # Case 5: M28943 (câu hỏi cá nhân) không xuất hiện trong bất kỳ cụm nào
    results.append(("Case 5 - loại câu hỏi cá nhân M28943", msg_cluster(parsed, "M28943") is None))

    # Case 6: M55443 (câu hỏi chung) PHẢI xuất hiện trong 1 cụm nào đó
    results.append(("Case 6 - giữ câu hỏi chung M55443", msg_cluster(parsed, "M55443") is not None))

    # Case 7: 3 loại deadline khác nhau (Lab2 / ghép đội M19124 / feedback video M16662) không chung 1 cụm
    c_team = msg_cluster(parsed, "M19124")
    triple_distinct = len({id(c) for c in [c_lab2, c_team, c_video] if c is not None}) == len(
        [c for c in [c_lab2, c_team, c_video] if c is not None]
    )
    results.append(("Case 7 - không gộp 3 loại deadline khác nhau", triple_distinct))

    print(f"Tổng {len(candidates)} tin đưa vào AI, model trả về {len(parsed.get('clusters', []))} cụm.\n")
    passed = 0
    for name, ok in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        passed += int(ok)
    print(f"\n{passed}/{len(results)} case kiểm tra tự động đạt (còn lại chấm tay theo eval/golden_set.md)")

    with open(os.path.join(os.path.dirname(__file__), "run_log_1.md"), "w", encoding="utf-8") as f:
        f.write("# Lượt chạy 1 — kết quả thật\n\n")
        f.write(f"Tổng tin đưa vào AI: {len(candidates)} · Số cụm AI trả về: {len(parsed.get('clusters', []))}\n\n")
        f.write("| Case | Kết quả |\n|---|---|\n")
        for name, ok in results:
            f.write(f"| {name} | {'PASS' if ok else 'FAIL'} |\n")
        f.write(f"\n**{passed}/{len(results)} case tự động đạt.**\n")
        f.write("\nCác case còn lại trong `golden_set.md` (chất lượng topic label, câu hỏi thường, case hiếm) cần D chấm tay.\n")


if __name__ == "__main__":
    run()
