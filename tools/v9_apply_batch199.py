"""One-time two same-domain replacements using acquired primary full bodies."""
import json,html
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==4296
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_2_002',2,['S300'],'真田信治による国立国語研究所「ことば研究館」の2018年の記事「日本語とかかわるクレオールは存在しますか」で、宜蘭クレオールについて述べられていることを一つ選べ。同記事の調査報告を対象とする。',
['日本統治時代に日本語を学んだ高年層の「台湾日本語」と区別せず、日本語の変種の一つとだけ位置付けている。','アタヤル語と日本語の接触から生まれ再編された言語とし、その担い手が年配者から子供・孫世代に及ぶと述べている。','担い手は日本統治時代に日本語を学んだ高年層に限られ、子供・孫世代には及ばないと述べている。','日本語を語彙供給言語とするクレオールは存在しないとして、宜蘭の調査結果もその否定の根拠にしている。'],
['記事は、日本語の変種である「台湾日本語」と、接触・再編から生まれた宜蘭クレオールを区別しています。両者を同じ位置付けにする説明は合いません。','記事はアタヤル語と日本語の接触・再編、および子供・孫世代に及ぶ担い手を報告しています。当該事例の説明であり、すべてのクレオールの成立史を一律に定めるものではありません。','記事は年配者だけでなく子供・孫世代も担い手であると述べています。高年層に限定する説明は逆です。2018年の記事の記述であり、現在の話者数を示すものではありません。','記事は日本語を上層、すなわち語彙供給言語とするクレオールが宜蘭で確認されたと報告しています。存在を否定する説明ではありません。'],
['誤：記事が区別する台湾日本語と同一視','正：接触・再編と世代にまたがる担い手に対応','誤：子供・孫世代を除外','誤：日本語を上層とする事例の存在を否定'],
'Foley1988の導入要約だけによる旧承認は撤回したまま、同じ接触言語・クレオール領域の宜蘭事例へ差替え。S300は調査研究者本人の署名付き解説記事の全本文を取得精読した一次的報告であり、未取得論文の抄録ではない。2018年記事に対象を限定し、台湾日本語との区別、接触・再編、担い手の世代、語彙供給言語を全肢全解説で照合。全クレオールの普遍的成立過程・現在の危機状況や話者数・未取得参考文献を根拠にしない。'),
('Q_4_076',1,['S149'],'Celce-Murcia・Dörnyei・Thurrell（1995）のTable 5における「回避・縮小方略（avoidance or reduction strategies）」に分類されるものを一つ選べ。同論文の方略分類を問う。',
['ある話題を避けたり、伝えようとしたメッセージを断念したりする。','分からない語を、意味を説明する迂言で補って伝える。','考える時間を得るために、つなぎ語を使ったり発話を繰り返したりする。','自分の発話の誤りに気付き、自分から言い直して修正する。'],
['原著27頁の説明と28頁のTable 5は、話題の回避とメッセージの断念を回避・縮小方略に挙げています。ここでは分類を問い、誤用数だけから個人の回避や習得を断定していません。','Table 5は迂言を達成・補償方略に分類しています。語の意味を説明して伝えようとする例であり、同表の回避・縮小方略ではありません。','原著27頁とTable 5は、つなぎ語や繰り返しを時間稼ぎの方略に挙げています。同表では回避・縮小方略と別の区分です。','原著27頁とTable 5は、自発的な修復を自己モニタリング方略に挙げています。同表では回避・縮小方略と別の区分です。'],
['正：原著27頁とTable 5の話題回避・メッセージ断念','誤：Table 5の達成・補償方略','誤：Table 5の時間稼ぎ方略','誤：Table 5の自己モニタリング方略'],
'Schachter1974の著者要旨だけによる旧承認は撤回したまま、同じ第二言語使用の回避領域で原著全文取得済みの方略分類へ差替え。S149原著全16PDF頁を再取得、原著26～29頁の本文と表5原画像を精読。回避・縮小、達成・補償、時間稼ぎ、自己モニタリングを全肢全解説に照合。旧題の誤用分析研究のデータ検証を完了したとはしない。単独の誤用数から意図・習得を断定せず、このモデル以外の全方略分類への一般化や指導効果の保証もしない。')]
extra=[]
for k,key,sources,stem,opts,exps,verdicts,reason in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第198バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='取得した全本文に合わせ資料・対象・モデルを明示し全肢と単一正答性を照合。',explanation_review='全4解説を取得本文に照合。元の未取得原著のデータ検証とは区別し一般化を避けた。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定資料に整合',no_correct_risk=f'なし：{key}の本文根拠を取得')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch199.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
