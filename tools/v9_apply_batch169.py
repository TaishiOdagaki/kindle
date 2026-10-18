"""Evidence-bound paragraph guidance; one-time append after batch168."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3363
d=json.loads((p/'decisions.json').read_text());k='Q_4_088';ak='A_4_088'
assert d[k]['status']=='要追加確認'
_,q,a=qa.audit(str(b.DST));assert a[ak]['ans']=='2'
stem='アカデミック・ジャパニーズの段落構成を指導する。見延庄士郎「レポート・卒論の書き方初級編」の段落構成と推敲の説明に合うものを一つ選べ。'
opts=[
'各段落には、中心となる事項と関係のない話題も、順序を考えずに混在させる。',
'段落の早い位置で扱う事項を示し、それに沿って内容をまとめ、段落間の論理の流れも点検する。',
'推敲では個々の文の表現だけを直し、各段落が何を述べるかや、段落間のつながりは点検しない。',
'トピック・センテンスを置けば、段落の内容が乏しくても文章の説得力は保証される。']
exps=[
'教材の2.2節では、トピック・センテンスで示す事項の範囲に沿って段落を構成し、範囲から外れる内容は別の段落にするか削除するよう説明しています。無関係な話題を無秩序に混ぜる指導とは異なります。',
'2.2節では、その段落で何を述べるかをなるべく早く示す文をトピック・センテンスと呼び、その範囲で内容をまとめるよう説明しています。6.1節では、各トピック・センテンスが全体として論理の流れを作るかも点検します。位置だけを整えるのではなく、示す事項と本文の対応も確かめる指導です。',
'6.1節では、段落構成を大局的に点検したうえで、文と文の関係や各文の構成も見直します。個々の表現だけを直し、段落の役割やつながりを点検対象から外す方針ではありません。',
'6.1節は、トピック・センテンスが整っていても説得力が乏しい場合には、書く内容が乏しい可能性を指摘しています。案内する文の形式だけで、内容の充実や説得力が保証されるわけではありません。']
reason='S226北海道大学の見延庄士郎による大学教材のHTML原バイトを取得し、2.2節（注3を含む）と6.1節を本文照合。旧稿の受動態・無生主語が客観性や中立性を高めるという未裏付け一般化、学術プレゼンも含めた文末形式の一律指定を撤回。同じ談話構造領域の段落構成と推敲に限定して全4肢・全4解説を改訂し、形式だけで説得力が保証されない条件も明示。旧メタ言語表現の効果や頻度を独立検証したとは扱わない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
  extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S226'],applied=True,before_version='第168バッチ後',block_context=ak if field=='explanations' else k,**kw))
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S226'],reason=reason,option_verdicts=['誤：段落の中心事項に関係しない内容を混在','正：早い位置で事項を示し本文・段落間の対応を点検','誤：大局的な段落構成の点検を除外','誤：形式だけで内容不足を補い説得力を保証'],candidate_answers=[],stem_review='出典を明示し、学術的文章の段落構成・推敲という同領域に限定。全学術分野で例外のない構造規則とはしない。',explanation_review='2.2節と6.1節に全4解説を照合。トピック・センテンスは早い位置とし、必ず第一文や必ず要約文とはしない。受動態頻度・客観性保証・口頭発表文体の一般化を撤回。',unresolved='',multiple_correct_risk='なし：2のみ教材の範囲と点検方針に一致',no_correct_risk='なし：2が取得本文に対応')
for n,obj in [('changes.json',cs+extra),('changes_batch169.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
f=Path(__file__).resolve().parents[2]/'hokudai169.html';raw=f.read_bytes()
(p/'evidence/batch169_sources.json').write_text(json.dumps([dict(source_id='S226',url='https://geodynamics.sci.hokudai.ac.jp/poc/minobe/class/how2write_1.htm',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-18',author='見延庄士郎',page_modified='2003-01-25（ページ表記）',read_scope='2.2段落全文・注3、6.1チェックのポイント全文。2.1.1のスペースによる段落構成の条件も参照。日本の教育史一般化や引用書籍本文は検証対象外。',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch169_source_attempts.json').write_text(json.dumps([dict(url='https://www.kansai-u.ac.jp/ctl/labo/useful/pdf/report/20170426_hatten.pdf',result='検索・初回web展開では旧PDFテキストが得られたが、直接原バイト取得と再openは404。検索抜粋を承認に使用せず。2025新版はLMSログイン要求のため未取得。',used_for_approval=False)],ensure_ascii=False,indent=2)+'\n')
