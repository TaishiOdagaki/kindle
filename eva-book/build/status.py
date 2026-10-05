#!/usr/bin/env python3
"""Progress dashboard. Default: Japanese, all volumes. Options: --lang=en  --vol=1|2|3"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib
ROOT = lib.ROOT
lang = "en" if "--lang=en" in sys.argv else "ja"
vol = next((a.split("=")[1] for a in sys.argv if a.startswith("--vol=")), "all")
rows = [r for r in lib.load_rows() if lib.in_volume(r, vol)]
nums = lib.chapter_numbers(lib.load_rows(), vol)
def size(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"\[\[CHECK.*?\]\]", "", t, flags=re.S)
    return len(re.sub(r"[\s#|>*\-]", "", t)) if lang == "ja" else len(re.findall(r"\w+", t))
unit = "字" if lang == "ja" else "words"
tot_t = tot_n = 0
print(f'{"id":4} {"vol":5} {"ch":>3} {"tier":4} {"status":8} {"fact":6} {"now":>7}/{"target":<7} {"figs":>6} title')
fig_t = fig_n = 0
for r in rows:
    t = (ROOT / "manuscript" / lang / r["file"]).read_text()
    n = size(t)
    target = int(r["chars_target_ja"] if lang == "ja" else r["words_target"])
    tot_t += target; tot_n += n
    st = r["status"] if lang == "ja" else r["status_en"]
    flag = " *UPDATE*" if r["update_sensitive"].lower() == "yes" else ""
    chk = t.count("[[CHECK")
    title = r["title_ja"] if lang == "ja" else r["title"]
    ch = nums.get(r["id"], "")
    fn = len(re.findall(r"\{\{fig:", t)); ft = int(r["figs_target"]); fig_n += fn; fig_t += ft
    print(f'{r["id"]:4} {r["volume"]:5} {ch!s:>3} {r["tier"]:4} {st:8} {r["fact_check"]:6} {n:>7}/{target:<7} {fn:>3}/{ft:<2} {title[:34]}{flag}{f"  [{chk} checks]" if chk else ""}')
print(f"\nTOTAL {tot_n}/{tot_t} {unit} ({100*tot_n//tot_t}%)  figures {fig_n}/{fig_t}  [lang={lang}, vol={vol}]")
