"""One-time source-grounded audit of preference and a short conversation sample."""
import json, html
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text())
# Only allow repair of this uncommitted batch after a failed staged rebuild.
if len(c) in (1405,1413):
 previous=json.loads((b.OUT/'changes_batch70.json').read_text())
 assert len(previous) in (27,35) and c[-len(previous):]==previous
 c=c[:-len(previous)]
assert len(c)==1378
d=json.loads((b.OUT/'decisions.json').read_text()); _,q,a=qa.audit(str(b.DST)); extra=[]
paragraphs=[p.text for p in Document(b.DST).paragraphs]
items={
'Q_4_109':(2,
'Pomerantz（1984）による評価発話への応答の分析に照らし、会話分析の選好について最も適当な説明を一つ選べ。',
['選好とは、教師が特定の学習者だけを指名する授業中の行動を指す。',
'先行する行為に対して選好される応答と、その代替となる応答を区別する。どちらが選好されるかは、先行する行為によって異なる。',
'選好とは、話し手が個人的に好きな人物を会話相手として選ぶことだけを指す。',
'どのような先行する評価発話に対しても、同意だけが選好され、不同意は常に非選好となる。'],
['原著63〜64頁は、先行する行為とそれに続く応答の関係を分析しています。教師の指名相手の偏りを定義した用語ではありません。',
'原著は、先行する評価が一方の次行為を促す構造と応答の組み立てを扱います。例えば自己卑下に続く同意は非選好となり、同意がいつでも選好されるわけではありません。',
'原著の選好は、先行する行為に対する次の行為とその発話形式の関係です。好きな会話相手を選ぶという個人的好みだけでは説明できません。',
'原著64頁は、自己卑下への同意を非選好とする場合を挙げています。したがって、すべての評価発話について同意と選好を同一視する説明は誤りです。'],
['誤：指名の偏りを定義するものではない','正：原著63〜64頁の行為依存の区別と一致','誤：個人的な相手の好みだけに還元している','誤：原著の自己卑下の反例に反する'],['S135'],
'選好を心理的好みと区別し、同意が常に選好となるという一般化を原著の反例で排除。未照合の招待一般の説明を評価発話の原著分析へ限定。'),
'Q_4_110':(1,
'東京外国語大学言語モジュール「誘いの受け方、断り方」の表現例を参考に、友人からの映画への誘いを、理由と謝意を添えて断る練習を行う。Eさん「今週末、一緒に映画に行きませんか」に対するDさんの応答として、最も目的に合うものを一つ選べ。',
['「誘ってくれてありがとう。でも、今週末は予定があるんです。すみません」と断る。',
'「いいですね。ぜひ一緒に行きましょう」と誘いを受ける。',
'「いいえ、行きません」とだけ答え、理由と謝意は述べない。',
'「はい、行きません」とだけ答え、理由と謝意は述べない。'],
['この応答は誘いへの謝意、参加できない理由、謝罪を含み、設問で指定した練習目的に合います。大学教材にも「ありがとうございます。でも、あしたはちょっと」や、謝罪に理由を続ける断りの例があります。',
'大学教材では「いいですね。行きましょう」を誘いを受ける例として示しています。断るという今回の練習目的には合いません。',
'この肢には設問が求める理由と謝意がありません。明示的な断りがどの場面でも必ず失礼になると断定しているわけではありません。',
'この肢にも設問が求める理由と謝意がありません。大学教材の練習でも、映画への誘いに対する「はい、行きません」はふさわしい返事として扱われていません。'],
['正：断り・理由・謝意がすべて明示される','誤：断りではなく受諾','誤：明示した練習条件の理由と謝意がない','誤：理由と謝意がなく教材の勧誘応答にも不適合'],['S136'],
'拒絶が常に顔を潰すという根拠不足の評価を除き、理由と謝意を添えて断るという明示した練習目的に改訂。'),
'Q_5_101':(2,
'以下は作成した会話例の抜粋である。Aさん「昨日、新しいパソコンを買いました。」Bさん「そうなんですか。どんなパソコンですか？」Aさん「（沈黙）……ノートパソコンです。」Bさん「へえ、使いやすいですか？」この抜粋から読み取れる内容として、最も適当なものを一つ選べ。',
['Aさんは、種類を尋ねる質問にも使いやすさを尋ねる質問にも、すでに答えている。',
'Aさんはパソコンの種類を尋ねる質問に答え、Bさんは使いやすさを尋ねる質問へ進んでいる。この抜粋だけでAさんの会話への協力姿勢が不足しているとは断定できない。',
'Bさんが質問を続けていることから、Aさんの返答をまったく理解できず、会話が破綻したと確定できる。',
'沈黙の後の返答が短いので、会話参加者はすべての質問に必ず長い返答をしなければならないという会話の規則に違反している。'],
['種類への返答はありますが、使いやすさへの返答は抜粋に示されていません。記録されていない応答を補って判断してはいけません。',
'種類への質問に対応する返答の後、別の質問が続いています。Sacksら（1974）はターンの長さや順序の可変性を扱っており、全質問への長い返答を必須とはしていません。短い抜粋を根拠に協力姿勢全体を断定する判断は避けます。',
'Bさんは使いやすさという次の内容を尋ねています。質問が続くという事実だけから、全く理解できていないことや破綻を確定することはできません。',
'原論文699頁はターンの長さや順序が変わることを述べています。すべての質問に長く答えることを義務づける規則ではありません。沈黙の原因も、この抜粋には記録されていません。'],
['誤：使いやすさへの返答を捏造','正：記録にある返答と次の質問を識別し態度を断定しない','誤：継続質問から理解不能・破綻は導けない','誤：ターンの可変性に反し全質問への長答を義務化'],['S133'],
'一つの短い返答から共同作成姿勢不足を認定した正答不存在疑いを解消。未提示の使い心地回答を解説が補う誤りも修正。実在商品名を一般的な種類へ置換。')}
for key,(ans,stem,opts,exps,verdicts,sources,reason) in items.items():
 assert int(a['A_'+key[2:]]['ans'])==ans
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new: continue
   old=html.unescape(old); removed=[]
   if field=='stem' and old not in paragraphs:
    starts=[j for j,t in enumerate(paragraphs) if t and old.startswith(t)]
    assert len(starts)==1
    j=starts[0]; parts=[]
    while not paragraphs[j].startswith('1. '): parts.append(paragraphs[j]); j+=1
    assert ' '.join(parts)==old
    old=parts[0]; removed=parts[1:]
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第69バッチ反映後の累積作業稿')
   if field=='options': e['stem_context']=stem
   if field=='explanations': e['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==ans else '誤')+'）'
   extra.append(e)
   for t in removed:
    extra.append(dict(id=key,field='stem',index=None,before=t,after='',remove_paragraph=True,previous_paragraph=stem,reason='複数段落の旧設問を統合改訂したため、残存する旧段落を明示的に除去。'+reason,sources=sources,applied=True,before_version='第69バッチ反映後の累積作業稿'))
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='原著または大学教材の取得本文と明示した設問条件に全4肢を独立照合。',explanation_review='全4解説の補助主張まで照合。原著63〜65頁と699〜700頁は画像精読、大学教材は解説・練習問題全文取得。教育効果・礼儀違反・学習者の人格への普遍化を除く。',unresolved='',multiple_correct_risk='なし：明示した条件に適合する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch70.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
