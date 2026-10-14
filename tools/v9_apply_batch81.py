"""One-time source-bounded review of task stages, information gaps and reordering."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1732
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
assert 'S145' not in (b.OUT/'sources.md').read_text()
items={
'Q_4_036':(1,'Jane WillisがTeachingEnglishの記事「From priming tasks and target tasks to language focus and grammar」で説明する授業の段階について、最も適切なものを一つ選びなさい。',[
'タスク・サイクルの後で、教科書の文法部分を使って形式に焦点を当てた学習を行うことを提案している。',
'Pre-taskの目的を、新しい文法形式を全員が完全に暗唱できるまで、その形式の産出だけを強制することと定義している。',
'Planningでは意味を伝える表現を改善してはならず、辞書の使用や教師への言語面の相談も禁止すると説明している。',
'Reportでは流暢さだけに焦点を当て、正確さへの注意を排除すると説明している。'],[
'記事の「Focus on Form: At the end of the task cycle」に対応します。ここでは取得した本人の記事の提案を問い、Prabhuの枠組みと一つにまとめたり、すべてのTBL授業で同じ手順が必須だとしたりはしません。',
'記事のPre-task/Primingは主なタスクへの準備であり、必要な語彙を活性化する活動などを挙げています。新形式の産出を暗唱完成まで強制するという定義ではありません。',
'記事のPlanningでは、伝えたいことを表す言語を改善し、辞書を調べたり、教師に相談したり、報告を練習したりできます。サイクル内では言語に注意を向けないという一括りの説明はできません。',
'記事はReportで流暢さと正確さの両方に焦点を当てると述べています。正確さを排除する説明は対応しません。'],[
'正：サイクル後の形式学習という本人の提案に一致','誤：準備段階を暗唱完成までの新形式産出強制と取り違える','誤：Planningでの辞書・教師相談・表現改善を禁止し本文と逆','誤：Reportでの正確さへの注意を排除し本文と逆'],['S145']),
'Q_4_040':(2,'Richards（2006）18頁のインフォメーション・ギャップの説明に照らし、持っていない情報を相手から得る必要がある活動案を一つ選びなさい。',[
'全員が見ている同じ単語を教師が発音し、学習者全員がその後に続いて一斉に復唱する。知らない情報を尋ねる課題は設けない。',
'ペアの二人が少しずつ異なる絵を持ち、互いの絵を見せずに質問と応答を行って、違いがいくつあるかを調べる。',
'全員が同じ文章を見て交代で音読する。各自だけが持つ情報や、相手から未知の情報を得る課題は設けない。',
'全員に同じ例文と語のリストを配り、各自が一人で文を書き換える。書いた内容を相手と交換したり質問したりはしない。'],[
'この案は同じ情報を見て教師の発音後に復唱する活動で、未知の情報を相手から得る課題がありません。復唱をシャドーイングと同一視する説明や、音声練習一般の価値の否定はしません。',
'同書18頁の絵の違いを探す例に対応します。互いに見えない絵について質問し、持っていない情報を得る必要があります。情報差を設けたことだけで習得効果が必ず生じるとするものではありません。',
'同じ文章を使う授業でも別の情報差を設計することは考えられますが、この案はそれを含めないと明示しています。音読そのものの是非ではなく、設問の条件への適合性を判断します。',
'この案は個人での書換えに限定され、未知の情報を相手から得るやり取りを含みません。活動に別の学習目的を設定できるかどうかとは区別します。'],[
'誤：共有済み情報の復唱だけで未知情報の取得なし','正：互いに見えない絵の情報差を質問と応答で埋める','誤：情報差の課題を含めない条件を明記','誤：個人の書換えに限定し相手からの情報取得なし'],['S144']),
'Q_4_046':(4,'教材のアダプテーションのうち、ここでは活動や教材部分の実施順序を変えることを「再配列」と呼ぶ。Jane WillisのTeachingEnglishの記事にある教科書を使う授業の組替えを参考にした次の説明で、再配列の例になっていないものを一つ選びなさい。',[
'先に予定していた主なタスクの前へ、その話題の語彙を活性化する小さな準備課題を移した。',
'主なタスクの直後に報告していたが、その間へ既存の報告準備の活動を移し、タスク、準備、報告の順に並べ替えた。',
'教科書で先に配置されていた文法練習を、同じ話題のタスクを行った後に移して実施した。',
'活動の順序と内容はそのままにして、学習者へ配る用紙の部数だけを増やした。'],[
'主なタスクより前に準備課題を置くよう実施順を変えており、設問で定めた再配列に該当します。本人の記事はPre-taskで語彙を活性化する小課題を使うことを提案しています。',
'タスクと報告の間に準備活動を置くよう順序を変えているので、再配列に該当します。記事のPlanningは、報告へ向けて表現を改善し準備する位置づけです。',
'教科書の文法部分を話題に関するタスクの後へ移す案は、記事の「Use the book but change the order」に対応します。すべての教材で常にこの順序が最善だという判断ではありません。',
'変更しているのは配布部数だけで、活動や教材部分の実施順序は変わっていません。このため、設問で定めた再配列の例には該当しません。'],[
'適切な対応：準備課題の実施位置を変更','適切な対応：準備をタスクと報告の間へ移動','適切な対応：文法部分をタスクの後へ移動','不適切な対応：部数だけの変更で実施順の変更なし'],['S145'])}
extra=[]
for key,(ans,stem,opts,exps,verdicts,sources) in items.items():
 assert int(a['A_'+key[2:]]['ans'])==ans and d[key]['status']=='修正必要'
 reason='Willis本人の記事の段階別の提案、又はRichards本人の情報差の説明へ限定。モデル混在、サイクル中の形式注意禁止、復唱とシャドーイングの同一視、未照合の分類体系と効果保証を除く。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第80バッチ反映後の累積作業稿',block_context='A_'+key[2:] if field=='explanations' else key)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='全4肢を指定した本文と明示条件で独立判定。Q_4_036は本人の公開記事を指定、Q_4_040は見せない絵と情報取得を明示、Q_4_046は再配列の操作的定義を明示し架空案を判定。',explanation_review='全4解説を照合。S145はJane Willis署名の著者記事本文のUse the book but change the order、Pre-task/Priming、Task Cycle、Focus on Form節。1996年書籍全体やPrabhu原著は未取得で一括承認しない。S144は52頁冊子の印刷18頁を本文・画像照合。言語指導の普遍的優劣、信頼度や長期習得効果の保証は含めない。',unresolved='',multiple_correct_risk='なし：明示した条件と出典に対応する選択肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27
for name,obj in [('changes.json',c+extra),('changes_batch81.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('3 questions / 27 edits; keys unchanged')
