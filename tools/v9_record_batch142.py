"""Record inference original-body audit after visual inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa142';targets={'Q_3_005','Q_3_006'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':348,'修正必要':14,'要追加確認':138}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==99
cs=json.loads((p/'changes_batch142.json').read_text());assert len(cs)==18
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('| 確認済み | 346問 |','| 確認済み | 348問 |').replace('修正必要15問','修正必要14問').replace('| 修正必要 | 15問 |','| 修正必要 | 14問 |').replace('要追加確認139問','要追加確認138問').replace('| 要追加確認 | 139問','| 要追加確認 | 138問').replace('343問2920箇所','345問2938箇所').replace('343問を部分修正','345問を部分修正');f.write_text(s)
report='''

## 第142バッチ（2026-10-18）

Q_3_005・Q_3_006を18箇所改訂し、独立正答4・1を確定。Graesser, Singer & Trabasso（1994）原論文全25頁のPDFを、著者公開業績ページのリンクから取得。本文371–378頁を精読し、374頁の知識に基づく推論の説明、375頁Table 1の因果的先行事象・因果的結果・状態、376頁の精緻化推論と生成条件、378頁の局所的一貫性を照合。抽出本文に加え374–376頁の画像を精読し、表の欄の対応を確認した。全25頁精読済みという意味ではない。初回376頁PNGは破損していたため除外し、当該頁を再描画して完全読込み・画像精読を行った。

橋渡し推論と精緻化推論の同義扱いを撤回。物語文の知識に基づく推論に対象を絞り、全種類の推論が常に生成されるとの断定や、全会話・全読者への無条件な一般化を避けた。Q_3_006は二文間の因果的なつながりを問う花瓶と水の作例に改訂。作例は本文の定義の適用のための監査者作成であり、原論文の実験刺激や実証結果として引用しない。文字列反復・因果関係に不要な外観の精緻化・将来展開の予測を区別し、4肢と4解説を照合した。

確認済み348・修正必要14・要追加確認138、残152問。累積345問2938箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。v8不変・500問構造・キー・タグ・早見表・リンク・影響外本文の不変検査、公開判定回帰8条件・置換回帰4条件を通過。機械警告99件で増減なし。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画し、全18変更文字列を検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。既存校正・documents手順で変更範囲を検査。全頁最終目視および残152問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第142バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第142バッチ S205（2026-10-18）

- S205 Graesser, A. C., Singer, M., & Trabasso, T. (1994). Constructing Inferences During Narrative Text Comprehension. Psychological Review, 101(3), 371–395. DOI 10.1037/0033-295X.101.3.371。[著者業績ページ](https://sites.google.com/site/graesserart/publications/1994-1993)の[原論文PDFリンク](https://drive.google.com/file/d/1pP-xIo8wTKMvuWAthukgLVkfXHbXqy6E/view)から全25頁を取得。本文371–378頁を精読し、374–376頁は画像でも照合。知識に基づく非明示情報の補完、Table 1の因果連鎖・予測・状態、精緻化と生成条件をQ_3_005・Q_3_006に照合。全25頁精読や全談話ジャンル・全理論の同一分類への一般化はしない。花瓶例は監査者作例で、原論文の実験刺激の引用ではない。

取得原バイトSHA256・読了範囲・制約はevidence/batch142_sources.json。原論文本文・頁画像は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=142,base_commit='31725d8df5dcc3ceb4ead8571844482f9e5ee25d',fully_rejudged=sorted(targets),edits=18,independent_answers={'Q_3_005':4,'Q_3_006':1},sources=['S205'],status_counts=m['status_counts'],remaining=152,machine_warnings=99,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_pdf_page_sha256={'374':sha(root/'graesser142-04.png'),'375':sha(root/'graesser142-05.png'),'376':sha(root/'graesser142-06-retry.png')},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch142_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('348 confirmed / 152 remaining',pages)
