"""One-time noticing-hypothesis rejudgment, recovered from the pending review."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3105
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_O_004';ak='A_O_004';assert d[k]['status']=='修正必要' and a[ak]['ans']=='3'
stem='ケース1の教師が検討している、質問と答えを対比して学習者の注意を言語形式へ向ける工夫について、Schmidt（1990）が論じた気づき（noticing）の説明に合うものを一つ選べ。'
opts=['学習者本人が形式に気づいたかどうかにかかわらず、教師が提示したインプットは全てインテイクになる。','抽象的な文法規則を言葉で説明できない学習者は、インプットのどの形式にも気づいていないと判定する。','意味内容だけでなく形式にも意識を向け、学習者自身がインプットの言語形式に気づく機会を作ろうとする。','一度気づいた形式は、その後に保持・再使用されるかを確かめなくても、全て習得済みと判定できる。']
exps=['139頁で著者が提案する仮説では、インテイクは学習者が気づいたインプットの部分です。教師が提示したことだけで、学習者の気づきとは無関係に全てがインテイクになるという説明ではありません。','132頁は気づきと理解を区別し、気づいた経験でも言葉で表現しにくい場合があると述べます。規則を説明できないことだけから、形式への気づきが全くないと結論することはできません。','139頁は、意味の理解に使われたインプットが全て形式学習のインテイクになるとは限らないとし、学習者の気づきを位置付けます。149頁でも形式を目立たせる指導の役割に触れます。この工夫は気づく機会を作る意図であり、教師の説明だけで本人の気づきや習得が保証されたという判断とは区別します。','141頁では、一時的に形式に気づいて繰り返したと考えられても、その後は使わなかった例を挙げ、紹介した研究が気づきだけで学習に十分だと実証したものではないと明記しています。気づきの確認と、その後の保持・習得の確認を同一視する肢は誤りです。']
verdicts=['誤：139頁の学習者が気づいた部分という仮説を、教師の全提示内容へ拡張する','誤：132頁の気づきと理解、言語化の条件の区別に反する','正：139頁の意味理解と形式への気づきの区別、149頁の指導の役割に対応する工夫の意図','誤：141頁の一時的な反復後に再使用されなかった例と、十分性を実証していないという留保に反する']
reason='S30原論文30頁PDFを大学から再取得。書誌、131–133頁の2.1–2.2、138–141頁の4冒頭・4.1と研究の留保、149–150頁の結論を精読し132・139・141・149頁を画像照合。現行ケース1は第4バッチでwhat/whereの質問条件へ既に修正済みで、今回ケースは変更しない。未照合の臨界期・文化変容・リンガフランカ各定義に依存する旧4択を、同じ学習領域の気づき仮説の内容を問う4択へ改訂し全肢・解説を独立照合。インテイクをpreliminary intakeとして論じる139頁を、習得・保持・自動産出の保証へ拡張しない。成人中心という原著の対象範囲と著者自身の実証上の留保を尊重し、現在の全理論の合意や当該授業の効果の実測として承認しない。'
ps=[p.text for p in Document(b.DST).paragraphs];assert q[k]['stem'] in ps
i=ps.index('ケース1　初級クラスにおける直接法での位置表現の導入');assert ps[i+4]=='問1' and '検討した' in ps[i+3]
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S30'],applied=True,before_version='第154バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==2 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=3,fixes_applied=True,sources=['S30'],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='現行ケース1全4段落と設問を対照。実施効果でなく教師が検討する工夫の意図とし、Schmidt1990の説明を明示、全4肢を独立照合。',explanation_review='全4解説を132・139・141・149頁の本文へ対照。気づきと理解、提示とインテイク、一時的反復と保持・習得を区別し、他仮説の未取得定義を承認しない。',unresolved='',multiple_correct_risk='なし：指定論文の説明に合うのは3のみ',no_correct_risk='なし：独立正答3')
for n,obj in [('changes.json',cs+extra),('changes_batch155.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'schmidt155.pdf').read_bytes()
e=[dict(source_id='S30',url='https://www.nflrc.hawaii.edu/PDFs/SCHMIDT%20The%20role%20of%20consciousness%20in%20second%20language%20learning.pdf',title='The Role of Consciousness in Second Language Learning',author='Richard W. Schmidt',year=1990,journal='Applied Linguistics 11(2),129–158',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=30,read_scope='書誌・標題・要旨、131–133頁の2.1–2.2、138–141頁の4冒頭と4.1（141頁の次頁へ続く末段落は頁内まで）、149–150頁の結論全文を精読。132・139・141・149頁（PDF4・11・13・21頁）を全頁画像照合。',limitations='全30頁精読ではない。Schmidt/Frota1986等の引用先原著の独立取得ではない。1990年論文の記述と留保へ限定し、現代の合意や当該日本語授業の効果の実測を承認しない。',full_source_redistributed=False)]
(b.OUT/'evidence/batch155_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Q_O_004: 9 edits / independent answer3 / case retained')
