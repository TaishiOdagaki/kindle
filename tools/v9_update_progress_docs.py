#!/usr/bin/env python3
"""Synchronize current summary counts without rewriting historical batch records."""
import json,re
from collections import Counter
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'audit/v9'
d=json.loads((out/'decisions.json').read_text());cs=json.loads((out/'changes.json').read_text())
c=Counter(x['status'] for x in d.values())
n=len({x['id'] for x in cs if x['id'].startswith('Q_')});ed=len(cs)
p=out/'README.md';t=p.read_text()
for s in ('確認済み','修正必要','要追加確認'):
 t=re.sub(r'\| '+s+r' \| \d+問',f'| {s} | {c[s]}問',t)
t=re.sub(r'\| 作業稿反映 \| \d+問\d+箇所',f'| 作業稿反映 | {n}問{ed}箇所',t)
t=re.sub(r'：\d+問を部分修正',f'：{n}問を部分修正',t)
t=re.sub(r'の修正必要\d+問を',f'の修正必要{c["修正必要"]}問を',t)
t=re.sub(r'要追加確認\d+問と修正必要\d+問の全残存主張',f'要追加確認{c["要追加確認"]}問と修正必要{c["修正必要"]}問の全残存主張',t)
p.write_text(t)
p=out/'interim_report.md';t=p.read_text()
for s in ('確認済み','修正必要','要追加確認'):
 t=re.sub(r'\| '+s+r' \| \d+ \|',f'| {s} | {c[s]} |',t,count=1)
t=re.sub(r'\d+問・\d+箇所を累積作業稿に反映',f'{n}問・{ed}箇所を累積作業稿に反映',t,count=1)
t=re.sub(r'修正必要\d+問と要追加確認\d+問の全主張',f'修正必要{c["修正必要"]}問と要追加確認{c["要追加確認"]}問の全主張',t)
p.write_text(t)
print(dict(c),n,ed)
