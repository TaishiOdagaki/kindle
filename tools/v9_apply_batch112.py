"""One-time review against the specified MEXT2024 guidance, not causal proof."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2475
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_118'
assert d[k]['status']=='要追加確認' and a['A_4_118']['ans']=='4'
stem='文部科学省「初等中等教育段階における生成AIの利活用に関するガイドライン」（2024年12月26日、Ver.2.0）を踏まえ、日本語を学ぶ児童生徒の作文活動で生成AIを活用する際の説明として、適切なものを一つ選びなさい。'
opts=q[k]['opts'].copy()
opts[1]='求める出力を得るために課題や指示文を工夫する必要はなく、出力の真偽や適切性も確認しなくてよい。'
opts[3]='発達段階や学習状況、利用上の留意点を踏まえ、AIの修正案はたたき台とし、本人が確かめて推敲した過程と結果を示す活動を検討する。'
exps=[
'18頁は、誤りを含む出力を教材として生成AIの性質や限界に気付く例を挙げています。したがって検証を一切排除する説明は合いません。ただし17頁は発達段階や学習状況、リスクへの対策を踏まえた適否の見極めを求めており、誤りに触れれば誰でも学習効果が高まると保証しているわけではありません。',
'7頁は、適切な課題設定と指示文により求める出力につなげ、その真偽や適切性を判断することを前提としています。指示の工夫も出力の確認も不要とする肢は、この考え方と反対です。プロンプトごとの学習効果の大きさを実証した説明としては扱いません。',
'7頁は出力を参考の一つとし、最適解とは限らず最後は人間が判断するという姿勢を示しています。18頁と20頁も、生成物をほぼそのまま自己の成果物として提出することの問題を扱います。100％正確だから写してよいという説明は合いません。',
'18頁と20頁には、本人が書いた文章へのAIの修正をたたき台として、自分で推敲し、過程と結果を示す例があります。17頁の発達段階・学習状況等を踏まえる条件と合わせて、この肢が対応します。これは活動設計の参考例であり、すべての学習者に高い文法・語用論の学習効果が生じるという実証結果ではありません。']
reason='S171文科省2024-12-26ガイドライン本文7・17・18・20頁へ全肢照合。推奨活動と学習効果の因果実証を区別し、高い言語学習効果が得られる等の断定を除く。対象を同資料の初等中等教育に限定し、成人日本語教育や現行法の包括的判断へ拡張しない。'
extra=[]
for field,old,new in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_4_118']['txt'],exps)]:
 for i,(o,n) in enumerate(zip(old,new)):
  o=html.unescape(o)
  if o==n:continue
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S171'],applied=True,before_version='第111バッチ反映後',block_context='A_4_118' if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(e)
assert len(extra)==7
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S171'],reason=reason,option_verdicts=['誤：性質・限界を扱う教材例や検証を一切排除する','誤：適切な課題・指示と出力の確認を不要とする','誤：正確性を無条件保証し、そのまま提出を推奨する','正：本人の判断・推敲を含む活動を対象や条件に応じて検討する'],stem_review='版・日付と初等中等教育段階を明示。全4肢を本文7・17・18・20頁に独立照合。残した誤答1・3も本文の検証・人間判断と整合しないと確認。',explanation_review='全4解説をガイドラインの趣旨・適否条件・活動例に照合。高い学習効果、全プロンプトの効果差の大きさ、Noticingの理論的因果は同資料だけでは承認せず除去。法的評価や利用規約の個別判断は問わない。',unresolved='',multiple_correct_risk='なし：指定資料の考え方に合うのは4のみ',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',c+extra),('changes_batch112.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/01d7c3f9b818/mext112.pdf').read_bytes()
(b.OUT/'evidence/batch112_source.json').write_text(json.dumps(dict(id='S171',author='文部科学省初等中等教育局',date='2024-12-26',version='2.0',title='初等中等教育段階における生成AIの利活用に関するガイドライン',url='https://www.mext.go.jp/content/20241226-mxt_shuukyo02-000030823_001.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),obtained_pdf_pages=33,body_review_pages=[7,17,18,20],image_review_pages=[7,18,20],limits='Specified2024 guidance for elementary/secondary education, not current law/terms interpretation or causal proof of language learning effects; not entire33 pages reviewed. Full official PDF obtained, not summary-only.'),ensure_ascii=False,indent=2)+'\n')
print('1 full question/7 edits; key4 unchanged')
