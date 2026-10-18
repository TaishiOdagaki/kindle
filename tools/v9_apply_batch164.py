"""Independent source-limited task design and reflective review audit."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3263
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data={
'Q_O_052':(4,['S144'],'ケース11のB教師の活動に、使う表現を固定せず、依頼内容を伝えて相手が引き受けられるかを確かめる目標を加える。Richards（2006）のタスクの説明に照らし、この活動と事後の言語整理の流れに合うものを一つ選べ。',[
'依頼の意味が伝わったかは問わず、指定された文を一字一句正確に再生することだけを達成目標とする。',
'言語形式を一切扱ってはならないので、活動後に表現を確認する段階は必ず除く。',
'新しい文型の提示と統制された練習を先に行うPPPの順序を、そのまま実施したと判断する。',
'既有の言語資源で意味のある依頼を行い、その経験を基に必要な言語表現を振り返る構成と捉える。'],[
'Richardsは、意味への焦点と、言語の学習だけではない成果をタスクの特徴に挙げます。指定文の再生だけを目標にすると、設問で加えた依頼内容の伝達と応諾の確認を達成目標として扱えません。',
'同書は、タスクの遂行を基に言語への意識や言語の発達を扱う説明を示しています。活動後に表現を確認することまで一律に禁止する説明ではありません。',
'同書のPPPの説明は、新しい形式の提示、統制された練習、異なる文脈での使用という順序です。この設問はまず依頼を行い、その後に表現を整理するため、そのまま同じ順序とは言えません。',
'同書31–32頁の、既有の言語資源を使い意味と成果を重視するタスクの説明に対応します。B教師の事後整理は、活動で必要になった言語へ注意を向ける機会として捉えられます。ロールプレイという名称だけでタスクと判定したり、気づきや習得が必ず起こると保証したりするものではありません。'],
'S144 Richards2006著者公開冊子の印刷14–16・31–35頁本文、15・31–33頁画像を再取得・照合。Q_O_052ではケース本文にない成果条件を推測せず、使用表現非固定・依頼伝達と応諾確認の目標を設問の追加条件として明記。Richards自身のタスク概説・PPP順序の比較に限定し、ロールプレイであればタスクという同一視と気づき・習得の効果保証を避ける。引用されるWillis等の全原著の独立検証ではない。'),
'Q_O_055':(3,['S144'],'ケース11の活動を選ぶ際、Richards（2006）の正確さと流暢さを扱う活動の説明に合う方針を一つ選べ。',[
'意味を伝える活動を入れるなら、学習者の言語使用に問題が見られても、その後の形式面の練習をすべて除く。',
'どの活動も同じ働きをするので、何をできるようにするかを考えず、教師の好みだけで選ぶ。',
'正確さと流暢さの目標を区別し、活動で見られた課題に応じて形式面の練習や意味を伝える活動を関連付ける。',
'正確さを扱う活動は必ず流暢さの活動より前に置き、後から扱うことは認めない。'],[
'同書は、流暢さを重視する活動にも、準備や言語使用への事後のフィードバックに注意が必要だと述べます。意味を伝える活動を入れたという理由だけで、その後の形式面の練習を全排除する方針ではありません。',
'同書は正確さを重視する活動と流暢さを重視する活動の焦点を区別します。活動の働きや目標を検討せず、すべて同じとして教師の好みだけで選ぶ説明は、この区別を無視しています。',
'同書15–16頁は、両方の活動を組み合わせ、正確さを扱う活動で流暢さを扱う活動を支える考え方を示します。活動中に観察した文法・発音の課題を後の練習で扱う例もあります。目標と観察に基づく選択であり、教授法を混ぜるだけで効果が保証されるという主張ではありません。',
'同書15頁は、正確さを扱う活動が流暢さを扱う活動の前にも後にも置かれ得ると説明します。必ず前に置くという一律の順序制限は合いません。'],
'S144 Richards2006印刷14–16頁の活動比較・相互支援と前後両方の順序を本文照合。旧問の折衷的アプローチが実践上有効という包括的効果説明を撤回し、正確さ・流暢さの目標と観察された課題に基づく活動選定へ改訂。全教授法の混合や学習者全員への効果を承認するものではない。'),
'Q_MO_004':(3,['S213'],'この教師の同僚との相談を、RFCDC第1巻の批判的な自己理解の観点から進める場合、最も適当な行為を一つ選べ。',[
'学習者が理解できるはずだという自分の前提は検討せず、相談を終える。',
'同僚から一つの助言を得た時点で、教材や活動を見直す必要はなくなったと決める。',
'学習者の反応と自分の見立てを照らし、前提や判断の限界を同僚と点検して、教材・活動の見直しを検討する。',
'原因について考え直す必要はないとして、教材と活動を今後一切変更しないと決める。'],[
'RFCDCは、自分の見方の前提や先入観を理解し、それらが判断に及ぼす影響を捉えることを挙げます。理解できるはずだという前提を検討から除く行為は、この観点に合いません。',
'批判的理解は、能動的な振り返りと評価を伴うものです。助言を一度得たという事実だけで見直しを不要とする説明ではありません。同僚への相談自体が改善を保証するわけでもありません。',
'RFCDCの52–53頁は、自分の前提や偏り、それらが判断に及ぼす影響、自分の力量の限界を理解することを示します。ケースの学習者の反応と教師の見立てを照らす行為に、この観点を適用したものです。相談や変更の効果を確定した説明ではありません。',
'RFCDCは批判的理解を、自動的・習慣的・無反省な解釈と区別します。原因を考え直さず今後の変更も初めから拒否する行為は、振り返って見直すという説明に合いません。'],
'S213 RFCDC第1巻52–53頁のKnowledge and critical understanding of the selfの全6項目と導入本文を取得済みPDFで照合し両頁画像を確認。原バイトSHA256は第156バッチと一致。旧問の包括的な名称当てと未照合のコーパス・誤用・対照分析の定義を、この問から除き、同じ授業後の自己点検領域の具体的行為を問う設問へ改訂。RFCDCは授業分析という技法名を定義する資料ではないためその定義の根拠に代用せず、自己理解の観点のケースへの適用として明示する。')}
extra=[]
for k,(key,sources,stem,opts,exps,reason) in data.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第163バッチ反映後',block_context=ak if field=='explanations' else k)
   assert c['before']!=new
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==key else '誤')+'）'
   extra.append(c)
 verdicts={'Q_O_052':['誤：意味と成果の条件を指定文の再生に置換','誤：活動後の言語整理を全禁止','誤：提示先行の順序と同一視','正：既有資源で遂行し言語を振り返る設計'], 'Q_O_055':['誤：形式面の練習を全排除','誤：正確さ・流暢さの焦点の違いを無視','正：目標と観察に応じた両活動の関係付け','誤：前後両方が可能な順序を前だけに限定'], 'Q_MO_004':['誤：自分の前提を検討から除く','誤：一度の助言で見直し不要と断定','正：前提と判断の限界を振り返る適用','誤：無反省で変更を一切拒否']}[k]
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='全4肢を指定した取得本文とケースの明示情報へ独立照合。追加の目標は設問の条件であることを明記し、元ケースの事実として推測しない。',explanation_review='各4解説の根拠・適用範囲を照合。効果の保証や未取得原著・他の技法定義を承認せず、記述された枠組みのケースへの適用と区別。',unresolved='',multiple_correct_risk='なし：独立正答'+str(key)+'のみ条件に一致',no_correct_risk='なし：独立正答'+str(key))
assert len(extra)==27
for name,obj in [('changes.json',cs+extra),('changes_batch164.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];e=[]
for sid,fn,url,scope in [('S144','richards164.pdf','https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','2006年著者公開冊子52頁を再取得。印刷14–16・31–35・45頁本文を精読、15・31–33頁画像。引用先Willis等の全原著と介入効果の独立検証は未実施。'),('S213','rfcdc150.pdf','https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c','取得済みPDFの52–53頁本文・全6項目、両頁画像、47頁批判的思考本文を確認。第156バッチ原バイトSHA256と一致。授業分析という技法名の定義資料ではない。')]:
 raw=(root/fn).read_bytes();h=hashlib.sha256(raw).hexdigest()
 if sid=='S213':assert h=='a93866bccc575a825b4cc9e9b5f25c115d7c1ffd29dc677a1acc0aa226daa612'
 e.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=h,checked='2026-10-18',read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch164_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('3 questions /27 changes /keys4,3,3')
