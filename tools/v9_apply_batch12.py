#!/usr/bin/env python3
"""Repair no-answer premise and unrestricted you-ni-naru analysis."""
import json,html
from docx import Document
from docx.oxml.ns import qn
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==249
_,Q,A=qa.audit(str(b.DST));doc=Document(b.DST);extra=[]
def change(k,f,i,new,why,s):
 old=Q[k]['opts'][i] if f=='options' else A['A_'+k[2:]]['txt'][i]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=f,index=i,before=old,after=new,reason=why,sources=s,applied=True,before_version='第11修正バッチ作業稿'))
def full(k,stem,opts,exps,why,s):
 ps=doc.paragraphs;start=next(i for i,p in enumerate(ps) if any(t.get(qn('w:name'))==k for t in p._p.iter(qn('w:bookmarkStart'))));old=[]
 for p in ps[start+1:]:
  if p.text.startswith('1. '):break
  if p.text:old.append(p.text)
 assert ' '.join(old)==html.unescape(Q[k]['stem'])
 extra.append(dict(id=k,field='stem',index=None,before=old[0],after=stem,reason=why,sources=s,applied=True))
 for t in old[1:]:extra.append(dict(id=k,field='stem_continuation',index=None,before=t,after='',reason='全文改稿に伴い旧場面・例文段落を除去。',sources=s,applied=True,remove_paragraph=True))
 for f,ts in [('options',opts),('explanations',exps)]:
  assert len(ts)==4
  for i,t in enumerate(ts):change(k,f,i,t,why,s)
full('Q_4_079','許可を求める表現のロールプレイで、教師Tは「Bさんはスマホを使う許可を求める役、私は許可するか判断する役です。まず自分で質問を考えて言ってください」と指示した。Bが話し始める前に、Tは間を置かず「『スマホを使ってもいいですか』と言います」と質問のモデルを示した。Bが「スマホを使ってもいいです」と言うと、Tは「今は許可を求める質問です。最後に『か』を付けて、『スマホを使ってもいいですか』と言います」と訂正した。この発話記録の分析として、適切なものはどれか。',[
'Bが質問の形を言わなかった原因は、スマホという語彙を未習であることだけだと、この記録から確定できる。',
'Tは自分で質問を作るよう求めたが、Bの最初の発話前に完全な質問のモデルを与えている。また、最後の応答は質問の形を明示する訂正である。',
'Tは指示の後、モデルを示すまでに少なくとも3秒間待ったことが、記録に明示されている。',
'Tの最後の応答は、問題点を説明せずに暗示的に言い換えるだけのリキャストである。'],[
'この記録に語彙の未習を示す情報はなく、誤りの原因を語彙だけに確定できません。また、役割を指定しているので、ここでは許可を与える応答ではなく、許可を求める質問を作る課題です。',
'記録では自力で質問を作る指示の後、Bが話す前に教師が完全なモデルを提示しています。モデル提示自体を常に不適切とする一般論ではなく、この指示と手順の関係を読み取ります。最後には質問であることと「か」を明示し、正しい形を提示しています。',
'記録は「間を置かず」と明記しており、3秒以上待ったという情報はありません。通常の文字化記録に時間情報がなければ、待ち時間の長さを推測で確定することもできません。',
'教師は「許可を求める質問」「最後に『か』を付けて」と問題点を説明し、正しい形を示しています。誤りを明示しないリキャストだけとする分析は、この記録に合いません。'],
'旧発話では教師から許可を求められた学習者の応答が正用になり得た。役割・課題・モデル提示前の時間条件を明記し、誤用原因の推測や効果の保証を撤去。',['S46','S37'])
(b.OUT/'changes_batch12.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D['Q_4_079'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S46','S37'],option_verdicts=['語彙未習を示す情報がなく単一原因の確定は不可','明示された指示と発話順、問題点の明示と正用提示に一致','記録の時間条件と不一致','問題点を説明し正用を示しており暗示的言い換えだけではない'],stem_review='許可を求める側と与える側の役割、独立発話の課題、モデル提示までの間がない条件を明記。',explanation_review='許可要求と許可付与をJF公式教材、明示的訂正とリキャストの区別をLyster/Ranta原論文に照合。効果や誤用原因を記録外から推定しない。',multiple_correct_risk='なし：役割と観察可能な発話条件を明示',no_correct_risk='なし：独立正答2',unresolved='');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(extra),'repairs.')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S46 | 国際交流基金 [文型練習教材 Vてもいいです](https://www.jpf.go.jp/j/urawa/j_rsorcs/textbook/setsumei_pdf/setsumei06_2.pdf) | 公式PDF全2頁（印刷76–77）。許可を求めるVてもいいですかと、許可を与える表現を本文確認。旧JLPT級への記載を現行試験情報として使わない。 | Q_4_079 |\n')
