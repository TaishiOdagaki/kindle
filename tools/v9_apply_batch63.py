"""Apply original-source question-type revision with explicit multi-paragraph removal."""
import json,html
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
p=json.loads((b.OUT/'evidence/batch63_Q_4_017_pending_revision.json').read_text())
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==1277
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));key=p['id'];extra=[]
doc=Document(b.DST);ps=[x.text for x in doc.paragraphs];first='ある日本語クラスで、教師が学習者に対して行った以下のやり取り（発話）の分析として、最も適切なものを一つ選びなさい。';start=ps.index(first)
old_stem_parts=ps[start:start+4]
assert ' '.join(old_stem_parts)==html.unescape(q[key]['stem'])
for field,old,new in [('stem',[first],[p['proposed_stem']]),('options',q[key]['opts'],p['proposed_options']),('explanations',a['A_4_017']['txt'],p['proposed_explanations'])]:
 for i,(before,after) in enumerate(zip(old,new)):
  if html.unescape(before)==after:continue
  e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=p['finding'],sources=['S124'],applied=True,before_version='第62バッチ反映後の累積作業稿')
  if field=='options':e['stem_context']=p['proposed_stem']
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(e)
  if field=='stem':
   for text in old_stem_parts[1:]:extra.append(dict(e,field='case_text',before=text,after='',remove_paragraph=True,reason='旧会話3段落を撤去し、教師の知識状態を明示した設問に統合。'))
for name,obj in [('changes.json',cs+extra),('changes_batch63.json',extra)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
d[key].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S124'],option_verdicts=p['option_verdicts'],reason=p['finding'],stem_review='Nunan1990第5節の定義に照合し、質問者が答えを知らない条件を明記。',explanation_review='全4肢・全4解説を質問者の知識状態と定義に照合。回答長・習得効果の保証を除く。',unresolved='',multiple_correct_risk='なし：明示された知識状態と参照質問の定義に合うのは4のみ',no_correct_risk='なし：独立正答4')
(b.OUT/'decisions.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
