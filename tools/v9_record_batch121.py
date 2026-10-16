"""Record batch121 after new Japanese-font changed-page visual inspection."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa121';ids=['Q_1_019','Q_M_004']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':315,'修正必要':32,'要追加確認':153}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==90
cs=json.loads((p/'changes_batch121.json').read_text());assert len(cs)==14
matches=json.loads((r/'matches.json').read_text());assert len(matches)==14 and all(matches.values())
reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for f in ['tabunka14.png','tabunka-cover-01.png']:
 with Image.open(root/f) as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('313問','315問'),('34問','32問'),('315問2650箇所','316問2664箇所'),('315問を','316問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第121バッチ（2026-10-16）

Q_1_019・Q_M_004の設問・全4肢・独立正答・全4解説を一次本文へ照合し、14箇所改訂。正答1・3を維持。文科省公開の地域日本語教育コーディネーター研修案内の冒頭と5役割、および国の総合的な体制づくり事業の目的・対象取組を照合。地域担当と総括担当を区別し、地域担当が全運営業務を一人で総括するという読みに限定しない。実在未確認の指針にN1一律義務を帰属させる誤答を、取得済み役割と明確に矛盾する記述へ変更。試験合格自体を目標から全面排除する説明も除去。所管の2024年4月移管の解説は以前から修正済みであり、保持しただけで新発見に数えない。歴史的研修案内を現年度の募集条件と扱わず、最新年度の補助率・募集期限等は今回の承認対象外。

Q_M_004は総務省自治行政局国際室作成の改訂プラン説明資料を文化庁公開の原PDFで取得。表紙の作成主体とPDF14頁/印刷13頁の全本文・画像を照合。同資料は多言語にやさしい日本語を含むと明記している。元正答3の内容自体を誤りとはせず、設問を同資料の枠組みに限定した。地域の実情に応じて対応言語を検討すること、多様な媒体・経路、SNS、情報入手と相談の体制を確認。一言語向け情報提供を常に誤りとする解説を改め、実情や必要言語を検討せず一言語へ固定することを誤答にする。全世界の言語にすべて訳す義務や、どの自治体でも実施済みという実態、障害別の効果は認定しない。全60頁の全施策を承認したものではない。

確認済み315・修正必要32・要追加確認153、残件185。累積316問2664箇所、500問維持。台帳の原文はv8スナップショットであり、改訂はchangesと作業稿を参照。全500問の構造、正答タグ/表/リンク、影響外本文、v8不変、公開可否回帰8条件を通過。警告90件は前回と完全一致、新規なし。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全14変更文字列を検出し、'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。既存の隣接問題・解説の改頁や見出し分離は最終組版確認へ残す。全頁最終目視と残185問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第121バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第121バッチ S186〜S188（2026-10-16）

- S186 文科省公開[地域日本語教育コーディネーター研修](https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/coordinator_kenshu/)の本文冒頭・5役割を取得照合。旧文化庁による研修の歴史的案内であり、現在の全研修要件やリンク先実践研究の全承認ではない。
- S187 文科省[地域日本語教育の総合的な体制づくり推進事業](https://www.mext.go.jp/a_menu/nihongo_kyoiku/mext_02998.html)の目的と対象取組を取得照合。総括・地域の担当を区別。補助率、当年度の募集・採択条件、全実施状況は承認対象外。S06所管移管は既確認を維持。
- S188 総務省自治行政局国際室[地域における多文化共生推進プランの改訂について](https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/taikai/r02/pdf/92746701_03.pdf)。原60頁取得、表紙とPDF14/印刷13を本文・画像精読。「多言語」にやさしい日本語を含む明示、地域の実情に応じる言語検討、多様な媒体・経路、情報入手・相談を使用。他の施策・補助金の現行要件・因果効果は未承認。検索抜粋による承認ではない。

原バイトURL・SHA256・照合範囲はevidence/batch121_sources.json。著作物の原PDF/HTMLは非転載。資料内の定義と一般語義を混同しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第121バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全14変更文字列検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=121,base_commit='b324932ef67820540af9556d2a3c91ddbc5c2306',fully_rejudged=ids,edits=14,independent_answers=dict(zip(ids,[1,3])),sources=['S186','S187','S188','S06'],status_counts=m['status_counts'],remaining=185,machine_warnings=90,new_warnings=[],readiness_gate='8 cases passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S188_PDF':[1,14]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch121_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('315 confirmed/185 remaining;14 edits recorded',reviewed)
