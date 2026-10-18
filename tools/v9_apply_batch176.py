"""Use the issuing institutions' complete texts, not unspecified policy claims."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3480
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_2_010',3,'S239',
'文化庁「消滅の危機にある言語・方言」が、ユネスコの2009年2月発表「Atlas of the World’s Languages in Danger」第3版を紹介している。その掲載言語について、文化庁の説明に合うものを一つ選べ。',
[
'アイヌ語は危険の度合いが最も低く、安全な言語として一覧から除かれている。',
'日本国内の掲載言語は沖縄県内だけにあり、八丈語や奄美語は含まれない。',
'日本国内の8言語として、アイヌ語、八重山語、与那国語、八丈語、奄美語、国頭語、沖縄語、宮古語が挙げられている。',
'日本の言語・方言には消滅の危機にあるものはなく、文化庁は保存・継承の取組を行っていないと説明されている。'],
[
'文化庁の一覧では、アイヌ語は「極めて深刻」に挙げられています。安全な言語として一覧から除かれているという説明は合いません。ここでは同ページが紹介する2009年発表の一覧を確認しています。',
'一覧には、八丈語と奄美語も「危険」の区分に挙げられています。沖縄県内の言語だけに限定し、両言語を除く説明とは一致しません。',
'文化庁の本文と一覧に対応します。同ページは、ユネスコでは「言語」と「方言」を区別せず、全て「言語」として統一していると注記しています。これは2009年の資料を紹介する説明であり、日本の危機的なことばがこの8つに尽きるという主張ではありません。',
'ページ冒頭は、日本の言語・方言に消滅の危機にあるものがあると説明し、文化庁が実態や保存・継承の取組状況の調査研究等を行っていると述べています。東日本大震災の被災地の方言にも触れており、取組がないという説明とは逆です。'],
'S239文化庁の説明本文・8言語と危機度一覧・言語／方言注記・事業一覧を取得照合。指定を掲載へ修正し2009年資料の紹介と明示。旧稿の共通語政策やメディアを世代間継承断絶の主因と断定する補助説明を撤回。UNESCO Atlas原資料・最新話者数・全危機言語の網羅は今回未確認。',
['誤：アイヌ語の一覧掲載と深刻度を逆転','誤：八丈語・奄美語を除外','正：掲載8言語の一覧に対応','誤：国内の危機と文化庁の取組を全否定']),
('Q_2_012',1,'S238',
'国立国語研究所「外来語」委員会の2006年「外来語」言い換え提案 第1回～第4回総集編と「利用の手引き」に合う考え方を一つ選べ。',
[
'受け手や場面に応じて、言い換えや説明を工夫する。「インフォームドコンセント」には「納得診療」「説明と同意」が示され、必要に応じて意味の説明も付ける。',
'一つの外来語には必ず一つの言い換えだけを対応させ、場面や文脈が変わっても同じ語へ機械的に置き換える。',
'提案された言い換え語は、もとの外国語にある全ての意味と用法を、そのまま完全に反映するものとして用いる。',
'専門的な概念を正確に伝えるためであっても、外来語を使いながら説明を付ける方法は一切認めない。'],
[
'利用の手引きは、言い換えと説明のどちらがよいかを個別に考え、相手や場面にも配慮するよう求めています。同語の提案ページは二つの言い換え語と「十分な説明を受けた上での同意」という意味説明を示し、説明を付ける必要にも触れています。',
'利用の手引き（4）は、一つの言い換え語で全ての場合に対応できるわけではなく、場面や文脈によって適切に使い分けることを求めています。機械的に一語へ固定する説明は合いません。',
'利用の手引き（3）は、日本語の中で使われている外来語に対する提案であり、原語の意味・用法をそのまま反映するわけではないと注意しています。原語の全ての意味・用法へ無条件に適用する説明は合いません。',
'利用の手引き（5）は、言い換えによって概念が曖昧になる場合も考えられるとし、外来語を使いつつ正確な説明を付け加える方法も示しています。外来語と説明の併用を全面禁止する説明とは異なります。'],
'S238提案主体の総集編概要・利用の手引き全文・インフォームドコンセント項目全文を取得照合。納得診療のみの一律置換ではなく、説明と同意・文脈別選択・説明付与を確認。旧やさしい日本語、公用文・法令のルビ・仮名遣い等の別制度の補助説明は本問の採用範囲から外し、取得した2006年提案の使い方へ限定。現在の理解度や医療の法的要件は承認しない。',
['正：受け手・場面・意味説明を考慮する','誤：文脈による使い分けを否定','誤：日本語の外来語と原語の全意味を同一視','誤：外来語と説明の併用を禁止'])]
extra=[]
for k,key,sid,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第175バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='資料の主体と時点を明示し、全4肢を独立照合。現行の話者数・理解度や別制度の承認を含めない。',explanation_review='全肢全解説を取得した機関本文へ照合。掲載と法的指定、2006年提案と現在の理解度、言い換えと機械的な一律置換を区別。',unresolved='',multiple_correct_risk=f'なし：{key}のみ対象資料の説明に一致',no_correct_risk=f'なし：{key}に対応する本文取得済み')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch176.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [
 ('S238','ninjal176.html','https://www2.ninjal.ac.jp/gairaigo/Teian1_4/index.html','2006年総集編概要、提案主体・日付・目的。'),
 ('S238','guide176.html','https://www2.ninjal.ac.jp/gairaigo/Teian1_4/tebiki.html','利用の手引き全節。背景、理解度の当時の目安、世代差、原語との区別、文脈別選択、専門概念の説明、概念普及。理解度数値を現在値とは扱わない。'),
 ('S238','informed176.html','https://www2.ninjal.ac.jp/gairaigo/Teian1_4/Words/informed_consent.gen.html','提案項目本文全体。納得診療／説明と同意、意味説明、手引き、2006-03-13。現行医療の法的要件・1980年代語史の独立検証ではない。'),
 ('S239','endangered176.html','https://www.bunka.go.jp/seisaku/kokugo_nihongo/kokugo_shisaku/kikigengo/','文化庁本文・2009年発表資料掲載8言語と危機度一覧、言語／方言注記、事業一覧。UNESCO原Atlas本文・最新話者数・全方言の危機度を独立検証したとはしない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch176_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
