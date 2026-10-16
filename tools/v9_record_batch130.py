"""Record post-task form-focus revision and changed-page QA."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa130';ids=['Q_O_054']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':333,'修正必要':26,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch130.json').read_text());assert len(cs)==9
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('332問','333問'),('27問','26問'),('333問2806箇所','334問2815箇所'),('333問を','334問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第130バッチ（2026-10-17）

Q_O_054を9箇所改訂し、設問・全4肢・独立正答・全4解説をJane Willis本人署名の公開記事本文とケース11に照合。独立正答1を維持。記事全体の本文を再取得・精読し、教材の順序変更、Task Cycle、Focus on Form、Conclusionの提案を適用した。1996年書籍全体や、全TBL方式の共通規則とするものではない。

タスク後に教材の文法部分を使った形式学習を行う提案に沿って、B教師の事後確認・整理を計画する条件を明示。元の「定着に時間がかかる」という普遍的な比較や、「フィードバックの質が効果を大きく左右する」という未取得の因果的断定を承認せず撤回した。タスクを先にすると文法を扱えない、必ず全ての文法を先に教える、学習者自身の言語使用を排除する、という肢を本人記事に照合して誤りと判定。ケースがWillisの全サイクルを忠実に実施していたとは推定していない。

確認済み333・修正必要26・要追加確認141、残167問。累積334問2815箇所、全500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。500問の構造・キー/タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件、置換関数回帰4条件を通過。警告98件は前バッチと完全一致し、新規なし。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画、全9変更文字列を検出。'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の改頁を含む全頁最終QAと残167問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第130バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第130バッチ S145再取得（2026-10-17）

Jane Willis [From priming tasks and target tasks to language focus and grammar](https://www.teachingenglish.org.uk/comment/1307)、British Council TeachingEnglish。本人署名と記事本文全体を再取得・精読。Use the book but change the order、Task Cycle、Focus on Form: At the end of the task cycle、Conclusionの提案をQ_O_054に使用。タスク後に教材の文法部分で形式を学ぶ提案を確認し、全方式での文法先行/排除の一律規則にはしない。時間・効果の比較やフィードバックの因果実証、1996年書籍、コメント欄、リンク先原著の承認はしない。刊年の未表示は維持し、コメントやクロールの日付を刊年にしない。原バイトSHA256・範囲はevidence/batch130_sources.json。原記事非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第130バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全9変更文字列を検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=130,base_commit='27efdd1978e24e7e6e41065cdd56ff051138c24c',fully_rejudged=ids,edits=9,independent_answers={'Q_O_054':1},sources=['S145'],status_counts=m['status_counts'],remaining=167,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch130_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('333 confirmed/167 remaining;9 edits recorded',reviewed)
