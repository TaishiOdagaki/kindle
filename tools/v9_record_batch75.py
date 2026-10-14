"""Record source acquisition and verified partial checkpoint for batch75."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');targets={'Q_3_015','Q_3_016','Q_3_017','Q_4_072'}
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');r=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(r)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
f=p/'ledger.csv';old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records(f.read_bytes()))
f.write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
f=p/'README.md';s=f.read_text()
for x,y in [('175問','179問'),('74問','73問'),('251問','248問'),('188問1506箇所','192問1541箇所'),('188問を','192問を')]:s=s.replace(x,y)
f.write_text(s)
report='''\n\n## 第75バッチ（2026-10-14）

Selinker（1988）Papers in Interlanguageの全130頁PDFをERICから取得。本人改訂版の印刷27〜29・75〜77頁（PDF31〜33・79〜81頁）の本文と版面を照合し、Q_3_015・016・017、Q_4_072を改訂した。1972年原誌の本文そのものとは区別する。中間言語を別体系とする仮説を、常に目標言語へ発達し続けるという保証と同一視しない。観察期間内の安定、永久的化石化の判定、原因の推定を分離した。

Q_3_017は、永久的化石化の確定例から、同条件・複数年の観察による長期的安定の判別問題へ改訂。日本語使用歴15年や通じるという情報だけで化石化と原因を確定しない。即時改善から将来の再出現不能を導く説明、正用→誤用の二時点だけをU型発達とする説明も除去。架空の観察例であり、実在学習者の診断ではない。Q_4_072は、安定と永久性の見極めを著者自身が研究課題として挙げる点を問う。

4問35箇所を追加。確認済み179・修正必要73・要追加確認248、残件321。累積192問1541箇所。全500問・500解説、正答番号、未改訂問題、v8原本ハッシュを保持。全4問の設問・全4肢・全4解説を独立判定し、正答不存在・複数正答の危険を検討した。公開可否の回帰検査8条件を通過。機械警告43件（44件からQ_3_017のA1が解消）、新規警告なし。残存警告や未確認問題は一括承認しない。

documentsのrender_docx.pyと復旧したNoto Sans JP Static Regular400によりQAコピー401頁を描画し、44・45・82・242・243・281・282頁の7頁を直接画像目視。対象4問の設問・全4肢・正答・全4解説に日本語欠字・重なり・切れなし。Q_3_016の解説は242〜243頁、Q_4_072の解説は281〜282頁に分かれるため最終整形時の候補として残す。原稿書式は維持し、フォント指定はQAコピーのみ。全401頁の最終目視・最終v9は未了。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第75バッチの取得資料（2026-10-14）

| ID | 資料・URL | 照合箇所 | 取得段階と限界 | 対象 |
|---|---|---|---|---|
| S140 | Larry Selinker（1988）[Papers in Interlanguage ERIC公開PDF](https://files.eric.ed.gov/fulltext/ED321549.pdf)、[ERIC書誌ED321549](https://eric.ed.gov/?id=ED321549)、SEAMEO Regional Language Centre Occasional Papers44 | 第3章の印刷27〜29頁：学習者の発話から仮定する別体系、五つの過程、再出現。第5章末の印刷75頁：観察された安定と永久的化石化の見極め。第6章冒頭の印刷76〜77頁：体系的発達停止という一般的定義と、初期提案・仮説・研究課題の整理 | 全130頁PDF取得、上記6頁を画像精読。1988年の本人改訂論集で、序文は収録論文を改訂したと明記。1972年原誌本文そのものを取得したとは扱わない。第6章の原版はLamendella共著1978年論文で、今回使用したのは1988年改訂版。先天構造、成功者5％、全学習者への必然性などは承認範囲外。 | Q_3_015・016・017、Q_4_072 |

PDFには本文上部の印刷頁に加え、下部にERICの通し頁がある。例：PDF79頁は印刷75頁。OCRが下部の79・80を本文頁として抽出することがあるため、今回の頁指定は版面上部で検証した。台帳原文はv8スナップショットであり、改訂はchanges.jsonと累積作業稿を参照する。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第75バッチ
復旧したNoto Sans JP Static Regular400をQAコピーだけに適用し、documentsのrender_docx.pyで全401頁PNGを生成。44・45・82・242・243・281・282頁の7頁を直接画像目視。4問の設問・全4肢・正答・全4解説に日本語欠字・切れ・重なりなし。Q_3_016解説は242〜243頁、Q_4_072解説は281〜282頁に分割され、最終整形時の改頁見直し候補。原稿書式は維持。全401頁の最終画像目視は未了。
''')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
cs=json.loads((p/'changes_batch75.json').read_text());text=re.sub(r'\s+','',Path('/tmp/batch75.txt').read_text())
missing=[e['after'] for e in cs if re.sub(r'\s+','',e['after']) not in text];assert not missing,missing
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==43
pages=[44,45,82,242,243,281,282]
e={'batch':75,'base_commit':'a38534bacb1fbbdab9caf4678fcea80043f77f85','questions':sorted(targets),'edits':35,'status_counts':{'確認済み':179,'修正必要':73,'要追加確認':248},'remaining':321,'independent_answers':{'Q_3_015':3,'Q_3_016':1,'Q_3_017':4,'Q_4_072':3},'sources':{'S140':{'url':'https://files.eric.ed.gov/fulltext/ED321549.pdf','sha256':sha('/tmp/selinker1988.pdf'),'pdf_pages':130,'edition':'1988 revised collection, not 1972 journal original','image_verified_page_map':{'27':31,'28':32,'29':33,'75':79,'76':80,'77':81},'scope':'別体系・過程の区別・観察された安定と永久性の区別。日本語事例は本書の架空の観察例。'}} ,'machine_warnings':43,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':401,'visually_reviewed_pages':pages,'full_visual_qa_completed':False,'changed_strings_missing_in_pdf':missing,'font':'Noto Sans JP Static Regular400 QA copy only','font_sha256':sha('/tmp/lo-ja/libreoffice/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha('/tmp/batch75-qa/batch75.pdf'),'page_sha256':{str(i):sha(f'/tmp/batch75-qa/page-{i}.png') for i in pages},'release_ready':False}
(p/'evidence/batch75_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
