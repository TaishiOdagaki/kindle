"""Record batch113 after direct image inspection; do not rerun apply113."""
import json, hashlib, subprocess, io, csv, re, bisect, gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9'); r=Path('/workspace/scratch/01d7c3f9b818/batch113_recovery_qa')
ids=['Q_4_116','Q_4_117','Q_O_037','Q_O_038','Q_O_039','Q_O_040']
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline=''); rd=csv.reader(s); out=[]
 while True:
  start=s.tell()
  try: row=next(rd)
  except StopIteration: break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in ids else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text()); assert m['status_counts']=={'確認済み':291,'修正必要':39,'要追加確認':170}
machine=json.loads((p/'postfix_machine.json').read_text()); prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==75 and len(added)==3 and {x[1] for x in added}=={'Q_4_116','Q_O_037','Q_O_038'} and all(x[0]=='P1' for x in added)
assert all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch113.json').read_text()); assert len(cs)==41 and {x['id'] for x in cs}==set(ids)
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1]
assert len(pages)==402
parts=[re.sub(r'\s+','',s) for s in pages]; whole=''.join(parts);bounds=[0]
for s in parts: bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']); at=whole.find(needle); assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v}); assert reviewed==[97,98,152,153,297,298,355,356]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im: im.load()
src=json.loads((p/'evidence/batch113_sources.json').read_text())
for entry in src['S172']['pages']:
 raw=gzip.decompress((p/'evidence'/entry['archive']).read_bytes())
 assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256']
f=p/'README.md'; s=f.read_text()
for a,b in [('285問','291問'),('176問','170問'),('290問2482箇所','296問2523箇所'),('290問を','296問を')]: s=s.replace(a,b)
f.write_text(s)
report='''

## 第113バッチ（2026-10-16）

Q_4_116・117、Q_O_037〜040の6問について、設問・全4選択肢・独立正答・全4解説を一次本文に照合し、41箇所を改訂。正答は順に1・4・4・4・3・3で維持。

Q_4_116はMoodle4.5公式文書のQuiz・Forum・Activity completion report・Review optionsに限定。教員が結果・完了状況を確認して支援を検討する機能とし、全LMS共通機能、出欠把握の一般化、自動的な早期発見や学習効果の保証を除去。権限・設定と、完了表示が習得そのものではない点を明記。

Q_4_117はFLN2014原著2頁の定義・四本柱へ限定。動画必須、最適動画時間、ブレンディッド学習との分類の未照合断定を除去。個人学習空間への直接指導の移行と、教員が導く集団学習での応用・相互作用を区別。Q_O_037〜040はケース8の全3段落を読み、同原著F2/F3/I3/P1/P2へ照合。小テストは指導調整の資料であり視聴証明ではない。未視聴理由は記録されておらず、原因を推測で確定しない。支援の検討と、授業を改善して再試行する方針を明示し、補足説明・同一ペース・方法変更を無条件に誤りとしない設問へ改訂。架空ケースの10分動画は事例設定であり最適時間の根拠ではない。Q_O_036の教授法分類等は未照合が残り修正必要を維持し、ケース全体を一括承認していない。

確認済み291・修正必要39・要追加確認170、残件209。累積296問2523箇所。全500問を維持。台帳原文はv8スナップショットで、改訂本文はchangesと作業稿を参照。

全500問の構造・正答対応・タグ・表・リンク・影響外本文・v8不変の検査と公開可否回帰8条件が合格。警告72→75件。追加P1はQ_4_116の効果保証の否定、Q_O_037の視聴証明の否定、Q_O_038の原因断定の否定という留保への誤検出であり、正答を否定していない。他72件を保持。

未保存作業場の消失後、876060c95c24634f6a7f265b89a4ec2dfdfc879aから再取得し、未保存6問を記録に基づき再構成。一次資料を再取得してハッシュ照合し、新規402頁の描画で再検査した。過去の消失した描画を今回の証拠に使用していない。Noto Sans JPの日本語字形を確認、全41変更文字列をPDF本文で検出。97・98・152・153・297・298・355・356頁を1800px画像で直接目視し、完全読込み検査。欠字・重なり・文字切れなし。Q_4_116の選択肢・解説とQ_O_038の選択肢の頁またぎ、356頁末の次ケース見出しの孤立は最終組版改善対象。全402頁の最終目視、残209問の学術照合は未完了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name; assert '## 第113バッチ' not in f.read_text(); f.write_text(f.read_text()+report)
f=p/'sources.md'; f.write_text(f.read_text()+'''

## 第113バッチ S172・S173（2026-10-16）

- S172 Moodle4.5公式本文：[Quiz activity](https://docs.moodle.org/405/en/Quiz_activity)、[Quiz settings](https://docs.moodle.org/405/en/Quiz_settings)、[Forum activity](https://docs.moodle.org/405/en/Forum_activity)、[Activity completion report](https://docs.moodle.org/405/en/Activity_completion_report)。本文取得、Quiz/Forumの概要・教員表示、Review options、完了報告の権限・表示凡例を精読。HTML原バイトをgzipで保存しSHA256照合。Q_4_116の設定依存機能の根拠。他製品・全LMS・因果的学習効果の承認ではない。
- S173 Flipped Learning Network (2014), What Is Flipped Learning? [公式原著PDF](https://flippedlearning.org/wp-content/uploads/2016/07/FLIP_handout_FNL_Web.pdf)。全2頁を本文精読・画像照合。定義、Flipped Classroomとの区別、F/L/I/P四本柱と11指標を確認。URLの2016ではなく本文の引用指定2014を採用。Q_4_117とQ_O_037〜040は枠組み・形成的評価・柔軟な支援への対応を問う形へ限定。効果実証、最適動画時間、他教授法の分類は承認対象外。原著PDF全体は転載せずURL・ハッシュ・照合範囲をbatch113_sources.jsonへ保存。日本語の独立した要約・問題改訂であり全文翻訳ではない。
''')
f=p/'visual_qa.md'; f.write_text(f.read_text()+'\n\n## 第113バッチ\n復旧後の新規Noto Sans JP描画402頁を使用。全41変更文字列を検出。97・98・152・153・297・298・355・356頁を1800px画像で直接目視・完全読込み。欠字・重なり・文字切れなし。Q_4_116・Q_O_038の頁またぎと356頁末の次ケース見出し孤立は最終組版改善対象。全頁最終目視は未完了。\n')
e=dict(batch=113,base_commit='876060c95c24634f6a7f265b89a4ec2dfdfc879a',fully_rejudged=ids,edits=41,independent_answers=dict(zip(ids,[1,4,4,4,3,3])),sources=['S172','S173'],status_counts=m['status_counts'],remaining=209,machine_warnings=75,new_warnings=added,new_warning_judgment='P1 false positives from qualified guarantees/viewing evidence/causation, not denial of keys',readiness_gate='8 cases passed',render_pages=402,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},font='Noto Sans JP instantiated static400; Japanese glyphs visually checked',recovery='fresh clone from base; source reacquisition; new render only',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch113_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('291 confirmed /209 remaining; 6 questions41 edits;8 pages recorded')
