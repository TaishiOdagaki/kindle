#!/usr/bin/env python3
"""Print a progress dashboard from chapters.csv and manuscript word counts."""
import csv, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "chapters.csv", newline="")))
tot_t = tot_n = 0
print(f'{"id":4} {"status":8} {"fact":6} {"now":>6}/{"target":<6} title')
for r in rows:
    t = (ROOT / "manuscript" / r["file"]).read_text()
    n = len(re.findall(r"\w+", re.sub(r"<!--.*?-->", "", t, flags=re.S))) - len(r["title"].split())
    n = max(n, 0)
    tot_t += int(r["words_target"]); tot_n += n
    flag = " *UPDATE*" if r["update_sensitive"].lower() in ("yes",) else ""
    print(f'{r["id"]:4} {r["status"]:8} {r["fact_check"]:6} {n:>6}/{r["words_target"]:<6} {r["title"][:60]}{flag}')
print(f"\nTOTAL {tot_n}/{tot_t} words ({100*tot_n//tot_t}%)")
