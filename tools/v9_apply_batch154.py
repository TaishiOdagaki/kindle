"""One-time rejudgment of Q_O_012 using its already repaired case."""
import json,html,hashlib
from pathlib import Path
from docx import Document
from pypdf import PdfReader
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3098
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_O_012';ak='A_O_012';assert d[k]['status']=='修正必要' and a[ak]['ans']=='2'
stem='ケース3で、同じ部長の発言を社内の同僚と取引先の社員に伝える際、ウチ・ソトに応じて表現を選ぶことは、CEFR（2001）5.2節の区分では主にどの能力に関わるか。一つ選べ。'
opts=['文法能力（動詞の活用形を作る力）のみ',q[k]['opts'][1],'音韻能力（発音を正確に行う力）のみ','正書法能力（綴りや句読点などを扱う力）のみ']
exps=[
'CEFRの5.2.1.2は、文法的な資源を理解し用いる能力を扱います。本問の焦点は活用形の作り方ではなく、同じ部長の発言を誰に伝えるかによる表現の選択です。動詞の活用だけに限定する肢では、この使い分けを説明できません。',
'CEFRの5.2.2は、言語使用の社会的側面に関する知識と技能を扱い、社会的関係を示す表現や丁寧さの慣習などを挙げます。敬語の指針の会社内外の例とも照合すると、このケースの主な焦点は相手との関係に応じた表現選択であり、社会言語能力に対応します。本人への引用を一律に誤用とする判断ではありません。',
'CEFRの5.2.1.4は、音や韻律などの知識と知覚・産出の技能を扱います。本問が明示しているのは聞き手との関係による言葉遣いの選択であり、発音の正確さだけに限定する肢はその焦点に合いません。ケースだけから学習者の発音全体を評価したものではありません。',
'CEFRの5.2.1.5は、文字や綴り、句読点など、書かれたテキストを構成する記号を扱う知識と技能を挙げます。本問は文字表記の誤りではなく、社内と取引先への報告での表現選択を問うため、正書法だけに限定する肢は合いません。']
verdicts=['誤：活用形の形成だけでは、問いが明示する聞き手とウチ・ソトによる選択を説明しない','正：CEFR5.2.2の社会的関係と丁寧さに対応。会社内外の具体例をS04で確認','誤：音・韻律の知覚産出だけでは、明示した対人条件による表現の選択を説明しない','誤：文字・綴り・句読点の操作だけでは、口頭報告の対人条件による使い分けを説明しない']
reason='現行ケース3は第4バッチで会社Xの社員・自社部長・社内の同僚・取引先という条件へ既に改訂済み。その3段落とQ_O_011–014を再確認し、今回はケースを再変更せずQ_O_012を再判定。S04の22–23・43–44頁と謙譲語IIの18頁、S179 CEFR2001の5.2冒頭・5.2.1.2・5.2.1.4–5.2.1.5・5.2.2–5.2.2.4を取得本文へ対照。分類枠組みと問う対人条件を明示し、4肢・4解説を独立判定。未取得のCanale/Swain原著の承認ではない。本人への引用を一律不自然とする旧ケースを復元せず、学校での呼称慣習と会社のウチ・ソトを一般化して同一視しない。発音等の他能力の不足をケースだけから診断しない。'
ps=[p.text for p in Document(b.DST).paragraphs];assert q[k]['stem'] in ps
case_start=ps.index('ケース3　会社のウチとソトに応じた待遇表現の指導');assert ps[case_start+3]=='問1'
assert '会社Xの社員' in ps[case_start+1] and '取引先' in ps[case_start+2]
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  if html.unescape(old)==new:continue
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S04','S179'],applied=True,before_version='第153バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(c)
assert len(extra)==7
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S04','S179'],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='現行ケース3の全3段落と後続4問を確認。問いの対象を聞き手・ウチソトによる表現選択としCEFR2001を明示、全4肢を独立照合。',explanation_review='CEFRの文法・音韻・正書法・社会言語能力を区別し4解説を本文へ照合。S04の会社内外の例と謙譲語IIの説明でケース条件を確認。発音や知識全体の評価を推定しない。',unresolved='',multiple_correct_risk='なし：明示した焦点に対応するのは2のみ。実際の発話で他能力も関与することを排除しない',no_correct_risk='なし：独立正答2')
for n,obj in [('changes.json',cs+extra),('changes_batch154.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2]
def meta(f):
 raw=(root/f).read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=len(PdfReader(root/f,strict=True).pages))
e=[dict(source_id='S179',url='https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf',title='Common European Framework of Reference for Languages: learning, teaching, assessment',year=2001,read_scope='再取得。5.2冒頭（108頁）、5.2.1.2の定義と列挙（112–113頁）、5.2.1.4・5.2.1.5本文（116–117頁）、5.2.2冒頭から5.2.2.4末（118–120頁）を精読。118・119頁（PDF127・128頁）を全頁画像照合。5.2.3.1本文も参照したが、本問の4肢には用いない。',limitations='全273頁の精読ではない。CEFR2001の説明を用い、別の理論モデルや現在の試験仕様を同一視しない。',**meta('cefr154.pdf')),dict(source_id='S04',url='https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93927001_09.pdf',title='敬語の指針',date='2007-02-02',read_scope='再取得。18頁の謙譲語II、22–23頁の立てる人物とウチ扱い、43–44頁の本文を精読。Q22–24は全文、Q25は44頁内まで。43・44頁（今回のPDF46・47頁）を画像照合。会社と学校の例の違いを確認。',limitations='今回の取得版は印刷44頁がPDF47頁であり、従来catalog行の2頁差という表記は本取得版へ適用しない。全書精読・現在の慣習頻度の再調査ではない。',**meta('keigo154.pdf'))]
for x in e:x.update(retrieved='2026-10-18',full_source_redistributed=False)
(b.OUT/'evidence/batch154_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Q_O_012: 7 edits / independent answer2 / case retained')
