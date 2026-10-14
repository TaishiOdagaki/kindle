"""Record batch73 verification without rewriting unrelated CSV records."""
from pathlib import Path
import json,hashlib,subprocess,io,csv
p=Path('audit/v9')
r=p/'README.md';s=r.read_text()
for x,y in [('169問','171問'),('76問','74問'),('182問1453箇所','184問1471箇所'),('182問を','184問を')]:s=s.replace(x,y)
r.write_text(s)
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');r=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(r)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
f=p/'ledger.csv';old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records(f.read_bytes()));targets={'Q_3_021','Q_3_022'}
f.write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
report='''\n\n## 第73バッチ（2026-10-14）

Q_3_021・022の設問、全4肢、全4解説をS15の原著抜粋86・88〜90頁へ照合し、2問18箇所を改訂。独力での実際の発達水準と支援下での潜在的水準を区別し、「常に変化する」「既習課題は新たな学びを生まない」という過度の一般化を除去。日本語授業の例は定義を適用した本書の例であり、特定授業の実証結果ではない。一回の支援下の完成から、その後の独力での習得を保証しない。

確認済み171、修正必要74、要追加確認255、残件329。累積184問1471箇所。全500問・500解説、正答番号、未改訂本文、v8原本ハッシュの保持検査と公開可否8条件の回帰検査を通過。機械警告43件。今回のQ_3_022のP1は正答解説末尾の習得保証を避ける限定と誤答解説の文末表現に反応したもの。全4肢・正誤タグとの対応を手動確認し誤検出と判定。他の警告を一括承認しない。

Noto Sans JP Staticの一時QAコピーを401頁へ描画し、46・47・244・245・246頁の5頁を画像目視。対象の設問・全4肢・全4解説に欠字・重なり・切れなし。Q_3_021解説の244〜245頁への分割は最終整形の見直し候補。全401頁の最終目視は未了。作業稿は最終版ではない。

作動記憶のBaddeley（2000）の大学公開PDFリンクは404で本文未取得。Q_3_012・013は承認せず要追加確認を維持。Wood・Bruner・Ross（1976）の原論文PDFは取得したが、当該論文を新たな確認済み判定の根拠にはまだ使用していない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n### 第73バッチ S15再照合（2026-10-14）
New Learning掲載のVygotsky（1978）原著抜粋の本文を再取得。86頁の独力／成人の指導・より有能な仲間との協働による水準差、88〜90頁の学習と発達の区別をQ_3_021・022の全4肢・全4解説へ照合。原著全冊を取得したとは扱わない。日本語作文の例は定義の適用例であり、個別教授法の効果を実証した事例とはしない。復習一般の無効、支援の必然的効果、常時変化は承認範囲から外す。
Baddeley（2000）追加候補 https://www2.psychology.uiowa.edu/faculty/hollingworth/prosem/Baddeley_2000.pdf は404。本文未取得としてS16の承認範囲は拡大しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第73バッチ
documentsのrender_docx.pyとNoto Sans JP Static Regular 400を使用したQAコピー全401頁を描画。46・47・244・245・246頁の5頁を直接画像目視し、改訂2問の設問・全4肢・正答・全4解説に日本語欠字・切れ・重なりなし。原稿書式は維持。Q_3_021解説は244〜245頁にまたがり、最終整形時の見直し候補。全401頁の最終目視は未了。
''')
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'
e={'batch':73,'questions':list(targets),'edits':18,'source_ids':['S15'],'source_scope':'掲載原著抜粋86・88〜90頁。全冊取得ではない','independent_answers':{'Q_3_021':3,'Q_3_022':2},'machine_warnings':43,'manual_false_positive':'Q_3_022 P1：正答の習得保証を否定する限定は正誤と矛盾しない','readiness_gate':'8 cases passed','render_pages':401,'visually_reviewed_pages':[46,47,244,245,246],'full_visual_qa_completed':False,'docx_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),'page_sha256':{str(i):hashlib.sha256(Path(f'/tmp/batch73-qa/page-{i}.png').read_bytes()).hexdigest() for i in [46,47,244,245,246]},'unresolved':['全残件329問','全頁最終QA','Q_3_012・013の本文取得・判定']}
(p/'evidence/batch73_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
