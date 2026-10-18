"""One-time institutional primary-text audit; rebuild separately."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3498
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_1_017',3,'S188',
'総務省自治行政局国際室「地域における多文化共生推進プランの改訂について」の「意識啓発と社会参画支援」（2020年改訂プラン抜粋）の説明に合うものを一つ選べ。',
[
'地域住民と外国人住民が相互に交流する場づくりは行わず、外国人住民だけが一方的に地域の習慣を学ぶことを求める。',
'多文化共生の意識啓発は外国人住民だけを対象とし、地域住民等への意識啓発は施策に含めない。',
'相互交流の場づくりや、外国人住民が主体的に地域で活動するためのネットワーク・自助組織の支援を進める。',
'外国人住民は支援を受ける側に固定し、災害時の支援の担い手となることや自治会等への参画は認めない。'],
[
'同資料の「多文化共生の場づくり」は、地域住民と外国人住民が相互に交流し、理解を深める場を推進するとしています。一方向の学習だけに限定する説明は、この方針に合いません。',
'「地域住民等に対する多文化共生の意識啓発」という項目が示されています。また、学校・図書館・公民館等を活用した相互交流も挙げられています。対象を外国人住民だけに限る説明とは異なります。',
'「多文化共生の場づくり」と「キーパーソン・ネットワーク・自助組織等の支援」に対応します。資料は、外国人住民が地域住民として主体的に活動できるよう支援する方針を示しています。',
'資料は、災害時の支援等の担い手となる外国人住民の育成と協力を挙げ、地域の実情に応じた自立支援体制の整備と自治会・商店街・PTA等への参画促進を示しています。被支援者への固定や参画の禁止とは逆です。'],
'S188総務省自身の説明資料を文化庁掲載原PDFで再取得。PDF43／印刷42頁の全本文・画像に全肢全解説を照合。旧稿の定義引用や同化の一般理論を本問の承認対象から外し、同じ多文化共生領域の取得済み施策本文に限定。資料の政策方針と施策効果の実証を区別。改訂プラン全条項や現行補助金要件の検証ではない。',
['誤：相互交流の場づくりを否定','誤：地域住民等への意識啓発を除外','正：相互交流と主体的活動への支援','誤：支援の担い手と社会参画を禁止']),
('Q_1_030',4,'S72',
'2010年（平成22年）11月30日告示「常用漢字表」の前書きと「表の見方及び使い方」の説明に合うものを一つ選べ。',
[
'都道府県名に用いる漢字も例外なく対象外とし、固有名詞は全て同じ扱いで除外している。',
'過去の著作や文書の漢字使用を否定し、現在の表に合わせて一律に改めることを求めている。',
'個々人の表記まで及ぶ規則であり、私的な日記や手紙も含めて表外の漢字使用を一律に禁止している。',
'一般の社会生活で現代の国語を書き表す場合の漢字使用の目安であり、本表には2136字を掲げている。'],
[
'前書き3は、都道府県名に用いる漢字及びそれに準じる漢字を除き、固有名詞を対象とするものではないとしています。都道府県名の漢字まで例外なく対象外とする説明は、この留保を落としています。',
'前書き4は、過去の著作や文書における漢字使用を否定するものではないとしています。過去の表記の一律改変を求める説明は合いません。',
'前書き2は、各種専門分野や個々人の表記にまで及ぼそうとするものではないとしています。ただし、一般の社会生活と密接に関連する専門分野の語には参考とすることが望ましいという留保があります。個人の表外字使用を全面禁止する規則ではありません。',
'前書き1の目安という性格と、「表の見方及び使い方」2の本表2136字に対応します。前書き5は、運用に当たって個々の事情に応じた適切な考慮の余地も示しています。'],
'S72告示原PDFを再取得。第1頁の前書き1～5・表の見方1～6を本文と画像で照合。読み書きの容易さを字数増の原因とする旧説明、手書き不要の一般化、追加196字／削除5字、別告示の現代仮名遣いの補助説明を本問から撤回。2010年告示本文の性格・範囲・2136字に限定。改定原因や教育漢字制度の承認ではない。',
['誤：都道府県名等の留保を削除','誤：過去の表記を否定','誤：個々人の表記への全面規制','正：目安という性格と本表2136字'])]
extra=[]
for k,key,sid,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第176バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='発行主体と資料の対象範囲を明示。全4肢を独立照合。',explanation_review='全4解説を取得本文に対応。未取得の制度・理論・因果説明を撤回し、本文の留保を反映。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定本文に一致',no_correct_risk=f'なし：{key}の根拠本文取得済み')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch177.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [
 ('S72','kanji177.pdf','https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf','原164頁PDF。第1頁の前書き1～5、表の見方1～6を本文・画像で照合、第2頁の説明も参照。全164頁精読ではない。'),
 ('S188','plan177.pdf','https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/taikai/r02/pdf/92746701_03.pdf','原60頁PDF。表紙、PDF6／印刷5頁の改訂概要、PDF43／印刷42頁の意識啓発と社会参画支援全本文を精読、PDF43頁画像照合。略と示された原プランの省略箇所や全60頁の精読ではない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch177_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
