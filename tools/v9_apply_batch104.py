"""One-time article 35 compensation / quotation statutory-text audit."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2330
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_4_124':(4,'著作権法第35条第1～3項による授業での利用と補償金の関係について、条文に対応する説明を一つ選べ。',[
'補償金さえ支払えば、第1項の必要限度やただし書の条件を満たさなくても、同項による公衆送信が認められる。',
'第1項の対象となる公衆送信は、リアルタイムで行いさえすればすべて第3項に当たり、補償金が不要になる。',
'第1項はリアルタイムの授業にしか適用されず、授業過程で必要な資料のオンデマンド送信は、同項の他の条件を満たしても一切対象にならない。',
'第1項による公衆送信では設置者の補償金支払が原則必要で、第3項の条件に当たる同時授業送信にはその例外がある。'],[
'第1項の必要と認められる限度や、権利者の利益を不当に害する場合を除くただし書は、補償金の支払によって無効になりません。支払だけで第1項の対象外の利用まで認める肢は誤りです。',
'第3項は、直接授業を受ける者への原作品・複製物の提供・提示による利用等と、別の場所で同じ授業を同時に受ける者への送信を条件とします。リアルタイムであることだけで、すべて同項に該当するわけではありません。',
'第1項は、自動公衆送信では送信可能化も含む公衆送信を対象とし、リアルタイムだけに限定していません。オンデマンドでも同項の全条件を個別に確認し、第2項の補償金との関係も検討します。',
'第2項は第1項による公衆送信について教育機関を設置する者の補償金支払を定め、第3項は特定の同時授業送信には第2項を適用しないとしています。特定年度の特例や漠然とした無償対象と混同しません。'],[
'誤：補償金支払だけで第1項の条件はなくならない',
'誤：第3項はリアルタイムであること以外の条件もある',
'誤：第1項の公衆送信はリアルタイムに限定されない',
'正：第2項の原則と第3項の限定的な不適用を区別']),
'Q_4_125':(2,'著作権法第32条第1項による引用と、第48条の出所表示について、条文に対応する説明を一つ選べ。',[
'第32条第1項は、未公表の著作物でも、引用者に研究目的があるだけで同項による引用を認めている。',
'第32条第1項は公表された著作物を対象とし、公正な慣行と引用目的上正当な範囲を求める。引用して複製する場合は第48条の出所表示も必要となる。',
'第32条第1項では、公正な慣行に合致すれば、引用目的上正当な範囲かどうかを検討する必要はない。',
'第48条に従って出所を示せば、第32条第1項の公正な慣行や目的上正当な範囲の条件は満たさなくてよい。'],[
'第32条第1項の対象は公表された著作物です。研究という目的名だけで、未公表作品が同項による引用の対象となるわけではありません。別の許諾等による利用まで否定する説明ではありません。',
'第32条第1項は、公表された著作物の引用が公正な慣行に合致し、かつ引用目的上正当な範囲内であることを求めます。引用して複製する場合には、第48条第1項第1号により、合理的な方法・程度で出所を示します。著作者名の表示は同条第2項とその例外も確認します。',
'第32条第1項は、公正な慣行への合致と、報道・批評・研究その他の引用目的上正当な範囲を、ともに条件としています。一方の条件を満たすだけで他方を省略できるという肢は誤りです。',
'出所表示をしても、第32条第1項の公正な慣行や引用目的上正当な範囲の条件がなくなるわけではありません。URL等を記載しただけで、転載の量や利用の事情を問わず引用として認められるとはいえません。'],[
'誤：第32条第1項の公表済みという対象条件を落とす',
'正：第32条第1項の条件と第48条第1項第1号の出所表示を区別',
'誤：公正慣行と目的上正当な範囲は選択的な条件ではない',
'誤：第48条の出所表示は第32条の条件を代替しない'])}
extra=[]
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 reason=('保存済みe-Gov本則第35条全3項を照合。補償金支払を第1項の全条件の代替とせず、第3項の限定的な同時授業送信の免除と、リアルタイム一般・年度特例・曖昧な無償対象を区別。' if k=='Q_4_124' else '保存済みe-Gov本則第32条・第48条全項を照合。公表済み・公正慣行・目的上正当な範囲という条文条件と出所表示を区別。未取得の裁判例の独立要件を条文そのものとして断定する旧解説は、条文対応問題へ改訂して撤回した。')
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S26'],applied=True,before_version='第103バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S26'],reason=reason,option_verdicts=verdicts,stem_review='条文に対応する説明を問う範囲を明記し、設問・全4肢を取得済み法令本文から独立判定。年度別制度運用や具体的事件の適法性を包括承認しない。',explanation_review='各問全4解説を第35条全3項又は第32条・第48条全項と照合。第35条の支払免除条件を落とさず、出所表示だけで引用が成立するとしない。未取得の判例・年度特例についての旧主張は承認せず削除。',unresolved='',multiple_correct_risk='なし：本文の条件と関係を両方満たす肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==18
for name,obj in [('changes.json',c+extra),('changes_batch104.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('2 full reviews/18 edits')
