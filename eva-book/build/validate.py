#!/usr/bin/env python3
"""Validate atlas/ entities. Exits non-zero on errors."""
import sys, re, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPES = {'episode','work','character','term','theme','event','person','source','debate'}
STATUS = {'stub','draft','reviewed','verified'}
PREFIX = {'episode':'ep-','work':'work-','character':'ch-','term':'term-','theme':'theme-','event':'ev-','person':'pe-','source':'src-','debate':'db-'}

def load():
    ents = {}
    errs = []
    for p in sorted((ROOT/'atlas').rglob('*.md')):
        if p.name == 'SCHEMA.md': continue
        t = p.read_text()
        m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
        if not m: errs.append(f'{p.name}: missing front matter'); continue
        meta = yaml.safe_load(m.group(1)) or {}
        meta['_body'] = m.group(2); meta['_path'] = p
        i = meta.get('id')
        if i in ents: errs.append(f'{p.name}: duplicate id {i}')
        ents[i] = meta
    return ents, errs

def main():
    ents, errs = load()
    for i, e in ents.items():
        n = e['_path'].name
        if e.get('type') not in TYPES: errs.append(f'{n}: bad type {e.get("type")}')
        elif not str(i).startswith(PREFIX[e['type']]): errs.append(f'{n}: id must start with {PREFIX[e["type"]]}')
        if i != e['_path'].stem: errs.append(f'{n}: id != filename')
        if e.get('status') not in STATUS: errs.append(f'{n}: bad status {e.get("status")}')
        for k in ('related','sources'):
            for r in e.get(k) or []:
                if r not in ents: errs.append(f'{n}: {k} -> unknown id {r}')
        if e.get('status') == 'verified':
            if not e.get('sources'): errs.append(f'{n}: verified but no sources')
            if 'TODO' in e['_body']: errs.append(f'{n}: verified but body has TODO')
            if '[[CHECK' in e['_body']: errs.append(f'{n}: verified but has unresolved [[CHECK]]')
    from collections import Counter
    c = Counter((e['type'], e['status']) for e in ents.values())
    print(f'{len(ents)} entities'); [print(f'  {t:10} {s:9} {n}') for (t,s),n in sorted(c.items())]
    if errs: print('\nERRORS:'); [print(' -', x) for x in errs]; sys.exit(1)
    print('OK')
if __name__ == '__main__':
    main()
