"""Record explicit case time repair after direct changed-page inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa148c';target='Q_O_031';targets={target,'Q_O_032'}
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':355,'修正必要':9,'要追加確認':136}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==103 and machine['issues']==prior
added=[]
cs=sum([json.loads((p/f'changes_batch148{s}.json').read_text()) for s in ['', 'b', 'c']],[]);assert len(cs)==22
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
assert d['Q_O_032']['status']=='要追加確認'
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==12 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('354問','355問').replace('修正必要10問','修正必要9問').replace('| 修正必要 | 10問 |','| 修正必要 | 9問 |').replace('350問2990箇所','352問3012箇所').replace('350問を部分修正','352問を部分修正');f.write_text(s)
report='''

## 第148バッチ（2026-10-18）

Q_O_031・共有ケース7・Q_O_032の設問を、公開前の追加照合を含む22件の順序付き編集で改訂。Q_O_031の独立正答4を確定し、Q_O_032は要追加確認を維持。S211・S212東京外国語大学言語モジュールの「Vています」の進行・状態の両解説本文・注記・全例文を取得・精読した。

進行用法だけを照合した初稿では、過去の期間と本人に確認する条件を追加して誤用扱いを残した。しかし、リンク先の状態用法まで広げて照合すると、S212第5項に過去の経験・記録の用法があり、3年前アメリカで勉強していますという例が存在した。このため初稿をそのまま承認せず、公開前に再改訂した。初稿10件を消去・上書きせず、追加11件を148bとして累積changesへ追記した。ケース末尾の一律な誤用認定も148cの1件で撤回した。

最終的なケースでは、教師の「過去だから誤用」という断定そのものを別の教師が問い直す。Q_O_031の全4肢・4解説を両教材へ照合し、過去経験用法を排除しない文脈・意図確認を正答4とした。過去の継続形への修正は可能な別の意図に対応する例であり、唯一の修正とも、元文が必ず誤りとも扱わない。

共有ケースのQ_O_032〜035の設問・全4肢・全4解説も影響点検。句点による文境界の別例を変えず、確認済みQ_O_033〜035の対象と正答は不変。Q_O_032は設問を教師が当初そう判断した表現の背景検討へ限定。ただし4肢・解説に残る誤用原因分析の根拠とケース整合は未了と明記し、自動承認しない。

最終改訂後の機械警告は103件で増減なし。初稿描画qa148は最終変更頁のQAには使用せず、新規qa148cへ再描画した。qa148bも最終QAには使用しない。

確認済み355・修正必要9・要追加確認136、残145問。累積352問3012箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。v8不変、500問の構造・キー・タグ・早見表・リンク・影響外本文、公開判定回帰8条件・置換回帰4条件を検査。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、上書きでなく追記された最終12変更文字列を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。全頁最終QAと残145問の学術照合は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第148バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第148バッチ S211（2026-10-18）

- S211 東京外国語大学言語モジュール「Vています（進行）／Vていません」解説 https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/044.html 。本文1〜3、例文1〜5、注記を全て取得・精読。継続・過去形・日本語を勉強するの表記を照合。原バイトSHA256はevidence/batch148_sources.json。
- S212 同「Vています（状態）」解説 https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/045.html 。本文1〜9、全例文・注記を取得・精読。第5項と例5の過去経験・記録用法に基づき、進行用法だけから判断した148初稿を148bで訂正。Q_O_031・ケース7の過去だから誤用という断定を撤回。母語干渉等の原因や本人の意図をこの教材だけで確定せず、Q_O_032は未了を維持。原バイトSHA256はevidence/batch148b_sources.json。両教材本文は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=148,base_remote_commit='90da89da028c19718251155ea068f14b16d3436a',fully_rejudged=[target],shared_case='CASE_O_07',case_impact_checked=['Q_O_032','Q_O_033','Q_O_034','Q_O_035'],case_impact_result='Q_O_032 stem changed but remains unverified; confirmed Q_O_033–035 unchanged.',edits=22,initial_edits=10,followup_edits=12,initial_draft_status='Superseded before publication after checking past-experience teiru use; initial changes preserved in ordered history; qa148 and qa148b excluded from final changed-page QA.',independent_answers={target:4},sources=['S211','S212'],status_counts=m['status_counts'],remaining=145,machine_warnings=103,new_warnings=added,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch148_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('355 confirmed / 145 remaining',pages)
