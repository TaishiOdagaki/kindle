"""Replace unsupported immigration detail and bound assimilator interpretation."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3453
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_1_013',3,'S236',
'外務省の2026年1月22日付「高度専門職査証：高度専門職、特別高度人材」の案内に合う説明を一つ選べ。ここでは同案内の査証申請手続を問い、高度専門職2号の国内手続や永住許可の要件は扱わない。',
[
'高度専門職外国人の家族等には、申請しても在留資格認定証明書は一切交付されない。',
'必要書類は全ての国籍で完全に同一であり、国籍による追加書類はないと案内されている。',
'滞在期間は5年と案内され、高度専門職外国人の査証申請では在留資格認定証明書の提示が必ず必要とされている。',
'電子在留資格認定証明書の提示や写しの提出は認められず、紙の原本だけが必要とされている。'],
[
'注2では、高度専門職外国人の家族等についても、申請に基づき在留資格認定証明書が交付されると説明しています。申請しても一切交付されないという説明は合いません。家族等の全ての申請が無条件で許可されるという意味ではありません。',
'注1は、申請者の国籍によって記載事項以外にも必要書類があると説明し、各在外公館の案内を参照するよう求めています。本文にも中国籍の方の追加書類や申請書等の通数の違いが示されています。全ての国籍で完全に同一という説明は合いません。',
'案内の滞在期間欄と注2に対応します。このページで説明される査証申請手続を答えるもので、国内の在留資格変更・更新や高度専門職2号まで一律に5年とする主張ではありません。',
'必要書類欄は在留資格認定証明書の原本又は写しを挙げ、電子在留資格認定証明書の場合は同証明書の提示又は写しの提出としています。紙の原本しか認めないという説明は合いません。'],
'S236外務省2026-01-22付の公式案内本文・表・注1/2を取得照合。旧稿のポイント制・活動類型・親帯同・配偶者就労・2号・永住・技能実習からの移行の残存主張は本文取得できておらず承認せず、同じ高度専門職領域の査証手続へ差替え。1号と2号を混同する一般化、年収要件を一律に扱う説明を掲載しない。ISAの2ページは403であり検索抜粋を本文照合の代用にしない。',
['誤：家族等への認定証明書交付を全否定','誤：国籍による必要書類の違いを否定','正：対象案内の5年と認定証明書提示に一致','誤：原本だけに限定し電子証明書等を否定']),
('Q_4_097',1,'S237',
'Weldonほか（1974）の技術報告書「A Laboratory Test of the Effects of Culture Assimilator Training」が説明するカルチャー・アシミレーターの学習形式に合うものを一つ選べ。',
[
'集団間の対立を含む事例を読み、行動の理由について複数の解釈から選び、選択に対するフィードバックを受ける。',
'事例や解釈を示さず、単語の発音だけを聞いて模倣する反復練習を行う。',
'他の集団の視点を取り上げず、学習者側の文化が常に優れていると確認する。',
'解釈を選んだ後には説明を与えず、選択した理由について考え直す機会も設けない。'],
[
'報告書3頁の説明に一致します。事例中の他集団の行動について解釈を選び、別の頁でフィードバックを受けます。学習形式の説明であり、それだけで実際の対人行動が必ず改善するという効果の保証ではありません。',
'報告書3頁で提示されるのは、集団間の対立を含む事例と、行動の原因に関する解釈です。単語の発音を模倣するだけの練習という説明には対応しません。',
'報告書3頁は、他の集団の人々による解釈に近づけるための訓練として説明します。学習者側の文化の優越を確認し、他集団の視点を排除する形式ではありません。',
'報告書3頁では、選択後にフィードバックを受け、不適切な解釈を選んだ場合には、事例を再検討して別の解釈を選ぶよう促すとあります。適切とされる解釈にも理由の説明が伴います。'],
'S237 Weldon・Carlston・Rissman・Slobodin・Triandis1974技術報告書の3頁全文と画像を照合。事例・解釈選択・分岐フィードバックを確認。旧稿の効率的な内面理解や一般的な行動改善保証を撤回し、報告書にある学習形式に限定。未取得1971原著の内容を確認したとはしない。',
['正：事例・解釈選択・フィードバック','誤：事例と解釈を発音模倣へ置換','誤：他集団の視点を排除し自文化優越を目的化','誤：フィードバックと再検討を否定']),
('Q_4_102',3,'S237',
'Weldonほか（1974）の報告書3頁は、アメリカ人がタイの人々の視点を理解するためのカルチャー・アシミレーターで、訓練上の「正解」を定める例を示している。その説明に合うものを一つ選べ。',
[
'作成者一人がタイの人々の考えを推測し、両集団には解釈への反応を尋ねずに決める。',
'学習者となるアメリカ人側のパネルが選ぶ解釈だけを正解とし、タイ人側の反応は使わない。',
'両集団のパネルに解釈への反応を尋ね、タイ人側が選びアメリカ人側が選ばない解釈を、タイの視点を理解する訓練のために正解とする。',
'ある解釈を訓練上の正解としたら、以後は国籍だけから、全ての個人の行動原因を同じものと断定する。'],
[
'報告書3頁では、アメリカ人とタイ人のパネルに各解釈への反応を求めています。作成者一人の推測だけで決め、対象となる集団の反応を求めないという説明は合いません。',
'例示では、タイ人側が選び、アメリカ人側が選ばない解釈を、アメリカ人がタイの視点を理解するという訓練目的に照らして正解としています。学習者側の選択だけを基準にする説明とは逆です。',
'報告書3頁末のパネルを用いる例に一致します。「正解」はここで説明される訓練目的に対する位置づけです。全てのタイ人が同じ理由で行動する、あるいは個々の出来事には文化以外の原因がないという証明ではありません。',
'報告書の例は、パネルの反応を使った教材中の解釈の選定です。その観察から、国籍が同じ全個人の行動原因を一つに決めるという結論は導けません。訓練上の解釈の選定と、実在の個人の原因診断を区別する必要があります。'],
'S237報告書3頁の両集団パネル・訓練目的上の正解の定め方を本文画像で照合。対象文化の視点を客観的に一つに確定するという旧説明を改訂。パネルに基づく教材上の基準と、国籍から実在個人を断定する推論を区別。全対象者の同一性や文化のみの因果説明は承認しない。',
['誤：両パネルの反応を作成者一人の推測にする','誤：対象集団のパネルの役割を逆転','正：両パネルと訓練目的上の選定に対応','誤：教材の選定から全個人の原因を断定'])]
extra=[]
for k,key,sid,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']==('修正必要' if k=='Q_1_013' else '要追加確認') and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第174バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='資料の主体・日付・対象範囲を明示して独立比較。取得できなかった旧主張全体を承認した扱いにはしない。',explanation_review='設問・全4肢・全4解説を取得した本文に照合。手続と在留資格全般、訓練目的上の解釈と個人の原因診断、方法と効果保証を区別。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定資料に一致',no_correct_risk=f'なし：{key}に対応する本文取得済み')
assert len(extra)==27
for n,obj in [('changes.json',cs+extra),('changes_batch175.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [
 ('S236','mofa175.html','https://www.mofa.go.jp/mofaj/toko/visa/chouki/visa16.html','外務省2026-01-22付高度専門職査証案内の表・注1/2本文全体。原本／写し／電子証明、国籍条件、家族等への認定証明書、滞在期間5年。同2号の国内手続、ポイント全項目、親帯同・配偶者就労・永住の条件全般は照合対象外。'),
 ('S237','assimilator175b.pdf','https://files.eric.ed.gov/fulltext/ED095249.pdf','Weldon et al.1974 Technical Report20の43頁PDF。表紙、Triandis序、本文1～6頁、25・32頁を精読、本文3頁の画像確認。形式・パネルによる訓練目的上の正解の選定。1971原著・1970報告・全実証研究の再検証ではない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch175_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
attempts=[dict(url=u,outcome=o,used_to_approve=False) for u,o in [
 ('https://www.moj.go.jp/isa/applications/resources/newimmiact_3_qa.html','本文取得403。検索結果に本文らしき記載があるが本文照合の代用としない。'),
 ('https://www.moj.go.jp/isa/publications/materials/newimmiact_3_preferential_index.html','本文取得403。ブラウザ迂回なし。'),
 ('https://files.eric.ed.gov/fulltext/ED042343.pdf','curl --failのHTTP404。1970原報告本文未取得。1974共同著者を含む別の一次研究報告を取得し、明示して採用。')]]
(p/'evidence/batch175_source_attempts.json').write_text(json.dumps(attempts,ensure_ascii=False,indent=2)+'\n')
