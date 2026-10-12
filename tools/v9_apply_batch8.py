#!/usr/bin/env python3
"""One-time repair of feedback premises using the author-published original."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==176
_,Q,A=qa.audit(str(b.DST));extra=[]
def change(k,f,i,new,why,s):
 old=Q[k]['stem'] if f=='stem' else Q[k]['opts'][i] if f=='options' else A['A_'+k[2:]]['txt'][i]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=f,index=i,before=old,after=new,reason=why,sources=s,applied=True,before_version='第7修正バッチ作業稿'))
k='Q_4_067';s=['S28','S37'];why='そしてによる自然な接続を誤用とする前提を撤回し、明示的な誤り指摘なしのタ形への言い換えを設定。原論文の4分類と照合。'
change(k,'stem',None,'動詞「見る」のタ形を使って昨日の行動を報告する練習で、学習者が「昨日、友達と映画を見ます」と言った。教師は誤りを明示的に指摘せず、「昨日、友達と映画を見たんですね」と言い換えた。この教師の応答をLysterとRantaの分類で捉えると、最も適切なものはどれか。',why,s)
# The source stem consists of three Word paragraphs; the parser joins them.
from docx import Document
ps=Document(b.SRC).paragraphs
extra[-1]['before']=ps[1422].text
for j in [1423,1424]:extra.append(dict(id=k,field='stem_continuation',index=None,before=ps[j].text,after='',reason='全面改稿後の旧事例2段落を除去。',sources=s,applied=True,remove_paragraph=True))
change(k,'options',1,'メタ言語的フィードバック',why,s)
for i,t in enumerate([
 '明確化要求は、発話の聞き取り・理解又は形式の問題を示し、繰り返しや言い直しを求めるものです。この応答は聞き返しではなく、教師が修正した形を提示しています。',
 'メタ言語的フィードバックは、正しい形を直接提示せず、発話の適切さについて情報や質問を与えるものです。この教師は「見た」という形を直接提示しています。',
 '明示的訂正では、誤りであることを明確に示し、正しい形を提示します。本問の教師は誤りを明示的には指摘していません。',
 '教師は、学習者の発話の一部を修正した形で言い換えています。「見る」のタ形は「見た」です。誤りを明示的に指摘しない言い換えという条件から、ここではリキャストに当たります。']):change(k,'explanations',i,t,why,s)
change('Q_M_034','stem',None,'学習者の誤りを含む発話に対し、教師が「その言い方は誤りです」などの明示的な指摘をせず、誤りを取り除いた形で発話の全部又は一部を言い換えて示す。この訂正方法を指す用語として最も適当なものを選べ。','正しい形の提示だけでは明示的訂正も含むため、誤りの明示的指摘なしという条件を追加。',['S37'])
change('Q_M_034','explanations',3,'リキャストは、学習者の発話の全部又は一部を、誤りを取り除いた形で言い換えて示す方法です。本問では誤りを明示的に指摘しないことも条件にしています。正しい形を示すだけでは、明示的訂正との区別が十分ではありません。','リキャストと明示的訂正の区別に必要な条件を明示。',['S37'])
(b.OUT/'changes_batch8.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D[k].update(status='確認済み',fixes_applied=True,independent_answer=4,sources=s,option_verdicts=['言い直しを求めておらず不一致','正しい形を提示する点で不一致','明示的な誤り指摘がない点で不一致','修正した形で暗示的に言い換える条件に一致'],stem_review='タ形練習と教師の暗示的な言い換えを明示して4肢を再判定。',explanation_review='4分類を原著印刷頁46–48に、見たをJF教材に照合。',multiple_correct_risk='なし：明示的指摘の有無と正用形提示で分類を区別',no_correct_risk='なし：独立正答4',unresolved='')
D['Q_M_034'].update(fixes_applied=True,sources=['S37'],unresolved='リキャストの条件を修正。コードスイッチング・プロンプト・ダイグロシアと全解説の原資料照合が残る。')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(extra),'repairs.')
