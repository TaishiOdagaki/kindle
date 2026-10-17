"""One-time inference audit using the acquired author-publication original."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2920
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_3_005':dict(key=4,
 stem='物語文の理解における、背景知識に基づく推論（インファレンス）の説明として、最も適切なものを一つ選べ。',
 opts=['橋渡し推論とは、現在の記述と先行する文脈の関係を補うことではなく、未来の結末を予測することだけを指す。','背景知識に基づく推論とは、文章に明示された語句を、意味を補わずそのまま再現することだけを指す。','可能な種類の推論はすべて読解中に必ず生成され、読者の目的や背景知識による違いは生じない。','関連する背景知識を用い、文章に直接は明示されていない因果関係などの情報を補って、意味の理解を構成する。'],
 exps=['現在の記述と先行する文脈との因果的なつながりを補うことも、橋渡し推論の一例です。未来の展開を予測することだけに限定する説明は不適切です。','明示された語句をそのまま再現するだけでは、背景知識に基づいて明示されていない情報を補う推論の説明にはなりません。','推論には種類があり、読解中にすべてが必ず生成されるわけではありません。読者の目的や背景知識なども、生成される推論に関わります。','文章の明示的な情報と関連する背景知識を結び付け、明示されていない情報を補う説明です。どの推論が生成されるかは、文章や読者の条件によって異なります。'],
 verdicts=['誤：先行文脈との因果的橋渡しを否定し未来予測だけに限定','誤：明示的語句の再現だけと知識による情報補完を混同','誤：全種類が必ず生成されるとし、読者条件を否定','正：背景知識を用いる非明示情報の補完に一致']),
'Q_3_006':dict(key=1,
 stem='「太郎は花瓶を床に落とした。床に水が広がった。」という2文を読んだ際、2文間の因果的なつながりを補う橋渡し推論に当たるものを一つ選べ。',
 opts=['「花瓶に入っていた水がこぼれたのだろう」と補って、花瓶を落としたことと床の水を結び付ける。','2文の文字列を、書かれている順番のまま繰り返す。','「花瓶には青い模様が付いていたのだろう」と、書かれていない外観の詳細を思い浮かべる。','「この後、太郎は新しい花瓶を買いに行くだろう」と、先の展開を予測する。'],
 exps=['花瓶の中の水がこぼれたという、明示されていない出来事を補い、先行する花瓶の落下と現在の床の水を因果的につなぎます。与えられた2文を一貫して理解するための橋渡し推論です。','明示された文字列の反復であり、2文の間の明示されていない因果的なつながりを補っていません。','花瓶の模様を加えるのは、2文の因果関係をつなぐためには必要のない情景の精緻化です。ここで問う因果的な橋渡しとは異なります。','新しい花瓶を買うという将来の展開を予測しています。すでに記述された花瓶の落下と床の水を結び付ける推論ではありません。'],
 verdicts=['正：現在の床の水と先行する落下の間の因果連鎖を補う','誤：文字列の反復で非明示関係を補わない','誤：因果的つながりに不要な物体属性の精緻化','誤：先行文脈との接続でなく後続展開の予測'])}
reason='Graesser, Singer & Trabasso（1994）原論文全25頁のPDFを著者公開業績ページのリンクから取得。本文371–378頁を精読し、374頁の知識に基づく推論、375頁Table 1の因果的先行事象・因果的結果・状態、376頁の精緻化推論と生成条件の連続性、378頁の局所的一貫性を照合。Table 1は頁画像でも確認。橋渡し推論と精緻化推論の同義扱い、および全会話・全読者で常に推論が働くという過剰一般化を撤回。Q_3_006の花瓶例は監査者が定義の適用のために作成した例であり、原論文の実験刺激の引用ではない。'
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']!='確認済み' and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   assert html.unescape(old)!=new
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S205'],applied=True,before_version='第141バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
  
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=['S205'],reason=reason,option_verdicts=v['verdicts'],stem_review='物語文の知識に基づく推論、または明示した2文間の因果的な橋渡しに対象を限定。4肢を独立照合。',explanation_review='全4解説を原論文本文の定義・Table 1・分類説明・条件差へ照合。原著未取得の一般分類や音声文字変換の補助主張を残さない。',unresolved='',multiple_correct_risk='なし：設問で明示した対象を満たす説明は一つ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch142.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'graesser142.pdf').read_bytes()
e=dict(source_id='S205',title='Constructing Inferences During Narrative Text Comprehension',authors=['Arthur C. Graesser','Murray Singer','Tom Trabasso'],year=1994,journal='Psychological Review 101(3), 371–395',doi='10.1037/0033-295X.101.3.371',landing_url='https://sites.google.com/site/graesserart/publications/1994-1993',pdf_url='https://drive.google.com/file/d/1pP-xIo8wTKMvuWAthukgLVkfXHbXqy6E/view',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=25,read_scope='本文371–378頁を精読。374–376頁の定義・Table 1・分類説明を頁画像でも確認。全25頁の精読ではない。',limitations='本論文は物語文の知識に基づく推論を中心とする。全談話ジャンル・全理論・全読者への無条件の一般化をしない。花瓶例は監査者作例であり研究の実証例として引用しない。初回376頁PNGが破損したため除外し、当該頁再描画版を完全読込み・画像精読。',full_source_redistributed=False)
(b.OUT/'evidence/batch142_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 18 edits')
