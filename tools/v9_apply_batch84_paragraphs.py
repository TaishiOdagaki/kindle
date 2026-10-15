"""One-time repair of batch84 stem records before successful cumulative rebuild.

The initial records joined multi-paragraph stems. Rebuild rejected them safely
and preserved the preceding valid DOCX. Explicitly remove all old continuations.
"""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1858
assert c[-54:]==json.loads((b.OUT/'changes_batch84.json').read_text())
paras,_=qa.load(str(b.DST));qb,_=qa.blocks(paras)
out=[];fixes=0
for e in c[-54:]:
 if e['field']=='stem' and e['id'] in {'Q_4_014','Q_4_025'}:
  parts=[html.unescape(x['t']) for x in qb[e['id']][1:-1] if not x['ind']]
  assert e['before']==' '.join(parts)
  e=dict(e,before=parts[0]);out.append(e)
  for t in parts[1:]:
   out.append(dict(id=e['id'],field='stem_continuation',index=None,before=t,after='',remove_paragraph=True,block_context=e['id'],reason='複数段落の設問を一段落へ統合したため旧継続段落を明示除去。'+e['reason'],sources=e['sources'],applied=True,before_version=e['before_version']))
   fixes+=1
 else:out.append(e)
assert fixes==5 and len(out)==59
for name,obj in [('changes.json',c[:-54]+out),('changes_batch84.json',out)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Replaced two joined-stem records with first-paragraph matches; explicitly removed five continuations; 59 edits')
