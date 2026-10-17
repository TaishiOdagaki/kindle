"""One-time evidence record after direct changed-page visual review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa151';targets={'Q_4_095','Q_4_096'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':361,'修正必要':5,'要追加確認':134}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues']
assert len(machine['issues'])==105 and machine['issues']==prior
cs=json.loads((p/'changes_batch151.json').read_text());assert len(cs)==18
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
_,q,a=qa.audit(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'))
for k in targets:
 rows=[c for c in cs if c['id']==k]
 assert html.unescape(q[k]['stem'])==next(c['after'] for c in rows if c['field']=='stem')
 assert int(a['A_'+k[2:]]['ans'])==d[k]['independent_answer']
 for field,values in [('options',q[k]['opts']),('explanations',a['A_'+k[2:]]['txt'])]:
  assert [html.unescape(t) for t in values]==[c['after'] for c in rows if c['field']==field]
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('359問','361問').replace('修正必要6問','修正必要5問').replace('| 修正必要 | 6問 |','| 修正必要 | 5問 |').replace('135問','134問').replace('355問3053箇所','357問3071箇所').replace('355問を部分修正','357問を部分修正');f.write_text(s)
report='''

## 第151バッチ（2026-10-18）

Q_4_095・Q_4_096の2問を18箇所改訂し、公式手引きの本文に基づいて設問・全4肢・独立正答・全4解説を確定。確認済み361・修正必要5・要追加確認134、残139問。累積357問3071箇所、500問維持。

S214欧州評議会CompassのUsing Compass for human rights educationページをHTMLで取得。General tips on running activitiesからManaging conflict節末までの本文を通読し、時間管理、安全、基本ルール、話合い、デブリーフィングと評価、フィードバック、抵抗、対立への対応を前後とともに精読した。検索抜粋だけで承認していない。全書や同ウェブページの全節を通読したとはしない。

Q_4_095は、感情→事実→原因→適用をKolbの4段階に帰属させた旧解説を撤回。未取得のKolb原著を判定したことにはせず、Compassが提案する活動と感情、自分自身と課題についての学び、今後の活用を振り返る問いに対象を限定した。参加者が話したくない内容を開示するよう強いない条件を明示。全ての体験活動に唯一の固定順序があるという一般化や、省略が必ず偏見を強化するという未実証の因果を残さない。独立正答2。

Q_4_096は、クラス内で発話が重なり不満が出たという同じ領域の仮想事例を保ち、国別規範や身勝手な性格を原因として断定した解説を撤回。本人たちが話せる範囲の状況・考えの確認、傾聴、全員の参加の機会、基本ルールの共同検討を問う形へ改訂した。特定の文化の劣等性や排除、記録からの単一原因の断定は手引きの方針に合わないと判定。これは手引きへの適合と事例への適用であり、原因の実証や対応の効果検証ではない。独立正答3。

今回の両設問がWord上で各1段落であることを変更前に確認。累積履歴を追記し、旧3053件を不変に保持。安全な再構成・台帳再生成を順に実行し、v8不変、500問の構造・既存キー・正誤タグ・早見表・リンク・影響外の問の本文、公開判定回帰8条件・置換回帰4条件を検査した。機械警告105件で前回の一覧から増減なし。台帳原文はv8スナップショット、改訂後本文はchangesと作業稿を参照。

画像291頁は初回表示時にPNGの途中破損を検出したためQAには使用せず、同じ最新PDFからページを再生成し、画像全体の読込みと目視をやり直した。再生成後の画像ハッシュを証跡に記録する。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列18件を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。残139問の照合と全頁最終QAは未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第151バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第151バッチ S214（2026-10-18）

Council of Europe [Compass — Using Compass for human rights education](https://www.coe.int/en/web/compass/using-compass-for-human-rights-education)。公式HTML全頁を取得し、General tips on running activitiesからManaging conflict節末までの本文を通読。Managing time、Creating a safe environment、Setting ground rules、Facilitating discussions、Debriefing and evaluation、Giving feedback、Resistance from the participants、Managing conflictを前後とともに精読した。Q_4_095の振り返りと今後の活用への問い・時間確保・強制開示を避ける条件、Q_4_096の傾聴・意見の確認・共同ルール・安全と参加に全4肢・解説を照合。Compass全書や当ページ全節の精読ではなく、Kolb原著や国別規範、効果の実証研究も取得・承認していない。原バイトSHA256・取得範囲はevidence/batch151_sources.json。資料本文は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=151,base_remote_commit='5d79c74ab6bcfacafc9c9e7531a680547f24a7a8',fully_rejudged=sorted(targets),edits=18,independent_answers={k:d[k]['independent_answer'] for k in targets},sources=['S214'],status_counts=m['status_counts'],remaining=139,machine_warnings=105,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch151_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('361 confirmed / 139 remaining',pages)
