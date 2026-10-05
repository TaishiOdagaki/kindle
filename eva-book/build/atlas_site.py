#!/usr/bin/env python3
"""Generate a static 'Evangelion Atlas' site and atlas.json from atlas/ entities."""
import json, html, pathlib, sys, pypandoc
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'build'))
import validate
ents, errs = validate.load()
assert not errs, errs
OUT = ROOT/'build'/'site'; OUT.mkdir(parents=True, exist_ok=True)
def name(e): return e.get('title_en') or e.get('name_en') or e.get('term_en') or e['id']
back = {i: [] for i in ents}
for i,e in ents.items():
    for r in e.get('related') or []: back.setdefault(r,[]).append(i)
CSS = 'body{font:16px/1.6 system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a}a{color:#0b5fff}.badge{font-size:.75rem;padding:.1rem .5rem;border-radius:1rem;background:#eee}.stub{background:#ffe8b3}.verified{background:#c8f0c8}table{border-collapse:collapse}td,th{border-bottom:1px solid #ddd;padding:.2rem .6rem;text-align:left}'
def page(title, body): return f'<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style>{body}'
for i,e in ents.items():
    meta = ''.join(f'<tr><th>{html.escape(k)}</th><td>{html.escape(str(v))}</td></tr>' for k,v in e.items() if not k.startswith('_') and k not in ('id','type','status','related','sources') and v not in ('',[],None,False))
    rel = ''.join(f'<li><a href="{r}.html">{html.escape(name(ents[r]))}</a></li>' for r in (e.get('related') or []) if r in ents)
    bl = ''.join(f'<li><a href="{b}.html">{html.escape(name(ents[b]))}</a></li>' for b in back.get(i,[]))
    body_html = pypandoc.convert_text(e['_body'].replace('<!--','<!--'),'html',format='markdown')
    banner = '<p><b>Draft notice:</b> this entry is not yet verified.</p>' if e['status']!='verified' else ''
    open(OUT/f'{i}.html','w').write(page(name(e), f'<p><a href="index.html">Atlas</a></p><h1>{html.escape(name(e))} <span class="badge {e["status"]}">{e["status"]}</span></h1>{banner}<table>{meta}</table>{body_html}'+(f'<h2>Related</h2><ul>{rel}</ul>' if rel else '')+(f'<h2>Linked from</h2><ul>{bl}</ul>' if bl else '')))
groups = {}
for i,e in ents.items(): groups.setdefault(e['type'],[]).append(i)
idx = ''.join(f'<h2>{t.title()}s</h2><ul>'+''.join(f'<li><a href="{i}.html">{html.escape(name(ents[i]))}</a> <span class="badge {ents[i]["status"]}">{ents[i]["status"]}</span></li>' for i in v)+'</ul>' for t,v in sorted(groups.items()))
open(OUT/'index.html','w').write(page('Evangelion Atlas', f'<h1>Evangelion Atlas</h1><p>Work in progress. Entries marked <span class="badge stub">stub</span> are placeholders.</p>{idx}'))
json.dump([{k:(v if not k.startswith('_') else None) for k,v in e.items() if not k.startswith('_')} | {'body':e['_body'].strip()} for e in ents.values()], open(ROOT/'build'/'atlas.json','w'), ensure_ascii=False, indent=1, default=str)
print(f'site: {len(ents)} pages -> build/site/, build/atlas.json')
