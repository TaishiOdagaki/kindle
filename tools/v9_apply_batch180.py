"""One-time source-bounded history and method revision; never rerun."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3561
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_1_006',4,'S244','修正必要',
'国史館台湾文献館が2013年に公開した解説「臺灣總督府首任學務部長伊澤修二來臺推展日語教育」の本文に照らし、1895年の伊沢修二と芝山巌学堂について合うものを一つ選べ。',
['李春生の提案を受け、現地を視察せずに劍潭寺をそのまま学堂の場所に決めた。',
'学務部の活動は日本語教育に限られ、台湾語の研究や会話教科書の編集は含まれなかった。',
'学堂の学生は日本から来た留学生だけであり、地元の子弟は教育の対象にしなかった。',
'芝山巌の惠濟宮に学堂を設け、地元の士林の子弟に日本語と西洋文明の基礎科目を教えた。'],
['本文では、李春生が劍潭寺の利用を提案した後、伊沢が現地を調べ、芝山巌山頂の惠濟宮を選んだと説明しています。提案された場所と最終的な選定を混同しています。',
'本文は、学務部が芝山巌へ移った後の活動として、台湾語の研究、会話教科書の編集、台湾人への日本語教育を挙げています。日本語教育だけに限る説明は合いません。',
'本文は、士林の子弟を募集して日本語と西洋文明の基礎科目を教えたと説明し、地元の学生の名も挙げています。日本からの留学生だけという説明は合いません。',
'本文の学堂の場所、対象となった地元の子弟、教授内容の説明に対応します。この問題は同館の公開解説を根拠としており、当時の教育政策全体の評価を問うものではありません。'],
'S244国史館台湾文献館2013-09-30電子報114期の解説記事本文全体を原HTMLから取得・精読。提案と現地視察後の選定、士林の子弟、日本語と西洋文明基礎科目、台湾語研究・会話教材編集を全肢全解説へ照合。旧問の松本亀次郎・満州・教授法分類・最初の組織的教育等の未照合主張は承認せず撤回し、同じ台湾日本語教育史領域で本文に範囲を指定して差替え。2013年の公的史料機関の解説であり、引用された1895年の史料全冊や任命画像の独立取得とはしない。',
['誤：提案と視察後の選定を混同','誤：台湾語研究と会話教材編集を排除','誤：地元子弟を対象から排除','正：場所・対象・教授内容が本文に一致']),
('Q_O_001',1,'S242','要追加確認',
'ケース1の実物や絵カードによる意味提示を教授法の原則と比較する。Larsen-FreemanとAnderson（2011）『Techniques and Principles in Language Teaching』第3版で、母語への翻訳を介さず、目標言語と意味を直接結び付けると説明される方法を一つ選べ。',
['直接法（Direct Method）','コミュニティ・ランゲージ・ラーニング（Community Language Learning）','デサジェストペディア（Desuggestopedia）','文法訳読法（Grammar-Translation Method）'],
['同書の直接法の原則3は、実物、絵、身振りで新出語句の意味を示し、母語へ翻訳しないと説明しています。ケースの意味提示を、この原則と比較することができます。',
'同書のCLLの原則3では、初級の学習者が母語で話し、教師が目標言語への訳をまとまりごとに与える過程が説明されています。教師の支援的な役割だけでなく、この母語と翻訳の利用も区別の根拠です。',
'同書のデサジェストペディアの原則3では、目標言語の長い対話文の隣に母語訳を付けた教材を使うと説明されています。音楽や安心感だけで分類せず、この翻訳の利用を設問の原則と区別します。',
'同書の文法訳読法の原則3は、二言語間の翻訳と、規則・例を与えて別の例へ適用する文法学習を説明しています。母語への翻訳を介さないという設問の原則には対応しません。'],
'S242著者2名の2011年第3版原著書を再取得し原バイト照合。直接法PDF52～53頁、文法訳読法39～40頁、デサジェストペディア110頁、CLL127～128頁の本文を精読、39・52・110・127頁画像照合。ケース1本文も照合。実物利用だけから教授法全体を断定せず、同書の意味提示と母語利用の原則比較へ限定。Lozanov・Curran等の引用先原典、脳機能・促進効果・全教授法史は承認しない。電子再組版PDF頁で印刷版頁を推定しない。',
['正：母語への翻訳を介さない意味提示','誤：同書の初級過程では母語と翻訳を利用','誤：同書の教材には母語訳を併記','誤：同書では二言語間の翻訳を扱う'])]
extra=[]
for k,key,sid,status,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']==status and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   assert html.unescape(old)!=new
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第179バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='取得した著作・公的史料機関の解説本文に範囲を指定して全4肢を独立照合。旧未照合主張は撤回し承認しない。',explanation_review='全4解説を取得本文へ照合。引用先原典・効果・政策全体への一般化はしない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定本文に一致',no_correct_risk=f'なし：{key}の根拠本文取得済み')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch180.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2]
entries=[]
for sid,name,url,title,scope in [
 ('S242','methods180.pdf','https://elearning.usm.md/pluginfile.php/190241/mod_resource/content/2/Larsen-freeman%203rd%20ed_techniques-in-language-teaching.pdf','Larsen-Freeman and Anderson 2011 Techniques and Principles in Language Teaching third edition','直接法PDF52～53、文法訳読法39～40、デサジェストペディア110、CLL127～128頁。39・52・110・127頁画像。全書・引用先原典の精読ではない。'),
 ('S244','taiwan180.html','https://www.th.gov.tw/Epaper_Content/236/7518/','國史館臺灣文獻館 2013-09-30 電子報114 臺灣總督府首任學務部長伊澤修二來臺推展日語教育','HTML template内の記事本文全体。2013年の公的史料機関の解説。引用された1895年原史料全冊・任命画像は未取得。')]:
 raw=(root/name).read_bytes();entries.append(dict(source_id=sid,url=url,title=title,checked='2026-10-19',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope=scope,full_source_redistributed=False))
assert entries[0]['sha256']==json.loads((p/'evidence/batch179_sources.json').read_text())[0]['sha256']
(p/'evidence/batch180_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch180_source_attempts.json').write_text(json.dumps([dict(url=entries[1]['url'],result='Web openはsys-rootのみで本文抽出なし。別途urllibで92184バイト原HTML取得、template内の記事本文全体を精読。検索抜粋・JSON-LDのみで承認していない。')],ensure_ascii=False,indent=2)+'\n')
