"""Record the six-question assessment audit and final batch78 partial QA."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');targets={'Q_4_052','Q_4_053','Q_4_056','Q_4_057','Q_4_058','Q_4_115'}
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
for x,y in [('186問','192問'),('73問','71問'),('241問','237問'),('199問1604箇所','205問1658箇所'),('199問を','205問を')]:s=s.replace(x,y)
f.write_text(s)
report='''

## 第78バッチ（2026-10-14）

GitHubの最新HEAD6c75628d477a0c7885cd2b6ca5a8cb0a584488e2を取得し、監査正本を引き継いだ。共同学会標準の全240頁と、波及効果の著者原発表稿の全23頁を取得。新しい一度限りのスクリプト78と78bを順に適用し、6問54箇所を改訂した。初期のreview/applyを再実行して既存判断を上書きしていない。

確認済み192・修正必要71・要追加確認237、残件308。累積205問1658箇所。500問・500解説、正答番号、影響外原文、v8原本ハッシュを保持。採用問題を削除せず、全6問の設問・全4肢・独立正答・全4解説を取得本文に照合し、正答不存在・複数正答の危険を再判定した。

Q_4_053はルーブリック一般を必ず複数観点マトリクスとする定義から、共同標準79頁の分析的採点に範囲を限定。観点ごとの独立した評価と得点を総合的採点の一得点と区別し、ルーブリック使用だけで採点者の判断や訓練が不要になるとの説明も認めない。採点者間信頼性の向上を無条件に保証する旧解説は除去。

Q_4_056は、得点の一貫性を完全一致の保証とせず、課題・実施機会・採点者などの変動を検討する概念へ明確化。再測定時の能力不変や前回実施の影響がないことという前提を補った。Q_4_057は古典的妥当性分類の混在から、指定用途に対する得点解釈を証拠と理論で支えるという2014年版の定義へ改訂。一用途の根拠が他用途へ自動的に一般化できるとはしない。

Q_4_058は、直接テストなら一般に正、難しすぎれば一般に負という効果の断定を除去。AldersonとWallの1992年発表稿に沿い、教える内容と方法、学び方、教師・学習者の個人差等を分け、影響を検証する視点を問う。列挙された仮説を実証済みの全員普遍則として扱わない。1993年原誌そのものを取得したとはしない。

Q_4_052は、規範準拠と基準準拠の得点解釈の比較対象を明示。実在のJLPTの制度区分や合格方式、共通テスト一般を一括して規範準拠とする未照合の説明は除去し、定義を問う問題へ改訂した。特定試験の現行仕様をこの共同標準だけで承認したわけではない。Q_4_115は、コンピュータによる実施方式とCATの適応的な項目選択を区別。問題プールからの選択を問題文の自動生成そのものとする混同を修正し、全CBTへの機能・セキュリティ効果・紙との同等性の一般化は除去した。

機械検査は500問・500解説を再確認、公開可否回帰8条件に合格。警告46件（従前45件）、解消0件・追加1件。新規Q_4_058 P1は、正答解説末尾で仮説を普遍的実証則とすることを否定したための極性検出。全4肢・全4解説とタグを直接照合し、独立正答2と一致を確認。検出器を弱めて警告を消さず、未解決の従前警告も保持。

日本語フォントがない環境だったため、Google FontsのNoto Sans JP可変フォントからRegular400を作成し、作業用LibreOfficeに復旧。documentsのrender_docx.pyでQAコピー400頁を描画し、PDFの埋込フォントNotoSansJPStaticを確認した。追補適用後の再描画が完全終了してから、74・75・76・98・99・273・274・275・276・298頁の10頁を直接画像目視。先行描画の画像と最新PDFを混在させず、最新版画像を再確認した。全54変更文字列のPDF反映を検査し、対象6問の欠字・切れ・重なりなし。

Q_4_115は設問末尾と選択肢が98〜99頁に分かれ、Q_4_053解説は273〜274頁、Q_4_058解説は275〜276頁にまたがる。最終整形時の改頁調整候補として残す。フォント変更はQAコピーだけで、原稿書式は維持した。全400頁の最終画像目視・最終v9は未了。台帳原文はv8スナップショット、改訂後はchanges.jsonと累積作業稿を参照する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第78バッチの取得資料（2026-10-14）

| ID | 資料・URL | 照合箇所 | 取得段階と限界 | 対象 |
|---|---|---|---|---|
| S142 | AERA・APA・NCME（2014）[Standards for Educational and Psychological Testing 公式全文](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf)、[公式オープンアクセス一覧](https://www.testingstandards.net/open-access-files.html) | 印刷11・14頁：指定用途に対する得点解釈・妥当性の統一的概念。33〜34頁：信頼性・精度、変動源と再測定の前提。79頁：採点基準・分析的/総合的採点・採点者の訓練等。215・217頁：適応型、CBT、CATの定義。218・221頁：基準準拠と規範準拠の得点解釈 | 全240頁公式PDF取得。上記9頁を本文・画像照合。2014年版として明示し、最新版・法的義務とは主張しない。個別試験や製品の現行仕様、全ルーブリックの効果保証、語彙文法以外の心理学的因果の実証には拡大しない。 | Q_4_052・053・056・057・115 |
| S143 | J. Charles Alderson・Dianne Wall（1992年2月）[Does Washback Exist? ERIC公開発表稿](https://files.eric.ed.gov/fulltext/ED345513.pdf)、[ERIC書誌ED345513](https://eric.ed.gov/?id=ED345513) | 印刷5〜6頁：テストの質から影響の質を単純に導く見方、動機づけと成果の複雑さ。8〜9頁：影響の要因を分けた仮説と個人差・検証の必要性 | 全23頁の著者発表稿取得。印刷5〜6・8〜9頁（PDF6〜7・9〜10頁）を画像精読。後の1993年Applied Linguistics掲載版の取得とは区別。仮説の列挙を実証済み普遍法則とは扱わず、引用される他の研究の本文取得ともみなさない。 | Q_4_058 |

S142の印刷頁にはPDF通し頁で10を加える（例：79頁＝PDF89頁）。S143は本文上部の印刷頁と下部のERIC通し頁が異なる（例：印刷5頁＝PDF6頁）。版面上部の番号で照合した。取得PDF全体は資料の同定と参照のために使用し、全文をリポジトリへ転載しない。台帳原文はv8スナップショットである。
''')
pages=[74,75,76,98,99,273,274,275,276,298]
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第78バッチ
Noto Sans JPのRegular400を復旧し、QAコピーのみに適用。documentsのrender_docx.pyで400頁を再描画し、完了後の74・75・76・98・99・273・274・275・276・298頁を直接画像目視。PDF埋込フォントNotoSansJPStaticと、追加54文字列の反映を確認。対象6問に欠字・重なり・切れなし。Q_4_115設問と選択肢98〜99頁、Q_4_053解説273〜274頁、Q_4_058解説275〜276頁の分割は最終改頁調整候補。古い描画画像は最新版の検証に使用しない。全400頁の最終画像目視は未了。
''')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
cs=json.loads((p/'changes_batch78.json').read_text());assert len(cs)==54
text=re.sub(r'\s+','',Path('/tmp/batch78.txt').read_text())
missing=[e['after'] for e in cs if re.sub(r'\s+','',e['after']) not in text];assert not missing,missing
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==46
oldm=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newwarnings=[x for x in machine['issues'] if x not in oldm['issues']]
assert len(newwarnings)==1 and newwarnings[0][:2]==['P1','Q_4_058']
e={'batch':78,'base_commit':'6c75628d477a0c7885cd2b6ca5a8cb0a584488e2','questions':sorted(targets),'edits':54,'application_order':['tools/v9_apply_batch78.py','tools/v9_apply_batch78b.py'],'status_counts':{'確認済み':192,'修正必要':71,'要追加確認':237},'remaining':308,'independent_answers':{'Q_4_052':2,'Q_4_053':2,'Q_4_056':1,'Q_4_057':4,'Q_4_058':2,'Q_4_115':1},'sources':{'S142':{'url':'https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf','sha256':sha('/tmp/standards2014.pdf'),'pdf_pages':240,'edition':'2014','image_verified_page_map':{'11':21,'14':24,'33':43,'34':44,'79':89,'215':225,'217':227,'218':228,'221':231}},'S143':{'url':'https://files.eric.ed.gov/fulltext/ED345513.pdf','sha256':sha('/tmp/washback1992.pdf'),'pdf_pages':23,'edition':'1992年2月発表稿、1993年原誌とは区別','image_verified_page_map':{'5':6,'6':7,'8':9,'9':10}}},'machine_warnings':46,'new_machine_warnings':newwarnings,'new_warning_manual_review':'Q_4_058 P1は仮説の普遍化を否定する正答解説末尾による極性検出。全4肢と解説・タグ、独立正答2の一致を直接確認。検出器変更なし。','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':pages,'full_visual_qa_completed':False,'changed_strings_missing_in_pdf':missing,'font':'Noto Sans JP Static Regular400 QA copy only','font_download':'https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf','font_sha256':sha('/tmp/lo-ja/libreoffice/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha('/tmp/batch78-qa/batch78.pdf'),'page_sha256':{str(i):sha(f'/tmp/batch78-qa/page-{i}.png') for i in pages},'release_ready':False}
(p/'evidence/batch78_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
