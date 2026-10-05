#!/usr/bin/env python3
"""Progress dashboard. Default: Japanese (primary). Use --lang=en for English."""
import csv, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
lang = "en" if "--lang=en" in sys.argv else "ja"
rows = list(csv.DictReader(open(ROOT / "chapters.csv", newline="")))
def size(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"\[\[CHECK.*?\]\]", "", t, flags=re.S)
    return len(re.sub(r"[\s#|>*\-]", "", t)) if lang == "ja" else len(re.findall(r"\w+", t))
unit = "字" if lang == "ja" else "words"
tot_t = tot_n = 0
print(f'{"id":4} {"tier":4} {"status":8} {"fact":6} {"now":>7}/{"target":<7} title')
for r in rows:
    t = (ROOT / "manuscript" / lang / r["file"]).read_text()
    n = size(t)
    target = int(r["chars_target_ja"] if lang == "ja" else r["words_target"])
    tot_t += target; tot_n += n
    st = r["status"] if lang == "ja" else r["status_en"]
    flag = " *UPDATE*" if r["update_sensitive"].lower() == "yes" else ""
    chk = t.count("[[CHECK")
    title = r["title_ja"] if lang == "ja" else r["title"]
    print(f'{r["id"]:4} {r["tier"]:4} {st:8} {r["fact_check"]:6} {n:>7}/{target:<7} {title[:40]}{flag}{f"  [{chk} checks]" if chk else ""}')
print(f"\nTOTAL {tot_n}/{tot_t} {unit} ({100*tot_n//tot_t}%)  [lang={lang}]")
