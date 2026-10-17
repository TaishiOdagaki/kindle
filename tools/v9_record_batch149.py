"""Record two evidence-gated rejudgments after direct changed-page inspection."""
import json,hashlib,subprocess,io,csv,html,sys
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from docx import Document
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa149b';targets={'Q_O_032','Q_4_103'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':357,'修正必要':8,'要追加確認':135}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues']
added=[x for x in machine['issues'] if x not in prior]
assert len(machine['issues'])==104 and len(added)==1 and added[0][:2]==['P1','Q_4_103']
assert all(x in machine['issues'] for x in prior)
cs=json.loads((p/'changes_batch149.json').read_text());assert len(cs)==22
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
paragraphs=[p.text for p in Document(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx').paragraphs]
removed=[c for c in cs if c.get('remove_paragraph')];assert len(removed)==4
assert all(c['before'] not in paragraphs for c in removed)
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('355問','357問').replace('修正必要9問','修正必要8問').replace('| 修正必要 | 9問 |','| 修正必要 | 8問 |').replace('136問','135問').replace('352問3012箇所','353問3034箇所').replace('352問を部分修正','353問を部分修正');f.write_text(s)
report='''

## 第149バッチ（2026-10-18）

Q_O_032・Q_4_103の2問を22件の順序付き編集で改訂し、設問・全4肢・独立正答・全4解説を取得した根拠本文へ照合した。確認済み357・修正必要8・要追加確認135、残143問。累積353問3034箇所、500問維持。

Q_O_032はS118 Corder（1967）の原誌166–169頁を再精読し、168頁を画像照合。表面的に逸脱しない形でも状況と意味の対応が必要だという論述と、誤用の多くは母語体系と関係するが全てではないという限定に照合した。母語対照だけを正答とし、ケースの日本語をなお文法的誤用と扱った旧解説を撤回。著者の議論を問う設問へ改訂し、個別例の誤用や原因そのものを確定したとはしない。正答4は不変。sources.mdで母語に関する段落の所在を169頁（PDF11頁）としていた誤記を168頁（PDF10頁）へ訂正した。

Q_4_103はS213 欧州評議会RFCDC Volume1（2018）印刷41–50頁の本文・注記を精読し、41・45・48頁を画像照合。国や文化の特定も本人への確認もない会話から、母文化での形式的辞退が原因だと断定し、語彙理解の可能性を誤答として排除していた旧問題を撤回した。同じ異文化事例の背景検討という学習領域を保ち、判断の保留、複数解釈、相手の視点と利用可能な証拠を確認する対応を問う。正答3は不変。枠組みの事例への適用であり、特定の文化規範や会話の実際の原因の実証ではない。カルチャー・アシミレーターという方法の原著取得・承認もしていない。

Q_4_103の旧設問が5段落であったため、先頭を統合設問へ置換し、旧続き4段落の削除をchangesに明示した。初回再構成は、削除より先に選択肢の隣接文脈を検査したため停止。旧3012件の履歴を変えず、新規22件内で続き4段落の削除を選択肢の置換より前へ並べ直して復旧した。一度限りのapplyを再実行して判断を上書きしていない。失敗後に走ったcheckpointの数値は再構成成功後に再生成し、古いDOCXから生成を始めたqa149は新稿QAから除外、空のqa149bへ新規描画した。

機械警告104件（旧103件維持、新規P1・Q_4_103が1件）。正答解説の末尾が「会話の原因が特定の文化規範だと実証されたという意味ではありません」という適用範囲の注意で終わるため、否定語末検出に該当した。選択肢3の妥当性の否定ではなく、全4解説の対応・正誤タグを直接確認した。警告を隠すための文面変更や検査除外はしない。

v8不変、500問の構造・既存キー・タグ・早見表・リンク・影響外の問の本文、公開判定回帰8条件・置換回帰4条件を検査。台帳原文はv8スナップショット、改訂はchangesと累積作業稿を参照。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終非空変更文字列18件を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。全頁最終QAと残143問の学術照合は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第149バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';s=f.read_text();s=s.replace('S118追加照合：原誌169頁（PDF11頁）の末尾で','S118追加照合：原誌168頁（PDF10頁）の末尾で');f.write_text(s+'''

## 第149バッチ（2026-10-18）

- S118 Corder（1967）原論文をERICから全12頁再取得。原誌166–169頁本文を再精読し、168頁（PDF10頁）全体を画像照合。非逸脱形の状況との意味の対応、母語体系との関係は多くにあるが全てではないという限定をQ_O_032へ適用。上記母語関連段落の頁番号169（PDF11）は168（PDF10）の誤記として訂正。全12頁の今回の精読や個別日本語例文の原因の実証とは扱わない。
- S213 Council of Europe（2018）[Reference Framework of Competences for Democratic Culture, Volume 1: Context, concepts and model](https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c)。全89頁PDFを公式サイトから取得。印刷41–50頁（PDF43–52頁）本文と注記を全て精読し、41・45・48頁を画像照合。41頁の開放性の判断保留、45頁の曖昧さへの寛容性と複数解釈、47頁の批判的思考と証拠・前提の点検、48頁の共感と相手の視点をQ_4_103の全4肢・解説へ照合。仮想事例への教育的適用であり、特定の国・文化の習慣や原因の実証、カルチャーアシミレーターの原著承認ではない。全89頁精読ではない。
- URL、取得範囲、取得原バイトのSHA256はevidence/batch149_sources.json。原資料本文は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=149,base_remote_commit='821220bfd58a20b48d46af6e07ac6381483d3eca',fully_rejudged=sorted(targets),edits=22,explicit_removed_stem_paragraphs=4,independent_answers={k:d[k]['independent_answer'] for k in targets},sources=['S118','S213'],status_counts=m['status_counts'],remaining=143,machine_warnings=104,new_warnings=added,new_warning_review='P1: Correct explanation ends in a limitation on causal attribution, not a denial of the correct option. All four explanation/tag alignments inspected; warning retained.',operational_recovery='Reordered only batch149 removals ahead of option context checks after rebuild assertion. Initial 3012 changes preserved. Checkpoint regenerated after successful rebuild. Stale qa149 excluded; fresh qa149b used.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch149_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('357 confirmed / 143 remaining',pages)
