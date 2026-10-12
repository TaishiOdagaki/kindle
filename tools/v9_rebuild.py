#!/usr/bin/env python3
"""Rebuild current cumulative draft from v8 and ordered changes.json. Safe to rerun."""
import hashlib,html,json,zipfile
from docx import Document
import v9_apply_batch1 as b
import quiz_audit as qa
cs=json.loads((b.OUT/'changes.json').read_text())
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
doc=Document(b.SRC)
# Keep a synchronized paragraph-text cache. Re-extracting every run for every
# replacement is costly; candidate matching and replacement assertions remain
# identical, and changed text is refreshed immediately after each operation.
paragraphs=list(doc.paragraphs)
texts=[p.text for p in paragraphs]
for c in cs:
 old=html.unescape(c['before']);matches=[i for i,t in enumerate(texts) if t is not None and old in t]
 if c['field']=='options':
  matches=[i for i in matches if texts[i]==str(c['index']+1)+'. '+old]
 assert len(matches)==c.get('count',1),(c['id'],c['field'],len(matches))
 for i in matches:
  p=paragraphs[i]
  if c.get('remove_paragraph'):
   assert c['after']=='' and p.text==old
   p._element.getparent().remove(p._element)
   texts[i]=None
  else:
   assert b.replace_paragraph(p,old,c['after'])
   texts[i]=p.text
doc.save(b.DST);assert zipfile.ZipFile(b.DST).testzip() is None
issues,q,a=qa.audit(str(b.DST));_,q0,a0=qa.audit(str(b.SRC))
assert len(q)==len(a)==500 and set(q)==set(q0) and set(a)==set(a0)
assert all(a[k]['ans']==a0[k]['ans'] for k in a)
assert not [i for i in issues if i[0] in {'S1','S3','S4','S5','S6','N1','N2'}]
modified={c['id'] for c in cs if c['id'].startswith('Q_')}
def norm(v):
 if isinstance(v,str):return html.unescape(v)
 if isinstance(v,list):return [norm(t) for t in v]
 if isinstance(v,dict):return {k:norm(x) for k,x in v.items()}
 return v
assert all(norm(q[k])==norm(q0[k]) and norm(a['A_'+k[2:]])==norm(a0['A_'+k[2:]]) for k in q if k not in modified)
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
(b.OUT/'postfix_machine.json').write_text(json.dumps(dict(questions=500,answers=500,v8_unchanged=True,answers_unchanged=True,unmodified_questions_unchanged=True,changed_questions=len(modified),case_replacements=sum(c['field']=='case_text' for c in cs),replacements=len(cs),issues=issues,statistics=qa.stats(q,a),full_visual_qa_completed=False,release_ready=False),ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.md').write_text('# 修正前後の比較 累積監査作業稿\n\n各修正は順次適用される。修正適用と問題全体の学術的承認は別に記録する。\n\n| ID | 対象 | 修正前 | 修正後 | 理由 | 根拠 |\n|---|---|---|---|---|---|\n'+''.join('| '+ ' | '.join([c['id'],c['field']+' '+('' if c['index'] is None else str(c['index']+1)),c['before'],c['after'],c['reason'],', '.join(c['sources']) or '原文対照・表記/具体例検算']).replace('\n',' ').replace('|','／')+' |\n' for c in []))
# Use proper per-cell escaping instead of replacing the table delimiters.
with (b.OUT/'changes.md').open('a') as f:
 for c in cs:
  cells=[c['id'],c['field']+' '+('' if c['index'] is None else str(c['index']+1)),c['before'],c['after'],c['reason'],', '.join(c['sources']) or '原文対照・表記/具体例検算']
  f.write('| '+' | '.join(s.replace('|','／').replace('\n','<br>') for s in cells)+' |\n')
print(f'{len(modified)} questions / {len(cs)} edits rebuilt; 500 questions revalidated.')
