"""Publishable checkpoint evidence, not final release approval."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa169';k='Q_4_088'
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[key].replace('\r\n','\n') if key==k else raw for key,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':398,'修正必要':2,'要追加確認':100} and not m['release_ready']
cs=json.loads((p/'changes_batch169.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {key for key in d if d[key]!=d0[key]}=={k}
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_4_088']['ans']=='2'
for c in cs:
 got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_4_088']['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches169.json').read_text());assert len(matches)==9 and all(matches.values())
pages=sorted({v for ns in matches.values() for v in ns});machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert machine['issues']==pre['issues'] and len(machine['issues'])==121
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第169バッチ 2026-10-18

Q_4_088をS226北海道大学の見延庄士郎「レポート・卒論の書き方初級編」（ページ改訂表記2003-01-25）の2.2節・6.1節の本文へ照合して9件改訂。独立正答2、キー変更なし。確認済み398・修正必要2・要追加確認100、残102問。累積393問3372件、500問維持。

旧稿の受動態・無生主語による客観性や中立性向上の未裏付け一般化、口頭発表まで含む文末形式の一律指定を撤回。同じ談話構成領域の段落構成と推敲へ絞り、段落の早い位置で示す事項と本文の対応、段落間の論理の点検を問う。案内の形式だけで内容の乏しさを補い説得力が保証されるとはしない。トピック・センテンスを必ず第一文・要約文に限定することもしていない。全4肢・全4解説の対応を取得本文へ照合済み。教材中の教育史一般化、授業効果の実証、引用書籍原著の検証までは承認していない。

関西大学旧PDFは検索側の展開後、原バイト取得と再openが404。2025新版はLMSログインのため未取得。検索抜粋・旧キャッシュで確認済みとせず、取得できた別大学教材に出題範囲を限定した。取得試行はevidence/batch169_source_attempts.json。

v8不変、500問、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件・ブロック文脈回帰が通過。機械警告121件で前回から増減なし。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifで{pagecount}頁を新規描画。新規9文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。日本語・中国語例字・IPAのフォント収録検査も通過。改訂箇所に欠字・重なり・切れを認めず。全頁最終QAと未照合102問は未了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第169バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第169バッチ S226 大学教材 2026-10-18\n\n[S226 北海道大学 見延庄士郎 レポート・卒論の書き方初級編](https://geodynamics.sci.hokudai.ac.jp/poc/minobe/class/how2write_1.htm)のHTML原バイトを取得。2.2段落全文と注3、6.1チェックのポイント全文、2.1.1段落構成のスペース条件を確認。Q_4_088の全4肢・全4解説へ対応。旧メタ言語表現の効果、受動態頻度・客観性、口頭発表文体、教育史一般化は承認対象外。原バイトSHA256と範囲はevidence/batch169_sources.json、原文全体非転載。関西大学旧PDF404等はevidence/batch169_source_attempts.json。\n''')
f=p/'README.md';f.write_text(f.read_text().replace('397問','398問').replace('101問','100問').replace('392問3363箇所','393問3372箇所').replace('392問を部分修正','393問を部分修正'))
e=dict(batch=169,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=[k],edits=9,independent_answers={k:2},sources=['S226'],status_counts=m['status_counts'],remaining=102,machine_warnings=121,new_warnings=warnings,regressions='readiness8; replacement4; block context byte-identical',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch169_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
