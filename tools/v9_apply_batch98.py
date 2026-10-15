"""One-time recovered full review of Q_M_046. Do not replay."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2175
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
k='Q_M_046';ans=3;ss=['S76']
stem='東京外国語大学言語モジュール「無声化母音の産出」の説明に照らし、母音の無声化について対応する記述を一つ選べ。'
opts=['文末にしか起こらず、語中で無声子音に挟まれた母音には起こらない。','無声化の起こる環境でも、母音にアクセント核がある方が、ない場合より無声化しやすい。','「い」「う」の声帯振動がなくなる現象で、無声子音に挟まれた場合や文末などに起こることがある。','母音の声帯振動が増す現象であり、母音をより強く有声で発音することを指す。']
exps=['同教材は、文末だけでなく、語中で無声子音に挟まれた「すき」などにも無声化が起こることを説明しています。','同教材は、無声化が起こる環境でも、母音がアクセント核を持つと起こりにくくなると説明しています。この肢はその傾向を逆にしています。','同教材の定義と条件に対応します。「すき」のような語中の環境と、文末の「です」「ます」の「す」を区別して挙げています。必ず起こるとはしていません。','同教材は、声帯振動がなくなることによって母音が聞こえにくくなると説明しています。声帯振動を増すという説明は逆です。']
reason='東京外国語大学「無声化母音の産出」のHTML全文を再取得し本文51〜54行を照合。語中の無声子音間と文末の条件を区別し、単に聞こえにくいという定義を声帯振動の消失へ精密化。アクセント核がある場合の起こりにくさも教材の範囲で明示。未保存の第97バッチは件数に含めない。'
assert d[k]['status']=='修正必要' and int(a['A_'+k[2:]]['ans'])==ans
parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
extra=[]
for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=ss,applied=True,before_version='第96バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
  extra.append(e)
  if field=='stem':
   for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=3,fixes_applied=True,sources=ss,reason=reason,option_verdicts=['誤：教材にある語中の条件を排除','誤：アクセント核があると起こりにくい傾向を逆転','正：声帯振動の消失と条件付きの説明に一致','誤：声帯振動の増加は定義と逆'],stem_review='指定教材の説明との対応を独立比較。文末と無声子音間を混同しない。唯一対応するのは3。',explanation_review='全4解説を教材本文の定義・すき等の語中例・ですますの文末例・アクセント核条件と照合。旧肢の連濁・音便・拗音化の未照合定義を承認する形にしない。',unresolved='',multiple_correct_risk='なし：指定教材と対応する肢は3のみ',no_correct_risk='なし：独立正答3。全方言・全話者の必発性は主張しない。')
for name,obj in [('changes.json',c+extra),('changes_batch98.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('1 full review /9 edits')
