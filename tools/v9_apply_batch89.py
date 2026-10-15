"""One-time original-paper review of communication strategy classifications."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1972
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
ref='Celce-Murcia・Dörnyei・Thurrell（1995）「Communicative Competence: A Pedagogically Motivated Model with Content Specifications」'
items={
'Q_2_013':(4,ref+'の27〜28頁に示された分類に対応する説明を一つ選びなさい。',[
'伝えようとした内容を諦めたり話題を避けたりする行動は、達成・補償ストラテジーの例である。',
'考える時間を得るためのフィラーや反復は、時間稼ぎではなく、すべて話題回避のストラテジーである。',
'母語の語を目標言語風の発音にして不足を補う行動は、回避・縮小ストラテジーの例である。',
'使える言語資源を工夫して伝達目標を達成し、言語知識の不足などを補う行動は、達成・補償ストラテジーに対応する。'],[
'同論文27頁と28頁の表5は、話題回避や伝達内容の放棄を回避・縮小ストラテジーに挙げています。伝えようとする内容を維持して不足を補う達成・補償とは区別します。',
'同論文27頁と表5は、考える時間を得るフィラーや反復を時間稼ぎの方略に挙げています。すべて話題回避と分類する説明は対応しません。',
'表5は母語の語を目標言語の発音に寄せる行動を達成・補償の欄に挙げています。この肢は、知識の不足を補って伝達しようとする行動を回避・縮小に分類しているため対応しません。',
'同論文27頁の達成・補償の説明に対応します。使える言語資源を用いて伝達目標に向かい、不足を補う行動です。あらゆる研究の分類が同一という意味ではなく、指定した論文の区分を問うています。'],[
'誤：話題回避・放棄は回避縮小','誤：時間稼ぎを回避だけと誤分類','誤：母語を目標言語風にする補完は達成補償','正：利用可能資源で目標達成し不足を補う']),
'Q_4_021':(3,ref+'の28頁表5を基準に、意味の交渉に関わる方略名と発話例が対応するものを一つ選びなさい。',[
'明確化要求：話し手が「私の説明についてこられますか」と、聞き手が理解できているかを確かめる。',
'時間稼ぎの方略：聞き手が「その言葉はどういう意味ですか」と、理解できない点の説明を求める。',
'確認要求（確認チェック）：聞き手が「今、火曜日とおっしゃいましたか」と、相手の発話を正しく聞き取ったか確かめる。',
'理解チェック：聞き手が「すみません、もう一度言ってください」と、相手の発話の反復を求める。'],[
'表5の理解チェックには、相手が話についてこられるか確かめる発話が挙げられています。この肢は話し手が相手の理解を確かめており、理解できない点の説明を求める明確化要求とは違います。',
'表5では、意味や説明を尋ねる発話は明確化要求に対応します。フィラーや反復によって考える時間を得る時間稼ぎの例ではありません。',
'表5の確認要求には、相手が何と言ったかを確かめる発話が挙げられています。この肢は相手の発話の聞き取りを確認しており、方略名と行動が対応します。',
'表5は、もう一度言うよう求める反復要求と、理解できない点の説明を求める明確化要求を区別しています。この肢は反復要求であって、話し手が相手の理解を確かめる理解チェックではありません。'],[
'誤：例は話し手による理解チェック','誤：例は意味の説明を求める明確化要求','正：相手が何と言ったかの確認要求','誤：例は相手への反復要求'])}
extra=[]
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert len(parts)==1
 reason='S149原論文印刷26〜29頁（PDF12〜13頁）の本文と表5を画像照合。著者ら自身の分類に限定し、Canale/Swain1980、Canale1983、Varonis/Gass1985原著全体の取得とは扱わない。分類体系と行動を指定し、母語借用の例の不適切さや反復・明確化・理解確認の混同を修正。'
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S149'],applied=True,before_version='第88バッチ反映後の累積作業稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S149'],reason=reason,option_verdicts=verdicts,stem_review='全4肢を原論文の本文・表5により独立判定。特定の分類を指定し、母語話者での頻度や熟達度の一般論は未照合のまま掲載しない。',explanation_review='全4解説をS149印刷26〜29頁で照合。旧問21所見にあったシラバス構成単位という別主題の理由は実際の設問と一致しないため撤回。リキャストの定義・辞書使用・指導効果の未照合主張を残さない。',unresolved='',multiple_correct_risk='なし：指定分類と対応するのは一つ',no_correct_risk='なし：独立正答'+str(ans))
e=d['Q_2_018'];assert e['status']=='要追加確認';e['sources']=sorted(set(e.get('sources',[])+['S149']));e['unresolved']+=' S149の著者らは独自のモデルを述べる一次資料だが、同論文による1980/1983の説明は二次的な紹介であり、問18の原著本文照合に代用しない。'
assert len(extra)==18
for name,obj in [('changes.json',c+extra),('changes_batch89.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('2 full reviews/18edits; Q_2_018 remains unconfirmed')
