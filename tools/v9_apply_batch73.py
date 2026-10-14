"""One-time bounded ZPD definition and classroom-example audit."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1453
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_3_021':(3,'ヴィゴツキーの「発達の最近接領域（ZPD）」の定義について、最も適切なものを一つ選びなさい。',[
'どのような支援を受けても解決できない課題の水準だけを指す。',
'年齢によって遺伝的に固定され、他者との協働を定義に含めない領域を指す。',
'独力で問題を解決できる実際の発達水準と、成人の指導や自分より有能な仲間との協働で解決できる潜在的な発達水準との間を指す。',
'他者の支援なしに、自分ひとりで問題を解決できる現在の水準だけを指す。'],[
'支援を受けても解決できないという条件だけでは、支援下で解決できる潜在的な水準を捉えていません。ZPDの定義とは異なります。',
'原著抜粋86頁の定義は、独力での問題解決と、成人の指導やより有能な仲間との協働での問題解決を区別します。年齢による固定領域という定義ではありません。',
'原著抜粋86頁の定義に対応します。ZPDは、独力での実際の水準と、支援下での潜在的な水準との間です。あらゆる支援が必ず発達を促すという効果保証とは区別します。',
'独力で解決できる現在の水準は、実際の発達水準に当たります。それだけでは支援下での潜在的な水準との差を表しません。']),
'Q_3_022':(2,'ZPDの定義に照らし、「独力ではまだ解決できないが、適切な支援下では解決できる範囲」に取り組む日本語授業の例として、最も適切なものを一つ選びなさい。',[
'教師の説明やヒントを受けても理解できない論文を与え、そのまま一人で読み終えることを求める。',
'一人では文章を構成できない学習者が、教師の質問やヒントを受けながら、自分で表現を考えて文章を完成させる。',
'既に一人で正確に書けるひらがなだけを、他者の支援なしに書き写す。',
'一人では作文を完成できない学習者に、教師も仲間も手助けせず、独力で完成するまで待つ。'],[
'設問で問うのは、支援下なら解決できる範囲での活動です。この例は支援を受けても理解できないという条件なので、その例には当たりません。',
'独力ではできないことが、成人の指導下ではできるという二つの水準が示されています。ZPDの定義に対応する例です。完成した一回の課題だけで、その後の独力での習得まで確定するわけではありません。',
'この例は既に独力でできる範囲の活動であり、今回問う支援下で初めてできる活動ではありません。復習に学習上の意義が一切ないという意味ではありません。',
'この例では支援下で解決する活動が設定されていません。あらゆる自習が無効という意味ではなく、設問の条件に対応しないため誤りです。'])}
extra=[]
for key,(ans,stem,opts,exps) in items.items():
 assert int(a[key.replace('Q_','A_',1)]['ans'])==ans
 reason='S15の原著抜粋86・88〜90頁に定義と例を限定し、常時変化・支援の必然的効果・既習課題では新たな学びがないという未支持の一般化を除く。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a[key.replace('Q_','A_',1)]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S15'],applied=True,before_version='第72バッチ反映後の累積作業稿')
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S15'],option_verdicts=([ '誤：支援下でも不能','誤：遺伝的固定という定義ではない','正：独力と支援下の水準差','誤：実際の発達水準だけ'] if ans==3 else ['誤：支援下でも不能','正：独力では不能、教師の支援下では可能','誤：既に独力で可能','誤：支援下の活動がない']),reason=reason,stem_review='原著引用86頁の定義に範囲を限定し、全4肢の条件を明示して独立判定。',explanation_review='New Learning掲載の原著抜粋86・88〜90頁の本文を取得・照合。全4解説を定義の適用と非該当理由に限定。原著全冊取得とはしない。復習無効・支援の無条件の因果効果・一回の完成から内在化を断定しない。',unresolved='',multiple_correct_risk='なし：指定条件に一致するのは'+str(ans)+'のみ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch73.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
