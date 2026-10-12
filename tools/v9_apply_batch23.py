#!/usr/bin/env python3
"""Avoid defining every causative passive as reluctant coercion."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==407
_,Q,A=qa.audit(str(b.DST));extra=[]
why='使役受身を常に嫌々の強制とする旧解説と、させたを使役＋てもらうの例とする誤記を撤去。取得した大学公開論文の強制・感情や思考の誘発の区別に即して全肢を再構成。'
stem='使役受身表現の意味に関する説明として、適切なものはどれか。'
opts=['使役受身は、どの文脈でも他者から命令されて嫌々動作を行う意味だけを表し、それ以外の用法はない。','他者に動作を強制される用法に加え、ある事柄が原因となって感情や思考が生じる用法もある。','感情や思考を表す動詞から使役受身表現を作ることはできない。','使役受身文では、主語は常に他者へ動作を命令する側であり、働きかけを受ける側になることはない。']
exps=['強制される意味は代表的な用法ですが、すべての使役受身表現をそれだけで説明することはできません。感情や思考がある原因によって生じる用法もあります。','使役受身には、意に反して動作を強制される用法と、出来事などが原因となって感情や思考が生じる用法があります。ここでは代表的な用法の存在を述べており、意味用法がこの二つだけに尽きると断定していません。','大学公開論文には、世の中の変化の激しさにびっくりさせられるなど、感情や思考が生じる用法の例が示されています。この用法を否定する説明は誤りです。','動作を強制される用法では、主語は他者にその動作を行わせられる側です。主語が常に命令する側だとする説明は、使役する側と働きかけを受ける側を取り違えています。']
for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
 for i,new in enumerate(vs):
  old=Q['Q_5_056']['stem'] if field=='stem' else Q['Q_5_056']['opts'][i] if field=='options' else A['A_5_056']['txt'][i]
  extra.append(dict(id='Q_5_056',field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S60'],applied=True,before_version='第22修正バッチ作業稿'))
(b.OUT/'changes_batch23.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D['Q_5_056'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S60'],option_verdicts=['全用法を命令・嫌々に限定して誤り','強制と感情・思考の生起の用法の存在を述べ正しい','感情・思考の用法を排除して誤り','強制する側とされる側を逆転して誤り'],reason=why,stem_review='全称的な強制の定義から代表的用法の区別へ改稿。体系の二分法の普遍性までは問わない。',explanation_review='大学公開論文の導入・先行研究検討本文を取得し4肢・4解説を照合。従来分類で捉えきれない用法の留保も反映。',unresolved='',multiple_correct_risk='なし：2のみ代表的用法の存在に一致',no_correct_risk='なし：独立正答2')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S60 | 孫聴雨 [使役受身構文の意味と形式―BCCWJに基づく記述的分析―](https://ir.library.osaka-u.ac.jp/repo/ouka/all/102191/gbkp_2024_r.pdf) 大阪大学公開論文集 | PDF9–12頁の導入・先行研究検討を本文取得。強制と感情・思考の生起の用法、従来分類では捉えきれない用法の存在を確認。原著の日本語記述文法研究会等は引用先として扱い、未取得原著の直接照合を主張しない。 | Q_5_056 |\n')
print('Recorded',len(extra),'repairs')
