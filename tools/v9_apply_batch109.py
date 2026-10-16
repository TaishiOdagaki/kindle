"""One-time complete review of professional development against the authors' text."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2448
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_003';assert d[k]['status']=='要追加確認' and a['A_4_003']['ans']=='2'
stem='RichardsとFarrell（2005）第1章が示す、言語教師の継続的な専門性開発の考え方に合うものを一つ選びなさい。'
opts=q[k]['opts'].copy();opts[1]='自分の実践を振り返るとともに、同僚との知識・経験の共有や新たな知識の学習を行う。学校側も学びの機会を支援する。'
exps=[
'2〜4頁では、教師が知識を更新する機会や、新たな理論・動向を学ぶことも専門性開発に含めています。過去の経験だけを絶対視して学びを避ける説明とは異なります。新しい技術や理論をすべて無批判に採用するという意味ではありません。',
'2頁は教師間の知識・経験の共有、3頁は教師自身の取組と学校・管理者による機会の提供、4頁は実践の省察と他の知識の学習を扱います。個人の努力と組織の支援を含めた肢が、この説明に対応します。',
'1〜3頁では、正式な養成を終えた後も教師の学びが続くと説明されています。資格取得時点で必要な学びがすべて完了し、就職後の研修や研究が不要になるという肢は誤りです。',
'2頁は知識・経験の相互共有を成長の資源とし、4頁は同僚との対話や共同の取組も挙げています。他者との情報交換を禁止する独学法という説明は一致しません。個人の振り返り自体を否定するものでもありません。']
reason='S167出版社公開の原著第1章抜粋1〜10頁を取得・精読。特に2〜4頁の知識更新、継続性、協働と個人・機関の支援を照合。アクション・リサーチの特定サイクルや主要手法という未照合の追加主張は承認せず、同じ専門性開発領域の本文対応へ改訂する。'
extra=[]
for field,old,new in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_4_003']['txt'],exps)]:
 for i,(o,n) in enumerate(zip(old,new)):
  o=html.unescape(o)
  if o==n:continue
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S167'],applied=True,before_version='第108バッチ反映後',block_context='A_4_003' if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(e)
assert len(extra)==6
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S167'],reason=reason,option_verdicts=['誤：過去の経験のみを絶対視し知識更新を排除','正：個人の省察・協働・知識の学習と機関の支援','誤：正式な養成後の継続的学習を不要とする','誤：教師間の情報・実践共有を禁止する'],stem_review='著者と第1章を指定し全4肢を独立照合。変更していない誤答3肢も原著2〜4頁の説明に反することを確認。',explanation_review='全4解説を1〜4頁に照合。原著の推奨・説明であり全教師の効果実証とはしない。アクション・リサーチ第12章や他の引用元研究は未取得のため承認しない。',unresolved='',multiple_correct_risk='なし：本文に対応する肢は2のみ',no_correct_risk='なし：独立正答2')
for name,obj in [('changes.json',c+extra),('changes_batch109.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/697c245d9771/richards109.pdf').read_bytes()
(b.OUT/'evidence/batch109_source.json').write_text(json.dumps(dict(id='S167',authors='Jack C. Richards and Thomas S. C. Farrell',year=2005,title='Professional Development for Language Teachers Strategies for Teacher Learning',url='https://assets.cambridge.org/97805218/49111/excerpt/9780521849111_excerpt.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),obtained='publisher excerpt of chapter1, printed1-10, all10 pages read',image_review_pages=[2,3,4],limits='Not the complete book, not chapter12, not the primary studies cited by the authors; scan date is not publication year'),ensure_ascii=False,indent=2)+'\n')
print('1 complete review/6 actual edits')
