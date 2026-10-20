#!/usr/bin/env python3
"""Rebuild current cumulative draft from v8 and ordered changes.json. Safe to rerun."""
import hashlib,html,json,zipfile,os,tempfile
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt
import v9_apply_batch1 as b
import quiz_audit as qa
from copy import deepcopy
cs=json.loads((b.OUT/'changes.json').read_text())
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
doc=Document(b.SRC)
# Keep a synchronized paragraph-text cache. Re-extracting every run for every
# replacement is costly; candidate matching and replacement assertions remain
# identical, and changed text is refreshed immediately after each operation.
paragraphs=list(doc.paragraphs)
texts=[p.text for p in paragraphs]
block_contexts=[]
current_block=None
for p in paragraphs:
 for bm in p._element.iter(qn('w:bookmarkStart')):
  name=bm.get(qn('w:name'),'')
  if name.startswith(('Q_','A_')):current_block=name
 block_contexts.append(current_block)
for c in cs:
 old=html.unescape(c['before']);matches=[i for i,t in enumerate(texts) if t is not None and old in t]
 if c['field']=='options':
  matches=[i for i in matches if texts[i]==str(c['index']+1)+'. '+old]
  if c.get('stem_context'):
   matches=[i for i in matches if [t for t in texts[:i] if t is not None][-c['index']-1]==c['stem_context']]
 if c.get('paragraph_prefix'):
  matches=[i for i in matches if texts[i].startswith(c['paragraph_prefix'])]
 if c.get('block_context'):
  matches=[i for i in matches if block_contexts[i]==c['block_context']]
 if c.get('previous_paragraph'):
  matches=[i for i in matches if [t for t in texts[:i] if t is not None][-1:]==[c['previous_paragraph']]]
 assert len(matches)==c.get('count',1),(c['id'],c['field'],len(matches))
 for i in matches:
  p=paragraphs[i]
  if c.get('remove_paragraph'):
   assert c['after']=='' and p.text==old
   p._element.getparent().remove(p._element)
   texts[i]=None
  else:
   assert b.replace_paragraph(p,old,c['after'])
   if c.get('glossary_head'):
    head=c['glossary_head'];assert p.text==c['after'] and p.text.startswith(head+'　')
    first=next(r for r in p.runs if r.text)
    for run in p.runs:run.text=''
    first.text=head;first.bold=True
    body=p.add_run(c['after'][len(head):])
    if first._element.rPr is not None:body._element.insert(0,deepcopy(first._element.rPr))
    body.bold=False
    assert p.text==c['after']
   texts[i]=p.text
# Keep the appendix glossary together without changing its font or wording.
# Source-verified definitions added in batches 202--211 made the final entry
# spill onto a page by itself.  Reducing only the glossary paragraph-after
# spacing from 5.0 pt to 3.5 pt preserves the established three-page appendix
# while keeping clear separation between adjacent entries.
glossary_heading='頻出用語集（50音順）'
afterword_heading='あとがき'
g=[i for i,t in enumerate(texts) if t==glossary_heading]
a=[i for i,t in enumerate(texts) if t==afterword_heading and i>g[0]]
assert len(g)==1 and len(a)==1
for i in range(g[0]+1,a[0]):
 if texts[i]:paragraphs[i].paragraph_format.space_after=Pt(3.5)
# Keep the previous valid draft until all structure/content checks pass.
# A failed or interrupted ZIP write must not truncate the saved draft.
fd,stage_name=tempfile.mkstemp(prefix='.v9_rebuild-',suffix='.docx',dir=b.DST.parent)
os.close(fd)
staged=Path(stage_name)
try:
 doc.save(staged);assert zipfile.ZipFile(staged).testzip() is None
 issues,q,a=qa.audit(str(staged));_,q0,a0=qa.audit(str(b.SRC))
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
 os.replace(staged,b.DST)
finally:
 staged.unlink(missing_ok=True)
(b.OUT/'postfix_machine.json').write_text(json.dumps(dict(questions=500,answers=500,v8_unchanged=True,answers_unchanged=True,unmodified_questions_unchanged=True,changed_questions=len(modified),case_replacements=sum(c['field']=='case_text' for c in cs),replacements=len(cs),issues=issues,statistics=qa.stats(q,a),full_visual_qa_completed=False,release_ready=False),ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.md').write_text('# 修正前後の比較 累積監査作業稿\n\n各修正は順次適用される。修正適用と問題全体の学術的承認は別に記録する。\n\n| ID | 対象 | 修正前 | 修正後 | 理由 | 根拠 |\n|---|---|---|---|---|---|\n'+''.join('| '+ ' | '.join([c['id'],c['field']+' '+('' if c['index'] is None else str(c['index']+1)),c['before'],c['after'],c['reason'],', '.join(c['sources']) or '原文対照・表記/具体例検算']).replace('\n',' ').replace('|','／')+' |\n' for c in []))
# Use proper per-cell escaping instead of replacing the table delimiters.
with (b.OUT/'changes.md').open('a') as f:
 for c in cs:
  cells=[c['id'],c['field']+' '+('' if c['index'] is None else str(c['index']+1)),c['before'],c['after'],c['reason'],', '.join(c['sources']) or '原文対照・表記/具体例検算']
  f.write('| '+' | '.join(s.replace('|','／').replace('\n','<br>') for s in cells)+' |\n')
print(f'{len(modified)} questions / {len(cs)} edits rebuilt; 500 questions revalidated.')
