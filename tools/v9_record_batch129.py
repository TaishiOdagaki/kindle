"""Record case-based drill question and changed-page QA."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa129';ids=['Q_O_053']
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in ids else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':332,'修正必要':27,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch129.json').read_text());assert len(cs)==9
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
with Image.open(root/'tkt-drill-15.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('331問','332問'),('28問','27問'),('332問2797箇所','333問2806箇所'),('332問を','333問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第129バッチ（2026-10-17）

Q_O_053を9箇所改訂し、設問・全4肢・独立正答・全4解説をケース11の本文とCambridge公式TKT GlossaryのDrill項目（印刷14/PDF15）へ本文・画像照合。独立正答3を維持。原設問の「短期間で定着させやすい」という他方式との効果・時間の比較を承認する根拠は取得していないため、確認できる活動の特徴へ再構成した。

提示語に応じ同じ構造で語句を置き換える、教師が導く反復練習の機会を確認。自由な依頼条件の交渉、学習者による目標・場面の自由選択、黙読のみという肢はケースに書かれたA教師の活動に対応しない。元の解説に含まれた教授法間の自発的コミュニケーション能力の効果比較、即時訂正から不安への因果、学習スタイルへの一般化を推測で承認していない。「練習機会がある」と「短期定着の実証がある」を区別する。

確認済み332・修正必要27・要追加確認141、残168問。累積333問2806箇所、全500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。500問の構造・キー/タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件、置換関数回帰4条件を通過。警告98件は前バッチと完全一致し、新規なし。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画、全9変更文字列を検出。'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の改頁を含む全頁最終QAと残168問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第129バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第129バッチ S183追加照合（2026-10-17）

Cambridge English [TKT Glossary](https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf)を再取得、全59頁読込みを確認。印刷14/PDF15のDrill項目を本文・画像精読。guided repetitionと提示文/提示語による同構造の置換の公式用語定義を、ケース11のA教師の活動へ照合。学習効果の短期定着、他方式への比較優位、即時訂正と不安の因果、学習スタイルの実証を承認する資料として用いない。取得範囲・原バイトSHA256はevidence/batch129_sources.json。原資料は非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第129バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全9変更文字列を検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=129,base_commit='e3d47368accb91d7254ec4e48cef065f70dfa523',fully_rejudged=ids,edits=9,independent_answers={'Q_O_053':3},sources=['S183'],status_counts=m['status_counts'],remaining=168,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S183_PDF':[15]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch129_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('332 confirmed/168 remaining;9 edits recorded',reviewed)
