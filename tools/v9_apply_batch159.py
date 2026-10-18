"""Case13 source-bounded independent review, cumulative history only."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3166
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
common='S129共同開発者Kilmannの公開解説本文の二軸・全5様式と状況依存性を取得して精読。1974年の初版検査用紙・マニュアルを取得したとはしない。S213取得済み原PDFのSHA256を第158バッチ記録へ照合し、29–32・51–53頁を再精読、51–52頁画像照合。架空ケース13への定義の適用・明示された目的との対応であり、国籍別傾向、授業効果、対立の単独原因の実証ではない。'
items={
61:dict(answer=2,sources=['S129'],stem='ThomasとKilmannのTKIについて、共同開発者Kilmannの公開解説が示す五つの様式のうち、自分の関心を抑え、相手の関心を満たそうとするものを一つ選べ。',opts=['協働（collaborating）','受容（accommodating）','回避（avoiding）','競争（competing）'],exps=[
'協働は、自分と相手の双方の関心を十分に満たす解決を探る様式です。自分の関心を抑えて相手を優先するという設問の条件とは異なります。',
'受容は、自分の関心を抑えて相手の関心を満たそうとする様式です。自己主張が低く、相手への協力性が高いという二軸上の位置付けに対応します。',
'回避は、自分と相手のどちらの関心も追求せず、対立を扱わない様式です。相手の関心を満たそうとする受容とは区別されます。先送りだけが回避の形ではありません。',
'競争は、相手の関心を犠牲にして自分の関心を追求する様式です。自己主張が高く協力性が低いため、設問の条件とは逆です。'],verdicts=['誤：双方の関心の十分な充足を探る協働','正：自己主張低・協力性高の受容に一致','誤：両者の関心を追求しない回避','誤：自己主張高・協力性低の競争'],reason='曖昧な日本語の併記を英語名に対応する4様式へ整理。回避を先送りだけへ狭めず、性格の固定類型とも扱わない。'),
62:dict(answer=1,sources=['S129','S213'],stem='ケース13の次の話合いで、双方が一部を譲り、それぞれの希望が部分的にかなう中間案で合意したとする。この解決の仕方に当たるTKIの様式を、Kilmannの公開解説に基づいて一つ選べ。',opts=['妥協（compromising）','協働（collaborating）','競争（competing）','回避（avoiding）'],exps=[
'妥協は、双方が部分的に満足できる、互いに受け入れられる解決を探る様式です。設問が追加した、一部ずつ譲り合う中間案という条件に対応します。',
'協働は、双方の根底にあるニーズを探り、双方の関心を十分に満たす解決を探る様式です。部分的な充足で合意するという今回の条件は、妥協に対応します。',
'競争は、相手の関心を犠牲にして自分の関心を追求する様式です。双方が一部を譲って合意したという条件とは異なります。',
'設問では、双方が話し合って中間案に合意しています。対立を扱わない回避とは異なります。ケース本文の次回まで考える時間を設けたことだけで、対応全体を回避と決めることもできません。'],verdicts=['正：部分的な充足・譲歩交換という定義に直接一致','誤：双方の十分な充足を探る協働と部分的充足の妥協を区別','誤：一方が勝つ競争ではなく双方の譲歩が明示','誤：対立を扱って合意しており回避ではない'],reason='旧肢1の妥協または協働という二重分類を撤回。旧ケースの背景確認だけから両者を確定せず、次回の仮定として部分的充足・中間案の条件を設問へ明示し、妥協と協働を別肢にした。反省のための一時休止を一律に否定しない。'),
63:dict(answer=2,sources=['S213'],stem='ケース13の本文から直接読み取れる、進め方をめぐる対立の背景を一つ選べ。',overrides={1:'早い決定を優先するか、全員の納得まで話し合うかという、本人たちが述べた重視点の違い'},exps=[
'本文には、文法の誤りやその意味の取り違えを示す情報がありません。本人たちの発言を、文法能力の違いだけが原因だという証拠に置き換えることはできません。',
'本人たちは、早く決めることと全員の納得まで話し合うことを、それぞれ重視しています。RFCDC52頁の、対立の原因を文脈の中で捉える観点に沿う読みです。国籍や文化が単独の原因だと確定する判断ではありません。',
'本文には、双方が異なる進め方を重視して対立したという理由が示されています。特に理由がないとする説明は、この情報を無視しています。',
'本文には、発音が聞き取れなかったという情報がありません。発音の違いだけが原因だとするには、本文にない事実を加えることになります。'],verdicts=['誤：文法の誤り・取り違えの証拠がない','正：明示された迅速さと全員の納得という重視点に一致','誤：本文に対立した進め方の理由が示される','誤：発音による取り違えの証拠がない'],reason='文化が原因とする旧正答・解説を、本人の発言で確認できる重視点の相違へ限定。国籍からの推論を除き、本文にない原因は未提示と区別。'),
64:dict(answer=3,sources=['S213'],stem='ケース13で、学習者が意思決定の方法について意見を出し合い、合意を作る機会を設ける工夫として、RFCDC第1巻（2018年）の協働の説明に沿うものを一つ選べ。',overrides={},exps=[
'RFCDC51頁は、意見を表し他者の発言を促すことや、合意を作る技能を挙げます。学習者に話し合わせない方針は、今回求める学習者の合意形成の機会を設ける工夫ではありません。',
'国籍だけで分けても、意思決定の方法について意見を出し合う機会を設けたことにはなりません。30頁は文化集団の内部の多様性を示しており、同国籍なら同じ価値観だと推定する根拠にもなりません。',
'51頁の協働には、集団で意見を表し、他者の発言を促し、合意や妥協を作る技能が含まれます。事前にルールを話し合う時間を設けることは、これらを用いる機会を作る工夫です。対立の予防効果を保証する説明ではありません。',
'交流を最小限にする方針は、今回の設問が求める意見交換と合意形成の機会を設ける工夫ではありません。安全のため一時的に活動を中断する必要がある場合まで否定する説明ではありません。'],verdicts=['誤：発言を排除し今回の参加・合意形成の目的に不一致','誤：国籍による編成は意見交換機会を設ける行為ではない','正：51頁協働1–2の発言・合意形成を用いる機会の設計','誤：交流の最小化では今回求める合意形成機会を設けない'],reason='未取得のメタコミュニケーション理論と予防効果の断定を除去し、一次資料の技能を用いる機会の設計として出題。全てのルールの学習者決定を一般義務としない。'),
65:dict(answer=2,sources=['S213'],stem='ケース13で教師が明示した学習目標に対応する力として、RFCDC第1巻（2018年）の対立解決の説明に沿うものを一つ選べ。',overrides={1:'異なる視点を聞いて理解し、双方が受け入れられる解決を対話で探る力'},exps=[
'教師は、異なる重視点を聞き合い、双方が受け入れられる解決を探ることを目標として明示しています。発音の正確さだけに限定する肢は、この目標に対応しません。',
'RFCDC52頁は、当事者の異なる視点の理解、解決の選択肢の検討、受け入れられる解決への支援を挙げます。これらに対応する力は、本文で教師が明示した目標に合います。この授業だけでその力の習得が完了したとする判断ではありません。',
'本文の目標は、異なる重視点を理解して解決を探ることです。文法と語彙だけに限定する肢は、この目標に対応しません。文法や語彙の学習の価値を否定する説明ではありません。',
'本文の目標には、どの言語を用いるかだけでなく、異なる重視点を聞き合って解決を探る過程が含まれます。特定の言語を話せることだけに限定する肢は、この目標に対応しません。'],verdicts=['誤：明示した対立解決の目標を発音だけへ縮小','正：52頁5・10–12と本文に明記した教師の目標に対応','誤：文法・語彙だけでは明示した解決探索の目標に対応しない','誤：特定言語の使用だけでは視点理解・解決探索に対応しない'],reason='教師の意図を未提示のまま推定しないよう架空ケースに目標を明記。独自の異文化調整能力という一括名称を具体的技能へ改訂し、習得効果の測定と区別。')}
extra=[]
old='ケース13　多文化クラスにおけるコンフリクト・マネジメントの実践'
oldbody='教師は、対立を一方的に裁定するのではなく、双方の主張の背景にある価値観を確認し合う時間を設け、双方が譲歩できる点と譲れない点を整理させた上で、次回までに解決策を持ち寄るよう促した。'
newbody=oldbody+'教師は、この活動の目標を、異なる重視点を聞き合い、双方が受け入れられる解決を対話で探る力を育てることだと説明した。'
for before,after,count in [(old,old+'（架空事例）',2),(oldbody,newbody,1)]:
 assert [p.text for p in Document(b.DST).paragraphs].count(before)==count
 extra.append(dict(id='CASE13',field='case_text',index=None,before=before,after=after,count=count,reason=common+'架空事例の目標を明示、見出しは問題編・解説編を同期。',sources=['S213'],applied=True,before_version='第158バッチ反映後'))
for n,v in items.items():
 k=f'Q_O_{n:03}';ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and int(a[ak]['ans'])==v['answer']
 opts=v.get('opts',[v.get('overrides',{}).get(i,t) for i,t in enumerate(q[k]['opts'])])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(before,after) in enumerate(zip(olds,news)):
   if html.unescape(before)==after:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=common+v['reason'],sources=v['sources'],applied=True,before_version='第158バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==v['answer']-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['answer'],fixes_applied=True,sources=v['sources'],reason=common+v['reason'],option_verdicts=v['verdicts'],candidate_answers=[],stem_review='架空ケース13の全2段落・設問・4肢を独立比較。定義、明示条件、本人の発言と教師の明示目標に限定。',explanation_review='全4解説をS129の二軸・5様式、またはS213の29–32・51–53頁に照合。国籍別傾向、単独原因、予防効果、習得完了を推定しない。',unresolved='',multiple_correct_risk='なし：明示条件に合うのは'+str(v['answer'])+'のみ',no_correct_risk='なし：独立正答'+str(v['answer']))
assert len(extra)==37,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch159.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'rfcdc150.pdf').read_bytes();prior=json.loads((b.OUT/'evidence/batch158_sources.json').read_text())[0];assert hashlib.sha256(raw).hexdigest()==prior['sha256']
e=[dict(source_id='S129',url='https://kilmanndiagnostics.com/a-brief-overview-tki/',title='Ralph Kilmann, A Brief Overview of the Thomas-Kilmann Instrument',retrieved='2026-10-18',read_scope='公開HTML本文195–212行の二軸定義、全5様式、譲歩・中間案、全様式の利用可能性と状況依存性を精読。',limitations='共同開発者自身による定義説明の一次資料。1974年初版用紙・原マニュアルや妥当性実験を取得・承認したものではない。本文非転載。',full_source_redistributed=False),dict(source_id='S213',url=prior['url'],original_acquisition_record='evidence/batch157_sources.json',revalidated='2026-10-18',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),pdf_pages=89,read_scope='29–32・51–53頁本文を再精読、51–52頁（PDF53–54頁）を1800px全頁画像照合。',limitations='取得済み原本の再検証。全89頁通読、国籍別価値観や授業効果の実証ではない。原PDF非転載。',full_source_redistributed=False)]
(b.OUT/'evidence/batch159_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('5questions /37entries /keys2,1,2,3,2')
