"""Record completed batch145 after direct changed-page image inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa145';target='Q_3_004'
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':352,'修正必要':11,'要追加確認':137}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==102
added=[x for x in machine['issues'] if x not in prior];assert len(added)==2 and all(x[1]==target for x in added);assert all(x in machine['issues'] for x in prior)
cs=json.loads((p/'changes_batch145.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={target}
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns});assert pages==[39,237]
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages);assert pagecount==406
f=p/'README.md';s=f.read_text().replace('351問','352問').replace('138問','137問').replace('348問2963箇所','349問2972箇所').replace('348問を部分修正','349問を部分修正');f.write_text(s)
report='''

## 第145バッチ（2026-10-18）

Q_3_004を9箇所改訂し、独立正答3を確定。S205 Graesser, Singer & Trabasso（1994）原論文の全25頁PDFを著者公開リンクから再取得。印刷374頁本文全体を再精読し、同頁画像も照合した。全25頁精読ではない。経験に基づく背景知識構造（スキーマ、スクリプト等）が物語の理解に関わるという原論文の説明に照合。

「日本では風邪の時に入浴を控える」という文化的慣習の一律な断定を撤回。個人が経験から形成した食後払いへの期待と、物語の食前会計との食い違いに置換した。国民的慣習や医学的判断を問わず、論文の実験刺激を引用したものでもない。誤答1・2・4は明示条件が語義未習・接続表現未習・漢字の読みの未習であり、出来事の枠組みとの不一致を示さない。4解説の未照合なボトムアップ等の補助分類も削除した。

機械警告100→102件。追加P1は正答解説末尾の「国民全体に共通する慣習を述べた例ではありません」を正答の否定と取り違えたもので、これは一般化の制限。A1の「必ず」は、事例中の読者が持つ過剰な期待の内容であって、出題者による全飲食店への断定ではない。両警告と既存100件を保持し、隠蔽しない。

確認済み352・修正必要11・要追加確認137、残148問。累積349問2972箇所、500問維持。台帳原文はv8スナップショットであり、改訂はchangesと作業稿を参照。v8不変、500問の構造・キー・タグ・早見表・リンク・影響外本文の検査と、公開判定回帰8条件・置換回帰4条件を通過。Noto Sans JPで406頁を描画し、9変更文字列を全件検出。39・237頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。全頁最終目視と残148問の学術照合は未了。最終v9ではなく出版不可。
'''
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第145バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第145バッチ S205再照合（2026-10-18）

- Graesser, Singer & Trabasso (1994), Constructing Inferences During Narrative Text Comprehension, Psychological Review 101(3), 371–395。著者業績ページ https://sites.google.com/site/graesserart/publications/1994-1993 の公開PDFリンク https://drive.google.com/file/d/1pP-xIo8wTKMvuWAthukgLVkfXHbXqy6E/view から全25頁を再取得。印刷374頁全文と画像を再照合。スキーマ等の背景知識構造、経験に根ざしたレストランの出来事の枠組み、文章・読者の構成する意味の不一致に限定して使用。Q_3_004は定義の適用のための監査者作例であり、実験刺激の引用・国別慣習の実証ではない。全25頁精読や引用元の1977年書籍等の取得ではない。原バイトSHA256・読了範囲はevidence/batch145_sources.json。本文・頁画像は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=145,base_commit='80186ca2b199f9ed43f0021da22a258551d31f08',fully_rejudged=[target],edits=9,independent_answers={target:3},sources=['S205'],status_counts=m['status_counts'],remaining=148,machine_warnings=102,new_warnings=added,new_warning_review='P1: scope limitation is not negation of the answer. A1: always is the hypothetical reader belief, not an author assertion about all restaurants.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=406,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_page_sha256=sha(root/'graesser145-4.png'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch145_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('352 confirmed / 148 remaining')
