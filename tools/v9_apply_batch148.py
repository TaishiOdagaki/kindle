"""One-time explicit temporal-intention case repair; do not rerun."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2990
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_O_031';ak='A_O_031';assert d[k]['status']=='修正必要' and a[ak]['ans']=='4'
oldcase='中級クラスの学習者が提出した作文に、次のような文があった。「わたしは日本に来る前に、日本語を三年間勉強しています。」教師はこの文を読み、テンス・アスペクトの誤用があると判断した。'
newcase='中級クラスの学習者が提出した作文に、次のような文があった。「わたしは日本に来る前に、日本語を三年間勉強しています。」この学習者は作文を書いた時点で既に来日している。教師が本人に確認すると、この文では、来日前に終了した三年間の学習期間を述べたいということだった。教師は、文末の時制と本人の意図が合っていないと判断した。'
assert sum(oldcase in p.text for p in Document(b.DST).paragraphs)==1
stem='ケースで本人に確認した意図を踏まえた、この作文の問題点の説明として、最も適当なものを一つ選べ。'
opts=['「日本語」「勉強」という漢字表記そのものが誤っている。','文末を「勉強しています」のままにしても、本人が述べたい来日前に終了した期間とのずれはない。','「日本語を」の助詞「を」は誤りなので、必ず「日本語に」に直す。','来日前に終了した学習期間を述べたいのに、文末で現在の継続を表す形を選んでいる。']
exps=['「日本語を勉強しています」という表記は大学教材の例にも用いられています。このケースで問題になるのは、漢字そのものではなく、本人が述べたい期間と文末の時制との対応です。','本人が述べたいのは、作文を書いている現在まで続く期間ではなく、来日前に終了した三年間です。その確認条件を無視して、ずれがないとすることはできません。','大学教材にも「日本語を勉強しています」という例があります。「を」を必ず「に」に替える必要はありません。','大学教材は、動きの継続を表す「Vています」と、その過去の形「Vていました」を区別しています。本人に確認した過去の学習期間を述べるには、「勉強していました」など、過去として述べる形を検討できます。「来る前に」という語句だけから過去だと断定した分析ではありません。']
reason='S211 東京外国語大学言語モジュール「Vています（進行）／Vていません」解説本文全体を取得・精読。継続の説明、日本語を勉強していますの例、過去形Vていましたを照合。ケースに作文時点で来日済み・本人が来日前に終了した期間を述べたいという確認済み意図を明記。「来る前に」だけで過去と断定する旧分析を撤回し、ている自体が常に誤りとも扱わない。母語や学習歴による原因の確定はしない。関連Q_O_032〜035の設問・全肢・解説を点検し、文境界の例を変更せず、他の確認済み3問の対象・正答を変えない。Q_O_032の原因分析の追加照合は未了のまま維持。'
extra=[dict(id='CASE_O_07',field='case_text',index=None,before=oldcase,after=newcase,reason=reason,sources=['S211'],applied=True,before_version='第147バッチ反映後')]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S211'],applied=True,before_version='第147バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
assert len(extra)==10
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S211'],reason=reason,option_verdicts=['誤：教材にも用いられる漢字表記に問題を帰属','誤：本人が確認した過去の期間と現在継続形のずれを無視','誤：教材にもある日本語を勉強するのをを必ずにに替える必要はない','正：確認した意図と文末の時制との不対応に一致'],stem_review='来日済みと来日前に終了した期間を述べたいという本人確認の条件をケースへ追加。全4肢をこの条件で独立判定。',explanation_review='大学教材の継続・過去形・日本語を勉強するの例に全4解説を照合。「ている」は常に誤り、来る前にだけで過去という断定をしない。',unresolved='',multiple_correct_risk='なし：明示した意図との不対応を説明するのは4のみ',no_correct_risk='なし：独立正答4')
for n,obj in [('changes.json',cs+extra),('changes_batch148.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'tufs044-148.html').read_bytes()
e=dict(source_id='S211',title='Vています（進行）／Vていません 解説',institution='東京外国語大学言語モジュール',url='https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/044.html',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope='解説本文の1〜3、例文1〜5、注記を全て精読。',limitations='ケースの本人の意図は監査者の仮想条件。元の孤立文だけから時点や学習履歴・母語干渉の原因を推定しない。',full_source_redistributed=False)
(b.OUT/'evidence/batch148_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question plus shared case / 10 edits')
