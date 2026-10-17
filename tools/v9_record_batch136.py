"""Record historical quality-assurance revision and recovered-font QA."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa136'
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_1_027' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':338,'修正必要':21,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch136.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={'Q_1_027'}
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text();s=s.replace('| 確認済み | 337問 |','| 確認済み | 338問 |').replace('22問','21問').replace('337問2847箇所','337問2856箇所');f.write_text(s)
report='''

## 第136バッチ（2026-10-17）

Q_1_027の設問・全4肢・全4解説を9箇所改訂し、独立正答2を確定。文部科学省公開の学制百二十年史の該当節本文全2段落を取得・精読。1988年12月の運営基準、1989年5月の任意団体発足・審査認定事業開始、1990年2月の財団法人許可、同年11月の三省共管を照合した。制度整備の歴史に範囲を明示し、異なる段階の混同を避けた。元の留学生政策の対象範囲、教師需要の「爆発的」増加と養成課程の増加の因果・幅は未照合のため承認せず撤回。歴史上の審査・認定を現在の法的認定制度と同一視しない。

確認済み338・修正必要21・要追加確認141、残162問。累積337問2856箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。500問の構造・キー・タグ・表・リンク、影響外本文、v8不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。警告98件は前バッチと完全一致。

旧作業場のGit管理情報が消失していたため、最新GitHubから新規cloneで再構成。旧作業ファイルは削除せず保護。描画環境も再構成し、LibreOffice複写時の所有者属性エラーは所有者を保存しない複写で解決。初回Noto Sans JP取得は5021696バイトの欠損でcmap検証に失敗したためQAに使用せず除外。再取得9589900バイトのフォントの日本語cmapを検証してから描画に使用した。欠字描画をQAとして採用していない。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全9変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。全頁最終目視と残162問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第136バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第136バッチ S198（2026-10-17）

文部科学省公開 [学制百二十年史 三 日本語教育施設の質的向上](https://www.mext.go.jp/b_menu/hakusho/html/others/detail/1318583.htm)の歴史記述本文全2段落を取得・精読。Q_1_027の1988年基準、1989年任意団体発足・審査認定開始、1990年財団法人許可・三省共管の経緯に使用。現在の法的認定制度、留学生政策の全対象、教師需要増加の因果を承認しない。「平成21年以前」のサイト登録表示を本文の刊年とはしない。原バイトSHA256と範囲はevidence/batch136_sources.json。原文非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=136,base_commit='e67e1c1cb5df6d93f342a197714c45faf59e4309',fully_rejudged=['Q_1_027'],edits=9,independent_answers={'Q_1_027':2},sources=['S198'],status_counts=m['status_counts'],remaining=162,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),excluded_font_bytes=5021696,full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch136_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('338 confirmed / 162 remaining',pages)
