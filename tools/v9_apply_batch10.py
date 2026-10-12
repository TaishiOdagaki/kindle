#!/usr/bin/env python3
"""Repair no-answer premise and unrestricted you-ni-naru analysis."""
import json,html
from docx import Document
from docx.oxml.ns import qn
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==215
_,Q,A=qa.audit(str(b.DST));doc=Document(b.DST);extra=[]
def change(k,f,i,new,why,s):
 old=Q[k]['opts'][i] if f=='options' else A['A_'+k[2:]]['txt'][i]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=f,index=i,before=old,after=new,reason=why,sources=s,applied=True,before_version='第9修正バッチ作業稿'))
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
full('Q_5_008','第二言語学習者の誤用の原因を分析する際、母語と目標言語の対照、および目標言語内の規則学習をどのように考えるべきか。Richardsの誤用分析の議論に照らして、適切なものはどれか。',[
 '母語の影響を検討する対照分析は有用だが、目標言語内の規則の過剰般化なども検討し、全ての誤用を母語干渉だけで説明しない。',
 '学習者の誤用は全て母語の構造だけから生じるため、目標言語内の規則の学び方を検討する必要はない。',
 '目標言語の規則の過剰般化による誤用は、必ず特定の一つの母語を持つ学習者だけに生じ、異なる母語の学習者には共通して生じない。',
 '母語と目標言語の相違点を比較すれば、個々の学習者が実際に生む全ての誤用とその原因を、それ以外の資料なしで確定できる。'],[
 'Richardsは母語からの干渉を重要な要因として認めつつ、異なる母語の学習者にも見られる目標言語内の規則学習に関わる誤用を区別しています。母語の対照だけに原因を限定しないことが適切です。',
 '誤用の原因を母語の構造だけに限定する説明は、目標言語内の規則学習に関わる誤用を扱えません。学習者が規則をどのように一般化したかなども検討します。',
 '目標言語内の規則の一般化に関わる誤用は、母語が異なる学習者にも生じ得ます。必ず一つの母語の学習者だけに生じるという限定は誤りです。',
 '対照分析には母語の影響を検討する役割がありますが、全ての誤用を説明できるとは限りません。実際の誤用資料や、学習・指導の過程に関わる要因を検討する必要があります。'],
 '旧正答は代名詞/必須補語と解説の対比/主語が不一致で、正答が成立しない。自然な接続や主語反復を無条件に誤用とする例を撤去し、原著の母語干渉と目標言語内誤用の区別に全面改稿。',['S29'])
full('Q_4_069','学習者Aは、以前は理解して読めなかった日本語の新聞を、今は理解して読めるようになったという能力の変化を述べようとしている。Aが「日本語の新聞が読むようになりました」と言うと、教師は「その意味なら、『読む』ではなく『読める』です。『日本語の新聞が読めるようになりました』と言います」と答えた。Aはそのモデルを繰り返した。この場面の分析として、適切なものはどれか。',[
 '教師は正しい形を一切提示しておらず、学習者が教師のモデルを使わずに自分だけで正しい形を作った。',
 '「〜ようになる」にはどの用法でも可能形だけが接続するため、習慣の変化を表す「手伝うようになった」も誤りである。',
 '教師は誤りを明示的に指摘せずに言い換えただけなので、この応答はリキャストである。',
 '能力の変化というAの意図に合わせて「読める」を提示している。また、元の形を明示的に退けて正しい形を示しているため、明示的訂正に当たる。'],[
 '教師は「読める」と正しい形を直接提示し、学習者はそのモデルを繰り返しています。モデルを使わない学習者自身の修正という説明は、この記録に一致しません。',
 '「〜ようになる」は習慣の変化にも使え、辞書形による「手伝うようになった」などもあります。全ての用法で可能形だけに接続するという限定は誤りです。',
 '教師は「『読む』ではなく『読める』です」と元の形を明示的に退け、正しい形を提示しています。暗示的な言い換えだけではありません。',
 '本問では能力の変化という意味を明示しており、「読めるようになった」がその意図に合います。教師の応答は元の形の明示的な指摘と正用形の提示を含むため、明示的訂正と分析できます。'],
 '能力の変化を述べる条件を明示し、ようになるには常に可能形が必要という一般化を撤回。辞書形による習慣変化も認め、教師の明示的訂正とモデル反復を区別。',['S43','S44','S37'])
(b.OUT/'changes_batch10.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
for k,v,s in [('Q_5_008',1,['S29']),('Q_4_069',4,['S43','S44','S37'])]:
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=v,sources=s,option_verdicts=[('設問条件と原資料に一致' if i==v else '改訂解説で特定した限定又は観察事実に不一致') for i in range(1,5)],stem_review='旧誤用例・曖昧な場面を撤去又は能力変化の条件を明示し、4肢を独立判定。',explanation_review='4解説をRichards原著、JFの文型解説又はLyster/Rantaの分類に照合。',multiple_correct_risk='なし：全4肢を新条件で再判定',no_correct_risk='なし：独立正答が存在',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(extra),'repairs.')
