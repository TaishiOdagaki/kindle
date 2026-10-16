"""Record source-backed OPI/scoring judgments and latest changed-page images."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa120';ids=['Q_1_036','Q_1_037']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':313,'修正必要':34,'要追加確認':153}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==90 and len(added)==2 and {x[1] for x in added}==set(ids) and all(x[0]=='P1' for x in added) and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch120.json').read_text());assert len(cs)==13
matches=json.loads((r/'matches.json').read_text());assert len(matches)==13
reviewed=sorted({n for vs in matches.values() for n in vs});assert reviewed==[20,21,218]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for n in range(3,9):
 with Image.open(root/f'opi-source-{n:02}.png') as im:im.load()
for name in ['standards21.png','standards-043.png','standards-044.png']:
 with Image.open(root/name) as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();assert len(text.split('\f')[:-1])==404
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']))
assert {k for k in d if d[k]!=old_d[k]}==set(ids)
f=p/'README.md';s=f.read_text()
for a,b in [('311問','313問'),('35問','34問'),('154問','153問'),('314問2637箇所','315問2650箇所'),('314問を','315問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第120バッチ（2026-10-16）

Q_1_036・037の設問・全4肢・独立正答・全4解説を一次本文へ照合し13箇所改訂。正答4・3を維持。ACTFL自身の2024年版OPI受験案内3〜8頁を本文・画像精読。面接・質問調整・任意のロールプレイ、FACTの全体的評価、OPIのNovice〜Superiorと能力記述ガイド全体のDistinguishedの違い、下位区分と認定/基準調整/再認定を照合。以前から正しかったSuperiorの非三分割という修正は保持し、新発見として数えない。全レベルに段落発話を一律要求しない。引用される妥当性研究の原論文は今回未取得であり、提供者の案内を実証研究の代わりにはしない。現行の料金・予約・合理的配慮・認定年限等は承認対象外。

Q_1_037は2014Testing Standards11・33〜34頁を本文・画像照合し、用途のための得点解釈の支持と反復測定での一貫性を区別。TKT公式用語集の客観採点、CEFR2001の熟達度を併用。「採点者の主観や誤差が介入しないため極めて高い信頼性」という説明を、正答・配点を定め同じ基準を適用すれば採点者の判断差を抑えられるという条件付きの説明へ変更。採点処理の誤り・測定全体の誤差ゼロを保証しない。未照合のJLPT固有運用や波及効果/転移の補助分類は改訂本文の根拠にしない。OPIの訓練不要という誤答は認定・調整を説明する当事者資料に反するが、制度の存在からあらゆる採点の完全一致を認定しない。

確認済み313・修正必要34・要追加確認153、残件187。累積315問2650箇所、500問維持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。全500問の構造・正答タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告88→90、新規P1はQ_1_036の全レベル同じ要求を否定する留保とQ_1_037の誤差ゼロ保証を否定する留保への誤検出。正答の否定ではなく、他88件と検出器を保持。

Noto Sans JP新規404頁描画で全13変更文字列を検出、20・21・218頁を1800px画像で直接目視・完全読込み。変更箇所に欠字・重なり・文字切れなし。Q_1_037の選択肢3・4が次頁に分離し、隣接問題の一部見出し・リンクの分割もあるため最終組版改善対象に残す。全404頁最終目視と残187問の学術照合は未完了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第120バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第120バッチ S185とS142追加照合（2026-10-16）

- S185 ACTFL [OPI Familiarization Guide 2024](https://www.actfl.org/uploads/files/general/OPI_Familiarization_Guide_2024_FINAL.pdf)。11頁の通常取得、3〜8頁を本文・画像精読。表1・FACT・範囲と下位区分・認定を使用。出版年は著作権頁2024から確認。OPIはNovice〜Superior、Guidelines全体はDistinguishedも含むという区別を維持。引用された個別の妥当性研究は未取得。認定手続きを、それ自体で全採点の完全一致を示す因果実証と扱わない。現行料金・予約条件等の承認ではない。
- S142 AERA/APA/NCME [Testing Standards 2014](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf)を再取得。印刷11/PDF21、33〜34/PDF43〜44を本文・画像精読。妥当性の用途別得点解釈と信頼性/精度、測定手続きの反復・課題/時点/採点者の変動を使用。印刷12〜14も本文参照したが全書・全理論を承認しない。S179 CEFR2001の9.3.1とS183 TKT Assessment客観採点は既取得照合を使用。

原バイトのURL・SHA256・範囲はevidence/batch120_sources.json。原資料は非転載、独立した問題改訂・解説への要約である。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第120バッチ\nNoto Sans JP新規404頁。全13変更文字列検出。20・21・218頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。Q_1_037選択肢3・4の次頁分離等は最終組版課題。全頁最終目視は未完了。\n')
e=dict(batch=120,base_commit='edb602c53558bef644e46fb04728f1d7b82055e5',fully_rejudged=ids,edits=13,independent_answers=dict(zip(ids,[4,3])),sources=['S185','S142','S179','S183'],status_counts=m['status_counts'],remaining=187,machine_warnings=90,new_warnings=added,new_warning_judgment='P1 false positives from qualifications about all-level paragraph requirement and error-free scoring',readiness_gate='8 cases passed',render_pages=404,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'OPI2024':[3,4,5,6,7,8],'Standards2014_printed':[11,33,34]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch120_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('313 confirmed/187 remaining;13 edits/3 pages recorded')
