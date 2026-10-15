"""One-time original Holec review of autonomy and learning support."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2075
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_4_006':(2,'次は教材用の架空事例である。作文の学習者は「説明文を丁寧体で統一して書けるようになりたい」と教師に相談した。現在の作文には「昨日は映画を見ました。とても面白かった」とある。Holec（1981）の、学習者が学習を引き受ける能力の発達を支える立場に照らし、最も適切な対応を一つ選びなさい。文体の混在がすべての文章で誤りだという前提は置かない。',[
'学習者が示した目標は話し合わず、教師が別の目標を決め、学習者には知らせずに採点する。',
'目標と見直しの観点を話し合い、文末を比較する方法を提案し、学習者自身が推敲して目標に照らして振り返る機会を設ける。',
'学習者の目標や判断は不要と伝え、教師の訂正文を理由を考えず10回写すことだけを求める。',
'教師が修正・評価をすべて引き受け、学習者が方法を選んだり自分で振り返ったりする機会は今後も設けない。'],[
'学習者の目標を扱わず、判断も共有しない設定です。本人が目標や評価を引き受ける能力を支える方針に合いません。',
'教師が助言しつつ、本人が方法を使い、結果を目標に照らして検討する機会を設けています。一度の活動で自律性の完成を保証するものではありません。',
'理由を考えず写すことだけを求め、本人の目標や判断を排除しています。反復練習一般の効果や情意フィルターの変化を断定する説明ではありません。',
'ここで問題なのは、本人の選択や振り返りを今後も排除する条件です。教師による明示的訂正が常に不適切という意味ではありません。'],[
'誤：本人の目標と判断を排除','正：助言と本人による方法・評価の検討を両立','誤：本人の目標と判断を不要とする','誤：本人の選択・振り返りを継続的に排除']),
'Q_M_017':(1,'Holec（1981）の定義に基づく学習者オートノミーの説明として、最も適切なものを一つ選べ。',[
'自分の学習を引き受ける能力であり、目標、内容、方法、学習の進め方、評価に関する判断を含む。',
'教師がその場にいなければ、目標や方法を誰が決めていても、必ず自律性が成立している。',
'教師の助言を一度でも受けると、その学習者には自律性がないと判定される。',
'能力ではなく行動だけを指すため、自律性を持つ学習者は常にその能力を全面的に使わなければならない。'],[
'自律性は学習を引き受ける能力です。その能力と、実際に自己主導で学ぶ行動・形態を区別します。',
'教師の不在だけでは、目標・内容・方法などの決定主体は分かりません。それだけで自律性とは判定できません。',
'同書は教師の支援を受ける自己主導学習も認めています。助言の有無だけで否定しません。',
'同書は能力と行動を区別し、能力を持っていても常に全面的に行使するとは限らないと述べています。'],[
'正：能力としての定義と判断領域に対応','誤：教師不在と自律性を同一視','誤：支援を受ける学習を排除','誤：能力とその行使を同一視']),
'Q_O_074':(1,'ケース15は教材用の架空事例である。教師の助言を受けた学習者が、自分の学習を振り返り、計画や方法を選んで実践したという記述に着目する。Holec（1981）の立場に照らし、この働きかけの意義として最も適切なものを一つ選べ。',[
'学習者が自分に合う方法を検討し、自ら学習を引き受ける能力を育てるための支援と捉えられる。',
'学習者に判断させず、計画・方法・評価をすべて教師が固定することが目的である。',
'教師が決めた一つの方法を、本人の目標や状況にかかわらず必ず選ばせることが目的である。',
'数週間後の成績の記述だけから、この指導がすべての学習者に同じ効果を生むと証明できる。'],[
'助言を受けながらも本人が方法や学習の進め方を検討しています。支援と本人の責任の両立を考える例です。',
'本人が方法を選んだというケースの事実に合いません。教師が判断を全面的に固定したという記述はありません。',
'自分に合った方法を本人が選んだという記述に反します。一つの方法を全員に強制する設定ではありません。',
'この教材用の架空事例は、指導効果の実証研究ではありません。成績の記述を普遍的な因果効果に拡張できません。'],[
'正：助言を受けつつ本人が学習を検討','誤：本人による選択というケースの事実と不一致','誤：唯一の方法の強制はケースにない','誤：架空事例を普遍的効果の証拠にする'])}
reason='S152 Holec1981原著公開本文の3〜4頁（能力と行動、支援の有無）、23〜24頁（学習を支える教師の助言）を照合。文体混在の無条件の誤用前提、反復・明示的訂正の効果の一律断定、自律性と教師不在・学習形態の同一視を撤回。ケース15は既存本文も照合し教材用の架空事例であり普遍的効果の証拠ではないと明示。'
extra=[];removed=0
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']!='確認済み' and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S152'],applied=True,before_version='第92バッチ反映後の累積作業稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問の継続段落を明示削除。'+reason));removed+=1
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S152'],reason=reason,option_verdicts=verdicts,stem_review='原著の定義と支援の立場、明示した学習目標または教材用ケースの事実から全4肢を独立判定。能力と行動・学習形態を区別。',explanation_review='全4解説をS152本文3〜4・23〜24頁と対応。特定の反復・訂正方法が情意面・自律性へ必ず及ぼす効果は断定しない。架空事例から効果を実証したとは扱わない。',unresolved='',multiple_correct_risk='なし：指定定義・明示条件に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27+removed
for name,obj in [('changes.json',c+extra),('changes_batch93.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(f'3fullreviews;{len(extra)}edits;{removed}old-stem removals')
