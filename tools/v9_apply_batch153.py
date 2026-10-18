"""One-time evidence-bounded repair of the threshold-hypothesis question."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3089
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_2_003';ak='A_2_003';assert d[k]['status']=='修正必要' and a[ak]['ans']=='2'
stem='Cummins（1976）の閾値仮説と、同論文が紹介する加算的・減算的バイリンガリズムの区別について、本文の説明に合うものを一つ選べ。'
opts=[
'閾値は、教育環境や第二言語を使う時間、そこで求められる認知的課題にかかわらず、全員に共通する固定的な値である。',
'二言語で到達した言語能力の水準が、二言語学習経験と認知的発達との関係を媒介し得るという仮説である。',
'加算的バイリンガリズムとは、第一言語が第二言語に徐々に置き換えられ、第一言語の能力が低下していく状況を指す。',
'減算的バイリンガリズムとは、第一言語を第二言語に置き換えることなく、新しい言語を言語技能のレパートリーへ加える状況を指す。']
exps=[
'本文24頁では、閾値は絶対的な値としては定義できず、第二言語を使う時間や、その言語で表現する認知的操作によって変わり得るとしています。全員に同じ固定値とする説明ではありません。',
'本文23頁は言語能力の水準を媒介変数として位置付け、より基礎的な社会的・教育的要因などとも区別します。27頁では仮説の単純化と今後の研究の必要性も認めています。これは1976年の仮説の内容を問うもので、個人の言語面の困難だけから思考能力全体の不足を診断する基準ではありません。',
'本文20頁がLambertの区別として紹介する説明では、新しい言語を加える加算的な状況と、第一言語が第二言語に置き換えられる減算的な状況を区別します。この肢は減算的な状況を加算的と呼んでいます。',
'本文20頁では、第一言語を置き換えずに新しい言語をレパートリーへ加える方を加算的と説明します。減算的な状況では第一言語の減退と第二言語への置き換わりを扱うため、この肢は名称を逆にしています。']
verdicts=['誤：24頁の絶対的な定義不可・使用時間と認知的操作による変動に反する','正：23頁の媒介変数としての仮説に対応。27頁の研究上の限界も全解説へ反映','誤：20頁が紹介する減算的な状況と加算的な状況の名称を逆にする','誤：20頁が紹介する加算的な状況を減算的と呼ぶ']
reason='S217の原論文全文ファイルを取得し、書誌・20–27頁の全本文を連続精読、20・23・24・27頁を画像照合。設問を1976年論文の説明に限定し、閾値の可変性・媒介変数・社会的教育的要因・仮説の限界と加算/減算の区別を4肢・4解説へ対照。旧正答と解説のセミリンガルというラベルを思考能力不足の診断と同一視する説明、根拠未確認の現在の呼称の普及度、順次と継承の同義扱いを撤回する。歴史的仮説を現在の確定的な因果法則や個人の知的能力を判定する基準として承認しない。Lambertの区別はCummins本文が紹介する記述に限定し、未取得のLambert原著や引用先の個別研究まで検証済みとはしない。'
assert q[k]['stem'] in [p.text for p in Document(b.DST).paragraphs]
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S217'],applied=True,before_version='第152バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S217'],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='原著の説明内容を問うと明示し、4肢を別々に20・23・24・27頁へ照合。独立正答2。',explanation_review='4解説を原著本文へ照合。仮説・媒介変数と基本原因を区別し、知的能力の診断や現在の実証的結論へ拡張しない。旧ラベルと現在の呼称・継承概念の未検証の主張は改訂で除去。',unresolved='',multiple_correct_risk='なし：指定論文の説明に対応するのは2のみ',no_correct_risk='なし：23頁に対応する正答2あり')
for n,obj in [('changes.json',cs+extra),('changes_batch153.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'cummins153.pdf').read_bytes()
e=[dict(source_id='S217',url='https://files.eric.ed.gov/fulltext/ED125311.pdf',title='The Influence of Bilingualism on Cognitive Growth: A Synthesis of Research Findings and Explanatory Hypotheses',author='James Cummins',year=1976,series='Working Papers on Bilingualism, No. 9',eric_id='ED125311',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=44,read_scope='書誌・標題・要旨、印刷20–27頁（PDF21–28頁）の全本文を連続精読。印刷20・23・24・27頁を全頁画像照合。印刷7頁の同時獲得に関する箇所も読んだが、その引用先の実験は本問の承認根拠にしない。',limitations='全44頁精読ではない。引用先のLambert原著・個別実証研究の独立検証ではない。1976年の仮説内容を限定して出題し、現在の確定的な因果法則・知的能力の診断基準・呼称の現在の普及度は承認しない。',full_source_redistributed=False)]
(b.OUT/'evidence/batch153_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Q_2_003: 9 edits / independent answer 2 / 1 repair resolved')
