"""One-time follow-up of the same acquired statutory body, not a replay."""
import json,html,gzip,xml.etree.ElementTree as E,re
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2285
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
root=E.fromstring(gzip.decompress((b.OUT/'evidence/egov_batch101.xml.gz').read_bytes()));assert root.findtext('.//Result/Code')=='0'
articles={e.get('Num'):e for e in root.findall('.//MainProvision//Article')}
(b.OUT/'evidence/egov_batch102_excerpts.txt').write_text('第101バッチ取得・保存済みe-Gov原応答からの追加照合。本則のみ。\n\n'+'\n\n'.join(re.sub(r'\s+',' ',''.join(articles[n].itertext())).strip() for n in ['20','27','35','47_6','50'])+'\n')
items={
'Q_O_046':(4,'このケースで確認した第35条第1項の利用に対応するものを一つ選べ。',[
'授業とは関係なく、個人が自分の趣味だけのために行う複製。',
'営利を目的として設置された語学スクールであることだけを理由に、同項の対象とする利用。',
'公表されていない著作物を、公表済みかどうかは関係ないとして同項で複製する利用。',
'非営利設置の教育機関で教員が授業過程に必要な限度で公表作品を複製し、権利者の利益を不当に害しない利用。'],[
'第1項は、教育を担任する者や授業を受ける者が、その授業の過程で使うことを目的とする利用を対象にしています。授業とは無関係な個人の趣味を、そのまま同項の対象とする肢は対応しません。',
'第1項は、営利を目的として設置されている教育機関を対象から除いています。語学を教えるという活動だけで、設置目的の条件がなくなるわけではありません。',
'第1項が複製等の対象とするのは、公表された著作物です。未公表でも関係ないとする肢は、この条件を落としています。',
'第1項の機関・利用主体・授業過程・必要限度・公表済みという条件と、ただし書の不当に利益を害しない条件に対応します。紙の複製に関する本問とは別に、公衆送信には第2・3項も確認します。'],[
'誤：授業過程での利用目的を満たさない','誤：営利設置の除外を無視','誤：公表済みという条件を無視','正：第1項本文とただし書の条件を満たす']),
'Q_O_047':(3,'新聞コラムの複製について、第35条第1項ただし書の範囲を確認する。他の許諾や権利制限による利用ではなく、同項に基づく利用について適切な説明を一つ選べ。',[
'必要な限度内であれば、著作権者の利益を不当に害する場合でも同項を適用できる。',
'配付先を受講者に限れば、複製の部数や利用態様を考慮する必要はない。',
'著作物の種類・用途、複製部数や利用態様に照らし、権利者の利益を不当に害する場合には同項を適用できない。',
'教育目的でさえあれば、必要な限度や権利者の利益への影響に関する条件はなくなる。'],[
'第1項本文の必要な限度の条件と、ただし書の条件は別に確認します。必要な限度内という理由だけで、利益を不当に害する利用を認める肢は誤りです。',
'第1項ただし書は、複製の部数や利用態様も考慮するよう定めています。配付先を限定することだけで、それらを検討しなくてよいとはしていません。',
'第1項ただし書に対応します。本問は同項に基づく利用の範囲を問うもので、権利者の許諾を得た利用や、別の権利制限規定の適用まで一律に否定する説明ではありません。',
'第1項は授業過程での利用を対象にする一方、必要な限度とただし書の条件も設けています。教育目的だけで無条件になるという肢とは異なります。'],[
'誤：ただし書の条件を必要限度だけで排除','誤：部数と利用態様の検討を排除','正：ただし書の考慮事項と除外に対応','誤：教育目的だけで全条件を無効化']),
'Q_O_049':(2,'この教師は、元の創作的表現を引き継ぐ形で文章を要約・翻案して授業に使うことを検討した。第35条を根拠とする利用と第47条の6・第50条の関係について適切な説明を一つ選べ。',[
'第35条第1項の要件を満たさなくても、教育目的であれば、第47条の6で同条を根拠とする翻案が無条件に認められる。',
'第35条第1項により利用できる場合は、同条の例により翻案もできるが、著作者人格権との関係は別に確認する。',
'第47条の6に基づく翻案であれば、同一性保持権などの著作者人格権も一律に適用されなくなる。',
'第35条第1項により利用できる場合でも、第47条の6の同条に関する規定は翻案を認めていない。'],[
'第47条の6第1項第1号は、列挙する規定により著作物を利用できる場合に、その規定の例による翻案等を認めています。第35条を根拠とするなら同条の要件が必要で、教育目的だけでは足りません。',
'第27条の翻案権を踏まえ、第47条の6第1項第1号は、第35条第1項による利用が可能な場合の翻案等を認めています。一方、第50条は権利制限の規定が著作者人格権に影響しないとしています。要約と呼ぶだけで無条件に自由とは扱いません。',
'第50条は、この款の権利制限を著作者人格権に影響するものと解釈してはならないとしています。第20条の同一性保持権とその例外も含めて確認する必要があり、人格権を一律に無効とする肢は誤りです。',
'第47条の6第1項第1号は、第35条第1項を挙げ、その規定の例による翻訳・編曲・変形・翻案を認めています。翻案は含まれないという肢とは逆です。'],[
'誤：第35条による利用が可能であるという前提を削除','正：第47条の6の翻案と第50条の人格権の留保を区別','誤：第50条と逆に人格権を一律排除','誤：第47条の6第1項第1号の翻案を否定'])}
extra=[]
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status'] in {'修正必要','要追加確認'} and int(a['A_'+k[2:]]['ans'])==ans
 ss=['S26','S161'] if k!='Q_O_049' else ['S26']
 reason='保存済みe-Gov原応答の本則を追加照合。第35条の適用前提・ただし書、第47条の6第1項第1号の翻案、第50条の人格権への留保を各問の対象に合わせ独立判定。他の許諾・権利制限による利用まで全否定せず、教育目的や要約という名称だけでの無条件承認を撤回する。'
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=ss,applied=True,before_version='第101バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=ss,reason=reason,option_verdicts=verdicts,stem_review='修正済みケース10の全前提と設問・全4肢を本則条文に照らし独立比較。要約が実際に翻案に当たるかは、創作的表現を引き継ぐ翻案と設問で仮定しており、全要約に一般化しない。',explanation_review='全4解説を本則第20・27・35・47条の6・50条のうち各問の対象と照合。人格権の例外や他の許諾・権利制限の可能性を一律否定しない。',unresolved='',multiple_correct_risk='なし：指定根拠による利用という条件に合う肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27
for name,obj in [('changes.json',c+extra),('changes_batch102.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('3 full reviews /27 edits')
