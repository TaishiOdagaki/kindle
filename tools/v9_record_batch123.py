"""Record batch123 definitions and Japanese-font changed-page inspection."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa123';ids=['Q_4_043','Q_M_032']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':320,'修正必要':32,'要追加確認':148}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==93 and len(added)==1 and added[0][0:2]==['P1','Q_M_032'] and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch123.json').read_text());assert len(cs)==14
matches=json.loads((r/'matches.json').read_text());assert len(matches)==14 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for n in [3,7,39,45,49]:
 with Image.open(root/f'tkt-extra-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('318問','320問'),('148問（未精読','148問（未精読'),('150問','148問'),('319問2686箇所','321問2700箇所'),('319問を','321問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第123バッチ（2026-10-16）

Q_4_043・Q_M_032の設問・全4肢・独立正答・全4解説をCambridge公式TKT Glossaryの印刷2・6・38・44・48頁/PDF3・7・39・45・49へ本文・画像照合し14箇所改訂。正答1・1を維持。コースブックは通常シラバスに沿って授業で継続的に使う教材、副教材はそれに加えて使う教材、adaptは特定クラスに適するよう文章等を変更するという定義と具体例に設問を限定。すべてのコースブックの完全な体系性、教材選定で学習者分析が常に最優先という未取得の順位付け、あらゆる教具・全メディアが無条件に副教材という拡張は承認しない。難しすぎる文章の一部を省くという同書の例から、全内容を無条件に原順序で実施する誤答を退ける。

授業後に成功点・不成功点を考えて今後の改善を判断する省察と、活動や段階に要する時間の見積りというtimingを照合。実施結果を振り返って配分見直しを検討することを両定義に沿う具体例と判定した。これは時間を変えれば必ず成果が上がるという実証の承認ではない。無変更を絶対とする、無作為配分だけで省察とする、授業計画・自己点検と無関係とする誤答を独立に検討。用語集の刊年や全研究の取得、日本語教育全体で統一された定義とは主張しない。

確認済み320・修正必要32・要追加確認148、残件180。累積321問2700箇所、500問維持。台帳原文はv8スナップショットであり、改訂はchangesと作業稿を参照。全500問の構造・正答タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告92→93、新規P1はQ_M_032正答解説末の効果保証を否定する留保への誤検出であり、省察例という正答の否定ではない。他92件と検出器を保持。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全14変更文字列を検出、'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の見出し・問題・解説の改頁は最終組版点検へ残す。全頁最終目視と残180問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第123バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第123バッチ S183追加照合（2026-10-16）

Cambridge English [TKT Glossary](https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf)。既取得原59頁の印刷2・6・38・44・48/PDF3・7・39・45・49を本文・画像精読。Adapt/Book/Reflect on teaching/Reflective/Supplementary material/Timingの当事者用語定義と例を使用。授業実施後の時間見積り見直しは定義に沿う適用例であり、配分変更の効果を証明した実験ではない。刊年推定・他項目の全承認・引用研究の取得は主張しない。原バイトURL・SHA256・照合範囲はevidence/batch123_sources.json。原PDFは非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第123バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全14変更文字列検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=123,base_commit='6d42c205a2911c372feebe2310f06697fdf504da',fully_rejudged=ids,edits=14,independent_answers=dict(zip(ids,[1,1])),sources=['S183'],status_counts=m['status_counts'],remaining=180,machine_warnings=93,new_warnings=added,new_warning_judgment='P1 false positive: qualification rejecting guaranteed effect, not negating the reflective example',readiness_gate='8 cases passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S183_PDF':[3,7,39,45,49]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch123_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('320 confirmed/180 remaining;14 edits recorded',reviewed)
