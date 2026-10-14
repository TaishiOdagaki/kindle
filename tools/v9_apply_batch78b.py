"""One-time extension of batch78 using the acquired Standards glossary."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1640
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_4_052':(2,'AERA・APA・NCMEの2014年版共同標準における、規範準拠と基準準拠の得点解釈の区別として最も適切なものを一つ選びなさい。',[
'規範準拠の解釈とは、定義された基準領域に照らして、その人の遂行水準を示す解釈である。',
'基準準拠の解釈は、定義された基準領域との関係で遂行水準を示し、規範準拠の解釈は参照集団の遂行の分布との比較に基づく。',
'基準準拠の解釈とは、参照集団の遂行の分布と比較して、その人の相対的位置だけを示す解釈である。',
'規範準拠の解釈では、比較の対象となる参照集団を定める必要はない。'],[
'共同標準218頁の基準準拠の得点解釈に対応する説明です。規範準拠は221頁で参照集団の分布との比較として説明されています。',
'共同標準218・221頁の対比に対応します。ここでいう基準準拠は、他者の順位ではなく、定義された基準領域との関係に着目します。',
'参照集団の分布との比較は規範準拠の説明です。基準準拠との名称の対応が逆です。',
'共同標準221頁の定義には、特定された参照集団の遂行の分布との比較が含まれます。参照集団が不要という説明は誤りです。']),
'Q_4_115':(1,'AERA・APA・NCMEの2014年版共同標準の用語定義に沿った、CBTとコンピュータ適応型テスト（CAT）の説明として最も適切なものを一つ選びなさい。',[
'CBTはコンピュータを使って実施するテストを指す。CATでは、それまでの反応に応じ、項目の測定特性や内容を考慮して次の項目などを選ぶ。',
'コンピュータで実施していても、出題項目が過去の反応に応じて変わらなければ、CBTとは呼べない。',
'CATとは、受検者の反応や項目の測定特性・内容を考慮せず、次の項目を選ぶ方式である。',
'CATの定義は、問題文をその場でゼロから自動生成することであり、項目を選択することとは無関係である。'],[
'共同標準217頁のコンピュータ実施型テストとコンピュータ適応型テスト、および215頁の適応型テストの定義に対応します。コンピュータでの実施と、反応に応じた項目選択は区別します。',
'共同標準217頁のコンピュータ実施型テストの定義には、適応型であることという条件はありません。CBTというだけでCATの仕組みまで備わると決めることはできません。',
'共同標準215頁は、それまでの反応との関係で、項目の測定特性や内容に基づいて項目や項目群を選ぶと説明します。これらを考慮しないという記述は逆です。',
'共同標準215・217頁のCATの定義が扱うのは、反応に応じた項目などの選択です。それを問題文の自動生成そのものと定義する記述は誤りです。'])}
extra=[]
for key,(ans,stem,opts,exps) in items.items():
 assert int(a['A_'+key[2:]]['ans'])==ans
 reason='取得した共同標準2014の用語定義へ限定。規範準拠と基準準拠の比較先を明示し、未照合のJLPT・国家資格・共通テスト一般論を除く。CBTとCAT、項目選択と問題文自動生成の混同を修正。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S142'],applied=True,before_version='第78バッチ前半36箇所反映後の累積作業稿',block_context='A_'+key[2:] if field=='explanations' else key)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 verdicts={'Q_4_052':['誤：基準準拠の説明を規範準拠とする','正：基準領域と参照集団分布の対比に対応','誤：規範準拠の説明を基準準拠とする','誤：参照集団を不要とする'],'Q_4_115':['正：実施方式と反応に応じた選択を区別','誤：CBTの定義へ適応性を必須とする','誤：適応型の選択で考慮する要素を排除','誤：項目選択を問題文生成と取り違える']}
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S142'],option_verdicts=verdicts[key],reason=reason,stem_review='共同標準の2014年版を明示。全4肢を取得本文の定義に独立照合し単一正答性を確定。',explanation_review='全240頁公式PDF取得。印刷215・217・218・221頁（PDF225・227・228・231頁）の用語定義を本文・画像照合。特定の実在試験の制度区分・合格方式、CBT製品機能・セキュリティ効果・紙との同等性は承認範囲から除く。',unresolved='',multiple_correct_risk='なし：指定した定義に対応するのは'+str(ans)+'のみ',no_correct_risk='なし：独立正答'+str(ans))
batch=json.loads((b.OUT/'changes_batch78.json').read_text())
for name,obj in [('changes.json',c+extra),('changes_batch78.json',batch+extra),('changes_batch78b.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'additional edits')
