"""Record role-language and jargon body-text audit after changed-page QA."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa140';targets={'Q_M_010','Q_M_012'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':345,'修正必要':16,'要追加確認':139}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==99
added=[x for x in machine['issues'] if x not in prior];assert added==[['P1','Q_M_010','(正)3の解説が否定で終わる/肯定の(誤)がある: [2, 4]']]
assert all(x in machine['issues'] for x in prior)
cs=json.loads((p/'changes_batch140.json').read_text());assert len(cs)==16
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==16 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('| 確認済み | 343問 |','| 確認済み | 345問 |').replace('修正必要18問','修正必要16問').replace('| 修正必要 | 18問 |','| 修正必要 | 16問 |').replace('341問2895箇所','343問2911箇所').replace('341問を部分修正','343問を部分修正');f.write_text(s)
report='''

## 第140バッチ（2026-10-18）

Q_M_010・Q_M_012を16箇所改訂し、独立正答は3・1を確定。金水敏（2011年12月）「役割語と日本語教育」の原論文全8頁を取得。画像形式でテキスト抽出が0文字だったため、印刷34–41頁の全頁を画像で精読した。34頁の定義、36頁の現実性、38–39頁のスタイルとの連続性・発言引用例を根拠に、役割語をフィクションだけに限定する説明を撤回。位相語を排他的な誤答とする競合を避け、概念の説明そのものを全4肢で問う形に改訂した。2003年の書籍全冊は未取得であり取得済みとは扱わない。

ジャーゴンはGoogleの公式文書作成ガイド本文から、専門集団の用語・理解されにくい傾向・一部は広く理解されることを照合。「集団内部でのみ通じる」を必要条件とする説明を撤回。国語研の署名付き解説2件の本文全節で標準語・共通語・地域方言の定義を照合し、分類観点を設問に明示。生得説の未照合の補助説明を撤去し、同じ言語変異の領域の地域方言へ変更。別の分類軸でも同じ用語を捉え得る可能性を否定しない。

最初に取得した別の6頁講演PDF（Kinsui_JPN.pdf）はEOF欠損で完全なPDFとして読み込めなかったため、監査承認には採用しない。原論文の5頁目の初回PNGも破損検出のため除外し、当該頁を再描画して完全読込みと画像精読を実施した。論文の画像や本文をリポジトリへ転載せず、原バイトSHA256と取得・照合範囲を記録。

確認済み345・修正必要16・要追加確認139、残155問。累積343問2911箇所、500問維持。台帳原文はv8スナップショットで改訂はchangesと作業稿を参照。v8不変、500問の構造・正解番号・タグ・早見表・リンク・影響外本文の不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。

機械警告は98→99件。追加P1はQ_M_010で、正答3の「フィクションの中だけに限定されるわけではありません」という否定形の文末を正答の否定と誤認し、誤答2・4の解説に正しい補足説明があることを検出したもの。正答3は本文の定義と整合し、2・4はフィクション限定・実使用調査との混同が誤りであることを独立確認。誤検出の理由を記録し、警告を消す目的で学術的判断を変更しない。従来98件はそのまま保持。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全16変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。既存校正手順・documentsに基づく変更範囲QA。全頁最終目視と残155問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第140バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第140バッチ S201 S202 S203（2026-10-18）

- S201 金水敏（2011年12月）「役割語と日本語教育」『日本語教育』150、34–41頁。[原論文全8頁](https://www.jstage.jst.go.jp/article/nihongokyoiku/150/0/150_34/_pdf/-char/ja)を取得し、全8頁を画像で精読。定義（34頁）、現実性（36頁）、スタイルとキャラクタ・日常会話での発言引用（38–39頁）をQ_M_010へ照合。要旨のみではなく本文で承認。論文に引用される2003年書籍や他研究の全冊は未取得。別の講演PDFの欠損取得は承認根拠に含めない。
- S202 Google [Jargon 文書作成ガイド](https://developers.google.com/style/jargon)、更新表示2025-06-25。自動Page Summaryを除く本文全体で専門集団の用語・理解されにくい傾向・広く理解される場合を確認し、Q_M_012の絶対限定を修正。Googleの文書作成上の推奨を普遍的な語史や言語変化の法則に広げない。
- S203 三井はるみ、国立国語研究所 [共通語と標準語](https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-138/)（2021-07-19再掲）・[方言の定義](https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-137/)（2021-07-13再掲）の本文全節を取得。規範性・方言を越えた通用性・地域差の着眼点、現実には標準語と共通語に明確な実体差がないこと、地域内の多様性を確認。初出2003年書籍全冊の取得ではない。

原バイトSHA256と照合範囲はevidence/batch140_sources.json。原文非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=140,base_commit='3670230efac865859ad8e7949caabc03bf4aa7b1',fully_rejudged=sorted(targets),edits=16,independent_answers={'Q_M_010':3,'Q_M_012':1},sources=['S201','S202','S203'],status_counts=m['status_counts'],remaining=155,machine_warnings=99,new_warnings=added,new_warning_review='P1 false positive: negated fiction-only restriction in correct explanation; true explanatory content in wrong-option explanations does not make those options correct.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_pdf_page_sha256={str(n):sha(root/(f'kinsui2011-140-{n}.png' if n!=5 else 'kinsui2011-140-5-retry.png')) for n in range(1,9)},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch140_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('345 confirmed / 155 remaining',pages)
