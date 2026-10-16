"""Record worksheet/rapport review after new changed-page image inspection."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa124';ids=['Q_4_047','Q_4_016']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':322,'修正必要':31,'要追加確認':147}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==94 and len(added)==1 and added[0][0:2]==['P1','Q_4_047'] and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch124.json').read_text());assert len(cs)==16
matches=json.loads((r/'matches.json').read_text());assert len(matches)==16 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for name in ['krashen-source38.png','krashen-source39.png','tkt-feedback.png','tkt-rapport.png','tkt-extra-45.png']:
 with Image.open(root/name) as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('320問','322問'),('32問','31問'),('148問','147問'),('321問2700箇所','323問2716箇所'),('321問を','323問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第124バッチ（2026-10-16）

Q_4_047・016の設問・全4肢・独立正答・全4解説を一次本文・画像に照合し16箇所改訂。正答1・2を維持。Q_4_047は2020年版の出入国在留管理庁・文化庁ガイドライン印刷5〜10頁にある書き言葉の工夫を、外国人学習者へ渡すワークシートの作業案内に適用する例として明示。元解説の「例題を必ず一つ以上提示するのが鉄則」を撤回し、必要な情報の整理・補足、図等の補助、読み手に応じた調節や表記の見やすさを根拠に改訂。ガイドラインは特定のワークシート比較実験ではなく、適用例という判断を一般的な実証効果と混同しない。全初級学習者に同じ認知負荷が生じるという根拠未取得の断定も承認しない。

Q_4_016はKrashen1982原著印刷31〜32/PDF38〜39、TKT公式用語集印刷16・37・44/PDF17・38・45のFeedback/Rapport/Supportiveを本文・画像精読。情意フィルターの方向は仮説内の主張として説明し、現在の全実証的合意としない。ラポールを教師と学習者の関係概念として捉え、心理的安全性という別の概念そのものの定義にしない。学習者の援助・質問を促す支援的雰囲気を照合。リキャストや優しい促しで上達・信頼が必ず高まるという効果保証、ラポール形成には全フィードバック禁止という規則を残さない。引用先の原研究や心理的安全性の原著は今回未取得であり、主張をそこへ拡張しない。

確認済み322・修正必要31・要追加確認147、残件178。累積323問2716箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。全500問の構造・正答タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告93→94、新規P1はQ_4_047正答解説末の図だけで誰にでも伝わる保証を否定する留保への誤検出。正答の適用例自体を否定していない。他93件と検出器を保持。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全16変更文字列を検出、'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の見出し・問題・解説の改頁は最終組版点検へ残す。全頁最終目視と残178問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第124バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第124バッチ S13・S183・S189追加照合（2026-10-16）

- S13 Krashen [Principles and Practice in Second Language Acquisition](https://www.sdkrashen.com/content/books/principles_and_practice.pdf)を著者サイトから再取得。印刷31〜32/PDF38〜39を本文・画像精読。低不安・低フィルターは1982年の仮説内主張であり全原研究の取得や現在の実証的承認ではない。
- S183 [TKT Glossary](https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf)印刷16・37・44/PDF17・38・45を本文・画像精読。Feedback/Rapport/Supportiveの当事者用語集内の定義と例を使用。心理的安全性の原著、特定訂正手法の信頼・上達効果の証明として扱わない。
- S189 [2020年版やさしい日本語ガイドライン](https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/pdf/92484001_01.pdf)印刷5〜10/PDF6〜11の既取得本文・画像照合を使用。ワークシートの作業案内への適用は具体例であって、全教材へ例題数を義務付ける規則や効果実験ではない。

原バイトURL・SHA256・範囲はevidence/batch124_sources.json。原PDFは非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第124バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全16変更文字列検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=124,base_commit='dee7a5868bef90cff912e79f451d98c13b1cb523',fully_rejudged=ids,edits=16,independent_answers=dict(zip(ids,[1,2])),sources=['S13','S183','S189'],status_counts=m['status_counts'],remaining=178,machine_warnings=94,new_warnings=added,new_warning_judgment='P1 false positive: rejects universally guaranteed understanding, not the example itself',readiness_gate='8 cases passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S13_PDF':[38,39],'S183_PDF':[17,38,45]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch124_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('322 confirmed/178 remaining;16 edits recorded',reviewed)
