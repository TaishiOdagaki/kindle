"""One-time metonymy and word-formation-form audit using public teaching bodies."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2938
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_M_057':dict(key=3,sources=['S206'],
 stem='「永田町」で政界を表したり、「白バイに捕まった」の「白バイ」でそれに乗る警官を表したりする言い方を考える。このような隣接性に基づく比喩の説明として、最も適切なものを一つ選べ。',
 opts=['二つの例とも、用いられた名称と指し示す対象との間に関連はなく、無関係な対象を任意に指している。','「白バイに捕まった」の「白バイ」は、警官ではなく、車両そのものが人を捕まえたことを表す。',q['Q_M_057']['opts'][2],'「永田町」は地理的な場所を指すだけで、政界を指す用法はない。'],
 exps=['場所とそこに関わる組織・集団、乗り物とそれに乗る人という関連を利用しています。無関係な対象を任意に指しているのではありません。','この用例では、乗り物の名称を用いて、それに乗る警官を表しています。車両自体が人を捕まえたという意味ではありません。',a['A_M_057']['txt'][2],'この用例の「永田町」は、町の地理的な範囲だけでなく、その場所に関わる政界を表しています。場所で組織や集団を表す換喩の例です。'],
 reason='国際交流基金ソウル日本文化センター「カチカチの声」119号（2017年2月）、山口敏幸署名「日本語あれこれ(3) 換喩（メトニミー）」全4頁を取得。日本語本文全節・注記を抽出本文と全頁画像で精読。1頁の定義・日常使用、3頁の白バイの警官、4頁の永田町の政界および注3の部分全体の分類差を確認。車両そのものと乗る警官を混同しない文中の用例に明確化。「部分や関連物で全体」として部分全体を普遍的に一括する前提は撤回。佐藤信夫の引用元書籍全冊の取得とは扱わない。',
 verdicts=['誤：場所と集団、乗り物と人の関連を否定','誤：乗り物で警官を指す用例を車両自体の行為と誤解','正：関連に基づく換喩の定義と日常使用の説明に一致','誤：資料本文に明記された永田町の政界用法を否定']),
'Q_M_052':dict(key=3,sources=['S207'],
 stem='「読み方」の「読み」、「食べ物」の「食べ」という語形成に用いられる形に着目する。元の動詞とその連用形の対応を正しく示すものを一つ選べ。',
 opts=['「読む」の連用形は「読んだ」、「食べる」の連用形は「食べた」である。','「読む」の連用形は「読んで」、「食べる」の連用形は「食べて」である。','「読む」の連用形は「読み」、「食べる」の連用形は「食べ」である。','「読む」の連用形は「読む」、「食べる」の連用形は「食べる」である。'],
 exps=['「読んだ」「食べた」は、教材の活用形一覧では「た形」です。この設問で問う「読み」「食べ」という連用形とは異なります。','「読んで」「食べて」は「て形」です。この設問で問う連用形の対応にはなりません。','「読む」の連用形は「読み」、「食べる」の連用形は「食べ」です。設問に挙げた「読み」「食べ」と同じ形です。','「読む」「食べる」は辞書形です。連用形の「読み」「食べ」と辞書形を区別します。'],
 reason='東京外国語大学言語モジュール「普通形の体系」カード本文の全3表を取得・読了。表2の読む・食べるの行で辞書形・連用形・た形・て形を4肢と全解説に直接照合。「読み方」を接尾辞派生とする分析と複合語分析の体系差を未取得理論で解決したことにはせず、元の語形成と連用形という学習領域・2例を維持し、語形の対応を問う問題へ改訂。二つの語を一律に複合語と分類する前提を撤回した。',
 verdicts=['誤：た形を連用形と誤同定','誤：て形を連用形と誤同定','正：教材表2の読む・食べるの連用形と一致','誤：辞書形を連用形と誤同定'])}
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='修正必要' and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==html.unescape(new):continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=html.unescape(new),reason=v['reason'],sources=v['sources'],applied=True,before_version='第142バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=v['sources'],reason=v['reason'],option_verdicts=v['verdicts'],stem_review='分類の体系差を未取得理論で一般化せず、取得本文に対応した具体例と語形に対象を限定。4肢を独立照合。',explanation_review='全4解説を署名付き公的教材または大学の活用表本文に照合。維持したQ_M_057の選択肢3・解説3も定義と日常使用の記述に照合。',unresolved='',multiple_correct_risk='なし：明示した用例または語形に合う説明は一つ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==16
for n,obj in [('changes.json',cs+extra),('changes_batch143.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];sources=[]
for sid,file,url,scope in [('S206','metonymy143.pdf','https://www.jpf.or.kr/index/data/file/publish/3555240129_sHYuZjeG_201702.pdf','全4頁の日本語本文全節と注記を精読・全頁画像でも照合。韓国語対訳の独立監査ではない。山口敏幸署名、2017年2月、カチカチの声119号。佐藤信夫の引用元書籍全冊は未取得。'),('S207','tufs038-143.html','https://www.coelang.tufs.ac.jp/modules/ja/gmod/courses/c01/lesson11/step1/card/038.html','カード本文全3表を読了。表2の読む・食べるの行の辞書形・連用形・た形・て形を全4肢・解説に直接照合。語形成の派生と複合の分類理論を証明する資料としては使わない。')]:
 raw=(root/file).read_bytes();sources.append(dict(source_id=sid,url=url,retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch143_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 16 edits')
