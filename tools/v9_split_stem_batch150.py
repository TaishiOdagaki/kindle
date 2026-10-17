"""One-time repair of split Word stem metadata before successful application."""
import json,subprocess
from pathlib import Path
from docx import Document
p=Path('audit/v9');base=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']))
cs=json.loads((p/'changes.json').read_text());batch=json.loads((p/'changes_batch150.json').read_text());assert len(base)==3034 and cs==base+batch and len(batch)==18
ps=Document(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx').paragraphs
i=next(i for i,t in enumerate(ps) if t.text.startswith('日本語学校に通う留学生Cさんは、日本での生活'))
c=next(c for c in batch if c['id']=='Q_3_034' and c['field']=='stem')
assert c['before']==ps[i].text+' '+ps[i+1].text
c['before']=ps[i].text
rem=dict(c,field='stem_continuation',before=ps[i+1].text,after='',remove_paragraph=True,reason='旧設問が2段落であることを再構成失敗時に確認。先頭を統合文へ置換するため、続きの旧問い段落を明示的に削除する。'+c['reason'])
batch.insert(batch.index(c)+1,rem)
for name,rows in [('changes.json',base+batch),('changes_batch150.json',batch)]:
 (p/name).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('19 edits: old question continuation explicitly removed before options')
