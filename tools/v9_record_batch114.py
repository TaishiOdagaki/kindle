"""Record one-question follow-through after full changed-page image review."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch114_qa')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_O_036' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':292,'修正必要':38,'要追加確認':170}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==76 and len(added)==1 and added[0][:2]==['A1','Q_O_036'] and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch114.json').read_text());assert len(cs)==9
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];assert len(pages)==403
parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[152,355,356]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
src=json.loads((p/'evidence/batch113_sources.json').read_text())['S173'];assert sha('/workspace/scratch/01d7c3f9b818/fln113.pdf')==src['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('291問','292問'),('39問','38問'),('296問2523箇所','296問2532箇所')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第114バッチ（2026-10-16）

第113バッチ保存後、ケース8の残件Q_O_036を継続。S173 FLN2014原著全2頁とケース全3段落を照合し、設問・全4肢・独立正答・全4解説を再判定、9箇所改訂した。正答1維持。反転授業と反転学習の区別を問う形とし、事前の動画指示だけで四本柱すべての実施が確認されたとみなさない。教師の観察・支援の排除、動画以外の教材の禁止はいずれも原著に反する。従来の他教授法・blended分類の未照合主張は本問から除去し、その分野を確認済みにしたものではない。ケースの記録を超える実践・効果・最適動画時間は推定しない。第113バッチで残していた本問を今回の独立判定で確定。

確認済み292・修正必要38・要追加確認170、残件208。累積296問2532箇所（本問は過去にも部分修正済みで、累積修正問題数は増えない）。500問維持。台帳の原文はv8スナップショット、改訂本文はchangesと作業稿を参照。

全500問の構造・正答対応・タグ・表・リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告75→76件。追加A1は「すべて」という表現を正答内で用いたための形式警告だが、正答は全柱充足を断定せず証拠の限界を述べている。単一正答性を再確認し、検査を弱めず記録。他75件保持。documents手順でNoto Sans JPによる新規403頁を描画、全9変更文字列検出。152・355・356頁を1800px画像で直接目視・完全読込み。日本語欠字・重なり・文字切れなし。Q_O_036解説1と解説2以降の頁分割は最終組版改善対象。全403頁の最終目視と残208問の学術照合は未完了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第114バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第114バッチ S173再利用（2026-10-16）

FLN2014原著 [What Is Flipped Learning?](https://flippedlearning.org/wp-content/uploads/2016/07/FLIP_handout_FNL_Web.pdf) 全2頁を再照合。原バイトSHA256はbatch113_sources.jsonと一致。1頁のClassroomとLearningの非同義・四本柱条件、2頁F.2/P.1/I.2をQ_O_036全体へ照合。動画指示と応用活動という記録から全柱の充足を認定しない判断、観察・支援の位置づけ、媒体の非限定を問う。旧問題の他教授法やブレンディッド学習の一般的分類は根拠未取得のため改訂本文から除去し、承認対象外。原著の全訳やPDF転載ではなく独立した日本語問題と解説への改訂。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第114バッチ\n新規Noto Sans JP描画403頁。全9変更文字列検出。152・355・356頁を1800px画像で直接目視・完全読込み。欠字・重なり・文字切れなし。Q_O_036の解説1と2以降の頁分割は最終組版改善対象。全頁最終目視は未完了。\n')
e=dict(batch=114,base_commit='69d3aace39bbe9a35300632be814eb33a588cb75',fully_rejudged=['Q_O_036'],edits=9,independent_answers={'Q_O_036':1},sources=['S173'],source_sha256=src['sha256'],source_body_read_pages=[1,2],status_counts=m['status_counts'],remaining=208,machine_warnings=76,new_warnings=added,new_warning_judgment='A1 wording cue, not unsupported universal claim; independent key1 retained',readiness_gate='8 cases passed',render_pages=403,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},pagination_todo='Q_O_036 explanations split355/356; improve final pagination',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch114_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('292 confirmed/208 remaining;9 edits/3 pages recorded')
