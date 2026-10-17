"""One-time checkpoint after direct changed-page review; partial sources gated."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa152';targets={'Q_4_098','Q_4_104'};decision_targets=targets|{'Q_4_094'}
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in decision_targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':363,'修正必要':5,'要追加確認':132}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==105 and machine['issues']==prior
cs=json.loads((p/'changes_batch152.json').read_text());assert len(cs)==18
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==decision_targets and d['Q_4_094']['status']=='要追加確認'
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
_,q,a=qa.audit(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'))
for k in targets:
 rows=[c for c in cs if c['id']==k]
 assert html.unescape(q[k]['stem'])==next(c['after'] for c in rows if c['field']=='stem')
 assert int(a['A_'+k[2:]]['ans'])==d[k]['independent_answer']
 for field,values in [('options',q[k]['opts']),('explanations',a['A_'+k[2:]]['txt'])]:assert [html.unescape(t) for t in values]==[c['after'] for c in rows if c['field']==field]
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('361問','363問').replace('134問','132問').replace('357問3071箇所','359問3089箇所').replace('357問を部分修正','359問を部分修正');f.write_text(s)
report='''

## 第152バッチ（2026-10-18）

Q_4_098・Q_4_104の2問を18箇所改訂し、設問・全4肢・独立正答・全4解説を取得した本文へ照合。確認済み363・修正必要5・要追加確認132、残137問。累積359問3089箇所、500問維持。Q_4_094も資料取得段階を更新したが、要追加確認を維持し、作業稿の当該問は変更しない。

Q_4_098は、S214 CompassのDrama・Role-playing・Simulations節の全本文を再取得・精読。役割交換の効果が一律に高まるという旧説明をこの資料で実証したとは扱わず、同じロールプレイ学習の実施上の配慮へ限定した。役から離れる時間、本人が望まない露出や疎外を避ける配慮、傷ついた場合の真剣な対応と謝罪・説明、主に即興という定義、人物像と情報源を批判的に振り返る問いを全4肢・解説へ照合。独立正答1。

Q_4_104は、S216 Developing intercultural competence through education（2014）の第5章37–46頁を通読し、41頁（PDF42頁）を全頁画像照合。S214と併せ、文化事例を扱う指導で固定観念を強めないという学習領域を保ち、根拠本文が直接扱うロールプレイでの検討を明示した。過度一般化の回避、人物像が本物らしいか固定観念かという問い、文化的な違いが人間の価値を下げないという説明を4肢・全解説へ照合。旧解説の「あらゆる多視点学習で他参加者との集団討議が不可欠」という一般化を撤回。未取得のクリティカル・インシデント法の原著・普遍的定義を承認したものではない。独立正答2。刊行書の著作権頁は著者の見解が必ずしも欧州評議会の公式政策を反映しないと明記しており、その区別も保った。

Q_4_094は、S215開発者側の2006年ニュースレターのBarnga紹介節全体を取得・精読した。文化間での解釈の相違の概略は記載されているが、完全な実施・振り返りマニュアルではない。言語禁止、筆談、移動、各組のルールなどの全手順を紹介記事から推測で承認しない。リンク先thiagi.com/barngaと旧archiveの候補は今回取得できず、要追加確認のままとし、追加で必要な資料をdecisionsと台帳へ明記した。紹介本文だけを問う改訂案も検討したが、元の実施手順の根拠確認とは別になるため採用しなかった。

S216の旧coe.int/t/dg4/.../Pestalozzi3.pdfはプログラム入口のHTMLへ転送されるため、その応答をPDF本文として使用しない。公式刊行一覧と検索で同定したrm.coe.intのPDFを別に取得し、PDF署名・132頁の整合性を確認した。英仏合冊全132頁を精読したとはせず、読了範囲を証跡へ限定記録。原資料本文は転載しない。

両設問がWord上で各1段落であることを変更前に確認。旧3071件の累積履歴を不変に保って追記し、安全な再構成・台帳再生成を実行。v8不変、500問の構造・既存キー・正誤タグ・早見表・リンク・影響外の問の本文、公開判定回帰8条件・置換回帰4条件を検査。機械警告105件で前回一覧から増減なし。台帳原文はv8スナップショット、改訂後本文はchangesと作業稿を参照。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列18件を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。残137問の照合と全頁最終QAは未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第152バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第152バッチ（2026-10-18）

- S214 Compass公式HTMLを再取得しDrama・Role-playing・Simulations節の全本文を精読。Q_4_098の安全・役から離れる時間・人物像の振り返りと、Q_4_104の情報源と固定観念の批判的検討へ適用。ページ全体・全書の通読ではない。
- S215 [THIAGI GAMELETTER August 2006 — Barnga: 25th Anniversary Edition](https://thiagi.net/archive/www/pfp/IE4H/august2006.html)。開発者側ニュースレターのGame AnnouncementからOther Details末までを精読。これは紹介記事であり完全な実施規則ではない。Q_4_094の学術承認には使わず、同問は要追加確認のまま。
- S216 Josef Huber and Christopher Reynolds編、Martyn Barrettほか計5名寄稿（2014）[Developing intercultural competence through education](https://rm.coe.int/16808ce258)、Council of Europe Publishing、Pestalozzi Series No.3、ISBN978-92-871-7745-2。英仏合冊132頁PDFを取得。標題・著者・著作権・目次および印刷37–46頁（PDF38–47頁）の全本文を通読し、印刷41頁を画像照合。Q_4_104の4肢・4解説の根拠。著者の見解と公式政策を同一視せず、実証研究の効果を個別検証したとはしない。旧URLの入口HTMLは根拠PDFとして不使用。全132頁精読ではない。
- 原バイトSHA256・取得範囲・限界はevidence/batch152_sources.json。資料本文は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=152,base_remote_commit='1acc0a72b920035c0d4d399b2796d99a658146f4',fully_rejudged=sorted(targets),partial_source_only_kept_unverified=['Q_4_094'],decision_rows_updated=sorted(decision_targets),edits=18,independent_answers={k:d[k]['independent_answer'] for k in targets},sources=['S214','S215','S216'],status_counts=m['status_counts'],remaining=137,machine_warnings=105,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch152_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('363 confirmed / 137 remaining',pages)
