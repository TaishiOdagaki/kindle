"""One-time TUFS grammar review. Do not replay over newer decisions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2148
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_M_053':(3,['S154','S155'],'東京外国語大学言語モジュール「助詞とは」「副助詞」の分類に従う。「この本だけ読みました」「この本も読みました」の「だけ」「も」の分類名として、対応するものを一つ選べ。',[
'終助詞（「ですよ」「ですね」の「よ」「ね」など）',
'格助詞（「本を読みます」の「を」など）',
'取り立て助詞（同教材では副助詞、取り立て詞とも呼ぶ）',
'接続助詞（「春になると暖かくなります」の「と」など）'],[
'同教材の終助詞は、主に文末で伝達に伴う態度などを表すものです。設問の「だけ」「も」は、この教材では副助詞に分類されています。',
'同教材は「本を読みます」の「を」を格助詞に挙げています。「この本だけ」「この本も」の該当部分は副助詞として区別しています。',
'同教材は副助詞に「取り立て助詞」「取り立て詞」という名称を併記し、「だけ」の限定、「も」の並立・付加を説明しています。ここでは指定教材の分類を使います。',
'同教材の接続助詞は、従属節と主節の意味関係を示すものです。「春になると」の「と」と、設問の「だけ」「も」を区別しています。'],[
'誤：教材では終助詞の例と区別','誤：「を」の格助詞と区別','正：指定教材の副助詞・取り立て助詞に対応','誤：条件節の「と」と区別']),
'Q_M_054':(4,['S156'],'「昨日買った本」の「昨日買った」という連体修飾節の働きについて、最も適切な説明を一つ選べ。',[
'修飾される名詞「本」の後ろに置かれ、「本昨日買った」という語順になる。',
'動詞を含むまとまりは名詞を修飾できないので、この表現は成立しない。',
'「昨日買った」は動作主だけを表すまとまりで、述語を含んでいない。',
'「昨日買った」というまとまりが、後ろの名詞「本」を修飾している。'],[
'大学教材「V＋N」は、動詞で終わるまとまりを名詞の前に置く構造を示しています。本問も「昨日買った」が「本」に先行します。',
'同教材は、動詞で終わる文を使って名詞を修飾する構造を説明しています。「買った」を含むことは、この構造を否定する理由になりません。',
'このまとまりには述語「買った」が含まれています。節かどうかを語数だけで判断するのでなく、この例では述語を含むまとまりが名詞を修飾する関係を確認します。',
'同教材の「V＋N」の構造に対応します。名詞「本」の前に置いた「昨日買った」が、どの本かを説明する修飾部分として働きます。'],[
'誤：本問の修飾語と名詞の語順が逆','誤：動詞を含む修飾節を否定','誤：述語「買った」の存在を否定','正：節が後続名詞「本」を修飾']),
'Q_M_056':(3,['S157'],'予定表では彼は12時に来ることになっており、予定に変更はないという前提で「彼は12時に来るはずだ」と述べた。この「はずだ」の説明として、最も適切なものを一つ選べ。',[
'彼が既に来たことを直接確認したという、過去の事実だけを報告している。',
'予定表などの根拠とは無関係に、直感だけで確信を述べている。',
'予定表の情報を根拠として、理屈上は12時に来るという推論を述べている。',
'予定表がある以上、推論と実際の結果が食い違う可能性はないと保証している。'],[
'本問では、実際に到着を見てから報告しているのではなく、予定表を根拠に判断しています。「はずだ」のこの用法は推論を表します。',
'大学教材は「はずです」を、理屈上導かれる推論として説明し、直感的な確信も表せる「にちがいありません」と区別しています。本問は予定表という根拠を明示しています。',
'大学教材の「はずです」の推論の説明に対応します。本問では、予定表の情報と変更がないという前提から、到着時刻を判断しています。',
'同教材は、「はずです」が推論と現実の食い違う場合にも使えると説明しています。本問の予定表は推論の根拠であって、結果の保証ではありません。'],[
'誤：推論を直接観察済みの事実報告に置換','誤：予定表という根拠を無視','正：明示した根拠からの推論','誤：推論と現実の食い違いを排除'])}
reason='東京外国語大学の公刊教育用HTML本文を取得。助詞とは・副助詞・V＋N・はずですの各説明を照合。助詞の指定分類を明示、連体修飾節の語数による誤定義を撤回、はずだは根拠付き推論と直感的確信・結果保証を区別した。'
extra=[]
for k,(ans,ss,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status'] in {'修正必要','要追加確認'} and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=ss,applied=True,before_version='第95バッチ反映後の累積稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=ss,reason=reason,option_verdicts=verdicts,stem_review='指定した大学教材の分類・構造・用法に照らし全4肢を独立比較。助詞分類の全学説を同一とせず、はずだの予定表例は監査で構成した適用例とする。',explanation_review='4解説を大学教材の本文と照合。助詞とはの4分類と副助詞のも・だけ、V＋Nの前置修飾構造とはずですの根拠に基づく推論・現実との食い違いを確認。連体節の語数・全用法に普遍条件を付けない。',unresolved='',multiple_correct_risk='なし：指定分類・明示した表現の働きに合う肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27
for name,obj in [('changes.json',c+extra),('changes_batch96.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('3 full reviews /27 edits')
