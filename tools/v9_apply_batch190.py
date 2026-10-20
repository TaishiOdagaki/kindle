"""One-time revision of institutional and textbook history."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3867
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_1_025',2,['S261'],'JASSOが公表する国際学友会の沿革に合う記述を一つ選べ。創立、日本語教室の開設、学校の設置許可を区別する。',
['1935年12月の創立とは、財団法人としての設立許可と日本語学校の各種学校としての許可が同時に行われたことをいう。','1935年12月に外務省の外郭団体として創立され、1936年2月には会館の開設と学生の受入れ、日本語教室の開設が記されている。','1936年2月の会館は、日本で学ぶ学生を受け入れる施設ではなく、学生を海外へ送り出す業務だけを行い、日本語教室を持たなかった。','1943年1月の項目には、日本語学校の設置許可ではなく、国際学友会の団体としての最初の創立が記されている。'],
['沿革では創立は1935年12月、財団法人の許可は1940年12月、日本語学校の各種学校としての許可は1943年1月です。同時の出来事ではありません。','沿革の1935年12月と1936年2月の項目に対応します。団体の創立と教室の開設を区別して読みます。','1936年2月の項目には、会館開設、学生受入れ開始、日本語教室開設が記されています。受入れと教室を否定する説明は合いません。','1943年1月は国際学友会日本語学校の設置と各種学校としての許可の項目です。団体の創立は別の1935年12月に記されています。'],
['誤：創立と法人許可と学校許可を同時とする','正：1935年創立と1936年教室開設を区別','誤：学生受入れと教室開設を否定','誤：学校設置許可を団体創立と取り違え']),
('Q_1_028',3,['S262'],'長沼スクールが紹介する長沼直兄と『標準日本語讀本』の教材史に合う説明を一つ選べ。',
['長沼は大人の外国人にも小学生用の国語教科書をそのまま使うのが適切と考え、自作教材を作らなかった。','長沼は授業での試用や改良を行わず、教材を固定して用い続けたと説明されている。','長沼は構文・語彙・漢字を総合し、オーラル・メソッドを取り入れた自作教材を試用・改良し、読本作成につなげた。','1931年に初めて出た『標準日本語讀本』は、最初から全八巻の一般向け市販版として一度に刊行された。'],
['学校の解説では、小学生用国語教科書を大人の外国語学習用として不適当と考えたことが、自作教材を使う説明につながっています。この肢は逆です。','解説には、授業で試用と改良を繰り返したとあります。改良をせず固定したという説明は合いません。','解説の自作教材と読本成立の記述に対応します。ここでは学校が紹介する教材史を問い、特定の教授法の効果を実証したという判断はしていません。','解説は1931年の巻一の自費出版と、その後約3年の全七巻刊行を説明しています。全八巻の改訂版の一般向け出版は1950年として区別しています。'],
['誤：自作教材成立の契機を逆転','誤：授業での試用・改良を否定','正：自作教材の構成と改良から読本成立','誤：1931年初刊と戦後の一般向け八巻を混同'])]
reasons={
'Q_1_025':'S261 JASSO国際学友会の沿革の表本文全体を取得・精読。1935年12月の団体創立、1936年2月の会館・受入れ・日本語教室、1940年12月の財団法人許可、1943年1月の日本語学校各種学校許可を全肢全解説へ照合。旧稿の松本・宏文・東亜・周恩来・魯迅・日仏会館の個別史を未取得原典のまま承認せず、同じ戦前の日本語教育機関史で差替え。学校史の全一次史料を取得したとはしない。',
'Q_1_028':'S262 長沼スクール公式の標準日本語讀本解説の全本文を取得・精読。自作教材の構文・語彙・漢字、オーラル・メソッド取入れ、授業試用と改良、1931年巻一と全七巻・戦後一般向け全八巻の区別を全肢全解説へ照合。学校が紹介する教材史として限定し、原教材全巻の現物精読や教育効果の実証とは区別。旧稿のグアン・山口の教授法、直接法教材の決定版・国内外への影響という未照合評価は撤回。'}
extra=[]
for k,key,sources,stem,opts,exps,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reasons[k],sources=sources,applied=True,before_version='第189バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reasons[k],option_verdicts=verdicts,candidate_answers=[],stem_review='公表者を示し取得した沿革・教材史の本文に限定。',explanation_review='時点・設置段階・巻数・版の区別を全肢全解説へ照合。全一次史料・原教材全巻・教育効果を承認しない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ当該本文に整合',no_correct_risk=f'なし：{key}の根拠本文取得')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch190.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
