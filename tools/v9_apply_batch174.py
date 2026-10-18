"""Historical culture-shock descriptions without a universal clinical trajectory."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3435
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_3_030',4,
'オバーグ（1960）「Cultural Shock: Adjustment to New Cultural Environments」の2006年再録本文にある、滞在先への適応過程の説明に合うものを一つ選べ。',
[
'蜜月期は、帰国後に母国の生活習慣だけを再学習する段階として説明されている。',
'回復の説明では、現地の人々を理解するには、自分自身の生活の仕方を全て捨てなければならないとされる。',
'第4段階は、滞在先での生活ではなく、母国に帰った後の再適応だけを指している。',
'第2段階では、生活上の実際の困難を背景に、滞在先への敵意や攻撃的な態度が現れると説明される。'],
[
'再録143頁の蜜月期は、新しい環境に引かれている滞在初期の説明です。帰国後に母国の習慣を再学習する段階としては示されていません。期間にも状況による幅があると述べています。',
'再録146頁では、人々のやり方を理解することが、自分自身のやり方を捨てることを意味するわけではないと述べています。異なる行動の仕方を理解することと、元のものを全面的に放棄することを区別します。',
'再録143頁の第4段階は、滞在先の慣習を別の生活の仕方として受け入れ、その環境で暮らす説明です。帰国時や滞在先を去る際にも触れますが、第4段階を帰国後の再適応だけに限定していません。',
'再録143頁の第2段階の説明に対応します。ただし、著者は同じ頁で影響の程度に大きな個人差があることも述べています。これは歴史的な説明の照合であり、全員に同じ順序や期間で敵意が生じるという診断基準ではありません。'],
'S235 Oberg1960本文のcurare2006再録5頁を取得・全本文精読、142～143頁画像照合。旧LysgaardのUカーブ原著未取得のため、その帰属と必然的な困難のピークを承認せず、同じ異文化適応領域の取得済み原著再録の段階記述へ改訂。原著者の歴史的説明と、個人の臨床診断・全員同一経過の保証を区別する。',
['誤：蜜月期を帰国後へ移す','誤：自己のやり方の全面放棄を要求','誤：滞在先での第4段階を帰国後だけへ限定','正：第2段階の本文説明に一致']),
('Q_3_032',1,
'オバーグ（1960）「Cultural Shock: Adjustment to New Cultural Environments」の2006年再録本文で、カルチャーショックを説明する際の手がかりの捉え方に合うものを一つ選べ。',
[
'日常の社会的なやりとりを支える、慣れ親しんだ合図や手がかりを失うことから生じる不安に注目している。',
'手がかりとは意識して暗記した文法規則だけを指し、身振りや表情、習慣は含まれない。',
'人々への不満を述べることは、相手の社会を十分に客観的に理解した証拠なので、そのまま正確な評価として用いるべきだとしている。',
'現地の人々のやり方を理解したなら、自分自身のやり方を捨て、元の行動様式に戻れなくなることが必要だとしている。'],
[
'再録142頁冒頭の説明に対応します。慣れた手がかりの例には、挨拶の場面で何を言うか、招待を受けるか断るかなども含まれます。本文の理論的・歴史的説明を確認する問題であり、この一文から個人の症状や原因を診断するものではありません。',
'再録142頁は、言葉に加えて、身振り、表情、習慣や規範を挙げています。また、多くの手がかりは普段意識しないまま使われるとも説明します。意識的に暗記した文法規則だけに限る説明とは合いません。',
'再録143頁は、自分の不快さを理由に滞在先を否定的に批判する態度と、状況を分析することを区別しています。固定的な見方が相手社会の真の理解に至るとはしていません。不満があるという事実だけを、相手社会についての客観的評価の証拠とする説明は合いません。',
'再録146頁は、現地の人々のやり方を理解しても、自分自身のやり方を放棄する必要はないと説明します。異なる行動様式を持てることと、元の行動様式を失うことを同一視していません。'],
'S235原著再録の142～143・146頁本文に全4肢と解説を照合。旧解説の正常反応の一律宣言、乗り越えれば必ず成長するという推論、単独の文法対策の順位づけを撤回。原著の病理的比喩や性別・国籍の一般化を現行知見として採用せず、手がかりと文化理解の歴史的説明へ限定。',
['正：慣れた社会的手がかりの喪失と不安','誤：手がかりを文法規則に限定','誤：否定的批判を客観的理解と同一視','誤：理解を自己の行動様式の放棄と同一視'])]
extra=[]
for k,key,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S235'],applied=True,before_version='第173バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S235'],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='対象著者と再録本文を指定。異文化適応・手がかりの説明を独立比較。個人の症状や経過の診断ではない。',explanation_review='全肢全解説を取得した再録本文と照合。歴史的説明と現在の診断基準、個人差と普遍的経過を区別。未取得Lysgaard原著や原誌との全字比較の承認ではない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ再録本文と一致',no_correct_risk=f'なし：{key}に対応する本文を取得')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch174.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'oberg174.pdf').read_bytes()
e=[dict(source_id='S235',url='https://project-tree.net/wp-content/uploads/2019/10/Cultural_Shock_Adjustment_to_new_cultura.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope='curare29(2006)2+3:142–146に掲載されたOberg1960の再録5頁を第三者サイトから取得。全英語本文・再録注記、142～143頁画像を確認。再録の原誌出典注記を確認したが、1960原誌との全字対照・1954講演・現在の医学的診断基準の検証ではない。性別・国籍の一般化、病理的比喩は現行知見として採用しない。',full_source_redistributed=False)]
(p/'evidence/batch174_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
