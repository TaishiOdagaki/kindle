#!/usr/bin/env python3
"""Assemble manuscript/ into an EPUB following chapters.csv order.

Usage:
  python3 build/build.py                 # Japanese, all volumes in one file (editing copy)
  python3 build/build.py --vol=1         # Volume 1 only (also --vol=2, --vol=3)
  python3 build/build.py --lang=en       # English
  python3 build/build.py --tier-a        # only Tier A chapters (first edition)
  python3 build/build.py --vol=1 --release   # release gate: fails if anything is unfinished
"""
import re, sys, pathlib
import pypandoc
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib

ROOT = lib.ROOT
args = sys.argv[1:]
release = "--release" in args
lang = "en" if "--lang=en" in args else "ja"
tier_a = "--tier-a" in args
vol = next((a.split("=")[1] for a in args if a.startswith("--vol=")), "all")

rows = lib.load_rows()
sel = [r for r in rows if lib.in_volume(r, vol) and (not tier_a or r["tier"] == "A")]

problems, parts = [], []
for r in sel:
    text = (ROOT / "manuscript" / lang / r["file"]).read_text()
    if release:
        st = r["status"] if lang == "ja" else r["status_en"]
        if st != "final": problems.append(f'{r["id"]}: status={st} (need final)')
        if r["fact_check"] != "done": problems.append(f'{r["id"]}: fact_check={r["fact_check"]} (need done)')
        if "TODO" in text: problems.append(f'{r["id"]}: contains TODO')
        if "[[CHECK" in text: problems.append(f'{r["id"]}: {text.count("[[CHECK")} unresolved [[CHECK]] marks')
    text = lib.apply_volume_fences(text, vol)
    text = lib.resolve_refs(text, rows, vol)
    left = re.findall(r"\{\{[^}]+\}\}", text)
    if left: problems.append(f'{r["id"]}: unresolved reference tokens {left[:3]}')
    parts.append(text.strip() + "\n")

if problems and (release or any("unresolved reference" in p for p in problems)):
    print("BUILD BLOCKED:" if not release else "RELEASE BLOCKED:")
    print("\n".join(" - " + p for p in problems))
    sys.exit(1)

tag = ("release" if release else "draft") + ("-tier-a" if tier_a else "") + f"-v{vol}" + f"-{lang}"
meta = ROOT / "build" / f"metadata.{lang}.vol{vol}.yaml"
if not meta.exists(): meta = ROOT / "build" / f"metadata.{lang}.yaml"
out = ROOT / "build" / f"{tag}.epub"
md = "\n\n".join(parts)
pypandoc.convert_text(md, "epub3", format="markdown", outputfile=str(out),
                      extra_args=["--metadata-file", str(meta), "--split-level=1"])
clean = re.sub(r"<!--.*?-->", "", md, flags=re.S)
size = len(re.sub(r"[\s#|>*\-]", "", clean)) if lang == "ja" else len(re.findall(r"\w+", clean))
print(f"built {out.name}: {len(sel)} chapters, ~{size} {'chars' if lang == 'ja' else 'words'}")
