"""Add the full teacher-belief question review to batch109 before checkpointing."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2454
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_007';assert d[k]['status']=='要追加確認' and a['A_4_007']['ans']=='1'
stem='Borg（2003）が示す、信念を含む教師の認知（teacher cognition）と実践の関係について、説明に合うものを一つ選びなさい。'
opts=[
'教師の認知は、学習者としての経験や教員養成、教室での実践と関係し、文脈的要因とともに実践に関わる。',
'教員養成で理論を学べば、受講者全員の信念が同じ仕方で自動的かつ完全に変わる。',
'教師の認知には知識だけが含まれ、教師が信じていることや考えていることは含まれない。',
'教師が述べる信念と実際の授業行動は、文脈の制約にかかわらず常に完全に一致する。']
exps=[
'81〜82頁の枠組みと図1に対応します。信念・知識・思考を含む教師の認知を、学校での学習経験、専門的な養成、実践、文脈的要因と関連付けています。特定の信念が全教師の行動を一律に決めるという説明ではなく、相互の関係を示す枠組みです。',
'91頁の要約は、教員養成の影響に多様な結果と個別の発達過程があることを指摘しています。養成で変化が起こり得ることと、全受講者が同じ仕方で自動的・完全に変わることは区別されます。',
'81頁では、教師が知っていること、信じていること、考えていることを教師の認知として扱っています。信念や思考を除き知識だけに限定する肢は、その用語の範囲に合いません。',
'82頁の図1は文脈的要因によって認知と実践の不一致が生じ得ることを示し、91頁も認知の変化が行動の変化を保証しないと述べています。信念と行動が常に完全に一致するという説明は誤りです。']
reason='S168 Borg本人の2003年総説の枠組み・図1・教員養成節の要約を原文・版面照合。認知と実践の関係に限定し、信念が行動を強力に規定する一方向の因果断定、省察による無意識の偏見からの解放という未裏付けの効果主張を除く。総説が引用する各実証研究を取得済みとはしない。'
extra=[]
for field,old,new in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_4_007']['txt'],exps)]:
 for i,(o,n) in enumerate(zip(old,new)):
  o=html.unescape(o);assert o!=n
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S168'],applied=True,before_version='第109バッチ前半適用後',block_context='A_4_007' if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(e)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S168'],reason=reason,option_verdicts=['正：認知と学習経験・養成・実践・文脈の関係','誤：変化の多様性・個別性を否定','誤：認知から信念・思考を排除','誤：文脈と不一致の可能性を否定'],stem_review='Borg2003の枠組みと用語に限定した設問・全4肢を独立比較。',explanation_review='81〜82頁と91頁の全4解説対応を照合。枠組みと総説の整理を問うものとし、引用先の個別研究、全教師への因果・頻度・介入効果まで承認しない。',unresolved='',multiple_correct_risk='なし：対応する肢は1のみ',no_correct_risk='なし：独立正答1')
batch=json.loads((b.OUT/'changes_batch109.json').read_text())
for name,obj in [('changes.json',c+extra),('changes_batch109.json',batch+extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/697c245d9771/borg109.pdf').read_bytes()
(b.OUT/'evidence/batch109_source_borg.json').write_text(json.dumps(dict(id='S168',author='Simon Borg',year=2003,title='Teacher cognition in language teaching A review of research on what language teachers think know believe and do',journal='Language Teaching36(2),81-109',doi='10.1017/S0261444803001903',url='https://eprints.whiterose.ac.uk/1652/1/borgs1_language_teaching_36-2.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),obtained_pdf_pages=30,reviewed_printed_pages=[81,82,91],image_review_pdf_pages=[2,3,12],limits='Original authored review/framework, not all30 pages fully read; cited empirical studies and Borg1997 not separately acquired'),ensure_ascii=False,indent=2)+'\n')
print('2 full questions/15 combined edits')
