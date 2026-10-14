"""Record batch76 source limits, QA and reproducible checkpoint."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');targets={'Q_3_018','Q_1_040','Q_4_055','Q_M_031'}
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
for x,y in [('179問','183問'),('248問','244問'),('192問1541箇所','196問1577箇所'),('192問を','196問を')]:s=s.replace(x,y)
f.write_text(s)
report='''

## 第76バッチ（2026-10-14）

4問36箇所を改訂し、確認済み183・修正必要73・要追加確認244、残件317。累積196問1577箇所。全500問を維持し、正答番号とv8原本を変更しない。

Q_3_018はRichards（1970）の原資料全38頁を使用し、過剰般化を「誰もが必ず経験する普遍的ステップ」とする解説を除去。目標言語内の構造についての経験に基づく逸脱した構造の形成という本文の説明に限定した。本文が直接立証しない日本語例も外した。

国際交流基金（2017）『JF日本語教育スタンダード【新版】利用者のためのガイドブック』全92頁PDFを公式サイトから取得。印刷5〜6・25〜26・49頁（PDF9〜10・29〜30・53頁）を本文と画像で照合し、Q_1_040・Q_4_055・Q_M_031を改訂した。Q_1_040は「コミュニケーション能力が二つで構成」「単なる言語能力＝課題遂行能力」という混同を除き、相互理解の理念と二つの能力の必要性を問う。未照合の商品・サイト開発目的の説明は同ガイドの学習・評価共有の説明へ差し替えた。

Q_4_055は、一般的なポートフォリオ評価の大規模選抜適性や標準化の難易に関する未立証の断定を、JFガイドで確認できる三構成要素と本人の振り返りへ改訂。Q_M_031は、無関係な三研究法の定義を列挙する誤答から、Can-doを用いた本人の自己評価手続きが欠ける三手続きへ差し替え、全4肢・全4解説を同じ取得本文に照合した。自己評価だけで客観的な全技能測定が保証されるとはしない。

機械検査で500問・500解説、正答、影響外の原文、v8ハッシュを保持。公開可否回帰検査8条件に合格。警告44件（従前43件）。新規P1はQ_4_055で、正答解説末尾の「一律に断定するものではありません」と、誤答解説中の正しい構成要素の説明を極性ヒューリスティックが拾ったもの。本文とタグを直接照合し、正答4と全4肢の判定は一致する。検出器を弱めて警告を消さず、手動確認記録を残す。他の残存警告は未解決のまま保持。

documentsのrender_docx.pyと復旧したNoto Sans JP Static Regular400を使い、QAコピー401頁を描画。22・45・75・178・220・221・243・274・275・379頁の10頁を直接画像目視し、変更全36文字列のPDF反映も検査。欠字・重なり・切れなし。Q_1_040解説は220〜221頁、Q_4_055解説は274〜275頁にまたがり、最終整形候補として記録。フォント変更はQAコピーのみ。最終全頁目視と最終v9は未了。

回避研究Q_4_076についてSchachter（1974）の原著全文を探索したが、今回確認できたのは書誌・抄録段階で、本文未取得。要追加確認を維持し、他資料の要約だけで原著を取得済みとはしない。台帳の原文はv8スナップショットで、改訂後はchanges.jsonと累積作業稿を参照する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第76バッチの取得・再利用資料（2026-10-14）

| ID | 資料・URL | 照合箇所 | 取得段階と限界 | 対象 |
|---|---|---|---|---|
| S29（再利用） | Jack C. Richards（1970）[A Non-Contrastive Approach to Error Analysis](https://files.eric.ed.gov/fulltext/ED037721.pdf) | 印刷6頁（PDF9頁）§3.1の定義と前後の母語干渉との区別 | 全38頁原資料取得。1970年発表稿として使用し、1971年掲載版と同一版とはしない。英語事例からすべてのL1/L2学習者への必然性や日本語の個別例を直接立証しない。 | Q_3_018 |
| S141 | 独立行政法人国際交流基金（2017年3月初版）[JF日本語教育スタンダード【新版】利用者のためのガイドブック](https://www.jfstandard.jpf.go.jp/pdf/limited/3_JFS_guidebook.pdf)、[公式資料一覧](https://www.jfstandard.jpf.go.jp/publicdata/ja/render.do) | 印刷5〜6頁：拘束的でない枠組み・相互理解の理念・二つの能力。25〜26頁：ポートフォリオの三構成要素・本人の評価と成果選定。49頁：学習目標・自己評価チェックリストによる学習内容と評価内容の共有 | 全92頁公式PDFを取得し、上記5頁を画像精読。奥付の2017年3月を確認。JFの設計・手続きを根拠とし、すべての評価法の一般的優劣、効果の因果実証、自己評価だけの客観的技能測定保証を導かない。 | Q_1_040・Q_4_055・Q_M_031 |

Q_4_076関連：Schachter（1974）An Error in Error Analysis、DOI https://doi.org/10.1111/j.1467-1770.1974.tb00502.x の原著本文は今回取得できず。書誌・抄録だけで全主張を承認しないため、新たな確認済み資料IDを付けない。
''')
pages=[22,45,75,178,220,221,243,274,275,379]
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第76バッチ
復旧したNoto Sans JP Static Regular400をQAコピーのみに適用し、documentsのrender_docx.pyで401頁を描画。22・45・75・178・220・221・243・274・275・379頁を直接画像目視。4問の設問・全4肢・全4解説に欠字・重なり・切れなし。Q_1_040解説220〜221頁、Q_4_055解説274〜275頁の分割は最終改頁調整候補。変更36文字列はPDFに全て反映。全401頁の最終画像目視は未了。
''')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
cs=json.loads((p/'changes_batch76.json').read_text());text=re.sub(r'\s+','',Path('/tmp/batch76.txt').read_text())
missing=[e['after'] for e in cs if re.sub(r'\s+','',e['after']) not in text];assert not missing,missing
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==44
oldm=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newwarnings=[x for x in machine['issues'] if x not in oldm['issues']]
assert len(newwarnings)==1 and newwarnings[0][:2]==['P1','Q_4_055']
e={'batch':76,'base_commit':'dbde29bef59e3780fc77cf031ba69910413aa67c','questions':sorted(targets),'edits':36,'status_counts':{'確認済み':183,'修正必要':73,'要追加確認':244},'remaining':317,'independent_answers':{'Q_3_018':3,'Q_1_040':1,'Q_4_055':4,'Q_M_031':1},'sources':{'S29':{'url':'https://files.eric.ed.gov/fulltext/ED037721.pdf','sha256':sha('/tmp/richards1970.pdf'),'pdf_pages':38,'verified_print_pages':[6],'scope':'1970年原発表稿の説明。全員必然の段階を導かない。'},'S141':{'url':'https://www.jfstandard.jpf.go.jp/pdf/limited/3_JFS_guidebook.pdf','sha256':sha('/tmp/jfs-guide.pdf'),'pdf_pages':92,'edition':'2017年3月初版','image_verified_page_map':{'5':9,'6':10,'25':29,'26':30,'49':53},'scope':'JFの理念・構成・本人による自己評価の手続き。一般的評価法の優劣や測定保証ではない。'}},'machine_warnings':44,'new_machine_warnings':newwarnings,'new_warning_manual_review':'Q_4_055 P1は正答末尾の限定的否定と誤答解説内の正しい構成説明の極性検出。全4肢の内容と正誤タグ、独立正答4の一致を直接確認。検出器は変更しない。','readiness_gate':'8 cases passed','render_pages':401,'visually_reviewed_pages':pages,'full_visual_qa_completed':False,'changed_strings_missing_in_pdf':missing,'font':'Noto Sans JP Static Regular400 QA copy only','font_sha256':sha('/tmp/lo-ja/libreoffice/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha('/tmp/batch76-qa/batch76.pdf'),'page_sha256':{str(i):sha(f'/tmp/batch76-qa/page-{i}.png') for i in pages},'release_ready':False}
(p/'evidence/batch76_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
