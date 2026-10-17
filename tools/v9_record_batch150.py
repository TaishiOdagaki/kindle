"""One-time checkpoint after direct visual inspection; retains warning evidence."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from docx import Document
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa150';targets={'Q_2_031','Q_3_034'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':359,'修正必要':6,'要追加確認':135}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues']
added=[x for x in machine['issues'] if x not in prior];assert len(machine['issues'])==105 and len(added)==1 and added[0][:2]==['P1','Q_3_034'] and all(x in machine['issues'] for x in prior)
cs=json.loads((p/'changes_batch150.json').read_text());assert len(cs)==19
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
paragraphs=[x.text for x in Document(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx').paragraphs]
removed=[c for c in cs if c.get('remove_paragraph')];assert len(removed)==1 and all(c['before'] not in paragraphs for c in removed)
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('357問','359問').replace('修正必要8問','修正必要6問').replace('| 修正必要 | 8問 |','| 修正必要 | 6問 |').replace('353問3034箇所','355問3053箇所').replace('353問を部分修正','355問を部分修正');f.write_text(s)
report='''

## 第150バッチ（2026-10-18）

Q_2_031・Q_3_034の2問を19件の順序付き編集で改訂し、S213欧州評議会RFCDC Volume1（2018）の本文と照合して全4肢・独立正答・全4解説を再判定。確認済み359・修正必要6・要追加確認135、残141問。累積355問3053箇所、500問維持。

Q_2_031は、うなずきという身体動作と声をパラ言語として一括した旧文面、日本語と他言語の相槌頻度、国別の身ぶりや視線の意味を一般化した旧解説を承認せず、同じ非言語的側面を含む会話の観察という学習領域で改訂した。RFCDCの聞く技能と観察する技能（48頁）の本文・全6項を再照合。話し方と身体動作、言語・非言語間の不一致、社会的文脈、同じ状況での個人間の反応の類似・相違に各肢・解説を対応づけ、正答3を確定。日本語の相槌の頻度の実証や専門用語パラ言語の分類境界の承認とはしない。

Q_3_034は、「国に帰ると」という旧条件に帰国時の不適応とアイデンティティ変容が両立し得た問題を改訂。未取得の帰国時のショックの理論を推測で否定せず、同じ文化的所属とアイデンティティの領域で、複数のつながりを大切にし、相手や場面によって強く意識する所属が変わるという仮想事例にした。S213印刷29–33頁の本文を精読し、29・30頁を画像照合。複数のアイデンティティ、国家以外の集団の文化、個人が利用する資源の部分性と意味づけの個別性、所属の主観的重要性の変動を全4肢・4解説に照合し、正答4を確定。心理的症状の診断、葛藤の必然性、留学生一般の実態調査ではない。

Q_3_034の設問が2段落であることを最初の再構成停止時に確認。未適用の新規記録の置換前を実際の先頭段落へ合わせ、旧問いの続き1段落を明示的に削除する記録を追加した。旧3034件の履歴は不変。一度限りのapplyは再実行せず、再構成成功後にのみ台帳・描画を再生成した。元の18件と補修を実行するスクリプトも残し、19件へ至る経緯を記録する。

機械警告105件（前回104件維持、新規P1・Q_3_034が1件）。正答解説末尾の「心理的な不適応や特定の症状を診断したものではありません」という適用範囲の注意が否定語末検出に該当。正答肢の否定ではなく、4解説と正誤タグの対応を直接確認した。警告を除外せず保持する。

v8不変、500問の構造・既存キー・タグ・早見表・リンク・影響外の問の本文、公開判定回帰8条件・置換回帰4条件を検査。台帳原文はv8スナップショット、改訂はchangesと累積作業稿を参照。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、非空の最終変更文字列18件を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。全頁最終QAと残141問の学術照合は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第150バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第150バッチ S213追加照合（2026-10-18）

RFCDC Volume1の印刷27–33頁（PDF29–35頁）全本文を追加通読、概念定義の29–33頁を精読。29・30頁を全頁画像で照合。29頁の個人・社会・文化のアイデンティティ、30頁の多様な集団への複数所属・個別性・社会的文脈や関心等による主観的重要性の変動をQ_3_034へ適用した。既読の48頁の本文と全6項を再照合し、Q_2_031の声・身体動作・不一致・社会的文脈・反応の類似と相違の観察に対応づけた。全89頁精読ではない。原資料SHA256と範囲・限界はevidence/batch150_sources.json。国別一般化や理論上の診断は承認せず、本文も転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=150,base_remote_commit='b28835fc330f718a66362ecdf3fc2d94908f61da',fully_rejudged=sorted(targets),edits=19,explicit_removed_stem_paragraphs=1,independent_answers={k:d[k]['independent_answer'] for k in targets},sources=['S213'],status_counts=m['status_counts'],remaining=141,machine_warnings=105,new_warnings=added,new_warning_review='P1: correct explanation ends with limitation on psychological diagnosis, not denial of option4. All explanation/tag alignments directly inspected; warning retained.',operational_recovery='Initial rebuild caught split Q_3_034 stem. New unpublished replacement metadata matched to actual first paragraph and explicit continuation removal added; prior3034 changes preserved; apply not rerun.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch150_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('359 confirmed / 141 remaining',pages)
