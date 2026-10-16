"""One-time source-bounded replacement of overgeneralized L1/L2 comparison."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2716
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_3_008';key=4;extra=[]
assert d[k]['status']=='修正必要' and a['A_3_008']['ans']=='4'
stem='Krashen（1982）が「習得と学習の区別」で述べた、子供の第一言語習得と成人の第二言語に関する仮説内の主張として、最も適切なものを一つ選びなさい。'
opts=[
'子供は無意識的に言語を習得できるが、成人はその能力を失い、第二言語では意識的な規則学習しかできないとする。',
'子供が第一言語の能力を伸ばす過程を、規則を意識的に覚え、その規則を説明できるようになる学習だけで説明している。',
'成人にも第二言語を無意識的に習得する能力が残るということは、成人の全員が必ず母語話者と同等の水準に到達するという意味である。',
'成人にも、子供の第一言語習得と類似する無意識的な習得の過程があるとし、規則についての意識的な知識を得る学習とは区別する。']
exps=[
'著者は、成人も習得でき、言語を自然に身に付ける能力が思春期に消えるわけではないと主張しています。成人には意識的な学習しかできないという肢は、その仮説と異なります。',
'同書は無意識的な習得を子供の第一言語の発達過程と比較し、意識的な規則知識を得る学習と区別します。子供の第一言語の発達を意識的な規則学習だけで説明する肢ではありません。',
'印刷10頁は、成人にも習得能力があるという主張が、成人が常に母語話者並みの水準へ達するという意味ではないと明記しています。習得できるという可能性と、全員の到達を保証することを取り違えています。',
'同書は、成人が第二言語の能力を伸ばす二つの過程として、子供の第一言語習得と類似する無意識的な習得と、意識的な規則知識を得る学習を区別しています。これは著者の仮説内の主張を説明したものです。']
reason='Krashen1982原著印刷10〜11/PDF17〜18を本文・画像照合。元問の生得的LADを無条件の事実とする対比、第二言語は既に確立した第一言語を必ず持つという一般化、第一言語到達度の全人類一律説、第二言語転移の普遍性、明示指導/Focus on Formの効果という未取得の一般主張を承認せず、同じ学習領域の第一/第二言語比較を著者の仮説内に限定して再構成。成人にも習得可能だが全員母語話者並みの到達保証ではないという原文の留保を保持。引用一次研究や仮説の現在の実証的妥当性は今回未承認。'
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_3_008']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  old=html.unescape(old)
  if old==new:continue
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S13'],applied=True,before_version='第124バッチ反映後',block_context='A_3_008' if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S13'],reason=reason,option_verdicts=['誤：成人も習得できるという著者の明示的主張を否定','誤：子供の第一言語の発達を意識的規則学習だけとする','誤：成人にも習得可能という主張を全員の到達保証と取り違える','正：著者の無意識的習得と意識的学習の区別に対応'],stem_review='設問・全4肢を原著印刷10〜11頁へ独立照合。第一/第二言語の一般的総論ではなくKrashenの仮説内比較を問う。',explanation_review='全4解説を原著本文・画像へ照合。可能性と到達保証、著者の理論と普遍的な生物学的事実を区別。未取得の転移や明示指導の実証を補助根拠としない。',unresolved='',multiple_correct_risk='なし：独立正答4のみ適切',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',cs+extra),('changes_batch125.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'krashen1982.pdf').read_bytes()
(b.OUT/'evidence/batch125_sources.json').write_text(json.dumps([dict(source_id='S13',url='https://www.sdkrashen.com/content/books/principles_and_practice.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-16',body_read_scope='printed10-11/PDF17-18 full text+images; acquisition-learning hypothesis within author theory, no universal L1 attainment or instruction/transfer effects approval',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('1 question/9 edits')
