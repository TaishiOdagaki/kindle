"""One-time recovery of six independently reviewed questions from batch112."""
import json,html,hashlib,gzip
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2482
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,source,reason,verdicts,expl_review):
 assert d[k]['status']=='要追加確認' and a['A_'+k[2:]]['ans']==str(key)
 for field,old,new in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(o,n) in enumerate(zip(old,new)):
   o=html.unescape(o)
   if o==n:continue
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=[source],applied=True,before_version='第112バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(e)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[source],reason=reason,option_verdicts=verdicts,stem_review='指定した一次本文の範囲で設問・全4肢を独立に照合。元の正解番号を前提にせず単一正答性を再判定。',explanation_review=expl_review,unresolved='',multiple_correct_risk='なし：明示した判断条件に合うのは'+str(key)+'のみ',no_correct_risk='なし：独立正答'+str(key))
k='Q_4_116';opts=q[k]['opts'].copy();opts[0]='教師は、小テストの受験結果や活動完了状況のレポートを確認し、学習者への支援を検討する資料にできる。'
review(k,'LMSの例としてMoodle 4.5を用いる。公式文書に記載された機能と教師の運用に合う説明を一つ選びなさい。',opts,[
'公式文書のQuiz activityは教師による受験結果の確認、Activity completion reportは権限のある教師による完了状況の閲覧を説明しています。これらの情報を支援を考える資料にする説明です。完了印だけで習熟度を測定できる、あるいは支援の効果が保証されるという意味ではありません。',
'Quiz activityは教師が表示を事前確認し、成績を閲覧する運用を説明しています。Forum activityも教師による設定や返信を扱います。システムを導入しただけで教師の確認や支援がすべて不要になるという肢は、この運用の説明に合いません。',
'Quiz settingsのReview optionsには、解答ごとのフィードバックや問題全体の一般的なフィードバックを表示する設定があります。正誤だけしか示せず解説を設定できないという説明は誤りです。何をいつ見せるかは設定に依存します。',
'Forum activityは、学習者と教師が投稿と返信を通して意見を交換できる機能を説明しています。したがって資料配布と課題提出だけに限定し、対話の機能を避けるという説明は合いません。すべての製品や授業で同じ機能・効果があるという主張ではありません。'],1,'S172',
'Moodle4.5公式本文4ページを取得。製品横断の機能保証と学習支援の効果断定を避け、閲覧権限・表示設定を含む機能と教師の運用に限定。出席管理の標準搭載、Classroomの機能、学習の自動最適化等は未照合として本問から除く。',
['正：権限のある教師による結果・完了状況の閲覧と支援検討','誤：公式に説明される教師の設定・閲覧・返信まで不要とする','誤：個別・一般的フィードバックの表示設定を否定','誤：投稿・返信による対話機能を除外'],
'全4解説をQuiz activityのTeacher view、Quiz settingsのReview options、Forum activityの機能とTeacher view、Activity completion reportの権限・完了表示へ照合。自動的な早期発見や個別支援の因果効果は同資料で承認しない。')
review('Q_4_117','Flipped Learning Network（2014）の定義と「四つの柱」に照らし、反転学習（Flipped Learning）の説明に合うものを一つ選びなさい。',[
'個人で学ぶ教材は動画だけに限られ、授業外で文章を読ませる方法は認められない。',
'動画を配信しておけば、教師が学習状況を観察したり、形成的評価を行ったりする必要はなくなる。',
'集団で学ぶ場を廃止し、すべての活動を学習者が一人で完結させ、教師による支援をなくす。',
'直接指導を集団で学ぶ場から個人で学ぶ場へ移し、集団での時間は教師の支援の下で概念の応用や相互作用を伴う学習に充てる。'],[
'1頁は授業外での文章の読解も取り上げ、2頁のI.2も教材を「通常は動画」としており、動画だけに限定していません。特定の動画時間が全員に最適だという実証も、この定義資料からは導けません。',
'2頁のF.2は継続的な観察と調整、P.1は必要に応じたフィードバック、P.2は形成的評価を挙げています。動画の配信だけでこれらが不要になるという説明は一致しません。',
'1頁の定義は、集団で学ぶ場を相互作用のある学習環境へ変えるとしています。集団の活動や教師の支援をなくし、すべて一人で完結させるという説明ではありません。',
'1頁の定義に対応します。さらに同資料は、単に授業と宿題を入れ替えるだけのFlipped ClassroomとFlipped Learningを区別し、2頁で柔軟な環境、学習文化、意図的な内容、専門職としての教師という四つの柱を示しています。ここではその枠組みを問い、学習効果の普遍的保証や動画の必須化を主張していません。'],4,'S173',
'FLN自身の2014年定義・四つの柱の原資料2頁を通常取得し全文・両頁画像を照合。反転学習と単なる授業反転を区別し、数分〜10分の普遍最適性、動画配信だけの効果保証、blendedの範囲差という未照合主張を除く。同じ反転領域の原定義へ改訂。',
['誤：動画以外の教材を排除','誤：継続観察・フィードバック・形成的評価を排除','誤：集団での相互作用と教師支援を排除','正：直接指導の移行と集団での応用・相互作用'],
'全4解説を原資料1頁の定義・Classroomとの区別、2頁I.2・F.2・P.1・P.2と四つの柱へ照合。原資料の概念枠組みを問うもので、引用先の実証研究や全教育場面の効果は承認しない。')
def case(n,stem,opts,exps,key,verdicts):
 k=f'Q_O_{n:03}'
 review(k,stem,opts,exps,key,'S173','S173 FLN2014原資料1〜2頁と現行ケース8の全3段落を照合。F.2の観察・調整、F.3/I.3の学習方法・アクセスの配慮、P.1/P.2の支援と形成的評価を、この架空事例に適用する判断として明示。視聴の有無をテストから確定せず、原因や介入効果も断定しない。',verdicts,'全4解説を原資料1頁の個人と集団の学習場面、2頁F.2/F.3/I.3/P.1/P.2とケース本文へ照合。具体的対応は枠組みを適用する本問の提案であり、原著の実験結果・原文引用や効果保証ではない。動画視聴はすべての反転学習で必須とはしない。')
 d[k]['stem_review']='ケース8の動画・小テスト・応用活動・未視聴と結果不振という記録を精読。設問にFLNの基準と追加の判断条件を明示し、4肢を独立比較。ケースにない未視聴の理由・個々の習熟度を推定しない。'
opts=q['Q_O_037']['opts'].copy();opts[3]='基本的な内容の理解を確かめる手掛かりを得て、その後の活動や支援を調整するため'
case(37,'このケースの小テストを形成的評価として用いる場合、FLN（2014）のP.2に合う意義を一つ選びなさい。',opts,[
'P.2は観察や記録によって次の指導に情報を生かすことを挙げています。学期の成績に入れないことだけでは、その情報を活動や支援の調整に使う意義を説明できません。成績に算入しない運用自体を否定するものではありません。',
'ケースでは動画で基本的な説明を学ぶよう指示しています。理解を確かめるテストを置いたという事実だけで、その事前活動が不要になったとは判断できません。',
'P.2は反転学習における形成的評価を明示しています。小テストをそのための情報収集に使うこの設問の条件で、反転授業と無関係とする肢は合いません。',
'P.2の、観察や記録を次の指導へ生かすという考え方に対応します。このケースでは小テストを基本的な理解の手掛かりにできますが、得点だけで動画を実際に視聴したか、なぜ理解が不十分かまで確定できるわけではありません。'],4,
['誤：評価情報の利用ではなく成績からの除外だけを目的とする','誤：確認課題から事前活動不要を導く','誤：明示された形成的評価との関係を否定','正：理解の手掛かりから活動・支援を調整する'])
opts=q['Q_O_038']['opts'].copy();opts[0]='動画を視聴できたかは一切確認せず、教材にアクセスする方法も見直さない';opts[2]='全員が事前に動画を視聴し、内容を十分に理解したものと決めてよい';opts[3]='視聴してこなかった理由や視聴環境を確かめ、内容にアクセスできる方法を検討する'
case(38,'この記録には未視聴の理由までは示されていない。FLN（2014）のF.2・F.3・I.3を参考に、この授業設計を見直す際の対応を一つ選びなさい。',opts,[
'F.2は学習者を観察して調整すること、F.3とI.3は学習方法や内容へのアクセスを配慮することを挙げています。未視聴が記録されているのに確認も見直しも行わない肢は、この基準に合いません。',
'ケースは未視聴の理由や得点不振の原因を特定していません。偶然にすぎず授業設計と関係ないと断定する根拠はなく、F.2の観察と調整につながる検討を止めてしまいます。',
'ケースは一部の学習者が未視聴で小テストも不振だったと記しています。全員の視聴と十分な理解を前提にすることは記録に反し、学習者の状況を観察するF.2にも合いません。',
'未視聴の原因を決めつけずに事情を確かめ、学習方法や教材へのアクセスを検討する提案です。F.2・F.3・I.3をこのケースに適用したもので、通信環境や動機づけが原因だったと認定したり、特定の変更の効果を保証したりするものではありません。'],4,
['誤：学習者の状況確認とアクセスの検討を排除','誤：未記録の原因を偶然のみと断定','誤：未視聴という記録と矛盾する前提を置く','正：原因を確かめ学習方法・アクセスを検討する'])
opts=q['Q_O_039']['opts'].copy();opts[2]='必要な内容や理解の状況を確認し、補足説明やフィードバックを行うなど、教室活動への参加を支える'
case(39,'この日の活動に参加できるよう支援する方針をとる。FLN（2014）のF.2・P.1に合う、未視聴の学習者への対応を一つ選びなさい。',opts,[
'今後の支援を一切行わない方針は、この設問の参加を支える条件に反します。必要に応じてフィードバックを行うP.1の考え方とも合いません。',
'F.2は状況の観察と調整を挙げています。理解を確かめず、特に対応しないと決める肢は、その考え方に合いません。同じ活動やペースを用いることが、どの場面でも誤りだという意味ではありません。',
'F.2の観察と調整、P.1の必要に応じた個人・小集団・全体へのフィードバックを参考にした提案です。補足の内容や時間は理解の状況に応じて考え、短い説明だけで全員が理解できるとは仮定しません。',
'活動から完全に排除することは、この設問の参加を支える方針に反します。P.1が示す必要に応じた支援を検討する説明でもありません。'],3,
['誤：明示された支援方針とP.1に反する','誤：観察と調整を行わず一律に進めると決める','正：理解を確かめ必要な説明・フィードバックを検討','誤：活動参加を支えるという設問条件に反する'])
opts=q['Q_O_040']['opts'].copy();opts[2]='学習者が予習できなかった事情を確かめ、教材へのアクセスや、事前活動と教室活動のつながりを見直す'
case(40,'同じ授業設計を改善して再試行する方針をとる場合、FLN（2014）のF.2・F.3・I.3を参考に検討できる改善策を一つ選びなさい。',opts,[
'必要な内容を部分的に説明し直すことまで否定されません。しかし、この肢は教室で内容をすべて繰り返し時間を使い切るとしており、ケースで重視した応用活動につなぐ改善を説明していません。',
'今後一切採用しないという肢は、この設問の改善して再試行する方針に合いません。授業方法の中止が、どのような事情でも不適切だという一般論ではありません。',
'F.2の観察と調整、F.3とI.3の学習方法・アクセスへの配慮を、未視聴があったこのケースに適用する提案です。原因を確認してから改善を考えるもので、動画の長さや動機づけが原因だったと決めつけません。',
'予習の有無や理解の状態を確かめず、全員に同じ内容を行うと決めるだけでは、F.2の観察に応じた調整を説明できません。共通の内容を扱うこと自体を否定するものではありません。'],3,
['誤：応用活動へつなげる設計改善にならない','誤：改善して再試行するという設問条件に反する','正：事情を確かめ教材・活動のつながりを調整する','誤：状況による観察・調整を考慮しない'])
assert len(extra)==41,len(extra)
for name,obj in [('changes.json',c+extra),('changes_batch113.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
items=[]
for title,sections in [('Quiz_activity',['What is the Quiz activity?','Teacher view']),('Quiz_settings',['Review options']),('Forum_activity',['What is the Forum activity?','Teacher view']),('Activity_completion_report',['viewer permissions','completion key'])]:
 raw=Path('/workspace/scratch/01d7c3f9b818/'+title+'113.html').read_bytes();assert b'4.5 docs' in raw
 archive='batch113_moodle_'+title+'.html.gz';(b.OUT/'evidence'/archive).write_bytes(gzip.compress(raw,mtime=0))
 items.append(dict(url='https://docs.moodle.org/405/en/'+title,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),archive=archive,read_sections=sections))
raw=Path('/workspace/scratch/01d7c3f9b818/fln113.pdf').read_bytes()
(b.OUT/'evidence/batch113_sources.json').write_text(json.dumps(dict(S172=dict(title='Moodle4.5 official documentation',pages=items,limits='Specified4.5 docs, not other products or current default installations, permissions/settings required; no causal learning-effect proof'),S173=dict(title='The Four Pillars of F-L-I-P',author='Flipped Learning Network',year=2014,url='https://flippedlearning.org/wp-content/uploads/2016/07/FLIP_handout_FNL_Web.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pages=2,read_and_image_review_pages=[1,2],limits='Original definition/design framework only; case8 applications are independent editorial judgments, not quoted original experiments; not general blended-learning taxonomy or causal effect proof; copyrighted source PDF not redistributed')),ensure_ascii=False,indent=2)+'\n')
print('6 full questions/41 edits recovered; independent keys1,4,4,4,3,3 unchanged')
