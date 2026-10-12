#!/usr/bin/env python3
"""One-time repair of viewpoint and paired-verb examples."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==140
_,Q,A=qa.audit(str(b.DST));extra=[]
def full(k,stem,opts,exps,why,sources):
 for f,old,new in [('stem',[Q[k]['stem']],[stem]),('options',Q[k]['opts'],opts),('explanations',A['A_'+k[2:]]['txt'],exps)]:
  assert len(old)==len(new)
  for i,(x,y) in enumerate(zip(old,new)):
   x=html.unescape(x)
   if x!=y:extra.append(dict(id=k,field=f,index=None if f=='stem' else i,before=x,after=y,reason=why,sources=sources,applied=True,before_version='第5修正バッチ作業稿'))
full('Q_5_065','物の授受を表す「あげる」と「くれる」について、適切な説明はどれか。各文は話し手自身の発話であり、他者の発話の引用ではない。',[
 '他者から話し手自身への物の移動を表すには、「田中さんが私に本をあげた」が基本の形である。',
 '「あげる」と「くれる」は、与え手と受け手の関係にかかわらず必ず自由に置き換えられる。',
 '「くれる」は与え手が話し手自身である場合にだけ使い、「私が田中さんに本をくれた」が基本の形である。',
 '「くれる」は、他者が話し手や話し手側の人に物を与えるときに使う。話し手側の範囲は、家族という属性だけで機械的に決まるとは限らない。'],[
 '他者から話し手自身への授受は「田中さんが私に本をくれた」のように表します。この条件では「あげた」を基本の形とする説明は適切ではありません。',
 '「あげる」と「くれる」には授受の方向と話し手との関係に違いがあります。文脈や当事者の関係を確認せずに必ず置き換えられるとする説明は誤りです。',
 '「くれる」は他者から話し手側へ向かう授受を表します。話し手から田中さんへの授受は「私が田中さんに本をあげた」のように述べます。',
 '「くれる」の基本は他者から話し手側への授受です。話し手が受け手の事柄を自分の事柄として捉えるかなど、心理的・社会的な関係と文脈も考慮します。身内が受け取る場面に「あげる」が一切使えないとする旧説明は過度の一般化でした。'],
 '弟にあげるを一律に文法違反とする前提を撤回。話し手自身を受け手にして条件を明示し、心理的距離によるウチの範囲を公式解説に対応。',['S32'])
full('Q_5_070','窓の開閉について、「開く（あく）」と「開ける（あける）」の対、および結果状態の表現を説明したものとして、正しいものはどれか。',[
 '「開く（あく）」が他動詞、「開ける（あける）」が自動詞であり、「窓を開く（あく）」「窓が開ける」が基本の形である。',
 '「開く（あく）」は自動詞、「開ける（あける）」は他動詞である。「窓が開けてある」は、誰かが開けた結果としての窓の状態を述べる。',
 '「窓が開いている」は開く動作の進行中だけを表し、開いた結果の状態を表すことはできない。',
 '意図的に開けた結果の窓の状態を「てある」で述べる場合、「窓が開いてある」が基本の形である。'],[
 '自他の分類が逆です。この対では自動詞が「あく」、他動詞が「あける」であり、「窓が開く」「窓を開ける」となります。',
 '「あく／あける」は自他の対応する対です。「窓が開けてある」は、他動詞「あける」のテ形に「ある」を付け、意図的な働きかけの結果生じた窓の状態を述べています。',
 '「窓が開いている」は、窓が開いた結果の状態を述べることができます。「ている」を動作の進行だけに限定する説明は誤りです。',
 'この結果状態を「てある」で述べるときは、他動詞を使った「窓が開けてある」が基本です。自動詞「あく」による結果状態は「窓が開いている」と表します。本問は窓の開閉という条件であり、他の構文への一律の一般化はしません。'],
 'ひらくは自他両用でありあけるとの対の読みとして不適切。あくを明示し、他動詞は必ず意志的という一般化とてあるの全用法への断定を撤回。',['S33','S34'])
(b.OUT/'changes_batch6.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
for k,answer,s in [('Q_5_065',4,['S32']),('Q_5_070',2,['S33','S34'])]:
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=answer,sources=s,option_verdicts=[('条件と公式教材に一致' if i==answer else '改訂解説に示した条件と公式教材に不一致') for i in range(1,5)],stem_review='話し手又は窓の開閉という文脈を明示し全4選択肢を独立再判定。',explanation_review='4解説をJF又は東京外国語大学の本文と照合。',multiple_correct_risk='なし：場面を限定して4肢を判定',no_correct_risk='なし：独立正答が存在',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print('Recorded',len(extra),'repairs.')
