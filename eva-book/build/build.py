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
import lib, figs, design, cover

ROOT = lib.ROOT
args = sys.argv[1:]
release = "--release" in args
lang = "en" if "--lang=en" in args else "ja"
tier_a = "--tier-a" in args
vol = next((a.split("=")[1] for a in args if a.startswith("--vol=")), "all")

rows = lib.load_rows()
figreg = lib.load_figs()
nums = lib.chapter_numbers(rows, vol)
figs.render(lang)
cover.OUT.mkdir(parents=True, exist_ok=True); cover.render(lang)
used_figs = set()
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
        if "[[著者の記憶" in text: problems.append(f'{r["id"]}: {text.count("[[著者の記憶")} unfilled [[著者の記憶]] slots (author must write these)')
    text = lib.apply_volume_fences(text, vol)
    text = lib.resolve_refs(text, rows, vol)
    used_figs |= set(re.findall(r"\{\{fig:([\w\-]+)\}\}", text))
    vcol = vol if vol != "all" else lib.home_volume(rows, r["id"])
    text = lib.resolve_figs(text, r, nums, lang, figreg, problems, vcol)
    left = re.findall(r"\{\{[^}]+\}\}", text)
    if left: problems.append(f'{r["id"]}: unresolved reference tokens {left[:3]}')
    parts.append(text.strip() + "\n")

if release:
    for fid in sorted(used_figs):
        if figreg.get(fid, {}).get("verified") != "yes":
            problems.append(f"figure {fid}: verified != yes")
if problems and (release or any(("unresolved reference" in p) or ("unknown figure" in p) for p in problems)):
    print("BUILD BLOCKED:" if not release else "RELEASE BLOCKED:")
    print("\n".join(" - " + p for p in problems))
    sys.exit(1)

tag = ("release" if release else "draft") + ("-tier-a" if tier_a else "") + f"-v{vol}" + f"-{lang}"
meta = ROOT / "build" / f"metadata.{lang}.vol{vol}.yaml"
if not meta.exists(): meta = ROOT / "build" / f"metadata.{lang}.yaml"
out = ROOT / "build" / f"{tag}.epub"
css_path = ROOT / "build" / "css" / f"v{vol if vol != 'all' else 1}.css"
css_path.parent.mkdir(exist_ok=True); css_path.write_text(design.css(vol if vol != "all" else 1))
import os; os.chdir(ROOT)
md = "\n\n".join(parts)
pypandoc.convert_text(md, "epub3", format="markdown", outputfile=str(out),
                      extra_args=["--metadata-file", str(meta), "--split-level=1", "--resource-path", str(ROOT), "--css", str(css_path)] + ([f"--epub-cover-image=build/img/cover.v{vol}.{lang}.png"] if vol != "all" else []))
clean = re.sub(r"<!--.*?-->", "", md, flags=re.S)
size = len(re.sub(r"[\s#|>*\-]", "", clean)) if lang == "ja" else len(re.findall(r"\w+", clean))
print(f"built {out.name}: {len(sel)} chapters, {len(used_figs)} figures, ~{size} {'chars' if lang == 'ja' else 'words'}")
