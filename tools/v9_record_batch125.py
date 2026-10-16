"""Record L1/L2 comparison revision and changed-page QA."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa125';ids=['Q_3_008']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':323,'修正必要':30,'要追加確認':147}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==94
cs=json.loads((p/'changes_batch125.json').read_text());assert len(cs)==9
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for n in [17,18]:
 with Image.open(root/f'krashen-extra-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('322問','323問'),('31問','30問'),('323問2716箇所','324問2725箇所'),('323問を','324問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第125バッチ（2026-10-16）

Q_3_008の設問・全4肢・独立正答・全4解説をKrashen1982原著印刷10〜11/PDF17〜18へ本文・画像照合し9箇所改訂。正答4を維持。従来の第一/第二言語の一般比較は、生得的LADを無条件の事実として対比する、第二言語学習者はすべて第一言語が確立済みとする、第一言語習得の到達が全人類一律とする、転移を普遍的とする、明示指導/Focus on Formの効果を根拠未取得でまとめる等の問題があった。これらを推測で承認せず、同じ第一/第二言語の比較領域で、著者の習得と学習の区別の仮説内主張を問う問題へ再構成。

成人にも子供の第一言語の発達と類似する無意識的習得が可能とし、意識的な規則知識の学習と区別するという主張を原文から独立判定した。成人にも習得可能という主張は、成人全員が常に母語話者並みへ到達する保証ではないという印刷10頁の留保を保持。生物学的機構や現在の理論的合意、到達度比較、転移や明示指導の実証の承認とはしない。印刷11頁の引用先研究は今回未取得であり、著者の原著を読んだことを全研究の再検証と扱わない。

確認済み323・修正必要30・要追加確認147、残件177。累積324問2725箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。全500問の構造・正答タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告94件は前回と完全一致、新規なし。

第124バッチ保存時、GitHubのupdate_refが一度「UNPROCESSABLE / twirp error not_found: missing」を返した。ブランチHEADが前回のdee7a58のまま、作成済みb3474c3コミットの親・treeも正しいことを読み取り再確認。同じexpected_shaのleaseで一度再試行して成功し、再取得でb3474c3とtreeを確認した。一過性エラーから復旧済みで、他の変更の上書きや権限変更は行っていない。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全9変更文字列を検出、'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の見出し・問題・解説の改頁は最終組版点検へ残す。全頁最終目視と残177問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第125バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第125バッチ S13追加照合（2026-10-16）

Krashen [Principles and Practice in Second Language Acquisition](https://www.sdkrashen.com/content/books/principles_and_practice.pdf)印刷10〜11/PDF17〜18を本文・画像精読。成人の二過程、子供の第一言語発達と類似する無意識的習得、意識的規則知識としての学習、成人の母語話者並み到達を保証しない留保を使用。第一/第二言語習得の全般的な実証比較にせず1982年の仮説内主張に限定。引用先原研究・現在の全理論的合意・転移や明示指導の普遍的効果を承認しない。原バイトURL・SHA256・範囲はevidence/batch125_sources.json。原PDFは非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第125バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全9変更文字列検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=125,base_commit='b3474c327e8a6895e5056bedaca5b2a95b4d853c',fully_rejudged=ids,edits=9,independent_answers={'Q_3_008':4},sources=['S13'],status_counts=m['status_counts'],remaining=177,machine_warnings=94,new_warnings=[],readiness_gate='8 cases passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S13_PDF':[17,18]},previous_write_transient_error='batch124 update_ref UNPROCESSABLE missing; original lease retry succeeded and fetched',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch125_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('323 confirmed/177 remaining;9 edits recorded',reviewed)
