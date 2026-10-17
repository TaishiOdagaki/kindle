"""Record mother tongue audit after direct changed-page inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');r=Path(__file__).resolve().parents[2]/'qa134'
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_4_093' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':336,'修正必要':23,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'));assert machine['issues']==prior['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch134.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={'Q_4_093'}
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text()
for a,b in [('335問','336問'),('24問','23問'),('336問2833箇所','336問2842箇所')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第134バッチ（2026-10-17）

Q_4_093の設問・全4肢・全4解説を9箇所改訂し、独立正答1を確定。Cummins本人署名の2001年Sprogforum記事全6頁を取得・通読し、17–19頁の言語間の概念・読み書きの関連、二言語へのアクセス、母語減退の環境差と母語使用機会の提案を照合した。原記事誌面の公開ミラーであることを明示。2008年BICS/CALP記事にない母語保持の主張を、参考文献の列挙だけで承認していない。

母語発達が全員の第二言語能力を必ず高めるという断定、支援がなければ必ず急速に母語を喪失するという断定、セミリンガルという欠損的な診断、家庭での母語禁止による情緒発達への一律の重大影響を撤回。著者の説明に沿う支援方針という条件を設問に置き、既知の概念の言語間関連と、母語を使う機会の重要性を問う形にした。引用先の実証研究や2000年書籍全体、現在の日本の全児童への効果保証は承認していない。

確認済み336・修正必要23・要追加確認141、残164問。累積336問2842箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。500問の構造・キー・タグ・表・リンク、影響外本文、v8不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。警告98件は前バッチと完全一致。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全9変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。全頁最終目視と残164問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第134バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第134バッチ S196（2026-10-17）

Jim Cummins (2001), Bilingual Children's Mother Tongue: Why is it important for education?, Sprogforum19, 15–20。[原記事誌面公開ミラー](https://lavplu.eu/central/bibliografie/cummins_eng.pdf)全6頁を取得・通読、著者署名・誌名・巻号年頁を原PDFで照合。Q_4_093には17–19頁の概念・読み書きの言語間関連、二言語へのアクセス、母語減退の環境差と母語使用機会を使用し、PDF4・5頁の画像も精読した。引用先研究・書籍の個別取得ではなく、全効果・喪失年数・権利法制・現在の日本の政策を承認しない。範囲と原バイトSHA256はevidence/batch134_sources.json。原記事非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=134,base_commit='7c9f024ff95104b7cd3941d92b15ca6f0e9edb52',fully_rejudged=['Q_4_093'],edits=9,independent_answers={'Q_4_093':1},sources=['S196'],status_counts=m['status_counts'],remaining=164,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch134_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('336 confirmed / 164 remaining',pages)
