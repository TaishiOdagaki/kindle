"""Recover unsaved batch119 from review history, against saved batch118 only."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2625
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第118バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢をCEFR2001とCambridge公式TKTの本文へ独立照合。Q_O_010は現行ケース2全3段落と設問の仮定条件を確認。',explanation_review='全4解説の目的・評価主体・参照先を区別。診断と形成、総括とピア評価の併存を排除しない。CEFRは2001年版の章節を明示し、文法や母語話者との比較を全面禁止するものとしない。',unresolved='',multiple_correct_risk='なし：明示した問いに独立正答'+str(key)+'のみ適合',no_correct_risk='なし：独立正答'+str(key))
k='Q_O_010';exps=a['A_O_010']['txt'].copy()
exps[3]='診断的評価は強みや弱みを把握して指導に役立てるもので、開始前に限られません。この場面でも診断的な情報が得られ得ますが、その情報を途中の指導調整に使うという目的は形成的評価に対応するため、「診断的評価のみ」と限定する肢は合いません。'
review(k,q[k]['stem'],q[k]['opts'],exps,1,['S183','S179'],
'TKT Assessmentの診断・形成・総括とCEFR9.3.2・9.3.5を照合。ケース2全3段落と追加仮定を確認。診断は開始前だけで途中の形成と区別されるという元解説4を修正し、診断的情報と形成的利用の併存を認める。その他の肢・解説も独立照合。',
['正：学習途中の情報を指導の調整に戻す目的','誤：成績の総括より途中の指導調整を問う','誤：集団との比較という参照先だけでは目的の説明にならない','誤：診断的情報はあり得るが形成的利用があり診断のみとはいえない'])
k='Q_M_030';opts=q[k]['opts'].copy();opts[0]='総括的評価（成績を総括する評価）';opts[2]='診断的評価（強みや弱みを把握する評価）';opts[3]='自己評価（自分の学習や言語使用の評価）'
exps=a['A_M_030']['txt'].copy()
exps[0]='総括的評価は成績などをまとめる目的に着目した名称です。誰が評価するかを直接表す名称ではなく、ピア評価の結果を総括に用いる可能性まで排除するものではありません。'
exps[2]='診断的評価は強みや弱みを把握し、その後の指導に役立てる目的に着目します。開始前だけに限られず、学習者同士かどうかという評価主体を直接表す名称ではありません。'
exps[3]='自己評価では学習者が自分の学習や言語使用を評価します。設問は学習者同士が互いの発表や作品を評価する場合を問うため、自己評価という名称とは合いません。'
review(k,q[k]['stem'],opts,exps,2,['S183'],
'TKT AssessmentのPeer/Self/Diagnostic/Summativeの各定義を本文と画像へ照合。診断を開始前に限定する括弧書きを修正。評価目的と主体を区別し、総括・診断と相互評価の併存を排除しない。対照分析の選択肢は同じ評価領域の自己評価に差し替え、未照合の理論定義を補助主張にしない。',
['誤：総括は目的で評価主体の名称ではない','正：学習者同士の相互評価を指す','誤：診断は目的で主体の名称ではない','誤：自己の評価と相互の評価は異なる'])
k='Q_1_039'
review(k,'CEFR（2001年版）の言語教育の考え方と共通参照レベルに関する記述として、最も適切なものを一つ選びなさい。',q[k]['opts'],[
'1.3節は、理想的な母語話者を最終モデルとして各言語を別々に習得するという目標から、複数の言語経験を生かすレパートリーの発達へ視点を広げています。母語話者だけを唯一の目標とする肢は合いません。',
'3.3〜3.4節の尺度・記述文は、言語活動で何ができるかを示し、教師やカリキュラム作成者の目安にもなります。抽象的な性格の判定だけに使い、具体的な活動や教材開発には全く適さないとする説明は合いません。',
'2.1節は、学習者・言語使用者を社会的な行為者と捉え、状況の中で能力を用いて課題に取り組む枠組みを示します。文法や語彙の知識だけに限定しませんが、個々の学習目的で文法等に焦点を当てることを禁止するものでもありません。',
'3.2節の図1ではAをBasic User、BをIndependent User、CをProficient Userとし、それぞれを二分したA1〜C2を示します。これは2001年版の共通参照レベルであり、目的に応じた下位区分や記述の調整を禁じるものではありません。'],4,['S179'],
'CEFR2001の1.3節印刷4〜5、2.1節9〜10、3.2図1・3.3・3.4冒頭23〜25を本文・画像照合。2001年版という範囲を明示し、全版の下位区分を6段階だけに固定する誤解を避ける。複言語理念と課題遂行を、文法の学習・評価を全面禁止するものとしない。',
['誤：理想母語話者を唯一の最終モデルとする','誤：具体的言語活動の記述や教育への利用を全面否定','誤：文法・語彙の知識量だけへ限定','正：2001年版図1のA/B/CとA1〜C2に対応'])
assert len(extra)==12,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch119.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];meta=[]
for sid,name,url,scope in [('S179','cefr.pdf','https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf','CEFR2001printed4-5/PDF13-14,9-10/PDF18-19,23-25/PDF32-34 text and image review;3.2Figure1,3.3,3.4opening; prior9.3.2 and9.3.5 reused'),('S183','tkt.pdf','https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf','TKT Assessment printed4-5/PDF5-6:Peer/Self/Diagnostic/Formative/Summative; prior batch118 full entry text/image review reused')]:
 raw=(root/name).read_bytes();meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_read_scope=scope,retrieved='2026-10-16',full_source_redistributed=False))
(b.OUT/'evidence/batch119_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('3 questions/12 edits recovered')
