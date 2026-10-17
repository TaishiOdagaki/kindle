"""One-time bounded background-knowledge case revision; never rerun."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2963
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_3_004';ak='A_3_004';assert d[k]['status']=='要追加確認' and a[ak]['ans']=='3'
stem='読解における、経験に基づくスキーマなどの背景知識と文章の内容との食い違いを示す事例として、最も適切なものを一つ選べ。'
opts=['学習者が、文中の「ご飯」という語の意味を知らず、辞書でその意味を調べた。','学習者が、文中の接続表現「なぜなら」の意味をまだ学んでおらず、理由を示す表現だと理解できなかった。','食後に代金を払う店しか経験のない学習者が、飲食店では必ず食後に払うものだと考えていた。食前に会計を済ませる店の物語を読み、語句や文の意味は分かったが、支払いの順序に戸惑った。','学習者が、文中の漢字の読み方を知らず、その漢字の読みを辞書で調べた。']
exps=['提示された原因は「ご飯」という語の意味を知らないことです。経験に基づく出来事の枠組みと、文章の内容との食い違いを示した事例ではありません。','提示された原因は、接続表現の意味が未習であることです。経験に基づく出来事の枠組みと、文章の内容との食い違いは示されていません。','読者が経験から形成した支払いの順序についての枠組みと、物語中の店の順序が食い違っています。背景知識は物語の出来事の理解に関わりますが、その読者の経験に基づく期待が、すべての店に当てはまるとは限りません。国民全体に共通する慣習を述べた例ではありません。','提示された原因は、漢字の読み方を知らないことです。出来事についての経験に基づく期待と文章の内容との食い違いを示した事例ではありません。']
reason='S205の原論文全25頁を著者業績ページの公開リンクから再取得し、印刷374頁本文全体と画像を再照合。背景知識構造にはスキーマやスクリプト等があり、経験に根ざしたレストランでの食事の枠組みが物語理解に関わるという説明、および著者の意図・明示文・読者の構成する意味の不一致を照合。旧例の風邪時の入浴を日本の文化的慣習と一律に扱う主張を撤回。個人の経験による出来事の枠組みと物語内容の食い違いへ限定した監査者作例であり、論文の実験刺激や各国の実態調査ではない。誤答解説の未照合なボトムアップ等の補助分類も削除。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S205'],applied=True,before_version='第144バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==2 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=3,fixes_applied=True,sources=['S205'],reason=reason,option_verdicts=['誤：語の意味が不明という明示条件で、出来事の枠組みとの不一致を示さない','誤：接続表現の意味が未習という条件で、経験と物語内容の不一致を示さない','正：個人が経験から形成した支払い順序への期待と物語の順序の食い違いを明示','誤：漢字の読みが不明という条件で、経験と物語内容の不一致を示さない'],stem_review='スキーマなどの背景知識と文章内容との食い違いに限定。国別の慣習や医学的判断を問わない。',explanation_review='374頁本文と個々の事例の明示条件を照合。4解説から未照合な処理分類を外し、正答例を国民全体へ一般化しない。',unresolved='',multiple_correct_risk='なし：明示条件で経験に基づく出来事の枠組みとの食い違いを示すのは3のみ',no_correct_risk='なし：独立正答3')
for n,obj in [('changes.json',cs+extra),('changes_batch145.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'graesser145.pdf').read_bytes()
e=dict(source_id='S205',reacquired='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=25,read_scope='印刷374頁全文を再精読し、同頁画像も照合。全25頁精読ではない。',landing_url='https://sites.google.com/site/graesserart/publications/1994-1993',pdf_url='https://drive.google.com/file/d/1pP-xIo8wTKMvuWAthukgLVkfXHbXqy6E/view',limitations='原論文の背景知識構造・物語理解の説明を基礎とする監査者作例。支払い順序の例は実験刺激の引用でなく、国民的慣習の実証でもない。原論文の引用元である1977年書籍等の取得を意味しない。',full_source_redistributed=False)
(b.OUT/'evidence/batch145_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
