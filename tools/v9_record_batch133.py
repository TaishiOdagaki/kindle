"""Record source-bounded drill revision after changed-page image inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');r=Path(__file__).resolve().parents[2]/'qa133'
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_4_033' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':335,'修正必要':24,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch133.json').read_text());assert len(cs)==9
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}=={'Q_4_033'}
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text()
for a,b in [('334問','335問'),('25問','24問'),('335問2824箇所','335問2833箇所')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第133バッチ（2026-10-17）

Q_4_033の設問・全4肢・全4解説を9箇所改訂し、独立正答2を確定。Cambridge TKT用語集の印刷14/PDF15頁のDrill項目全体を再取得して本文・画像照合。変換・置換・斉唱反復・個別反復の定義に基づく四肢へ改訂し、語句の扱いを判断対象として明示した。学習者一人が答えるだけなら個別という軸も当てはまるため、誤答には「教師の発話を変えず、そのまま反復する」という定義を含め、語句を代入する正答と区別した。日本語の例は独自のもの。未照合の結合・応答の定義や単一／複数スロット分類を掲載文から除き、同じドリル分類の学習領域を維持。第132バッチの資料不足記録は保存し、S195の列挙だけによる承認へ遡及変更しない。

確認済み335・修正必要24・要追加確認141、残165問。累積335問2833箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。500問の構造・キー・タグ・表・リンク、影響外本文、v8不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。警告98件は前バッチと完全一致。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全9変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。全頁最終目視と残165問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第133バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第133バッチ S183追加照合（2026-10-17）

[Cambridge TKT Glossary](https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf)を再取得。印刷14/PDF15頁のDrill項目全体を本文・画像精読。変換・置換・斉唱反復・個別反復の定義をQ_4_033の全4肢・全4解説に使用。全用語集、ドリルの学習効果、結合・応答の定義やスロット分類を承認しない。原バイトSHA256と範囲はevidence/batch133_sources.json。原資料の例文の転載・翻訳はせず、独自の会話で照合した。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=133,base_commit='17913d64c4873954cc52190d92a14e2d55b82136',fully_rejudged=['Q_4_033'],edits=9,independent_answers={'Q_4_033':2},sources=['S183'],status_counts=m['status_counts'],remaining=165,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch133_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('335 confirmed / 165 remaining',pages)
