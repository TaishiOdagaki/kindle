"""One-time review of functional syllabuses and jigsaw information exchange."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1786
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_4_020':(4,'Richards（2006）19頁のジグソー活動の説明を参考に、互いに情報を伝え合わなければ課題を完成できない活動を設計する。次の案のうち、この条件に合うものを一つ選びなさい。',[
'必要な情報をすべて一人の学習者だけに渡し、その人が回答を完成させる。他のメンバーは黙って作業を観察する。',
'全員に同一の完成済みの回答を配り、相手への質問や情報の補足は行わず、教師の後について順番に音読する。',
'全員に同じ資料を配り、各自で回答を完成させる。メンバー間で資料や考えを伝え合う時間は設けない。',
'必要な情報をメンバーに分けて渡し、各自が持つ部分を相手に伝え、情報を組み合わせて一つの回答を完成させる。'],[
'一人だけが情報を使って完成させ、他のメンバーは発話しないという条件です。互いに情報を伝え合って完成させる設問の活動には対応しません。',
'完成済みの同一回答を読む案であり、情報を補い合う必要がありません。音読そのものの有用性ではなく、今回指定した情報交換の仕組みとの適合性を判断します。',
'個別に完結する作業で、メンバー間で情報を伝える過程を設けていません。グループに座ることだけでジグソー活動になるわけではありません。',
'各自が持つ部分情報を伝えて全体を完成させる点が、Richardsのジグソー活動の説明に対応します。情報交換が必要になる設計と、実際の全員参加や習得効果の保証とは区別します。'],[
'誤：一人で完結し他者との交換がない','誤：同じ完成回答の音読のみで不足情報がない','誤：個別作業で情報を伝え合う過程がない','正：部分情報を交換して全体を完成させる']) ,
'Q_4_024':(4,'Richards（2006）11頁の「機能シラバス」の説明に合う編成方針を一つ選びなさい。',[
'依頼や謝罪などの機能ではなく、文法項目の順序を編成の基準にし、その順序だけに従って単元を配置する。',
'依頼や謝罪などの機能は単元の基準にせず、教室で学習者が遂行する作業を基準にしてタスクを並べる。',
'依頼や謝罪などの機能は単元の基準にせず、読む・書く・聞く・話す技能と、その下位技能を基準にして内容を分ける。',
'依頼や謝罪など学習者が行う言語機能を基準に内容を編成し、扱う機能に応じて語彙や文法を選ぶ。'],[
'この案の編成基準は文法項目の順序です。指定資料が述べる、学習者の行う言語機能を基準とする編成とは異なります。',
'この案は遂行する作業を編成基準としており、指定資料のタスク・シラバスの説明に対応します。タスクを基準にすることから、成果物だけを評価し過程を無視すると結論づけることはできません。',
'この案は四技能とその下位技能を基準としており、同頁の技能シラバスの説明に対応します。言語機能に応じて内容を編成する今回の条件とは区別されます。',
'指定資料は、行うべき機能に沿って編成し、それに応じて語彙や文法を選ぶと説明しています。機能シラバスでも文法は扱います。即効性や、文法体系の理解が必ず後回しになるという効果・欠点を定義には含めません。'],[
'誤：機能ではなく文法項目順序が基準','誤：機能ではなく遂行作業が基準','誤：機能ではなく技能と下位技能が基準','正：機能に応じて語彙・文法を選択'])}
extra=[]
for key,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[key]['status']!='確認済み' and int(a['A_'+key[2:]]['ans'])==ans
 reason='S144の印刷11・19頁を取得本文と画像で照合。機能シラバスの未裏付けの利点・欠点、タスクは成果物のみ評価するという誤説明、ジグソーの全員参加・習得効果の保証を除去。編成単位と部分情報を交換する仕組みを明示して独立判定。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S144'],applied=True,before_version='第82バッチ反映後の累積作業稿',block_context='A_'+key[2:] if field=='explanations' else key)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S144'],option_verdicts=verdicts,reason=reason,stem_review='取得したRichards2006の特定頁と設問条件を指定。全4肢の編成単位または情報交換の有無を独立判定し、対応するのは4のみ。',explanation_review='S144著者公開52頁冊子の印刷11頁（PDF15頁）と19頁（PDF23頁）を本文・画像で再照合。全4解説について出典の定義と架空案への適用を区別。ジグソーの原提唱者の原著・実証研究を取得したとはせず、期待効果を無条件に保証しない。音読・個別作業一般を不適切とせず、今回の条件との差異に限定。',unresolved='',multiple_correct_risk='なし：明示した条件に合うのは4のみ',no_correct_risk='なし：独立正答4')
assert len(extra)==18
for name,obj in [('changes.json',c+extra),('changes_batch83.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 18 edits; independent keys 4 and 4; 500 questions retained')
