"""One-time source-scoped public-writing and council audit."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3516
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_1_007',4,'S241',
'文化審議会が2022年1月7日に建議した「公用文作成の考え方」の基本的な考え方と用語の扱いについて、説明に合うものを一つ選べ。',
[
'外来語は日本語に十分定着したものも含めて使用を全面的に禁止し、説明を付けて使うことも認めない。',
'文書の目的や読み手が異なっても書き方を変えず、一般向けの広報にも専門知識を前提とする表現だけを用いる。',
'分かりやすさを優先する場合には、基となる情報の内容や意味を変更してもよく、正確さとのバランスは考えなくてよい。',
'文書の目的や読み手に応じて書き方を工夫し、外来語も語の性質や使う場面に応じて、そのまま使う・言い換える・説明を付けるなどの方法を選ぶ。'],
[
'Ⅱ「用語の使い方」3は、日本語に十分定着している外来語はそのまま使うとし、日常の漢語や和語への言い換え、分かりやすい言い換えが困難な場合の説明付与も示しています。全面禁止という説明は合いません。',
'「基本的な考え方」1は、文書の目的や種類、想定される読み手に応じた工夫を認めています。広く一般に向けた解説・広報等では、特別な知識を持たない人の読みやすさを優先するとしています。',
'「基本的な考え方」2は、基となる情報の内容や意味を損なわないことと、分かりやすさと正確さのバランスを示しています。分かりやすくするためなら意味を変えてよいという方針ではありません。',
'「基本的な考え方」1とⅡ「用語の使い方」3に対応します。外来語を一律に排除するのではなく、定着の程度や使う場面を考え、必要な言い換えや説明を工夫します。'],
'S241文化審議会2022年建議原PDF取得。表紙、PDF3～4／本文1～2頁の前書き・基本的な考え方・分類例、PDF7／本文5頁の用語1～4を精読、7頁画像照合。全肢全解説を対応。旧稿の情報機器普及・手書き不要から漢字追加を説明する推測、国語分科会の日本語教育所管の現在形を本問から撤回。建議の説明であり、全別法令・全63頁の精読や言い換えの介入効果の承認ではない。',
['誤：定着語使用と説明付与を全面禁止','誤：目的・読み手別の工夫を否定','誤：情報の意味保持と正確さを否定','正：読み手への配慮と外来語の条件別対応']),
('Q_1_029',2,'S240',
'文化庁が公開する「文化審議会について」の設置経緯と国語分科会の説明に合うものを一つ選べ。',
[
'文化審議会は法務省に設置され、国語分科会の主な所掌事務は在留資格の審査基準だけを調査審議することである。',
'国語審議会など四つの審議会等の機能を整理・統合し、2001年1月6日付けで文部科学省に文化審議会が設置された。国語分科会は国語の改善と普及に関する事項を調査審議する。',
'文化審議会は国の省庁とは関係のない任意の民間団体であり、その中に国語分科会が置かれている。',
'国語分科会の主な所掌事務は文化財の保存と活用だけであり、国語の改善や普及は調査審議の対象に含まれない。'],
[
'文化庁の「設置の経緯」は文部科学省への設置を示し、「構成」の表は国語分科会の事務を国語の改善及びその普及に関する事項の調査審議としています。法務省設置・在留資格審査だけという説明とは異なります。',
'「設置の経緯」と「構成」の国語分科会の欄に対応します。統合前の四つは、国語審議会、著作権審議会、文化財保護審議会、文化功労者選考審査会です。',
'同ページは、中央省庁等の改革の中で文部科学省に設置されたことと、文化審議会に国語分科会等が置かれる構成を説明しています。省庁と無関係な任意の民間団体という説明は合いません。',
'「構成」の表では、文化財の保存及び活用に関する重要事項の調査審議は文化財分科会の主な所掌事務です。国語分科会の国語の改善及び普及に関する事務と取り違えています。'],
'S240文化庁公式紹介の設置経緯・主な所掌事務・構成表・答申一覧を原HTMLで取得精読。全肢全解説を設置経緯と構成表へ対応。2001年設置の文化審議会全体と国語分科会を区別。旧稿の当用漢字表を過度の制限主義と評価する説明、ローマ字化の全戦後史、日本語教育所管の現在形を撤回。法令原文全改正や日本語教育行政の現在の全所管を承認したとはしない。',
['誤：設置先と事務を取り違える','正：四機能の整理統合・設置日・国語分科会事務','誤：文部科学省への設置を否定','誤：文化財分科会の事務と混同'])]
extra=[]
for k,key,sid,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第177バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='発行主体・資料名・必要な時点を明示。各4肢を独立照合。',explanation_review='全4解説を取得本文へ照合。別制度・過度な歴史評価・根拠未確認の原因説明を撤回。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定本文に一致',no_correct_risk=f'なし：{key}に対応する本文取得済み')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch178.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [
 ('S240','council178.html','https://www.bunka.go.jp/seisaku/bunkashingikai/about/','設置の経緯・主な所掌事務・構成表・主な答申一覧の本文全体。リンク先の組織図・名簿や法令原文全改正の確認ではない。'),
 ('S241','public178.pdf','https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf','63頁原PDF。表紙、PDF3～4頁／本文1～2頁の前書き・基本的な考え方・公用文分類例、PDF7頁／本文5頁の用語1～4を精読、7頁画像照合。PDF8～10頁本文も参照。全63頁精読ではない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch178_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch178_source_attempts.json').write_text(json.dumps([dict(url='https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93650001_01.pdf',result='HTTP404。検索先URLでなく公式建議ページの実リンク93651301_01.pdfを取得して照合。検索抜粋の承認はしない。')],ensure_ascii=False,indent=2)+'\n')
