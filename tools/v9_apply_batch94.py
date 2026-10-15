"""One-time Rosch original-chapter review; do not replay over newer decisions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2103
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_5_074':(3,'Rosch（1978）「Principles of Categorization」の知見を、語彙や多義語の指導を考える手がかりにするときの留意点として、同章の説明に対応するものを一つ選びなさい。',[
'原型とは常に一つの具体的な成員そのものであり、自然言語の全カテゴリーについて同じ方法で一意に決まる。',
'典型性による反応時間の差があれば、多義語を教える唯一最適な順序と教材の効果まで確定できる。',
'典型性の差という知見と、処理・表象・学習の特定モデルを区別し、そこから特定の指導法の効果を直ちに保証しない。',
'同章は、あらゆる多義語の全用法が一つの中心義から歴史的に派生したことを実証している。'],[
'同章40頁は、自然言語のカテゴリーで原型を単一の実体とみなすことを戒めています。原型という語を一つの具体物に固定する説明ではありません。',
'同章38〜41頁は典型性に関わる課題成績と、特定の処理・表象・学習モデルを分けています。語彙指導の唯一の最適順序を実証した章ではありません。',
'同章28・40〜41頁で明示された留保に対応します。カテゴリーの典型性の研究を、語彙指導の効果保証や全語の意味史の証明に拡張しません。',
'同章はカテゴリーの構造と典型性を論じています。すべての多義語の歴史的な派生経路を調査・実証したという記述は対応しません。'],[
'誤：自然言語の原型を単一実体に固定','誤：課題成績から唯一最適な指導法へ飛躍','正：典型性の知見と特定モデル・指導効果を区別','誤：カテゴリー研究を全多義語の意味史の実証に拡張']),
'Q_M_016':(3,'次は考え方を確認するための架空の調査である。同じカテゴリーに属する複数の対象について、そのカテゴリーの「よい例」だと思う程度を尋ねたところ、評定に差があった。Rosch（1978）の典型性の観点に対応する解釈として、最も適切なものを一つ選べ。',[
'この評定は、異なる階層のカテゴリー同士の包含関係だけを測定している。',
'同じカテゴリーに属する対象は、どれも必ず同じ程度によい例だと判断される。',
'同じカテゴリーの成員でも、そのカテゴリーのよりよい例と判断される程度が異なりうる。',
'この差だけで、対象が頭の中にどのような形式で表象されているかが一意に確定する。'],[
'ここで尋ねたのは同一カテゴリー内の成員の典型性です。同章30頁の、包含関係による垂直方向の階層とは区別します。',
'同章36頁は、カテゴリー内の成員に典型性の差が認められることを述べています。この肢は差を認めない説明です。',
'同章36頁では、成員がそのカテゴリーのよい例である程度の判断によって典型性を操作的に捉えています。この架空調査を原著の実験結果とはしていません。',
'同章40〜41頁は、典型性の知見だけで特定の表象モデルを決めることを戒めています。評定差だけから一意の心的表象は導きません。'],[
'誤：典型性評定と階層的包含を混同','誤：同一カテゴリー内の典型性の差を否定','正：成員間の典型性の差に対応','誤：典型性の差から表象形式を一意に断定']),
'Q_M_058':(1,'Rosch（1978）32頁の表2.1では、furniture（家具）―chair（椅子）―kitchen chair（台所用の椅子）という階層例が示されている。同表でchairに対応する位置づけを一つ選べ。',[
'基本レベルのカテゴリー',
'上位レベルのカテゴリー',
'下位レベルのカテゴリー',
'階層上の位置ではなく、同一カテゴリー内の典型性の評定値'],[
'表2.1はchairを基本レベルの欄に置いています。この指定表での位置づけを問い、日本語の全話者・全場面での使用頻度を主張していません。',
'表2.1の例で上位レベルの欄にあるのはfurnitureです。chairの指定された位置とは異なります。',
'表2.1の例で下位レベルの欄にあるのはkitchen chairなどです。chairそのものの位置とは区別します。',
'同章は包含関係による垂直方向の階層と、同一カテゴリー内の典型性を区別します。この表の欄名は典型性の評定値ではありません。'],[
'正：表2.1でchairは基本レベル','誤：上位レベルはfurniture','誤：下位レベルはkitchen chair等','誤：階層上の位置と典型性の評定値を混同'])}
reason='S153 Rosch1978原著の22頁PDFを取得し、印刷28・30〜41・42〜43頁を画像で精読。典型性と階層の区別、表2.1、原型は特定の処理・表象・学習モデルではないという留保を照合。単一中心義から全多義語が歴史的に派生する普遍断定、かみ三語の未照合の語源、唯一効率的な指導法、犬やスズメの文化普遍的典型性・頻度の断定を撤回。'
extra=[];removed=0
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S153'],applied=True,before_version='第93バッチ反映後の累積作業稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問の継続段落を明示削除。'+reason));removed+=1
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S153'],reason=reason,option_verdicts=verdicts,stem_review='Rosch1978の本人の整理・表と指定した架空評定課題を基準に全4肢を独立判定。全多義語の単一中心ネットワークという旧主張は承認せず、原型理論を指導へ援用する際の限界を問う改訂。',explanation_review='4解説を原著の28・30・32・36・38〜41頁画像と照合。全語の語源史、日本語話者の頻度、特定指導法の普遍効果、引用先の各原研究全体は承認しない。',unresolved='',multiple_correct_risk='なし：指定した原著・課題に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27+removed
for name,obj in [('changes.json',c+extra),('changes_batch94.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(f'3fullreviews;{len(extra)}edits;{removed}old-stem removals')
