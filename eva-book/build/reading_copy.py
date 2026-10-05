#!/usr/bin/env python3
"""Build self-contained reading copies (HTML) of the chapters written so far.
  python3 build/reading_copy.py [--vol=1]
Outputs build/reading/vol<N>-with-checks.html (unverified marks highlighted) and vol<N>-clean.html."""
import re, sys, os, pathlib
import pypandoc
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib, figs, design
ROOT = lib.ROOT
vol = next((a.split("=")[1] for a in sys.argv if a.startswith("--vol=")), "1")
rows = lib.load_rows(); figreg = lib.load_figs(); nums = lib.chapter_numbers(rows, vol)
figs.render("ja", vols=(vol,))
sel = [r for r in rows if lib.in_volume(r, vol) and r["status"] != "stub" and r["id"] not in ("fm0",) and (ROOT/"manuscript"/"ja"/r["file"]).read_text().count("TODO: 執筆") < 3]
EXTRA_CSS = """
body { max-width: 46em; margin: 2em auto; padding: 0 1em; font-family: 'Hiragino Sans','Noto Sans JP','Yu Gothic',sans-serif; line-height: 1.85; color: #111; }
.check { background: #fff3b0; border-bottom: 1px dotted #a07800; font-size: 0.78em; padding: 0 0.25em; color: #5a4300; }
h1 { page-break-before: always; }
nav#TOC { background: #f6f6f6; padding: 1em 1.5em; border-radius: 6px; }
.banner { background: %s; color: %s; padding: 1.2em 1.5em; border-radius: 6px; margin-bottom: 2em; }
"""
def make(with_checks):
    th = design.theme(vol); problems = []; parts = []
    for r in sel:
        t = (ROOT / "manuscript" / "ja" / r["file"]).read_text()
        t = lib.apply_volume_fences(t, vol); t = lib.resolve_refs(t, rows, vol)
        t = lib.resolve_figs(t, r, nums, "ja", figreg, problems, vol)
        if with_checks:
            t = re.sub(r"\[\[CHECK:?\s*(.*?)\]\]", lambda m: '<span class="check">【要確認: ' + m.group(1).replace('"', "'") + '】</span>', t, flags=re.S)
        else:
            t = re.sub(r"\s*\[\[CHECK:?.*?\]\]", "", t, flags=re.S)
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        parts.append(t.strip())
    kind = "未確認の印つき" if with_checks else "読み物版(未確認の印を非表示)"
    head = f'<div class="banner"><b>『エヴァンゲリオン決定版』第{vol}巻 — 執筆中の原稿({kind})</b><br>日本語版・初稿。作品との照合は未了です。収録: ' + "、".join(f"{r['title_ja']}" for r in sel) + '</div>\n\n'
    md = head + "\n\n".join(parts)
    out = ROOT / "build" / "reading" / f"vol{vol}-{'with-checks' if with_checks else 'clean'}.html"
    css = ROOT / "build" / "reading" / "_style.css"
    css.write_text(design.css(vol) + EXTRA_CSS % (th["accent"], th["on_accent"]))
    os.chdir(ROOT)
    pypandoc.convert_text(md, "html5", format="markdown", outputfile=str(out),
        extra_args=["--standalone", "--embed-resources", "--toc", "--toc-depth=2", "--css", str(css), "--resource-path", str(ROOT), "--metadata", f"title=エヴァンゲリオン決定版 第{vol}巻 原稿(執筆中)", "--metadata", "lang=ja"])
    if problems: print("warnings:", problems)
    return out
for w in (True, False):
    o = make(w); print(o.name, f"{o.stat().st_size/1024:.0f} KB")
print("chapters:", [r["id"] for r in sel])
