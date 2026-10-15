"""One-time fresh source review of M47/M48; never replay over newer decisions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2184
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_M_047':(4,['S158'],'東京外国語大学言語モジュール「鼻濁音の聞き取り」の説明に照らし、語中のガ行音子音について対応する記述を一つ選べ。',[
'語中のガ行音子音は鼻濁音の[ŋ]に限られ、[g]で発音することはない。',
'語中で[g]を使うか鼻濁音の[ŋ]を使うかによって、単語の意味が変わると説明している。',
'語中のガ行音子音が、鼻から息が抜ける[ŋ]で発音されることはない。',
'語中では[g]で発音する場合と、鼻から息が抜ける[ŋ]で発音する場合があり、この違いで意味は変わらない。'],[
'同教材は、語中では[g]で発音する場合と、鼻濁音の[ŋ]で発音する場合があると説明しています。[ŋ]だけに限る説明とは異なります。',
'同教材は、語中で[g]と[ŋ]のどちらを使っても意味は変わらないと説明しています。この肢は意味への影響を逆にしています。',
'同教材は、鼻から息が抜ける[ŋ]を鼻濁音と説明し、語中の[ŋ]を聞き取る練習を扱っています。その存在を否定する説明とは異なります。',
'同教材の語中の発音と意味についての説明に対応します。ここでは指定教材の対比を問うのであって、全方言・全話者・全場面の使用率を一律に決めるものではありません。'],[
'誤：本文にある語中の[g]を排除','誤：意味は変わらないという本文の説明を逆転','誤：本文が練習対象とする[ŋ]の存在を否定','正：語中の二つの実現と意味不変の説明に対応']),
'Q_M_048':(2,['S36'],'東京外国語大学言語モジュール「アクセント基礎」が挙げる共通語の例「はし（箸）」「あなた」について、アクセント核の位置の組合せとして対応するものを一つ選べ。',[
'「はし（箸）」は第2拍「し」、「あなた」は第3拍「た」にある。',
'「はし（箸）」は第1拍「は」、「あなた」は第2拍「な」にある。',
'「はし（箸）」も「あなた」も、第1拍にある。',
'「はし（箸）」にも「あなた」にも、アクセント核はない。'],[
'同教材は、「箸」では「は」の直後、「あなた」では「な」の直後に高さが急に下がると説明します。核を下降後の「し」「た」に置く組合せは、この説明に対応しません。',
'同教材の具体例に対応します。下降そのものと、その直前の核を持つ拍を区別すると、「箸」は第1拍「は」、「あなた」は第2拍「な」です。本問は指定教材の共通語の例を対象にしています。',
'同教材では「箸」の核は第1拍ですが、「あなた」の核は第2拍「な」です。語による核の位置の違いを、両語とも第1拍とすることはできません。',
'同教材は、両語に核のある例を挙げています。「箸」は「は」、「あなた」は「な」にあると説明しており、核がないという組合せとは異なります。'],[
'誤：下降後の拍を核と取り違える','正：本文の核の位置「は」「な」に対応','誤：「あなた」の第2拍核と不一致','誤：本文が明示する両語の核を否定'])}
extra=[]
for k,(ans,ss,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status'] in {'修正必要','要追加確認'} and int(a['A_'+k[2:]]['ans'])==ans
 reason=('東京外国語大学の公開HTML全文を再取得・精読。語中の[g]/[ŋ]と意味不変を指定教材の範囲で照合し、全方言・個人・場面に関する未照合の分布説明を撤回。教材の「最近」を2026年の統計として使用しない。' if k=='Q_M_047' else '東京外国語大学「アクセント基礎」公開HTML全文を再取得・精読。下降そのものと下降直前の核のある拍を区別し、本文の共通語例「箸」第1拍・「あなた」第2拍に限定して全肢を照合。全方言へ一般化しない。')
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=ss,applied=True,before_version='第98バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=ss,reason=reason,option_verdicts=verdicts,stem_review='大学教材の本文と具体例に照らして全4肢を独立比較。旧正解番号を前提にせず唯一対応する肢を確認。',explanation_review='全4解説を指定教材本文と照合。語中の鼻濁音の対比と意味不変、または共通語の核の具体例という範囲を守る。音声の実測や全地域・全年齢の分布を確認したとはしない。',unresolved='',multiple_correct_risk='なし：指定教材の説明に合う組合せ・記述は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==18
for name,obj in [('changes.json',c+extra),('changes_batch99.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('2 full reviews /18 edits')
