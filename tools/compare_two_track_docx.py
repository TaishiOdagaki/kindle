#!/usr/bin/env python3
"""Extract and compare two 500-question DOCX manuscripts by Word bookmarks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from zipfile import ZipFile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
Q_RE = re.compile(r"^Q_(.+)$")
A_RE = re.compile(r"^A_(.+)$")
OPT_RE = re.compile(r"^\s*([1-4])[\.．]\s*(.*)$", re.S)
EXP_RE = re.compile(r"^\s*([1-4])[（(][^）)]*[）)]\s*(.*)$", re.S)
ANS_RE = re.compile(r"正解\s*[：:]\s*([1-4])")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def para_text(p) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()


def bookmark_names(p) -> list[str]:
    key = f"{{{W}}}name"
    return [x.get(key) for x in p.xpath(".//w:bookmarkStart", namespaces=NS) if x.get(key)]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s)).strip()


def join_parts(parts: list[str]) -> str:
    return "\n".join(x for x in parts if x).strip()


def load_paragraphs(path: Path):
    with ZipFile(path) as zf:
        root = etree.fromstring(zf.read("word/document.xml"))
    return root.xpath(".//w:body/w:p", namespaces=NS)


def indexed_blocks(paras, prefix_re):
    starts = []
    for i, p in enumerate(paras):
        for name in bookmark_names(p):
            m = prefix_re.match(name)
            if m:
                starts.append((i, name))
                break
    out = {}
    for pos, (start, name) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(paras)
        out[name] = paras[start:end]
    return out


def parse_question(block) -> dict:
    texts = [para_text(p) for p in block[1:]]
    body = []
    for t in texts:
        if not t:
            continue
        if "解説を見る" in t and "目次に戻る" in t:
            break
        body.append(t)

    stem: list[str] = []
    options: dict[str, list[str]] = {str(i): [] for i in range(1, 5)}
    current = None
    for t in body:
        m = OPT_RE.match(t)
        if m:
            current = m.group(1)
            options[current].append(m.group(2).strip())
        elif current is None:
            stem.append(t)
        else:
            options[current].append(t)
    return {
        "stem_paragraphs": stem,
        "stem": join_parts(stem),
        "case_context": join_parts(stem[:-1]) if len(stem) > 1 else "",
        "options": {k: join_parts(v) for k, v in options.items()},
    }


def parse_answer(block) -> dict:
    texts = [para_text(p) for p in block[1:]]
    body = []
    for t in texts:
        if not t:
            continue
        if "問題に戻る" in t and "目次に戻る" in t:
            break
        body.append(t)
    answer = None
    explanations: dict[str, list[str]] = {str(i): [] for i in range(1, 5)}
    current = None
    preface = []
    for t in body:
        am = ANS_RE.search(t)
        if am and answer is None:
            answer = am.group(1)
            continue
        em = EXP_RE.match(t)
        if em:
            current = em.group(1)
            explanations[current].append(em.group(2).strip())
        elif current is None:
            preface.append(t)
        else:
            explanations[current].append(t)
    return {
        "answer": answer,
        "explanation_preface": join_parts(preface),
        "explanations": {k: join_parts(v) for k, v in explanations.items()},
    }


def extract(path: Path) -> dict:
    paras = load_paragraphs(path)
    q_blocks = indexed_blocks(paras, Q_RE)
    a_blocks = indexed_blocks(paras, A_RE)
    records = {}
    for qname, block in q_blocks.items():
        ident = qname[2:]
        aname = f"A_{ident}"
        rec = {"id": qname}
        rec.update(parse_question(block))
        if aname in a_blocks:
            rec.update(parse_answer(a_blocks[aname]))
        else:
            rec.update({"answer": None, "explanation_preface": "", "explanations": {str(i): "" for i in range(1,5)}})
        records[qname] = rec
    return records


def errors(records: dict) -> list[dict]:
    out = []
    for qid, r in records.items():
        missing_o = [k for k, v in r["options"].items() if not v]
        missing_e = [k for k, v in r["explanations"].items() if not v]
        if missing_o or missing_e or not r["stem"] or not r["answer"]:
            out.append({"id": qid, "missing_options": missing_o, "missing_explanations": missing_e,
                        "missing_stem": not bool(r["stem"]), "missing_answer": not bool(r["answer"])})
    return out


def compare(left: dict, right: dict) -> dict:
    ids = sorted(set(left) | set(right))
    rows = []
    fields = ["stem", "case_context", "answer", "option_1", "option_2", "option_3", "option_4",
              "explanation_1", "explanation_2", "explanation_3", "explanation_4"]
    counts = {f: 0 for f in fields}
    all_equal = 0
    for qid in ids:
        l, r = left.get(qid), right.get(qid)
        if l is None or r is None:
            rows.append({"id": qid, "missing_in": "left" if l is None else "right"})
            continue
        vals_l = {
            "stem": l["stem"], "case_context": l["case_context"], "answer": l["answer"],
            **{f"option_{k}": v for k, v in l["options"].items()},
            **{f"explanation_{k}": v for k, v in l["explanations"].items()},
        }
        vals_r = {
            "stem": r["stem"], "case_context": r["case_context"], "answer": r["answer"],
            **{f"option_{k}": v for k, v in r["options"].items()},
            **{f"explanation_{k}": v for k, v in r["explanations"].items()},
        }
        diffs = {}
        for f in fields:
            if norm(str(vals_l[f] or "")) != norm(str(vals_r[f] or "")):
                counts[f] += 1
                diffs[f] = {"github": vals_l[f], "library": vals_r[f]}
        if not diffs:
            all_equal += 1
        rows.append({"id": qid, "different_fields": list(diffs), "diffs": diffs})
    return {"question_count": len(ids), "all_fields_equal": all_equal,
            "questions_with_any_difference": len(ids) - all_equal,
            "field_difference_counts": counts, "questions": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("github_docx", type=Path)
    ap.add_argument("library_docx", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    left = extract(args.github_docx)
    right = extract(args.library_docx)
    result = {
        "schema": "two-track-full-question-diff-v1",
        "github": {"path": str(args.github_docx), "sha256": sha256(args.github_docx), "count": len(left), "parse_errors": errors(left)},
        "library": {"path": str(args.library_docx), "sha256": sha256(args.library_docx), "count": len(right), "parse_errors": errors(right)},
        "comparison": compare(left, right),
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result["comparison"].items() if k != "questions"}, ensure_ascii=False, indent=2))
    print("github_parse_errors", len(result["github"]["parse_errors"]))
    print("library_parse_errors", len(result["library"]["parse_errors"]))


if __name__ == "__main__":
    main()
