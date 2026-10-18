"""Reconstruct the unsaved memory audit against the authoritative batch171."""
import json, html, hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT; cs=json.loads((p/'changes.json').read_text()); assert len(cs)==3390
d=json.loads((p/'decisions.json').read_text()); _,q,a=qa.audit(str(b.DST))
data=[
('Q_3_009',4,['S230'],
'アンダーソン（1982）「Acquisition of Cognitive Skill」のACTによる技能獲得の説明として、最も適切なものを一つ選べ。',
[
'宣言的知識はプロダクションとして、手続的知識は命題ネットワークとして表される。',
'手続き化が進むと、対応する宣言的知識は必ず消去され、以後は思い出せなくなる。',
'知識が手続的な形になれば、それ以後は調整や処理速度の向上に関わる学習は起こらない。',
'知識コンパイルは、宣言的知識を解釈して行う遂行から、知識を直接適用する手続的な遂行への移行を説明する。'],
[
'原論文370頁の表現形式の対応を逆にしています。ACTでは、宣言的知識を命題ネットワーク、手続的知識を条件と行為からなるプロダクションで表します。',
'383頁の電話番号の例は、手続き化されたプロダクションの形成が、対応する宣言的表象の喪失を必ず伴うわけではないと明記しています。手続き化と宣言的知識の一律消去は別です。',
'370頁では、手続的な形になった後にも、より適切な適用に向けた調整や段階的な高速化が続くと説明しています。手続き化の成立を、その後の学習の終了とする説明は合いません。',
'370頁の移行の説明に対応します。382～383頁では、複数のプロダクションをまとめる合成と、領域固有の知識をプロダクションへ組み込む手続き化を区別します。手続き化だけで、あらゆる課題を無意識・無誤りに行えるとする主張ではありません。'],
'S230原論文370・381～383頁を取得照合。Fittsの3段階の紹介とAnderson自身の宣言的／手続的な段階を区別し、手続き化と自動化の同一視、全第二言語処理の無意識化保証を撤回。全4肢全4解説をACTの表現形式・コンパイル・その後の学習に限定。',
['誤：表現形式を逆転','誤：宣言的表象の喪失を必然とする','誤：手続化後の学習を否定','正：知識コンパイルの移行に対応']),
('Q_3_010',4,['S230','S232'],
'学習者が「書く」のて形は「書いて」になると正しく説明したが、自由会話のある場面では「書きて」と発話したとする。アンダーソンの宣言的知識と手続的な遂行の区別を踏まえた、この観察の扱いとして最も適切なものを一つ選べ。',
[
'ルールを説明できる知識は、練習を経ても遂行には一切関わらないので、説明課題と会話課題を比較する意味はない。',
'この誤用は、ルールを説明する宣言的知識が完全に失われていることを証明する。',
'ルールを正しく説明できたので、場面や負荷にかかわらず、会話での手続的な遂行も常に完全である。',
'規則を説明できることは示されているが、会話で安定して使えるかは別に確かめる必要がある。一回の誤用だけで原因や手続き化の程度は断定しない。'],
[
'原論文370・381頁は、宣言的知識を解釈して遂行する段階と、練習を経てより直接的な手続的遂行に移る過程を扱います。説明できる知識が遂行に一切関わらないとする説明は、この立場と合いません。',
'設問では、その規則を正しく説明できたという観察もあります。誤用の一例だけを取り上げて、説明できる知識が完全に失われたとする判断は、その観察と矛盾します。',
'宣言的な形で知識を扱えることと、会話の処理で安定して使えることは同一の観察ではありません。原論文381頁も、宣言的知識を解釈する遂行では時間や作業記憶への負荷が問題になると説明します。説明課題の成功だけでは、どの場面でも完全な遂行になるとはいえません。',
'二つの課題で示されたことを区別する判断です。規則説明の成功は、その場で規則を説明できたことを示しますが、会話の処理全体が安定しているという証明ではありません。手続き化の不足は検討できる仮説でも、単発の誤用だけから唯一の原因や習得段階を認定することは避けます。'],
'S230の宣言的知識の解釈・作業記憶負荷・手続的遂行の区別を架空事例へ適用。S232のて形表「かきます→かいて」を本文確認。単発誤用から自動化不足を確定する旧説明、完全な自動化なら無誤用という含み、未取得モニター理論の説明を撤回。原因特定ではなく観察から言える範囲を問う。',
['誤：宣言的知識の遂行への関与を全否定','誤：規則説明の成功という観察と矛盾','誤：全場面で完全な遂行を保証','正：観察と原因診断を区別']),
('Q_3_011',1,['S231'],
'アトキンソンとシフリン「Human Memory A Proposed System and Its Control Processes」の公刊前原稿に示された記憶の枠組みに合う説明を一つ選べ。',
[
'短期貯蔵は、感覚登録器から選ばれた情報と長期貯蔵からの情報を受け取り、リハーサルは限られた情報の保持を維持する制御過程の一つである。',
'長期貯蔵に保持された情報が短期貯蔵へ戻る経路はなく、検索して利用することも想定されていない。',
'一つの貯蔵から別の貯蔵への転送は、情報を元の貯蔵から必ず消して移すことを意味する。',
'感覚登録器は、感覚入力の情報をそれ自体で数日から数週間保持する領域として説明されている。'],
[
'原稿2頁の3構成要素と制御過程の説明に対応します。短期貯蔵は感覚登録器と長期貯蔵からの入力を受け取り、リハーサルにより限られた情報を維持できます。貯蔵という構造的な区分と、保持のために用いる制御過程を区別しています。',
'図1と8頁本文は、長期貯蔵から短期貯蔵への情報の転送を示し、問題解決や思考での利用を例に挙げています。長期貯蔵を、検索して利用できない領域とする説明ではありません。',
'2・8頁では、転送を、選ばれた情報を別の貯蔵へ写すこととして説明し、元の貯蔵から情報を除去することとは区別しています。一方通行の移動で必ず元が空になるという説明は合いません。',
'5・9～10頁は、視覚の感覚登録で情報が短い時間に失われることを説明しています。感覚登録器そのものが数日・数週間の保持を担うという説明ではありません。原稿が示す仮説的な枠組みであり、全感覚で同じ保持時間が確定したという意味でもありません。'],
'S231 Stanford公開の著者公刊前原稿の2・5～10頁と図1を本文照合し図1・8頁画像確認。旧7±2と4項目の混在、長期記憶の半永久的保存の保証、情報流の一方向固定を撤回。原稿自身が感覚登録器から長期への直接経路を未確定としていることも尊重し、実在の確定経路として教えない。',
['正：構造と制御過程を区別し本文に対応','誤：長期から短期への転送を否定','誤：転送を原貯蔵からの必然的消去とする','誤：感覚登録の保持を数日・数週間とする'])]
extra=[]
for k,key,sources,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第171バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='原論文の枠組みを指定し独立比較。3_010は明示した架空の観察事例であり実験・診断の事実ではない。',explanation_review='全4解説を取得した原論文本文または原稿本文へ照合。手続化と自動化、構造と制御過程、枠組みと実証、観察と原因診断を区別。全原著・全引用先の検証とはしない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ対象の本文または明示された観察に整合',no_correct_risk=f'なし：{key}が本文または観察に対応')
assert len(extra)==27
for n,obj in [('changes.json',cs+extra),('changes_batch172.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [
 ('S230','anderson172.pdf','https://gwern.net/doc/iq/1982-anderson-2.pdf?download=1','Anderson1982原論文の第三者保管スキャン全38頁を取得。369～370・373・381～383頁本文、370・383頁画像。ACT1976書籍、Fitts1964原著、NevesAnderson1981未取得。'),
 ('S231','memory172.pdf','https://web.stanford.edu/group/csli-suppes/techreports/IMSSS_110.pdf','Stanford公開の著者公刊前原稿全194頁取得。表紙・原稿2・5～10頁本文、図1（6頁）・8頁画像。出版版の頁と同一視しない。全実験・引用先原著精読ではない。'),
 ('S232','tufs172.html','https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/043.html','東京外国語大学て形解説本文全体・全表。かきます→かいて。架空事例の誤用原因を実証する資料とはしない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch172_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
