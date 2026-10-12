#!/usr/bin/env python3
"""Narrow scalar-particle item to source-supported quantity interpretations."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==515
_,Q,A=qa.audit(str(b.DST));extra=[]
why='モを極端のサエと同義とする一般化と、シカを必ず失望とする説明を撤去。肯定文の数量＋もと否定を伴うしかの取得済み教材に限定。'
stem='肯定文「100人も来た」のような数量に付く「も」と、否定形と一緒に使う「しか」について、適切な説明はどれか。'
opts=['「も」は否定文でしか使えないため、「100人も来た」は文として成立しない。','「100人も来た」の「も」は、話し手が来た人数を少ないと捉えていることだけを表す。','肯定文の数量に付く「も」には、話し手がその量を多いと捉えていることを表す用法がある。','「しか」は肯定形でしか使えないため、「100人しか来なかった」は文として成立しない。']
exps=['国際交流基金の教材には、肯定文で量の多さを表す数量＋もの例があります。もを否定文に限定する説明は誤りです。','この用法では、話し手が量を多いと捉えていることを表します。少ないという捉え方だけを表すとする説明は逆です。','国際交流基金の食生活の教材は、助数詞＋もを使って、話し手が量を多いと感じていることを表す用法を説明しています。ここではその用法を問います。','しかは否定形と一緒に使い、数量などを限定します。「100人しか来なかった」はその形に合います。限定に伴う気持ちは期待や想定に左右されるため、必ず失望するとまでは断定しません。']
for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
 for i,new in enumerate(vs):
  old=Q['Q_5_064']['stem'] if field=='stem' else Q['Q_5_064']['opts'][i] if field=='options' else A['A_5_064']['txt'][i]
  extra.append(dict(id='Q_5_064',field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S68'],applied=True,before_version='第29修正バッチ作業稿'))
(b.OUT/'changes_batch30.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D['Q_5_064'].update(status='確認済み',fixes_applied=True,independent_answer=3,sources=['S68'],option_verdicts=['肯定文のモを排除して誤り','量の多さを少なさへ逆転して誤り','肯定文の数量＋モの用法に一致して正しい','シカと否定の共起を否定して誤り'],reason=why,stem_review='数量＋モと否定形を伴うシカの形・意味に限定。ハの全用法、モとサエの同義性を問う旧断定を撤去。',explanation_review='国際交流基金KML00128手順2–3・解答・音声スクリプト、BTS00122解説A–Cと先生へを本文照合。',unresolved='',multiple_correct_risk='なし：3のみ取得した用法に一致',no_correct_risk='なし：独立正答3')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S68 | 国際交流基金 [食生活 しか～ない／～も](https://www.kyozai.jpf.go.jp/kyozai/material/KML00128/ja/render.do)、[しか…否定](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00122/ja/render.do) | 手順2–3・解答・音声スクリプトと解説A–C・先生へを本文取得。数量＋もで多さを感じる用法、しか＋否定の限定、気持ちの期待・想定依存を照合。全肢・全解説を限定した用法に再判定。 | Q_5_064 |\n')
print('Recorded',len(extra),'repairs')
