"""Record environment-analysis scope revision after changed-page QA."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');r=Path(__file__).resolve().parents[2]/'qa135'
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_4_028' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':337,'修正必要':22,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'));assert machine['issues']==prior['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch135.json').read_text());assert len(cs)==5
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={'Q_4_028'}
matches=json.loads((r/'matches.json').read_text());assert len(matches)==5 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text()
for a,b in [('336問','337問'),('23問','22問'),('337問2842箇所','337問2847箇所')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第135バッチ（2026-10-17）

Q_4_028の設問・全4解説を5箇所改訂し、4選択肢を維持して独立正答4を確定。Paul Nation著者公式大学サイトの公開稿What Should Every ESL Teacher Know?の印刷/PDF12–14頁の本文・画像を精読した。環境分析は時間・資源だけでなく学習者・教師・状況を含み、ニーズ分析の一部として扱う場合もある。元の環境分析を物理的・制度的条件だけとする排他的な定義と、他の情報を一律に切り離す説明を撤回した。

設問が対象とする下位範囲をコース実施の時間・資源条件と明示し、既習知識・目標言語行動・アイデンティティ変化の情報との相違を各肢で確認。これらを教育上無価値とはせず、学習者の要因を環境分析全体から除外しない。本文の定義・例を用いたもので、分析を行えば必ず教育が成功するという効果保証ではない。書籍全192頁を取得したが承認範囲は12–14頁に限定し、引用先2000年論文や別著Language Curriculum Designを読了したとはしない。刊年はPDFから確定せず、ファイル名の日付と区別した。

確認済み337・修正必要22・要追加確認141、残163問。累積337問2847箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。500問の構造・キー・タグ・表・リンク、影響外本文、v8不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。警告98件は前バッチと完全一致。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全5変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。全頁最終目視と残163問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第135バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第135バッチ S197（2026-10-17）

Paul Nation, What Should Every ESL Teacher Know?、[著者公式大学サイト公開稿](https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/paul-nations-publications/publications/documents/what-should-every-esl-teacher-know-13-feb-2013-pdf)。全192頁を取得、印刷/PDF12–14頁の第2章導入・Needs Analysis・Environment Analysisの定義と例を本文・画像精読。Q_4_028の時間・人数・資源の例、および環境分析の学習者・教師・状況への広がりに使用。全書籍、引用先2000年論文、全学習効果を承認せず、ファイル名の日付を刊年としない。Web取得では410だが通常の直接ダウンロードは完全なPDFで成功。原バイトSHA256と範囲はevidence/batch135_sources.json。書籍本文は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=135,base_commit='17c30ad5b593ae1d3a0dcb80e05ec8348f33e815',fully_rejudged=['Q_4_028'],edits=5,independent_answers={'Q_4_028':4},sources=['S197'],status_counts=m['status_counts'],remaining=163,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch135_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('337 confirmed / 163 remaining',pages)
