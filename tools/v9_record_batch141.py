"""Record source-version-bounded legal case after changed-page inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa141';target='Q_2_008'
def oldfile(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(oldfile('ledger.csv'));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k==target else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':346,'修正必要':15,'要追加確認':139}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==99
cs=json.loads((p/'changes_batch141.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={target}
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('| 確認済み | 345問 |','| 確認済み | 346問 |').replace('修正必要16問','修正必要15問').replace('| 修正必要 | 16問 |','| 修正必要 | 15問 |').replace('343問2911箇所','343問2920箇所');f.write_text(s)
report='''

## 第141バッチ（2026-10-18）

Q_2_008を9箇所改訂。公用語・国家語という学習領域と正答1を維持し、複数国を一括する未照合の一般化を、シンガポール憲法第153A条の具体的事例へ変更。政府選挙局公開の憲法PDF全203頁を取得し、表紙の版表示（2020 Revised Edition、2023-04-24からの施行版）と印刷172頁の第153A条第1項・第2項・ただし書(a)(b)全文を、抽出本文および頁画像で直接照合した。全203頁精読済みという意味ではない。

公用語4言語と国家語マレー語の指定は同一ではないが、マレー語は両方に含まれることを明示。他言語の使用・教授・学習の禁止という誤答はただし書(a)と逆である。全4肢・全4解説の根拠範囲を取得条文に限定。日本法や国家語の普遍的定義の未照合補助主張は残さない。

現行SSOページの直接取得は403で失敗。検索結果に表示された現行条文のみでは承認せず、設問に取得した2023年版の時点を明示。2026年現行法全体を照合済みとは扱わない。一次資料の版情報・原バイトSHA256・読了範囲・取得制約はevidence/batch141_sources.jsonに記録し、原文PDFは転載しない。

確認済み346・修正必要15・要追加確認139、残154問。累積343問2920箇所、500問維持。台帳の設問等の原文はv8スナップショットで、改訂はchangesと作業稿を参照。v8不変・500問構造・キー・タグ・早見表・リンク・影響外本文の不変検査を通過。公開判定回帰8条件・置換回帰4条件を通過。機械警告99件で増減なし。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画し、全9変更文字列を検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。設問・選択肢の頁またぎは残存し、最終組版で全頁確認が必要。全頁最終目視および残154問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第141バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第141バッチ S204（2026-10-18）

- S204 シンガポール選挙局公開 [Constitution of the Republic of Singapore PDF](https://www.eld.gov.sg/Resources/Constitution%20of%20the%20Republic%20of%20Singapore.pdf)。表紙は2020 Revised Edition、欄外はInformal Consolidation – version in force from 24/4/2023。全203頁のPDFを取得し、表紙と印刷172頁の第153A条全項・ただし書(a)(b)の本文を精読・頁画像で照合。公用語と国家語の指定、他言語の使用・教授・学習の禁止・妨害を否定する条文をQ_2_008の設問・4肢・4解説へ照合。設問の対象は2023年版と明示。現行SSOは403で未取得、検索表示を承認根拠に含めない。全203頁精読・2026年法全体照合ではない。

取得原バイトSHA256・版・読了範囲・制約はevidence/batch141_sources.json。原文非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=141,base_commit='07211a1ca931f44d6cc69e3dc404bc9824efbee7',fully_rejudged=[target],edits=9,independent_answers={target:1},sources=['S204'],status_counts=m['status_counts'],remaining=154,machine_warnings=99,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_pdf_page_sha256={'173':sha(root/'singapore141-173.png')},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch141_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('346 confirmed / 154 remaining',pages)
