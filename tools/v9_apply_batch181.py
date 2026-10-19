"""One-time needs/environment analysis revision against acquired Nation text."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3579
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_4_027',4,
'Paul Nation『What Should Every ESL Teacher Know?』第2・3章のニーズ分析の説明に合うものを一つ選べ。',
['ニーズを調べる資料は質問紙だけに限定し、テストや課題の結果、教師の観察は利用しない。',
'ニーズはコース開始時に一度だけ調べ、その後は学習者の習熟や経験が変わっても調べ直さない。',
'ニーズ分析は学習者の希望だけを扱い、現在知っていることや将来必要となることは対象に含めない。',
'学習者が現在知っていること、必要となること、学びたいことを調べ、コースの途中でもニーズを捉え直す。'],
['第3章は、学習者の意見に加え、テストや課題の結果、教師の観察やコースの評価もニーズを知る資料として挙げています。質問紙だけへの限定は合いません。',
'第3章は、習熟や言語使用経験などに伴ってニーズが変わるため、開始時だけでなくコースを通じて分析を行うと説明しています。開始時だけという説明とは逆です。',
'第2章は、現在知っていること、必要となること、学びたいことの三つを扱います。希望以外を対象から外す説明は合いません。',
'第2章の三つの観点と、第3章の継続的なニーズ分析の説明に対応します。必要なことと本人が学びたいことは、一致する場合も一致しない場合もあるとされています。'],
['誤：テスト・課題・観察等の資料を排除','誤：継続的分析を否定','誤：既有知識・必要知識を排除','正：三観点と継続的分析に一致']),
('Q_4_030',2,
'地域日本語教室のコースを計画する際、Paul Nation『What Should Every ESL Teacher Know?』第2・3章のニーズ分析・環境分析の説明を参考にする。計画の検討方法として説明に合うものを一つ選べ。',
['学習者が現在できることや必要な生活場面を調べず、全員に同じ文法項目を同じ速さで教えることだけを優先する。',
'学習者が既に知っていること、生活上必要なこと、学びたいことを調べ、時間や資源などの条件も踏まえて内容を検討し、途中でも見直す。',
'学習者から希望を聞いたら、時間や実現可能性は検討せず、提案された内容を全てそのまま授業に組み込む。',
'利用できる時間や資源を一覧にすれば環境分析は終わりとし、それらをどう活用するか、制約にどう対処するかは検討しない。'],
['第2章は、学習者の既有知識、必要なこと、希望を調べると説明しています。これらを調べず固定の内容と速度だけを優先する案は、その検討を欠いています。',
'第2章のニーズの三観点、時間・資源等を扱う環境分析と、第3章の継続的な分析を、この教室の計画に応用した案です。特定のシラバスが常に最適だと保証する説明ではありません。',
'第2章の交渉によるシラバスでは、希望を単に受け入れるのでなく、有用性や実現可能性を教師と学習者が検討すると説明しています。第3章でも時間内に収まるよう提案を選ぶ例が示されています。',
'第2章は、促進要因や制約を見つけるだけでは足りず、活用や克服を検討する必要があると説明しています。一覧作成だけで終える案は、この次の検討を欠いています。'],
['誤：学習者の三観点を調べない','正：ニーズと環境条件を踏まえ継続的に検討','誤：交渉を無条件受入れに置換','誤：要因発見後の検討を排除']),
('Q_O_006',4,
'ケース2で志望学部と、その学部で学ぶために必要な日本語力を調べている部分に注目する。Paul Nation『What Should Every ESL Teacher Know?』第2章のニーズ分析の三観点では、特にどの観点に対応するか。一つ選べ。',
['学習者が現在どれだけの語彙を知り、どの程度読んだり話したりできるかを調べる観点。',
'教師の技能や学級の人数など、コースの実施に影響する環境条件を調べる観点。',
'将来の使用場面で何が必要かとは区別して、本人がどのようなことを学びたいかを調べる観点。',
'学習者がこれから行う学術的な学習のために、どのような言語知識や技能が必要かを調べる観点。'],
['これは第2章の、学習者が現在知っていることを調べる観点です。設問で指定したのは、現在の到達度ではなく、志望学部での学習に必要な言語知識や技能です。',
'教師の技能や学級の人数は、同章で環境分析の要因として挙げられています。設問が指定する、将来の学術的な学習に必要な言語知識や技能とは区別します。',
'これは同章の、学習者が学びたいことを調べる観点です。本人の希望と必要なことは重なり得ますが、設問はそのうち学部で学ぶために必要な日本語力を指定しています。',
'同章は、学術的な学習を予定する学習者について、専攻したい分野と、その学習に必要な言語知識や技能を調べる例を示しています。ケースの指定部分をこの観点と比較できます。'],
['誤：指定部分を現在の知識に置換','誤：指定部分を環境条件に置換','誤：指定した必要性と希望の観点を区別しない','正：学術的学習で必要となる知識技能']),
('Q_O_007',3,
'ケース2で調べた情報のうち「使える学習時間」に注目する。Paul Nation『What Should Every ESL Teacher Know?』第2章でニーズ分析と区別して説明される環境分析との関係について、合うものを一つ選べ。',
['学習時間は、学習者が現在どの程度の語彙や読解力を持つかを、それだけで直接示す情報である。',
'学習時間は、将来の大学の講義やレポートでどの言語知識が必要かを、それだけで直接示す情報である。',
'利用できる時間は、コースを設計する際に活用や制約への対処を考える環境要因の一つである。',
'環境要因は教師や教室の物理的条件だけを指すため、学習者が使える時間は環境分析に含まれない。'],
['同章は、既有知識を調べる例として語彙量、読解、文法、話す力を挙げています。利用できる時間の情報だけから、これらの現在の能力を確定することはできません。',
'同章は、予定する学術的な学習で必要となる言語知識や技能を調べる観点と、時間などの環境条件を区別して説明しています。学習時間だけで必要な言語知識が決まるわけではありません。',
'同章は、コースで利用できる時間を環境要因の例に挙げ、促進要因を活用し制約に対処する検討を求めています。ケースの時間の情報を、この環境面の検討に用いることができます。',
'同章では環境要因は学習者、教師、教育の状況に関わるとされ、学習者に十分な学習時間がある例も示されています。教師や物理的条件だけに限定する説明は合いません。'],
['誤：時間だけで現在の能力を確定','誤：時間だけで目標場面の必要知識を確定','正：時間を環境要因として検討','誤：環境要因から学習者の時間を排除'])]
extra=[]
reason='S197 Paul Nation原著書の出版社無料公開192頁PDFを取得。印刷/PDF12～15・23～25頁本文、12・13・14・25頁画像を精読。ケース2本文も照合。現在の知識・必要な知識・希望、環境分析の広がり、継続分析、交渉の実現可能性を全肢全解説へ対応。旧稿のニーズ＝目標のみ／既習歴等＝レディネスという排他的区分、主観客観の単純な逆転説明、未取得Hutchinson/WatersのLackの定義、特定シラバスの効果や離脱の因果断定は撤回し承認しない。ESLに関する著者の枠組みの日本語ケースへの応用であり、日本の地域施策や授業効果の実証ではない。'
for k,key,stem,opts,exps,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   assert html.unescape(old)!=new
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S197'],applied=True,before_version='第180バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S197'],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='著者の枠組みと設問の指定範囲を明示。ケース2は必要な知識と利用時間の別々の部分を指定し競合を解消。',explanation_review='各4肢・4解説を取得した原著本文へ照合。排他的なニーズ／レディネス分類や効果の断定を撤回。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定本文・ケースの指定部分に対応',no_correct_risk=f'なし：{key}の根拠本文取得済み')
assert len(extra)==36
for n,obj in [('changes.json',cs+extra),('changes_batch181.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'nation181.pdf').read_bytes()
entry=dict(source_id='S197',author='Paul Nation',title='What Should Every ESL Teacher Know?',url='https://wjcompass.com/userfiles/downloads/20130213132738_DW11.pdf',publisher_page='https://www.compasspub.com/eng/compass/level_view.asp?h_seq=1721',checked='2026-10-19',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pages=192,body_read='印刷/PDF12～15・23～25頁本文。12・13・14・25頁画像。ケース2全文。',version_note='第135バッチの大学公開稿とはサイズ・ハッシュが異なる出版社無料公開PDF。書名・著者・章本文と印刷頁を現物で確認し、原バイト同一とはしない。出版社商品ページ240p表示と取得PDF192頁を混同しない。刊年をファイル名から推定しない。',scope='著者自身の枠組みの説明とケースへの応用。全192頁・引用先原典・日本の地域施策・学習効果は未検証。',full_source_redistributed=False)
(p/'evidence/batch181_sources.json').write_text(json.dumps([entry],ensure_ascii=False,indent=2)+'\n')
attempts=[dict(url=u,result=v) for u,v in [
('https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/paul-nations-publications/publications/documents/What-Should-Every-ESL-Teacher-Know-13-Feb-2013.pdf','Web open・通常直接取得とも410'),
('https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/paul-nations-publications/publications/documents/what-should-every-esl-teacher-know-13-feb-2013-pdf','通常直接取得410'),
('https://openaccess.wgtn.ac.nz/articles/journal_contribution/Designing_and_improving_a_language_course/12560360','Web open403。迂回せず、2000年論文の本文取得済みとしない。'),
('https://www.cambridge.org/core/books/abs/english-for-specific-purposes/needs-analysis/7353C7268C9DFA810CF7D951A69AB284','検索は章の要約のみ。Hutchinson/Waters1987章本文の取得・承認には使わない。')]]
(p/'evidence/batch181_source_attempts.json').write_text(json.dumps(attempts,ensure_ascii=False,indent=2)+'\n')
