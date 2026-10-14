"""Record batch74 evidence, tests and partial visual QA."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');targets={'Q_3_012','Q_3_013','Q_3_014','Q_M_015'}
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
for x,y in [('171問','175問'),('255問','251問'),('184問1471箇所','188問1506箇所'),('184問を','188問を')]:s=s.replace(x,y)
f.write_text(s)
report='''\n\n## 第74バッチ（2026-10-14）

Baddeley（2012）本人による論文全文（付属頁を含む33頁、本文1〜29頁）を取得し、作動記憶の定義、音韻ループ、視空間スケッチパッド、中央実行系、二重課題実験の経緯を本文・画像へ照合。Q_3_012・013・Q_M_015を改訂した。1974年章・2000年論文本体の取得とは区別する。Q_3_013は、聴解が常に読解より高負荷・上級者は常に空き容量が大きい・保持と処理は完全な単一資源を奪い合うという未支持の一般化を除き、同じ学習領域の二重課題と多成分モデルの解釈に改訂した。

Squire（2004）の本人公開7頁PDFを取得。172頁の単語補完の教示条件、173頁図1と174頁の意味・エピソードの区別を照合し、Q_3_014を改訂。単語補完という表面的課題だけで潜在記憶を測ったと断定しない。言語スキル全般の一括分類や社会的プライミング一般は承認範囲外。

4問35箇所を追加。確認済み175・修正必要74・要追加確認251、残件325。累積188問1506箇所。500問・500解説、正答番号、未改訂問題、v8原本のSHA256保持検査と公開可否8条件を通過。全4問の全4肢・全4解説を独立判定。全問の正しさが確定したという意味ではない。

再構成時、同じ旧解説に2箇所が一致して安全検査が停止し、作業稿は保持された。新規変更にbookmarkのblock_contextを追加し、対象ブロックだけに適用。v9_rebuild.pyは指定がある場合だけブロックで絞り込む。回帰検査で前回コミットdcb9598の本文XMLとバイト単位で一致する再構成を確認した。初回判断スクリプトは再実行していない。

機械警告44件。新規S2のQ_M_015は「何と呼ぶか」という正常な問いの文末が正規表現に未登録のためであり、設問・全4肢・正答2・全4解説の対応を画像と本文で確認。未確認問題の既存警告は一括承認しない。

Noto Sans JP Static Regular 400を復旧し、原稿書式は維持してQAコピーだけフォントを指定。最終の部分改訂稿を401頁へ描画し、43・44・173・241・242・374・375頁の7頁を直接画像目視。改訂4問の設問・全4肢・全4解説の日本語欠字・切れ・重なりなし。Q_M_015の解説が374〜375頁に分割されるため最終整形候補。全401頁の最終目視は未了、最終v9未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第74バッチの取得資料（2026-10-14）

| ID | 資料・URL | 照合箇所 | 取得段階・限界 | 対象 |
|---|---|---|---|---|
| S138 | Alan Baddeley（2012）[Working Memory Theories Models and Controversies 大学教材公開PDF](https://jontalle.web.engr.illinois.edu/MISC/ReadingGroup.11/Papers/Baddeley-WorkingMemory.12.pdf)、Annual Review of Psychology 63,1–29、DOI10.1146/annurev-psych-120710-100422 | 4頁の保持と操作の区別、6頁の二重課題とモデル形成、7頁の枠組みと音韻ループ、13〜15頁の視空間・注意・第4成分への経緯 | 全33頁PDF取得。6・7・13〜15頁画像精読。提唱者自身による2012年の説明という一次資料。1974年章や2000年論文本体の全文取得とはしない。L2習熟度別・聴解対読解の一律の因果比較へ拡大しない。 | Q_3_012・013、Q_M_015 |
| S139 | Larry R. Squire（2004）[Memory systems of the brain A brief history and current perspective 著者所属大学公開PDF](https://whoville.ucsd.edu/PDFs/384_Squire_%20NeurobiolLearnMem2004.pdf)、Neurobiology of Learning and Memory82,171–177、DOI10.1016/j.nlm.2004.06.005 | 172頁の単語補完課題と想起教示、173頁の図1、174頁の意味・エピソード記憶の区別 | 全7頁本文取得、172〜174頁画像照合。著者本人の理論的整理。語の先行提示の意識と検索時の意識を混同せず、社会的プライミング等の全類型を一括承認しない。 | Q_3_014 |

S16のBaddeley（2000）は依然抄録段階。今回のS138取得で2000年本文も取得したことにはしない。台帳の原文はv8スナップショットであり、改訂本文はchanges.jsonと累積作業稿を参照する。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第74バッチ
Noto Sans JP Static Regular 400を復旧してQAコピーに適用し、documentsのrender_docx.pyで全401頁PNGを生成。43・44・173・241・242・374・375頁の7頁を直接画像目視。改訂4問の設問・全4肢・正答・全4解説に欠字・重なり・切れなし。Q_M_015解説は374〜375頁にまたがり、最終整形時の見直し候補。再構成検査が一度停止した時点の旧稿描画と、検査を通過した新稿の描画は別ディレクトリに分けた。証拠JSONは新稿の画像とハッシュのみを記録。原稿書式は維持し、フォント指定はQAコピーだけ。全401頁の最終画像目視は未了。
''')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
render=Path('/tmp/batch74-final-qa');pages=[43,44,173,241,242,374,375]
text=re.sub(r'\s+','',Path('/tmp/batch74-final.txt').read_text())
cs=json.loads((p/'changes_batch74.json').read_text());missing=[e['after'] for e in cs if re.sub(r'\s+','',e['after']) not in text]
assert not missing,missing
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==44
e={'batch':74,'base_commit':'dcb9598a8f5557ce372f674d5b07bfb54db393cd','questions':sorted(targets),'edits':35,'status_counts':{'確認済み':175,'修正必要':74,'要追加確認':251},'remaining':325,'independent_answers':{'Q_3_012':1,'Q_3_013':4,'Q_3_014':3,'Q_M_015':2},'sources':{'S138':{'url':'https://jontalle.web.engr.illinois.edu/MISC/ReadingGroup.11/Papers/Baddeley-WorkingMemory.12.pdf','sha256':sha('/tmp/baddeley2012.pdf'),'pdf_pages':33,'reviewed_print_pages':[4,6,7,13,14,15],'images_reviewed':[6,7,13,14,15]},'S139':{'url':'https://whoville.ucsd.edu/PDFs/384_Squire_%20NeurobiolLearnMem2004.pdf','sha256':sha('/tmp/squire2004.pdf'),'pdf_pages':7,'reviewed_print_pages':[172,173,174],'images_reviewed':[172,173,174]}},'machine_warnings':44,'manual_false_positive':'Q_M_015 S2：何と呼ぶかは正常な問い。正答2・全4肢・全4解説を照合。','readiness_test':'8 cases passed','rebuild_regression':'dcb9598 document.xml byte-identical','render_pages':401,'visually_reviewed_pages':pages,'full_visual_qa_completed':False,'changed_strings_missing_in_pdf':missing,'font':'Noto Sans JP Static Regular400 QA copy only','font_sha256':sha('/tmp/lo-ja/libreoffice/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'batch74-final.pdf'),'page_sha256':{str(i):sha(render/f'page-{i}.png') for i in pages},'release_ready':False}
(p/'evidence/batch74_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
