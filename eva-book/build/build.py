#!/usr/bin/env python3
"""Assemble manuscript/ into an EPUB following chapters.csv order.

Usage:
  python3 build/build.py            # draft build (allows stubs/TODOs)
  python3 build/build.py --release  # release gate: fails if anything is unfinished
  python3 build/build.py --tier-a   # only Tier A chapters (first edition)
  python3 build/build.py --lang=en  # English edition (default: ja, the primary text)
"""
import csv, re, sys, pathlib
import pypandoc

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "chapters.csv", newline="")))
release = "--release" in sys.argv
lang = "en" if "--lang=en" in sys.argv else "ja"
tier = "A" if "--tier-a" in sys.argv else None
if tier:
    rows = [r for r in rows if r["tier"] == "A"]

problems = []
parts = []
for r in rows:
    path = ROOT / "manuscript" / lang / r["file"]
    text = path.read_text()
    if release:
        st = r["status"] if lang == "ja" else r["status_en"]
        if st != "final":
            problems.append(f'{r["id"]}: status={st} (need final)')
        if r["fact_check"] != "done":
            problems.append(f'{r["id"]}: fact_check={r["fact_check"]} (need done)')
        if "TODO" in text:
            problems.append(f'{r["id"]}: contains TODO')
        n_chk = text.count("[[CHECK")
        if n_chk:
            problems.append(f'{r["id"]}: {n_chk} unresolved [[CHECK]] marks')
    parts.append(text.strip() + "\n")

if release and problems:
    print("RELEASE BLOCKED:")
    print("\n".join(" - " + p for p in problems))
    sys.exit(1)

out = ROOT / "build" / (("release" if release else "draft") + ("-tier-a" if tier else "") + f"-{lang}.epub")
md = "\n\n".join(parts)
pypandoc.convert_text(
    md, "epub3", format="markdown",
    outputfile=str(out),
    extra_args=["--metadata-file", str(ROOT / "build" / f"metadata.{lang}.yaml"),
                "--split-level=1"],
)
clean = re.sub(r"<!--.*?-->", "", md, flags=re.S)
size = len(re.sub(r"[\s#|>*\-]", "", clean)) if lang == "ja" else len(re.findall(r"\w+", clean))
print(f"built {out.name}: {len(rows)} chapters, ~{size} {'chars' if lang == 'ja' else 'words'} of text")
