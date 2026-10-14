"""Apply original-source distinctions for adjacency pairs and turn allocation."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1360
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
items={
'Q_4_108':(1,
'SchegloffとSacks「Opening Up Closings」が述べる隣接ペアの基本形式について、最も適当な説明を一つ選べ。',
['異なる話し手が産出する第1部分と第2部分が、「質問―回答」「挨拶―挨拶」などの行為の組合せとして、順序と関連性をもつ。','第1部分と第2部分は、必ず同じ話し手が続けて産出する。','第2部分を先に産出し、そのあとに対応する第1部分を産出することが基本形式である。','二つの発話が近接していれば、行為の組合せとして関連していなくても隣接ペアになる。'],
['原論文の再録版74頁は、異なる話し手による二つの部分、部分の相対的順序、行為の組合せを説明しています。ここでは、その基本形式を問うています。','基本形式では二つの部分を異なる話し手が産出します。同じ話し手が続けて産出することを要件とする説明は逆です。','第1部分が第2部分に先行することが基本形式です。順序を逆にした肢の説明とは一致しません。','単に二発話が近接するだけでなく、質問と回答など、部分同士の行為上の関連性があります。近接だけで定義することはできません。'],
['正：基本形式の異なる話者・順序・行為上の関連性に一致','誤：異なる話者という条件と逆','誤：第1部分と第2部分の相対的順序が逆','誤：単なる隣接性と行為上の関連性を混同'],['S134'],
'隣接ペアの基本形式を原著再録本文で限定し、未照合の修復・文法難度に関する補助説明を除く。'),
'Q_4_111':(4,
'Sacks・Schegloff・Jefferson（1974）が提案した発話交代規則に照らし、最初の移行適切場で現在の話し手が次話者を選んでいない場合の説明として、最も適当なものを選べ。',
['他の参加者による自己選択は認められず、誰も自発的に話し始めてはならない。','現在の話し手は、他の参加者が話し始めていても、必ずその参加者を遮って話し続けなければならない。','会話開始時にすべての発話順が固定され、その場での自己選択や継続は認められない。','他の参加者が自己選択して話し始めてよい。誰も自己選択しなければ、現在の話し手は話し続けてよい。'],
['原論文700頁の規則1(b)は、現在の話し手が次話者を選んでいない場合、自己選択によって次の話し手が決まることを認めています。','原論文の規則1(b)は、自己選択して先に話し始めた人に次のターンの権利があるとしています。現在の話し手に遮りを義務づける規則ではありません。','原論文の規則は、移行適切場で次話者選択・自己選択・現在話者の継続を扱います。会話全体の発話順を開始前に固定する規則ではありません。','原論文の規則1(b)は他の参加者の自己選択を認め、1(c)は誰も自己選択しない場合に現在話者が継続できるとしています。継続は義務ではありません。'],
['誤：規則1(b)の自己選択を否定','誤：自己選択者の権利と任意の継続を混同','誤：局所的な選択規則を事前固定と取り違え','正：規則1(b)・1(c)に一致'],['S133'],
'原著の適用条件を指定し、韻律・視線・終助詞を一律の交代合図とする未照合の一般化を除く。')}
for key,(ans,stem,opts,exps,verdicts,sources,reason) in items.items():
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第68バッチ反映後の累積作業稿')
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==ans else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='指定した原著の基本形式・規則の条件に全4肢を独立照合。',explanation_review='原著の該当頁画像を開き、全4解説の定義・条件・順序を照合。日本語授業の効果へ一般化しない。',unresolved='',multiple_correct_risk='なし：指定された形式・条件と一致する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch69.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
