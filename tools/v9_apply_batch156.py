"""One-time source-bounded empathy and ethnocentrism rejudgment."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3114
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_1_001':dict(answer=1,
stem='欧州評議会のRFCDC第1巻（2018年）用語集に示された、自文化中心主義（エスノセントリズム）の説明に合うものを一つ選びなさい。',
opts=['自文化を中心的な尺度として他文化を評価し、自集団のやり方を他集団より優れたものとみなす見方である。']+q['Q_1_001']['opts'][1:],
exps=['用語集73頁は、自文化を中心に据えて他文化をその尺度で評価する見方と、自集団のやり方が優れているとする偏見を説明しています。無意識であることを定義の必須条件にはしていません。',
'この肢は自文化を捨てて相手の文化へ吸収される過程を述べています。73頁の自文化中心主義の定義は、自文化を尺度に他文化を評価する見方であり、この過程を指すものではありません。',
'この肢は他国の文化を本質的に優れているとみなす方向の評価です。73頁が説明する、自集団のやり方を他集団より優れているとみなす偏見とは評価の方向が逆です。',
'この肢は相手の文化の基準や文脈に沿って理解しようとする姿勢です。73頁の自文化中心主義が説明する、自文化を中心的な尺度として他文化を評価する見方とは異なります。'],
verdicts=['正：73頁の自文化を中心とした尺度と自集団優位の記述に対応','誤：自文化の破棄・吸収過程は、73頁の自文化を尺度とする評価の定義ではない','誤：他文化の本質的優位は、73頁の自集団優位の偏見と方向が逆','誤：相手の基準・文脈に沿う姿勢は、73頁の自文化を尺度とする定義とは異なる'],
reason='S213 RFCDC第1巻用語集73頁のEthnocentrism項全体を本文・画像照合。指定資料に定義を限定し、正答の無意識・絶対的という必須条件化を除去。誤答2–4の本文は維持し、定義との相違を各解説で直接説明する。未取得の同化・文化自卑・文化コンプレックス・文化相対主義の別概念の定義を承認したものではなく、その名称による断定を解説から削除。BennettのDMIS原著や各発達段階を独立取得・承認したものでもない。'),
'Q_M_038':dict(answer=2,
stem='欧州評議会のRFCDC第1巻（2018年）のモデルにおけるエンパシー（共感）の説明として、適当なものを一つ選べ。',
opts=['相手と同じ感情が自分に生じる現象だけを指し、相手の考えや信念を理解する技能は含めない。',
'自分の見方からいったん距離を取り、相手の考え・信念・感情を相手の視点から理解し関わるための技能を指す。',
'相手の知覚・考え・信念の理解は含むが、相手の感情や必要の理解は共感の範囲から除外する。',
'相手への思いやりや気遣いは、このモデルでは共感のどの形態にも位置付けられていない。'],
exps=['49頁の注10は、同じ感情が生じる情動伝染など、共感という語の日常的な使い方にも触れています。ただし、このモデルは他者の考え・信念・感情を理解し関わるための技能として共感を位置付けており、情動伝染だけには限定しません。',
'48頁と用語集73頁は、自分の視点から距離を取り、他者の心理的な枠組みや視点を理解する技能として共感を説明します。相手の考えや信念を捉える認知的な視点取得と、感情や必要を捉える情動面の視点取得も含まれます。',
'48–49頁と用語集73頁には、他者の知覚・考え・信念を理解する形態に加え、感情・気持ち・必要を理解する形態も示されています。感情や必要の理解を範囲から除く点が誤りです。',
'49頁と用語集73頁は、相手の状態や事情の理解に基づく思いやり・気遣いをsympathyとして共感の一形態に含めています。他の研究で共感と同情をどう区別するかとは分けて、このモデルの分類に従って判断します。'],
verdicts=['誤：49頁注10の用法の多様性を、モデルの情動伝染だけという定義へ取り違える','正：48頁・73頁の脱中心化、相手の心理的枠組みと視点、考え・信念・感情を理解する技能に対応','誤：48–49頁・73頁は認知的と情動面の視点取得の双方を含む','誤：49頁・73頁はsympathyを共感の一形態に含める'],
reason='S213 RFCDC第1巻48–49頁のEmpathy項と注10、および用語集73頁のEmpathy項全体を本文・全頁画像で照合。日常語・科学的用法の多様性が明記されているため、全心理学共通の定義にせず当該モデルへ限定。元の用語当てから共感の内容・範囲を問う同領域の4択へ改訂し、情動伝染への限定、情動面の視点取得の排除、sympathyの排除を各誤答とした。旧肢のコーパス／ステータス・プランニングと統語論の定義を取得済みと見なして承認する処理は行わない。')}
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and int(a[ak]['ans'])==v['answer']
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=['S213'],applied=True,before_version='第155バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==v['answer']-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['answer'],fixes_applied=True,sources=['S213'],reason=v['reason'],option_verdicts=v['verdicts'],candidate_answers=[],stem_review='RFCDC2018第1巻のモデル・用語集の説明と明記し、設問と全4肢を指定本文へ独立照合。一般心理学の定義や未取得の引用先原著へ拡張しない。',explanation_review='全4解説の補助的主張も指定本文と照合。Q_1_001は73頁、Q_M_038は48–49頁と注10・73頁。旧解説の未照合の別概念の定義は削除。',unresolved='',multiple_correct_risk='なし：指定資料の定義に合うのは'+str(v['answer'])+'のみ',no_correct_risk='なし：独立正答'+str(v['answer']))
assert len(extra)==15
for n,obj in [('changes.json',cs+extra),('changes_batch156.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'rfcdc156.pdf').read_bytes()
e=[dict(source_id='S213',url='https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c',title='Reference Framework of Competences for Democratic Culture, Volume 1: Context, concepts and model',year=2018,retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=89,read_scope='書誌・著作権頁・著者チーム、47–49頁全文（Empathy項・注10を含む）、用語集73頁全文と74頁を精読。48・49・73頁（PDF50・51・75頁）を1800px全頁画像照合。',limitations='全89頁精読ではない。RFCDCモデル自身の説明の一次資料として使用し、心理学全分野の共通定義やBennett等の引用先原著の独立承認ではない。原PDF非転載。',full_source_redistributed=False)]
(b.OUT/'evidence/batch156_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 15 edits / keys1,2 retained')
