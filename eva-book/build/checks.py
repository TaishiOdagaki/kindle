#!/usr/bin/env python3
"""Collect every unresolved [[CHECK: ...]] mark into data/verification/CHECKLIST.md.

Marks look like:  ... claim text. [[CHECK: ep.19 / confirm Zeruel's number]]
Resolve a mark by verifying against the work or a primary source, then delete the mark
(and note the verification in the commit message or the atlas entry's `sources`).
"""
import re, csv, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
lang = 'en' if '--lang=en' in sys.argv else 'ja'
items = []
for r in csv.DictReader(open(ROOT/'chapters.csv', newline='')):
    t = (ROOT/'manuscript'/lang/r['file']).read_text()
    for m in re.finditer(r'\[\[CHECK:?\s*(.*?)\]\]', t, re.S):
        a = t.rfind('\n', 0, m.start()); line = t[a+1:t.find('\n', m.end()) if t.find('\n', m.end()) != -1 else len(t)]
        ctx = re.sub(r'\[\[CHECK.*?\]\]', '', line).strip()[:140]
        items.append((r['id'], (r['title_ja'] if lang=='ja' else r['title']), m.group(1).strip() or '(verify)', ctx))
for p in sorted((ROOT/'atlas').rglob('*.md')):
    if p.name == 'SCHEMA.md': continue
    t = p.read_text()
    for m in re.finditer(r'\[\[CHECK:?\s*(.*?)\]\]', t, re.S):
        items.append((p.stem, 'atlas', m.group(1).strip() or '(verify)', ''))
for r in csv.DictReader(open(ROOT/'figures.csv', newline='')):
    if r['verified'] != 'yes':
        items.append((r['chapter'], '図', f"図 {r['id']} の内容を作品・資料で確認し、figures.csv の verified を yes にする", r['caption_ja']))
out = ROOT/'data'/'verification'; out.mkdir(parents=True, exist_ok=True)
lines = ['# 検証チェックリスト(自動生成: `python3 build/checks.py`)', '',
         '各項目を**作品の視聴または一次資料**で確認し、原稿の `[[CHECK]]` を消す。',
         '確認できなかった・誤りだった場合は、原稿を直してから消す。', '']
cur = None
for i, title, what, ctx in items:
    if i != cur:
        lines += ['', f'## {i} — {title}']; cur = i
    lines.append(f'- [ ] **{what}**' + (f'  \n      > {ctx}' if ctx else ''))
lines.append(f'\n---\n合計 **{len(items)}** 件')
(out/'CHECKLIST.md').write_text('\n'.join(lines) + '\n')
print(f'{len(items)} unresolved checks -> data/verification/CHECKLIST.md')
