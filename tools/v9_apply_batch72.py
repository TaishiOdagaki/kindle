"""One-time original-author clarification of L2 learning experience."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1444
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));key='Q_3_039';assert int(a['A_3_039']['ans'])==4
stem='Dörnyei（2019）が振り返る「L2動機づけ自己システム」の構成について、最も適当な説明を一つ選べ。'
opts=['「L2学習経験」は将来の自己像だけを扱い、現在の教師・カリキュラム・学習者集団は扱わない。',
'「理想のL2自己」と「義務のL2自己」の二つだけで構成され、「L2学習経験」は構成要素に含まれない。',
'「L2学習経験」とは、過去の運動能力がそのまま言語能力に移る仕組みだけを意味する。',
'将来の自己の指針となる二つの要素に加え、教師やカリキュラム、学習者集団、成功経験など、現在の学習環境・経験に関わる「L2学習経験」が含まれる。']
exps=['原著21〜22頁は、直接の学習環境に関わる状況特有の動機を扱い、教師・カリキュラム・学習者集団などを挙げています。将来の自己像だけに限定する説明は逆です。',
'原著20頁は三つの主要要素を挙げ、二つの将来の自己の指針と、第三のL2学習経験を区別しています。二要素だけとする説明は誤りです。',
'原著が扱うのは、第二言語を実際に学ぶ過程や直近の学習環境に関わる動機です。運動能力がそのまま移る仕組みという定義ではありません。',
'原著20〜22頁の区別と一致します。著者は、二つの将来の自己の指針とは異なる水準で、現在の学習経験を位置づけています。自己像と現状の差だけで必ず意欲が生じるという意味ではありません。']
reason='提唱者の2019年原著本文へ照合し、二つの将来の自己の指針と現在のL2学習経験を区別。認知的不協和との無条件な同一視と、自己像の差から学習行動を必然化する補助説明を除去。'
extra=[]
for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_3_039']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  if html.unescape(old)==new:continue
  e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S137'],applied=True,before_version='第71バッチ反映後の累積作業稿')
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(e)
d[key].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S137'],option_verdicts=['誤：直接の学習環境・経験を除外','誤：第三の要素を除外','誤：実際のL2学習経験と運動転移を取り違え','正：二つの将来の指針と第三の現在の学習経験を区別'],reason=reason,stem_review='提唱者の2019年論文20〜22頁のモデルの振返りに設問を限定し、全4肢を照合。',explanation_review='全12頁PDF取得、20〜23頁画像精読。全4解説の構成要素・時間的区別を本文照合。2009年章そのものを取得したとはせず、2019年著者本人の説明に限定。効果量・因果・自己像の無条件の効力は承認しない。',unresolved='',multiple_correct_risk='なし：本文の三要素に対応するのは4のみ',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',c+extra),('changes_batch72.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
