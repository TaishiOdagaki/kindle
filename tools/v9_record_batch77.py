"""Record bounded JF Can-do continuation and partial visual QA."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');targets={'Q_1_041','Q_4_050','Q_O_009'}
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
for x,y in [('183問','186問'),('244問','241問'),('196問1577箇所','199問1604箇所'),('196問を','199問を')]:s=s.replace(x,y)
f.write_text(s)
report='''

## 第77バッチ（2026-10-14）

第76バッチのGitHub保存コミット1ca62f9ffb23557d999b355f729d31eac2830fd0を正本として継続。取得済みの国際交流基金2017年版ガイド全92頁により、関連未確認3問27箇所を追加改訂。確認済み186・修正必要73・要追加確認241、残件314。累積199問1604箇所。500問・500解説、正答番号、影響外原文、v8ハッシュは保持。

Q_1_041は、出典未照合の「熟達度Can-do／課題Can-do」二分法とCEFR/JFの区別を同一視する説明から、同ガイド19頁で明示されたCEFR Can-doの汎言語的・抽象的性質とJF Can-doの日本語使用場面に即した例示へ改訂。旧分類名称それ自体がすべての資料で誤りと判定したわけではなく、今回取得した版で確認できる区別に限定した。学術論文の批判的読解と学会論争を一括してC1〜C2に割り当てる未照合の説明も取り除いた。

Q_4_050は、すべてのCan-doを具体的な活動の記述だけに還元せず、できる言語活動と持っている言語能力の例示という14頁の説明と、言語材料の準備・複数記述の比較・非網羅性という18頁の留意点を問う。Q_O_009は49頁の学習目標一覧・自己評価チェックリストによる学習・評価内容の共有を問う。目標の形式だけで教材や評価の準備が不要になる、実際の能力向上が保証されるという推論を認めない。設問・全4肢・独立正答・全4解説を本文と版面へ照合した。

機械検査は500問・500解説を再確認し、公開可否回帰8条件に合格。機械警告45件（前44件）。新規Q_O_009のP1は正答解説の保証を否定する末尾と、誤答解説内の正しい手続きの説明による極性検出。原稿と正誤タグ、独立正答4を手動確認し、内容上の逆転ではないことを記録。検出器は弱めず、従前の未解決警告も残す。

documentsのrender_docx.pyとNoto Sans JP Static Regular400でQAコピー400頁を描画。22・73・145・221・272・346頁の6頁を直接画像目視し、追加27箇所は全てPDFへ反映。対象3問の設問・全4肢・正答・全4解説に日本語欠字・重なり・切れなし。累積改訂によってQAコピーは401頁から400頁へ変化したため、旧バッチの頁番号は当該時点の版に対する記録であり、最新版の全頁目視の代用にはしない。全頁最終目視・最終v9制作は未了。

台帳原文はv8スナップショット。改訂後の本文はchanges.jsonと累積作業稿を参照。未確認問題を推測で承認しない。採用500問を維持する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第77バッチ：S141の追加照合（2026-10-14）

国際交流基金（2017）[JF日本語教育スタンダード【新版】利用者のためのガイドブック](https://www.jfstandard.jpf.go.jp/pdf/limited/3_JFS_guidebook.pdf)、全92頁取得済み。印刷14・18・19・49頁（PDF18・22・23・53頁）の本文と版面を照合。

- 14頁：知識項目の個数との違い、できる言語活動と持っている言語能力の例示。Q_1_041・Q_4_050。
- 18頁：言語材料などの準備、複数Can-doの比較、非網羅性と現場に合った記述の作成、目標と評価への利用。対象3問の誤答・解説にも対応。
- 19頁：CEFR Can-doの汎言語的・抽象的性質と、日本語の使用場面を想定したJF Can-doの役割。Q_1_041。2017年版の説明を用い、2026年現在のサイト収録数や提供レベルの更新状況は主張しない。
- 49頁：学習目標一覧・自己評価チェックリストによる学習内容・評価内容の共有。Q_O_009。

他文献の「熟達度Can-do／課題Can-do」という分類そのものの普遍的な誤りは判定しない。今回の根拠は同ガイドで確認した区別と利用上の条件に限定する。
''')
pages=[22,73,145,221,272,346]
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第77バッチ
Noto Sans JP Static Regular400をQAコピーのみに適用し、documentsのrender_docx.pyで400頁を描画。22・73・145・221・272・346頁を直接画像目視。変更3問の設問・全4肢・正答・全4解説に欠字・重なり・切れなし。追加27文字列は全てPDFに反映。頁数が401から400に変わったため、旧バッチの頁番号を新版全頁検査の代用にはしない。全400頁の最終目視は未了。
''')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
cs=json.loads((p/'changes_batch77.json').read_text());text=re.sub(r'\s+','',Path('/tmp/batch77.txt').read_text())
missing=[e['after'] for e in cs if re.sub(r'\s+','',e['after']) not in text];assert not missing,missing
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==45
oldm=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newwarnings=[x for x in machine['issues'] if x not in oldm['issues']]
assert len(newwarnings)==1 and newwarnings[0][:2]==['P1','Q_O_009']
e={'batch':77,'base_commit':'1ca62f9ffb23557d999b355f729d31eac2830fd0','questions':sorted(targets),'edits':27,'status_counts':{'確認済み':186,'修正必要':73,'要追加確認':241},'remaining':314,'independent_answers':{'Q_1_041':3,'Q_4_050':4,'Q_O_009':4},'sources':{'S141':{'url':'https://www.jfstandard.jpf.go.jp/pdf/limited/3_JFS_guidebook.pdf','sha256':sha('/tmp/jfs-guide.pdf'),'pdf_pages':92,'edition':'2017年3月初版','image_verified_page_map':{'14':18,'18':22,'19':23,'49':53},'scope':'Can-doの例示性・利用上の留意点・CEFR/JFの役割・学習と評価内容の共有。現行サイト情報や効果の因果保証ではない。'}},'machine_warnings':45,'new_machine_warnings':newwarnings,'new_warning_manual_review':'Q_O_009 P1は正答末尾の保証の否定と誤答解説中の正しい手続きの極性検出。全4肢とタグ・独立正答4は一致。検出器は変更しない。','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':pages,'full_visual_qa_completed':False,'changed_strings_missing_in_pdf':missing,'font':'Noto Sans JP Static Regular400 QA copy only','font_sha256':sha('/tmp/lo-ja/libreoffice/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha('/tmp/batch77-qa/batch77.pdf'),'page_sha256':{str(i):sha(f'/tmp/batch77-qa/page-{i}.png') for i in pages},'release_ready':False}
(p/'evidence/batch77_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
