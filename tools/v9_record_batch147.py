"""Record batch147 after human inspection of every changed page."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa147';target='Q_4_107'
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':354,'修正必要':10,'要追加確認':136}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==103 and machine['issues']==prior
cs=json.loads((p/'changes_batch147.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={target}
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('353問','354問').replace('修正必要11問','修正必要10問').replace('| 修正必要 | 11問 |','| 修正必要 | 10問 |').replace('350問2981箇所','350問2990箇所');f.write_text(s)
report='''

## 第147バッチ（2026-10-18）

Q_4_107を9箇所改訂し、独立正答4を確定。S210 Sorokowskaら（2017）Preferred Interpersonal Distancesの原論文Accepted Version全36頁PDFをWarwick大学の公開機関リポジトリから取得。本文番号9–18頁（PDF14–23頁）の方法・結果・考察・限界を全文精読し、方法9頁・結果11頁・限界17頁は画像でも確認。全36頁精読、補足資料やHall原著の取得ではない。

旧問題の沈黙・ジェスチャーの未照合な補助主張と、日本・北欧・ラテン系を一括りにする文化分類を撤回。非言語コミュニケーションの対人距離という同じ学習領域で、研究方法と国間の平均の違いへ対象を限定した。全4肢・4解説を照合し、図を用いた質問紙による希望の測定と実際の行動、三つの相手区分、国間の平均差と個人への決め付けを区別した。特定国の順位・温度や性差の因果的説明は新稿に使用していない。

機械警告は103件で増減なし。確認済み354・修正必要10・要追加確認136、残146問。累積350問2990箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。v8不変、500問の構造・キー・タグ・早見表・リンク・影響外本文、公開判定回帰8条件・置換回帰4条件を検査。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、9変更文字列を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。ただし設問の選択肢4が95頁へまたがる状態は残り、最終組版の確認・改善対象。最終全頁QAと残146問の学術照合は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第147バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第147バッチ S210（2026-10-18）

- Agnieszka Sorokowska et al. (2017), Preferred Interpersonal Distances: A Global Comparison, Journal of Cross-Cultural Psychology 48(4), 577–592, DOI 10.1177/0022022117698039。Warwick公開機関リポジトリ https://wrap.warwick.ac.uk/id/eprint/100226/ のAccepted Version https://wrap.warwick.ac.uk/100226/7/WRAP-preferred-interpersonal-distances-global-comparison-Realo-2017.pdf 全36頁取得。本文番号9–18頁（PDF14–23頁）の方法・結果・考察・限界を全文精読し、方法9頁・結果11頁・限界17頁を画像照合。Q_4_107の方法・三つの相手区分・平均の国間差・一般化の限界に使用。全36頁精読や補足資料・Hall原著の取得ではない。希望を実際の行動と同一視せず、国別結果から個人を決め付けない。原バイトSHA256・読了範囲はevidence/batch147_sources.json。本文・頁画像は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=147,base_remote_commit='80186ca2b199f9ed43f0021da22a258551d31f08',after_local_batch146_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),fully_rejudged=[target],edits=9,independent_answers={target:4},sources=['S210'],status_counts=m['status_counts'],remaining=146,machine_warnings=103,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_page_sha256={str(n):sha(root/f'distances147-{n}.png') for n in [14,16,22]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch147_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('354 confirmed / 146 remaining',pages)
