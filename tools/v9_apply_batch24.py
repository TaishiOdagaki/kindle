#!/usr/bin/env python3
"""Replace blanket new/old-information rules with an explicit contrast example."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==416
_,Q,A=qa.audit(str(b.DST));extra=[]
why='はを格助詞とする設問名と、新旧情報だけによる一律分類、疑問詞＋はの絶対禁止を撤去。対比される飲み物二種を明示した文で対比用法を問う。'
stem='「紅茶は飲みますが、コーヒーは飲みません」の二つの「は」の働きとして、適切な説明はどれか。'
opts=['紅茶とコーヒーを飲む場所として示している。','紅茶とコーヒーを動作が行われる時刻として示している。','紅茶とコーヒーを対比して、飲むものと飲まないものを取り立てて示している。','紅茶とコーヒーを移動の出発点として示している。']
exps=['この文の紅茶とコーヒーは飲み物であり、動作が行われる場所ではありません。ここでは二つを対比しています。','紅茶とコーヒーは時刻を表していません。「は」はここで、飲むか飲まないかが異なる二つの飲み物を対比しています。','「は」には対比的に取り立てて示す用法があります。この文は、紅茶を飲むこととコーヒーを飲まないことを対比しています。','紅茶とコーヒーは移動の出発点ではありません。この文の「は」は移動の起点を示す助詞として使われていません。']
for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
 for i,new in enumerate(vs):
  old=Q['Q_5_052']['stem'] if field=='stem' else Q['Q_5_052']['opts'][i] if field=='options' else A['A_5_052']['txt'][i]
  extra.append(dict(id='Q_5_052',field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S59','S61'],applied=True,before_version='第23修正バッチ作業稿'))
(b.OUT/'changes_batch24.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D['Q_5_052'].update(status='確認済み',fixes_applied=True,independent_answer=3,sources=['S59','S61'],option_verdicts=['場所でなく飲み物なので誤り','時刻でなく飲み物なので誤り','飲む／飲まないの対比で正しい','移動の起点ではなく誤り'],reason=why,stem_review='国際交流基金の対比の例文と辞典の対比用法を照合。は／がの品詞名・新旧情報・疑問詞の過度な断定を問わない。',explanation_review='対比用法と飲み物二種の意味を全4肢・4解説で点検。はの全用法が対比だとは述べない。',unresolved='',multiple_correct_risk='なし：3のみ明示された対比',no_correct_risk='なし：独立正答3')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S61 | 小学館デジタル大辞泉 [は](https://kotobank.jp/word/%E3%81%AF-597777) | 現代助詞の主題提示・対比的取り立ての項目本文を取得。S59の国際交流基金の飲み物対比例と合わせて使用。は／がの全学説や新旧情報の一般論は承認対象から撤去。 | Q_5_052 |\n')
print('Recorded',len(extra),'repairs')
