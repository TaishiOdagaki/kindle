"""Record the completed verbal-report review and latest render, one time only."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch111_qa')
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_4_078' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':284,'修正必要':39,'要追加確認':177}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==71 and len(added)==1 and added[0][:2]==['D2','Q_4_078'];assert all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch111.json').read_text());assert len(cs)==6
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[82,282]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
f=p/'README.md';s=f.read_text()
for a,b in [('283問','284問'),('178問','177問'),('288問2469箇所','289問2475箇所'),('288問を','289問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第111バッチ（2026-10-16）

Q_4_078をEricsson・Simon1980の原論文本文217〜220頁へ照合し、設問・全4肢・独立正答・全4解説を再判定、6箇所改訂した。大学サーバ公開の画像PDF全37頁を取得し、215〜218頁と220頁を画像精読、217・218・220頁を1800pxで再確認。本文219頁はOCRで補助確認した。抄録だけの承認ではない。原論文217頁は言語報告を内的過程の特権的な直接観察と仮定せず、218頁は同時的言語化と回顧的言語化を時間との関係で区別し、220頁は動機・理由がそのまま報告可能とは限らないと説明する。思考を透明に可視化するような含意と、同時・回顧の単純な同一視を除いた。未変更の誤答3肢も、参加者の言語報告を得る手続きかどうかを原文と比較済み。引用先の全実証研究・全教育場面の効果は承認対象外。

正答4維持。確認済み284・修正必要39・要追加確認177、残件216。累積289問2475箇所、500問維持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。

全500問の構造・正答番号・タグ・表・リンク・影響外本文・v8不変を検査し、公開可否回帰8条件が合格。警告70→71件、追加D2のQ_4_078は解説2が無言・報告不在、4が同時言語化に対応し、並び替え疑いは誤検出と全肢対照確認。他70件は同一。documents手順でNoto Sans JPによる累積稿401頁を新規描画し全6変更文字列を検出、82・282頁を1800px画像で直接目視・完全読込み。対象部分に欠字・重なり・切れなし。全頁最終目視・組版の最終調整と残216問の学術確認は未了。作業稿は出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第111バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第111バッチ S170（2026-10-16）

K. Anders Ericsson・Herbert A. Simon（1980）Verbal Reports as Data, Psychological Review87(3),215–251, DOI10.1037/0033-295X.87.3.215。[大学サーバ公開原論文](https://acs.ist.psu.edu/ist597/papers/ericssonS80.pdf)画像PDF37頁を取得。215〜218頁と220頁を画像精読、217・218・220頁を1800pxで再確認、219頁はOCR補助読解。Q_4_078は原著者本人による方法論の区別に限定して承認。217頁の直接観察の非仮定、218頁の同時・回顧と記憶間隔、220頁の思考発話手続きと動機・理由の可用性の留保に対応。原論文の全37頁や引用先実証研究をすべて照合したとはしない。スキャン2004年と出版1980年を区別する。ハッシュ・取得範囲はevidence/batch111_source.json、PDF本文は再配布しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第111バッチ\nNoto Sans JPによる累積稿401頁、全6変更文字列を検出。82・282頁を1800px画像で直接目視。対象部分に欠字・重なり・切れなし。全頁最終目視と組版の最終調整は未完了。\n')
e=dict(batch=111,base_commit='952ad4db8af73c3c8e5e77157640249b97dd5381',fully_rejudged=['Q_4_078'],edits=6,independent_answers={'Q_4_078':4},sources=['S170'],status_counts=m['status_counts'],remaining=216,machine_warnings=71,new_warnings=added,new_warning_judgment='D2 false positive: explanation2 rejects silence/no verbal report; explanation4 matches concurrent verbalization; all4 individually checked',readiness_gate='8 cases passed',render_pages=len(pages),visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch111_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('284 confirmed/216 remaining;6 edits/2 pages recorded')
