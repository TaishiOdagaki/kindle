"""One-time original negotiation-text review of two pending questions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2057
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_5_103':(2,'Fisher・Ury・Patton『Getting to Yes』第2版の原則立脚型交渉について、同書の説明に対応するものを一つ選びなさい。異文化間の交渉を含め、成功率の普遍的な順位を問うものではない。',[
'人と問題を分けるとは、相手の感情や認識を一切扱わず、相手への人格批判に集中することである。',
'表明された要求・立場だけに固執せず、その背景にある双方のニーズや懸念を確かめ、複数の解決案を考える。',
'客観的基準を使うとは、自分の希望だけを唯一の基準として相手に受け入れさせることである。',
'同書の方法を使えば、双方の利害や力関係にかかわらず、必ず合意できる。'],[
'同書は人への配慮と問題の検討を分けます。感情・認識を無視した人格批判ではありません。',
'同書は要求の背景にある利害を検討し、双方の利益を考えた選択肢を作る方針を示します。どの場面でも最も効果的という実証的順位ではありません。',
'一方の意思だけに依存しない基準を検討する方針です。自分の希望を客観的基準と呼び替えることではありません。',
'同書は力関係などの現実的制約を認め、いかなる方法も成功を保証しないと述べています。'],[
'誤：人への配慮を人格批判に置換','正：立場の背景の利害と複数案を検討','誤：一方の意思と独立した基準を混同','誤：方法の説明を合意の必然保証に拡張']),
'Q_5_104':(4,'次は地域の日本語教室での架空の会話である。A「明日の準備、私は9時に行きます」。B「9時はちょっと早いかもしれませんね」。A「では9時に行きましょう」。この時点では合意を確認していない。後にBは「会場が開くのは10時だと伝えたかった」と説明した。『Getting to Yes』の、相手の意味・認識・制約を確認する方針に照らし、最も適切な対応を一つ選びなさい。',[
'Bの返答を明確な合意と決め、双方への確認をせず9時開始を確定する。',
'Aだけに察する責任があるとし、Bには意図や会場の条件を説明する必要はないと伝える。',
'敬語の形だけを直せば問題は解決するとし、会場が開く時刻や互いの希望は話し合わない。',
'AはBに意味を確かめ、Bも会場の条件を明示し、双方の都合を聞いて開始時刻を改めて相談する。'],[
'事例には合意の確認がありません。相手の意図を自分の解釈だけで決める対応は、指定の方針に合いません。',
'同書は聞き手の確認と話し手の分かるように伝える行動の双方を扱います。一方だけの責任にしません。',
'この事例では時刻の認識と会場の制約が未共有です。敬語の形だけの修正ではその情報を確かめられません。',
'意図と制約を共有し直して相談する対応です。日本語の間接表現や視線が常に同じ意味を持つという一般化ではありません。'],[
'誤：未確認の合意を確定','誤：話し手による明示と双方の確認を排除','誤：共有すべき条件を文法形式だけに還元','正：双方が意味と制約を確認して相談'])}
extra=[];removed=0
reason='S151原著第2版の公開再組版PDF11〜14、20〜24、31、42〜43、50頁を本文照合。利害への着目と複数案、相手の意味・制約の確認、成功の非保証を確認。文化類型の未照合断定と最も効果的という普遍順位を撤回し、会話は教材用の架空事例として双方の確認を扱う。'
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S151'],applied=True,before_version='第91バッチ反映後の累積作業稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問の継続段落を明示削除。'+reason));removed+=1
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S151'],reason=reason,option_verdicts=verdicts,stem_review='原著で明示された交渉上の方針と事例内の事実に基づき全4肢を独立判定。指定方法の効果を民族別に実証したとは扱わない。',explanation_review='全4解説をS151本文に照合。単一文化類型、視線や間接表現の一義的解釈、学習者のみへの責任帰属、合意の普遍保証を撤回。',unresolved='',multiple_correct_risk='なし：指定方針・事例に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==18+removed
for name,obj in [('changes.json',c+extra),('changes_batch92.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(f'2 full reviews;{len(extra)}edits;{removed}old-stem removals')
