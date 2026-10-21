#!/usr/bin/env python3
"""Compare two problem-book DOCX files by stable question bookmark IDs.

This is a read-only comparison utility.  It records semantic fields parsed by
tools/quiz_audit.py and package-level hashes without modifying either DOCX.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from quiz_audit import audit


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def package_hashes(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as zf:
        return {name: hashlib.sha256(zf.read(name)).hexdigest() for name in zf.namelist()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("current", type=Path)
    ap.add_argument("other", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--current-label", default="audit branch work DOCX")
    ap.add_argument("--other-label", default="Library education-history DOCX")
    args = ap.parse_args()

    current_issues, current_q, current_a = audit(str(args.current))
    other_issues, other_q, other_a = audit(str(args.other))
    ids = sorted(set(current_q) | set(other_q))
    diffs: dict[str, list[str]] = {}
    field_counts: dict[str, int] = {}

    def add(qid: str, field: str, before: object, after: object) -> None:
        # The comparison is full-text, but the evidence file records compact
        # field names instead of duplicating both entire 500-question books.
        diffs.setdefault(qid, []).append(field)
        field_counts[field] = field_counts.get(field, 0) + 1

    for qid in ids:
        cq, oq = current_q.get(qid), other_q.get(qid)
        aid = "A_" + qid[2:]
        ca, oa = current_a.get(aid), other_a.get(aid)
        if cq is None or oq is None:
            add(qid, "question_presence", cq is not None, oq is not None)
            continue
        if cq["stem"] != oq["stem"]:
            add(qid, "stem", cq["stem"], oq["stem"])
        for i in range(4):
            cv = cq["opts"][i] if i < len(cq["opts"]) else None
            ov = oq["opts"][i] if i < len(oq["opts"]) else None
            if cv != ov:
                add(qid, f"option_{i + 1}", cv, ov)
        if ca is None or oa is None:
            add(qid, "answer_presence", ca is not None, oa is not None)
            continue
        if ca["ans"] != oa["ans"]:
            add(qid, "answer", ca["ans"], oa["ans"])
        for i in range(4):
            cv = ca["txt"][i] if i < len(ca["txt"]) else None
            ov = oa["txt"][i] if i < len(oa["txt"]) else None
            if cv != ov:
                add(qid, f"explanation_{i + 1}", cv, ov)

    cp, op = package_hashes(args.current), package_hashes(args.other)
    package_names = sorted(set(cp) | set(op))
    package_diffs = [name for name in package_names if cp.get(name) != op.get(name)]
    result = {
        "comparison_kind": "read_only_full_question_id_field_diff",
        "direction_note": "current is the dedicated audit branch; other is the Library lineage. A difference is not an adoption decision.",
        "current": {
            "label": args.current_label,
            "file_name": args.current.name,
            "sha256": sha256(args.current),
            "size_bytes": args.current.stat().st_size,
            "questions": len(current_q),
            "answers": len(current_a),
            "machine_issue_count": len(current_issues),
        },
        "other": {
            "label": args.other_label,
            "file_name": args.other.name,
            "sha256": sha256(args.other),
            "size_bytes": args.other.stat().st_size,
            "questions": len(other_q),
            "answers": len(other_a),
            "machine_issue_count": len(other_issues),
        },
        "id_set": {
            "union": len(ids),
            "only_current": sorted(set(current_q) - set(other_q)),
            "only_other": sorted(set(other_q) - set(current_q)),
            "unchanged_question_ids": [qid for qid in ids if qid not in diffs],
            "changed_question_ids": list(diffs),
            "changed_question_count": len(diffs),
        },
        "field_difference_counts": dict(sorted(field_counts.items())),
        "package": {
            "current_parts": len(cp),
            "other_parts": len(op),
            "changed_or_missing_parts": package_diffs,
        },
        "question_differences": diffs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "current_sha256": result["current"]["sha256"],
        "other_sha256": result["other"]["sha256"],
        "changed_question_count": len(diffs),
        "unchanged_question_count": len(ids) - len(diffs),
        "field_difference_counts": result["field_difference_counts"],
        "package_changed_or_missing_parts": package_diffs,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
