#!/usr/bin/env python3
"""One-time evidence-based repairs; rebuild with v9_rebuild.py afterwards."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==122
_,Q,A=qa.audit(str(b.DST));extra=[]
def full(k,stem,opts,exps,why,sources):
 for f,old,new in [('stem',[Q[k]['stem']],[stem]),('options',Q[k]['opts'],opts),('explanations',A['A_'+k[2:]]['txt'],exps)]:
  assert len(old)==len(new)
  for i,(x,y) in enumerate(zip(old,new)):
   x=html.unescape(x)
   if x!=y:extra.append(dict(id=k,field=f,index=None if f=='stem' else i,before=x,after=y,reason=why,sources=sources,applied=True,before_version='第4修正バッチ作業稿'))
full('Q_3_019','学習者は「書く→書いた」などから、グループ1の「く」で終わる動詞のタ形は「く」を「いた」に変えると学んだ。次のうち、その規則を例外にまで適用した過剰般化の例はどれか。',[
 '「見る」のタ形を「見た」とした。',
 '「閉める」のタ形を「閉めた」とした。',
 '「来る」のタ形を「来た（きた）」とした。',
 '「行く」のタ形を「行いた」とした。'],[
 '「見る」はグループ2の動詞であり、「る」を除いて「た」を付ける「見た」は正用です。設問の「く→いた」の規則を過剰に適用した例ではありません。',
 '「閉める」はグループ2の動詞であり、「閉めた」は正しいタ形です。この例ではグループ1の「く→いた」の規則は適用されていません。',
 '「来る」はグループ3の動詞であり、タ形は「来た（きた）」です。正しい形であり、過剰般化による誤用ではありません。',
 '「行く」のタ形は例外的に「行った」となります。「く→いた」の規則を例外にも適用した「行いた」は、設問で示された学習済み規則の適用範囲を越えた例です。日本語例はRichardsの概念を用いて本監査で構成したものです。'],
 '選択肢1も過剰般化になり得たため、学習した規則を明示し正用3例と例外への過剰適用1例に全面改稿。',['S28','S29'])
full('Q_4_112','会話分析では、修復のきっかけを作る人と、修復を行う人を区別する。「自己」は問題となった発話の話し手、「他者」はそれ以外の会話参加者を指す。この区別について、正しい説明はどれか。',[
 '相手が「え？」と聞き返した後、元の話し手が自分の発話を言い直すのは、他者始動・自己修復である。',
 '元の話し手が自分で修復を始め、自分で言い直すのは、他者始動・自己修復である。',
 '修復を始めた人と修復を行う人は必ず同一なので、自己始動・他者修復という組合せはない。',
 '会話分析の修復は文法的な誤りの訂正だけを対象とし、聞き取りや理解の問題は対象としない。'],[
 '修復の開始を促したのは相手であり、実際に自分の発話を言い直したのは元の話し手です。始動と修復の実行者を分けると、他者始動・自己修復に当たります。',
 '修復を始めた人も言い直した人も元の話し手なので、自己始動・自己修復です。他者始動と呼ぶのは、元の話し手以外がきっかけを作る場合です。',
 '始動する人と修復を行う人は別になることがあります。原論文は、話し手が名前を思い出せずに修復を始め、相手がその名前を補う自己始動・他者修復の例も示しています。',
 '修復は、話すこと、聞くこと、理解することに関わる問題を扱います。文法的な誤りが見当たらない場合にも修復が生じ得るため、文法訂正だけに限定する説明は誤りです。'],
 '旧選択肢2も他者始動の自己修復であり正しい。始動と実行の2軸を明示して複数正答を解消し、選好を相手の顔を守りたいという動機に還元する旧解説を除去。',['S31'])
(b.OUT/'changes_batch5.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
for k,answer,s in [('Q_3_019',4,['S28','S29']),('Q_4_112',1,['S31'])]:
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=answer,sources=s,option_verdicts=[('本文の条件と資料に一致' if i==answer else '改訂解説に示した条件又は定義と不一致') for i in range(1,5)],stem_review='独立に全選択肢を再判定。規則又は始動・実行者を明示。',explanation_review='4解説をJF教材・Richards原著又はSchegloffら原著の該当本文と照合。',multiple_correct_risk='なし：全4選択肢の条件を区別',no_correct_risk='なし：独立正答が存在',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print('Recorded',len(extra),'repairs.')
