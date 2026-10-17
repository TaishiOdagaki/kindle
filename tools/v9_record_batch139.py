"""Record listening case audit with precise evidence and QA boundaries."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa139';targets={'Q_MO_001','Q_MO_005'}
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':343,'修正必要':18,'要追加確認':139}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch139.json').read_text());assert len(cs)==12
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==12 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('341問','343問').replace('141問','139問').replace('339問2883箇所','341問2895箇所').replace('339問を部分修正','341問を部分修正');f.write_text(s)
report='''

## 第139バッチ（2026-10-17）

Q_MO_001・Q_MO_005を12箇所改訂し、両問の独立正答4を確定。再取得・精読済みS99の本文から、語彙知識の不足と既知語を連続した音声中で認識できない場合の区別、背景知識と音声解読の併用を照合。共通ケース本文全2段落と全4肢・全4解説を独立に再判定した。誤答1–3の本文は維持し、それぞれの断定や設問条件との不一致を説明した。

Q_MO_001はケース本文だけからの原因の断定を避け、実態を確認する観点を問う形へ改訂。ふりがなのない文字提示を聴解の確定原因とする説明や、オンライン形式より教材が主因であるとの未検証の比較は撤回。Q_MO_005は聴解指導の継続という条件を明示し、学習者の実態と両処理の支援の検討を問う。速度を遅くすれば常に改善するとの処方や、一つの支援による理解の保証にはしない。いずれも特定ケースへの教育的な適用判断であり、因果効果を測定した研究結果と混同しない。

確認済み343・修正必要18・要追加確認139、残157問。累積341問2895箇所。500問維持、v8不変、正答番号不変、構造・タグ・早見表・リンク・影響外本文の不変を再検査。公開判定回帰8条件、置換回帰4条件を通過。警告98件は前回と完全一致。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全12変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。documentsと既存校正手順に基づく変更範囲QAであり、全頁最終目視は未完了。残157問の学術照合も未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第139バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第139バッチ S99継続照合（2026-10-17）

第137バッチで再取得したCatherine Morleyの[Listening Top-down and bottom-up](https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/listening-top-down-and-bottom)の本文「Bottom-up listening activities」冒頭、背景知識による予測と両処理の併用の節を、Q_MO_001・Q_MO_005へ照合。語を知らない場合と、知っていても速い連続音声中で認識できない場合を区別。ケースへの適用は学習者の実態を確認する観点と支援の検討であり、教材・オンライン形式の原因の確定や成功の保証ではない。原バイトの取得記録はevidence/batch137_sources.jsonを継承。新たに原著を取得したとの扱いにはしない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=139,base_commit='9ec5ed1cbf9075aef099b9450329f84d319e3472',fully_rejudged=sorted(targets),edits=12,independent_answers={k:4 for k in targets},sources=['S99'],source_acquisition='evidence/batch137_sources.json',status_counts=m['status_counts'],remaining=157,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch139_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('343 confirmed / 157 remaining',pages)
