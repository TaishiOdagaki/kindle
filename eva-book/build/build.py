#!/usr/bin/env python3
"""Assemble manuscript/ into an EPUB following chapters.csv order.

Usage:
  python3 build/build.py            # draft build (allows stubs/TODOs)
  python3 build/build.py --release  # release gate: fails if anything is unfinished
"""
import csv, re, sys, pathlib
import pypandoc

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "chapters.csv", newline="")))
release = "--release" in sys.argv

problems = []
parts = []
for r in rows:
    path = ROOT / "manuscript" / r["file"]
    text = path.read_text()
    if release:
        if r["status"] != "final":
            problems.append(f'{r["id"]}: status={r["status"]} (need final)')
        if r["fact_check"] != "done":
            problems.append(f'{r["id"]}: fact_check={r["fact_check"]} (need done)')
        if "TODO" in text:
            problems.append(f'{r["id"]}: contains TODO')
    parts.append(text.strip() + "\n")

if release and problems:
    print("RELEASE BLOCKED:")
    print("\n".join(" - " + p for p in problems))
    sys.exit(1)

out = ROOT / "build" / ("release.epub" if release else "draft.epub")
md = "\n\n".join(parts)
pypandoc.convert_text(
    md, "epub3", format="markdown",
    outputfile=str(out),
    extra_args=["--metadata-file", str(ROOT / "build" / "metadata.yaml"),
                "--split-level=1"],
)
words = len(re.findall(r"\w+", re.sub(r"<!--.*?-->", "", md, flags=re.S)))
print(f"built {out.name}: {len(rows)} chapters, ~{words} words of text")
