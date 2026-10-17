"""One-time role-language and jargon audit against acquired body text."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2895
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_M_010':dict(key=3,sources=['S201'],
 stem='金水敏の役割語研究における「役割語」の説明として、最も適切なものを一つ選べ。',
 opts=['特定の人物像と言葉遣いの結び付きではなく、話し声の大きさだけを表す概念である。','マンガやアニメにのみ現れる特殊な言葉であり、現実の会話での話し方の選択には関わらない。','特定の言葉遣いから人物像を思い浮かべたり、人物像からその人らしい言葉遣いを連想したりする、ステレオタイプ的な知識に関わる。','「わし」「〜じゃ」のような話し方を、現代の高齢者が一様に使うという調査結果そのものを指す。'],
 exps=['役割語は、人物像と言葉遣いの結び付きに関する概念です。語彙や語法、イントネーションなどが関わり、声の大きさだけを指すものではありません。','金水は、役割語をマンガやアニメにのみ現れる特殊な言葉に限定していません。現実の会話での話し方の選択や、他者の発言を引用する際にも役割語の知識が関わると論じています。','言葉遣いと人物像の連想上の結び付きを捉える説明です。現実の会話にも関わる知識であり、フィクションの中だけに限定されるわけではありません。','高齢者を連想させる話し方が知られていても、現代の高齢者全員が実際に同じように話すという意味ではありません。人物像の連想と、実際の言語使用の調査結果を区別します。'],
 reason='金水敏（2011）「役割語と日本語教育」原論文全8頁を取得し、テキスト抽出0文字のため全8頁を画像で精読。印刷34頁の定義、36頁の現実性、38–39頁のスタイルとの連続性・現実会話での発言引用例を照合。フィクション限定と現実の属性変種との排他的二分を撤回し、上位概念の位相語を誤答とする競合も避けた。原著2003年書籍全冊の取得とは扱わない。',
 verdicts=['誤：人物像と言葉遣いの関係を声量だけに縮減','誤：現実会話での話し方・引用の本文例に反する限定','正：言葉遣いと人物像の連想を捉えた定義','誤：ステレオタイプ的知識と全高齢者の実使用を混同']),
'Q_M_012':dict(key=1,sources=['S202','S203'],
 stem='特定の専門分野や集団で使われる専門的な用語を指す呼称として、最も適切なものを一つ選べ。ここでは、規範性や地域差ではなく、専門分野・集団との結び付きに着目する。',
 opts=['ジャーゴン（特定分野・集団の専門的な用語）','標準語（規範的な言語変種）','共通語（広く通じる言語変種）','地域方言（地域によることばの違い）'],
 exps=['ジャーゴンは、特定の分野や集団で用いられる専門的な用語を指します。集団外の人が一人でも知っていればジャーゴンではなくなる、という絶対的な限定はしません。','標準語は規範的な正式の言い方として捉える概念です。専門分野や集団に結び付いた用語を指す呼称として、この設問の着眼点には合いません。','日本語の共通語は、方言の違いを越えて通じ合うことばを指します。専門分野や集団の用語という着眼点とは異なります。専門用語が広く知られる可能性を否定するものではありません。','地域方言は地域によることばの違いに着目する概念です。この設問が問う専門分野や集団との結び付きとは、分類の観点が異なります。'],
 reason='Googleの公式文書作成ガイドJargon本文を取得し、専門集団の用語、一般に集団外で理解されにくい傾向、一部は広く理解されるという条件を確認。国語研の署名付き解説2件の本文から標準語・共通語・地域方言の着眼点を照合。「内部でのみ通じる」を必要条件とする説明を撤回。生得説は未取得理論の補助説明を足さず、同じ言語変異の領域の地域方言へ変更。分類観点を明示し、一つの用語が他の観点でも分類され得ることを排除しない。',
 verdicts=['正：専門分野・集団の用語という設問の着眼点に対応','誤：規範性を捉える概念で着眼点が異なる','誤：地域を越える通用性を捉える概念で着眼点が異なる','誤：地域差を捉える概念で着眼点が異なる'])}
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='修正必要' and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=v['sources'],applied=True,before_version='第139バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=v['sources'],reason=v['reason'],option_verdicts=v['verdicts'],stem_review='設問の概念・分類観点を限定し、4選択肢を本文に独立照合。上位概念や別の分類軸との重なりを誤りの根拠にしない。',explanation_review='全4解説と補助主張を取得本文へ照合。フィクション限定や内部通用の絶対限定を撤回。',unresolved='',multiple_correct_risk='なし：明示した着眼点に合う説明・呼称は一つ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==16
for name,obj in [('changes.json',cs+extra),('changes_batch140.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
sources=[];root=Path(__file__).resolve().parents[2]
for sid,file,url,scope in [('S201','kinsui2011-140.pdf','https://www.jstage.jst.go.jp/article/nihongokyoiku/150/0/150_34/_pdf/-char/ja','金水敏（2011年12月）役割語と日本語教育 日本語教育150:34–41。全8頁画像精読。2003年の引用元書籍全冊は未取得。'),('S202','jargon140.html','https://developers.google.com/style/jargon','Jargon公式本文全体。2025-06-25更新表示。自動生成Page Summaryではなく本文で定義・例外・使用条件を照合。'),('S203','ninjal138-140.html','https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-138/','三井はるみ 共通語と標準語 本文全節。2021-07-19再掲。2003年初出の全文書籍取得ではない。'),('S203','ninjal137-140.html','https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-137/','三井はるみ 方言の定義 本文全節。2021-07-13再掲。地域方言と社会方言の区分、地域内多様性を確認。')]:
 raw=(root/file).read_bytes();sources.append(dict(source_id=sid,url=url,retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch140_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 16 edits')
