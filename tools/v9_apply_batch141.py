"""One-time source-bounded official/national-language case revision."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2911
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_2_008';ak='A_2_008';assert d[k]['status']=='修正必要' and a[ak]['ans']=='1'
stem='公用語と国家語の関係について、シンガポール憲法第153A条（政府公開の2023年4月24日施行版）に照らして正しいものを一つ選べ。'
opts=['公用語はマレー語・中国語（Mandarin）・タミール語・英語の4言語であり、国家語はマレー語と定められている。','公用語は英語だけであり、マレー語・中国語（Mandarin）・タミール語は公用語に含まれない。','公用語と国家語の指定は完全に同一であり、国家語もマレー語・中国語（Mandarin）・タミール語・英語の4言語と定められている。','マレー語を国家語に定めることに伴い、他の言語の使用・教授・学習を禁止すると定められている。']
exps=['第153A条第1項は4公用語を列挙し、第2項はマレー語を国家語と定めています。この事例では、公用語の指定と国家語の指定は同一ではありません。マレー語は両方に含まれます。','第1項に列挙された公用語は4言語です。英語だけを公用語とする説明は、この条文に合いません。','第1項の4公用語の列挙と、第2項の国家語の指定を混同しています。第2項が国家語として定めるのはマレー語です。','第2項ただし書(a)は、他の言語の使用・教授・学習を禁止したり妨げたりしてはならない旨を定めています。国家語の指定を、他言語の禁止と同一視する説明は条文に反します。']
reason='政府選挙局公開の憲法PDF（2020 Revised Edition、2023-04-24からの施行版）全203頁を取得。表紙の版表示と印刷172頁の第153A条全項・ただし書(a)(b)を本文抽出と頁画像で直接照合。公用語・国家語という元の学習領域を保ち、一般概念の広範な定義・未取得の複数国事例を、取得版と時点を明示した具体的な条文事例へ改訂。現行SSOページは403で本文取得できず、検索表示のみの現行条文を承認根拠にしない。2026年現行法全体の確認済みとは扱わない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S204'],applied=True,before_version='第140バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S204'],reason=reason,option_verdicts=['正：第1項の4公用語と第2項の国家語の指定に一致','誤：第1項は英語だけでなく4言語を列挙','誤：国家語の指定と4公用語の指定を同一視','誤：第2項ただし書(a)の禁止・妨害の否定と逆'],stem_review='取得版の時点と条文番号を限定し、法的地位の具体的区別を問う。全4肢を第153A条全体に独立照合。',explanation_review='全4解説を第1項・第2項・ただし書(a)の本文へ照合。マレー語が両方に含まれることを明示し、排他的な2集合であるとの誤解を避ける。他国・日本法や国家語の普遍的な定義の未照合補助主張は掲載しない。',unresolved='',multiple_correct_risk='なし：指定の列挙とただし書に一致するのは1のみ',no_correct_risk='なし：独立正答1')
for n,obj in [('changes.json',cs+extra),('changes_batch141.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'singapore141.pdf').read_bytes()
e=dict(source_id='S204',url='https://www.eld.gov.sg/Resources/Constitution%20of%20the%20Republic%20of%20Singapore.pdf',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=203,version='2020 Revised Edition; Informal Consolidation – version in force from 24/4/2023',read_scope='表紙の版表示、印刷172頁の第153A条第1項・第2項・ただし書(a)(b)全文。該当頁の抽出本文と1800px画像を直接照合。全203頁の精読ではない。',limitations='SSO現行条文ページは403で取得不能。検索抜粋は承認根拠から除外。設問の時点を取得した2023年版に明示限定。',full_source_redistributed=False)
(b.OUT/'evidence/batch141_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
