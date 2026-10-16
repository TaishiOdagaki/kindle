"""One-time JSL elementary-report audit; ordered changes preserve past fixes."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2600
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));blocks,_=qa.blocks(qa.load(str(b.DST))[0]);extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 def entry(field,i,o,n,**kw):
  c=dict(id=k,field=field,index=i,before=html.unescape(o),after=n,reason=reason,sources=sources,applied=True,before_version='第117バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
  c.update(kw);extra.append(c)
 if q[k]['stem']!=stem:
  ps=[x['t'] for x in blocks[k][1:-1] if not x['ind']]
  entry('stem',None,ps[0],stem)
  for old in ps[1:]:entry('stem',None,old,'',remove_paragraph=True,previous_paragraph=stem)
 for field,olds,news in [('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(o,n) in enumerate(zip(olds,news)):
   if html.unescape(o)==n:continue
   kw={'stem_context':stem} if field=='options' else {'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'}
   entry(field,i,o,n,**kw)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢をCambridge TKT公式用語集、CEFR2001、公的評価用語の本文と独立比較。目的・参照先と時期を分けて判定。',explanation_review='全4解説を本文へ照合。テストの機能の併存を認め、時期だけによる診断/総括の区別、母集団情報不足での順位推定、未取得のJLPT評価範囲や一般的運用期間の主張を除去。',unresolved='',multiple_correct_risk='なし：明示した目的・報告の考え方で'+str(key)+'のみが適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_4_010';opts=q[k]['opts'].copy();opts[3]='特定のコースで教えた内容の達成度ではなく、言語の使用目的に対応する現在の能力を測定するテスト ── 診断テスト（ダイアグノスティックテスト）'
review(k,q[k]['stem'],opts,[
'この肢はコースの学習目標に対する到達度テストの目的です。熟達度テストは、特定コースの既習内容の再現ではなく、言語を使用する場面での能力に目を向けます。',
'クラスのレベルに学習者を配置するという目的は、配置テストの説明に合います。何を調べるかは、その学校のコースと配置の目的に合わせて定めます。',
'強みや弱み、既習内容を把握してその後の指導を考える目的は、診断テストに対応します。ここでは実施時期だけでなく、明示された利用目的で区別します。',
'言語の使用目的に対応する能力を測るという説明は、熟達度テストに対応します。診断という名称は、強みや弱みを把握し指導へつなげる目的と組み合わせる必要があります。'],2,['S183','S179'],
'Cambridge公式TKT Test各項目とCEFR9.3.1を照合。配置・到達度・診断・熟達度の目的を区別。熟達度を無限定な全能力測定とせず、未照合のJLPT例を除去。複数機能を持つ実際のテストを一律に排他的分類とはしない。',
['誤：到達度の目的に熟達度の名称','正：配置という目的と名称が合う','誤：診断の目的に熟達度の名称','誤：熟達度の目的に診断の名称'])
k='Q_4_012';opts=q[k]['opts'].copy();opts[2]='このコースで必要な文法・語彙の知識を筆記課題で、会話でのやり取りを面接課題で確かめ、それぞれの課題と評価基準を配置の目的に合わせて設計する。'
review(k,'日本語学校で、新入生の文法・語彙の知識と会話でのやり取りの両方を把握し、コースに合うクラスへ配置したい。開講後も学習状況に応じて配置を見直す方針とする。この目的・方針に合うテストの作成・運用を一つ選びなさい。',opts,[
'全員がゼロ点近くになるように問題を選ぶだけでは、この学習者集団のレベルの違いを配置に生かす情報が乏しくなります。難問だけという形式から信頼性が保証されるわけでもありません。',
'この設問の目的はクラスへの配置です。学習した内容の達成度を測る期末試験を、配置の目的との対応を検討せずそのまま使う理由にはなりません。到達度の情報を配置の判断材料に利用することまで否定するものではありません。',
'設問が求める知識と会話でのやり取りに、課題と評価基準を対応させる提案です。筆記と面接を組み合わせるだけで迅速さ・客観性・妥当性が自動的に保証されるという説明ではありません。',
'学習状況に応じて見直すという明示方針に、一切変更しない運用は合いません。配置の見直しの要否はその目的や得られた情報に照らして検討するもので、すべての学校で同じ変更期間を設けると断定できません。'],3,['S183','S179','S142'],
'TKT配置目的、CEFR9.3.6の直接課題と9.3.8の評価基準、Standards採点仕様を照合。知識と会話を把握する架空の学校方針を明示。複数方法の迅速性・客観性を保証せず、普及率や数日〜1週間という根拠不十分な一般化を除去。元の2段落は統合し旧段落を明示除去。',
['誤：全員ゼロ点を目指しても配置情報や信頼性を保証しない','誤：配置を単位授与と誤認し目的適合を検討しない','正：明示した知識と会話の対象に課題・基準を対応させる','誤：設問の見直し方針と一切変更しない運用が矛盾'])
k='Q_4_051';opts=q[k]['opts'].copy();opts[2]='診断評価は、強みや弱みの特定は行わず、コース終了時の成績の算出だけを目的として実施される。'
review(k,q[k]['stem'],opts,[
'クラス分けを目的とする配置テストや、強み・弱みを把握して指導計画に役立てる診断評価の説明が混ざっています。開始前という時期だけでなく、結果を何に使うかで区別します。',
'特定コースで教えた内容の達成度を測る目的は到達度テストに対応します。熟達度テストは言語の使用目的に対応する現在の能力を対象とし、特定教材を学んだ結果の確認とは区別されます。',
'成績の算出を中心とする説明は総括評価に対応します。診断評価は強みや弱みを特定して指導に役立てるため、この肢の「特定は行わず」と合いません。総括評価の結果を後の診断に利用することは可能で、終了時だから診断に使えないという意味ではありません。',
'学習の途中で得た理解や課題の情報を、フィードバックや指導の調整へ戻すという目的が形成評価に対応します。単に途中で実施するだけでなく、学習や指導の改善へ利用することが着眼点です。'],4,['S183','S179'],
'TKT Assessment/Test本文とCEFR9.3.1・9.3.5を照合。診断を開始前/途中に限定する誤解を除去し、成績だけが目的で強弱の特定を排除する誤答に精密化。総括結果の診断利用を認める。JLPTの全能力測定という未照合の例を除去。',
['誤：配置・診断の目的を総括とする','誤：到達度の目的を熟達度とする','誤：強弱の特定を排除し成績算出だけを診断とする','正：学習途中の情報を指導・学習の改善に使う'])
k='Q_4_059';opts=q[k]['opts'].copy()
opts[0]='Bさんの作文を、コースで定めた「理由を示して意見を述べる」という目標と評価基準に照らして評価した。'
opts[1]='Aさんの今回のテストの点数85点を、同じテストを受けたクラスの平均点70点と比べ、平均を15点上回ったと評価した。'
opts[3]='同じ読解テストを受けた100人の得点を比較し、その集団の中でDさんが20位だったと評価した。'
review(k,'評価において、その学習者自身の過去からの進歩を捉える個人内評価の事例に当たるものを一つ選びなさい。',opts,[
'あらかじめ定めた目標・基準への到達状況を見ています。この事例は、本人の以前の作文との比較によって進歩を判断したものではありません。',
'同じテストを受けたクラスの平均との比較です。85−70=15点ですが、この二つの値だけでは集団の何位か、上位何パーセントかまでは分かりません。',
'今回と3か月前の同じ学習者の録音を比べ、本人の進歩を捉えています。設問が指定した、本人の過去からの変化に目を向ける評価の事例です。他の目的の評価と併用できないという意味ではありません。',
'同じテストを受けた集団内での順位を見ているため、規範準拠評価の事例です。本人の以前の読解成績と比較した進歩の評価とは異なります。'],3,['S184','S179'],
'文科省FAQの評価用語段落とCEFR9.3.2を照合。本人の過去からの進歩という設問の範囲を明示。平均点だけから上位20%を推定する誤り、標準偏差だけから偏差値55を算出する条件欠落を除去。未照合のCEFR B1記述子はコース内の架空基準へ置換。四例は説明用の架空事例で実験結果ではない。',
['誤：コースの目標・基準への到達状況','誤：クラス平均という集団との比較','正：同じ本人の過去と現在を比較して進歩を捉える','誤：同じ受検集団内の順位'])
assert len(extra)==25,len(extra)
assert sum(bool(c.get('remove_paragraph')) for c in extra)==1
assert 85-70==15
for name,obj in [('changes.json',cs+extra),('changes_batch118.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path('/workspace/scratch/01d7c3f9b818');meta=[]
for sid,name,url,scope in [
('S183','tkt118.pdf','https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf','Assessment printed4-5/PDF5-6 and Test printed47/PDF48 full entries: diagnostic/formative/summative and achievement/placement/proficiency; not whole glossary or empirical effectiveness'),
('S184','mext118_faq.html','https://www.mext.go.jp/a_menu/shotou/gakuryoku/faq/001.htm','Historical FAQ question defining criterion/group/intraindividual evaluation and its complete answer; not current2003-era curriculum statements or present legal obligations'),
('S179','cefr116.pdf','https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf','2001 original printed183-185/PDF192-194 read as text and images;9.3.1-9.3.2 used; prior186-189 review reused for9.3.5-9.3.8')]:
 raw=(root/name).read_bytes();meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_read_scope=scope,retrieved='2026-10-16',full_source_redistributed=False))
(b.OUT/'evidence/batch118_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('four questions;25 edits incl1 obsolete paragraph')
