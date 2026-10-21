#!/usr/bin/env python3
"""Carry all explicit warning dispositions forward after appendix-only batch 212."""
import hashlib
import json
from pathlib import Path

import quiz_audit as qa

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit/v9"
DOCX = OUT / "登録日本語教員試験決定版問題集_v9_監査作業中.docx"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    old_path = OUT / "evidence/machine_clearance_checkpoint211.json"
    old = json.loads(old_path.read_text())
    issues, questions, answers = qa.audit(str(DOCX))
    raw = [list(i) for i in issues]
    assert len(questions) == len(answers) == 500
    assert raw == old["raw_issues"]
    assert len(old["dispositions"]) == 159
    assert old["undisposed_issues"] == []
    current = dict(old)
    current.update({
        "review_date": "2026-10-21",
        "docx_sha256": digest(DOCX),
        "inherited_dispositions_from": "evidence/machine_clearance_checkpoint211.json",
        "inherited_dispositions_file_sha256": digest(old_path),
        "revalidation": "第212バッチは出題範囲対応表の表題と第4章欄のみを変更。500問・500解答は不変で、生警告159件を第211チェックポイントと直接比較して全件同一。既存159処置の対象文脈は不変。",
        "manuscript_unchanged_this_batch": False,
        "question_answer_content_unchanged_this_batch": True,
        "appendix_only_changes": True,
        "changed_pages_visual_qa_completed": True,
        "changed_pages": [347],
        "adjacent_pages_checked": [346, 348],
        "rendered_pages": 351,
        "final_machine_inspection_after_remaining_edits_completed": False,
        "full_visual_qa_completed": False,
        "release_ready": False,
        "limitation": "現稿の159警告は全て個別処置済み。残る改頁編集後に最終機械検査を再実行し、全351頁を直接画像確認するまで出版不可。",
    })
    target = OUT / "evidence/machine_clearance_checkpoint212.json"
    target.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "docx_sha256": current["docx_sha256"],
        "raw_warning_count": len(raw),
        "disposed_warning_count": len(current["dispositions"]),
        "undisposed_warning_count": len(current["undisposed_issues"]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
