"""One-time CLIL primary-framework audit, after batch126 is saved."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2743
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
reason='Coyleを含む著者Bower/Cross/CoyleのCLIL枠組みの本文（出版社公開章抜粋、印刷9〜11/PDF8〜10）を取得・画像照合。CLILの内容と言語の二重焦点、4Csの正式名称、内容と結び付く言語・思考の活動を確認。BICS/CALP定義・課題の相対性はCummins2008著者稿PDF2〜3・5で補完。初級者全員の認知要求を一律排除する主張、CALPを書き言葉だけとする主張、全員の効果保証を認めない。ケース内活動の意義は設計意図であり学習成果の実証ではない。未取得の引用先研究や章全体・本全体の承認ではない。'
data={
'Q_4_037':(1,'CLILの内容と言語を結び付ける枠組みと、Cummins（2008）のBICS・CALPの区別を踏まえた授業設計として、最も適切なものを一つ選びなさい。',[
'教科内容に関わる概念や考えを理解し表現する言語も学習対象とし、内容・思考の活動と、それに必要な言語面の支援を結び付ける。',
'内容と言語を別々の学習とし、教科で必要な言語をすべて身に付けるまで、内容を扱う活動は始めないことをCLILの原則とする。',
'学習言語の熟達度が低ければ、学習者の既有知識や支援の有無にかかわらず、内容について考える活動を一切除く。',
'CALPは書き言葉だけの能力とみなし、教科内容について口頭で説明し合う活動は学習言語の育成に含めない。'],[
'CLILの枠組みは内容と言語の双方を焦点とし、思考と言語使用を結び付けます。CALPには教科の概念や考えを口頭・書面で理解し表現する側面があるため、内容・思考の活動と必要な言語面の支援を結び付ける設計は両者に整合します。',
'取得したCLILの説明は、内容の目標から必要な言語を分析し、授業前の支援計画と授業中に生じる言語使用の両方を扱います。すべての言語を先に習得してから内容を扱うという一律の順序原則ではありません。',
'CLILの枠組みは内容・思考と言語を結び付け、Cumminsは課題の認知的要求や文脈的支えが既有知識などで変わると述べます。言語の熟達度だけから、支援も検討せず内容について考える活動を一切除く判断にはなりません。',
'CumminsによるCALPの定義には口頭と書面の双方が含まれます。CLILでも内容の意味を伝え合う言語を扱うため、教科内容についての口頭の説明を一律に学習言語の対象外とすることはできません。']),
'Q_O_067':(4,'CoyleのCLILの「4Cs」枠組みに含まれないものを、次の1〜4の中から一つ選べ。',[
'内容（Content）','認知・思考（Cognition）','コミュニケーション（Communication）','競争（Competition）'],[
'Contentは枠組みの一要素であり、学ぶ分野や主題に関わる知識・概念・技能を指します。したがって「含まれないもの」には当たりません。',
'Cognitionは、理解・評価・省察・創造など、知識や経験について考え意味付ける側面を指します。枠組みの一要素です。',
'Communicationは、学ぶ知識・概念・技能について意味を作り伝えるための言語の側面を指します。単なる言語使用量だけを意味するのではなく、枠組みの一要素です。',
'4CsはContent、Communication、Cognition、Cultureです。Competitionはこの四要素に含まれません。ここで挙がっていないCultureは、社会的・授業的・分野別の慣習など、知識や経験との関わり方を扱います。']),
'Q_O_068':(2,'ケース14の資料読解・グループディスカッションを、CLILの内容と言語を結び付ける学習として設計する意義として、最も適切なものを一つ選べ。',[
'環境問題の内容の理解は学習目標とせず、日本語を使う量だけを増やす活動として位置付けられるため',
'環境問題について考え、資料の内容や自分の理解を日本語で伝え合うという、内容と言語の双方に関わる学習機会を設けられるため',
'環境問題の内容や相手の考えは扱わず、既習文型を決められた順に繰り返すことだけを学習目標とするため',
'環境問題について何を理解し伝えたかは問わず、発音の正確さだけを唯一の学習目標とするため'],[
'ケースは環境に関する資料を読み、内容について話し合い、比較したレポートを書く設計です。内容の理解を学習目標から除き日本語の使用量だけを目的とする説明は、内容と言語を結び付ける観点と一致しません。',
'ケースの内容について考える活動と日本語で伝え合う活動を、内容と言語の二重焦点から捉えた説明です。資料読解や対話を通じて学ぶ機会を設計する意義を述べたもので、全員の理解や言語能力の向上を保証する実験結果ではありません。',
'文型の練習が併用される可能性は否定しません。しかし、内容や相手の考えを扱わず決められた反復だけを目標にする説明では、このケースの読解・話し合いの学習機会を説明できません。',
'発音が指導対象になる可能性はありますが、内容の理解や意味の伝達を問わず発音だけを唯一の目標とする説明は、内容と言語の双方を扱うケースの設計と異なります。'])}
verdicts={
'Q_4_037':['正：内容・認知・言語支援を結び付ける設計','誤：すべての言語の事前習得という一律条件','誤：既有知識や支援を無視して思考を全排除','誤：CALPの口頭の側面を全排除'],
'Q_O_067':['誤：Contentは構成要素','誤：Cognitionは構成要素','誤：Communicationは構成要素','正：Competitionは構成要素ではない'],
'Q_O_068':['誤：ケースの内容目標を除外','正：内容と思考、意味を伝え合う言語の学習機会','誤：内容理解や対話を単純反復に置換','誤：内容と意味伝達を除いて発音だけに限定']}
for k,(key,stem,opts,exps) in data.items():
 assert d[k]['status']=='要追加確認' and a['A_'+k[2:]]['ans']==str(key)
 sources=['S190','S191'] if k=='Q_4_037' else ['S191']
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第126バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==key else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts[k],stem_review='全4肢を著者本人を含むCLIL枠組み記述に独立照合。応用2問はケース14本文の資料読解・対話・比較レポートと照合し、本文の不明な詳細を推定しない。',explanation_review='全4解説を取得本文と画像へ照合。4Csの正式名称と意味、授業の設計意図と効果の実証を区別。CALPは口頭/書面を含む。初級者の全排除や全員の効果保証をしない。',unresolved='',multiple_correct_risk=f'なし：独立正答{key}のみ適切',no_correct_risk=f'なし：独立正答{key}')
assert len(extra)==27
for name,obj in [('changes.json',cs+extra),('changes_batch127.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'clil.pdf').read_bytes()
(b.OUT/'evidence/batch127_sources.json').write_text(json.dumps([dict(source_id='S191',title='Bower, Cross and Coyle, CLIL in Multilingual and English-Background Contexts, in Curriculum Integrated Language Teaching: CLIL in Practice',url='https://assets.cambridge.org/97811087/29734/excerpt/9781108729734_excerpt.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-16',body_read_scope='Publisher chapter excerpt full body printed9-11/PDF8-10 text+images; 4Cs and Language Triptych, dual focus. Primary conceptual account coauthored by Coyle, not entire book or original cited intervention studies. S190 reused from batch126.',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('3 questions/27 edits')
