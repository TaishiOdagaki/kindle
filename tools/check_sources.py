#!/usr/bin/env python3
"""murakami-jp/manuscript.md の【海外の声】系の印と、台帳外の出典を検査する。
使い方: python3 -I tools/check_sources.py murakami-jp/manuscript.md murakami-jp/source-protocol.md
"""
import re, sys

ms = open(sys.argv[1], encoding="utf-8").read()
ledger = open(sys.argv[2], encoding="utf-8").read()
ledger_ids = set(re.findall(r"^\| ([A-Z]-[\w-]+) \|", ledger, re.M))
used = set(re.findall(r"\[\^(R-[\w-]+)\]", ms))

bad = used - ledger_ids
for m in sorted(bad):
    print(f"台帳にない出典ID: {m}")
for tag in ("海外の声を入れる位置", "読取不確実", "要確認", "原文挿入", "要改稿", "結果を受けて"):
    n = len(re.findall(tag, ms))
    if n:
        print(f"未解決の印 {tag}: {n}か所")
sys.exit(1 if bad else 0)
