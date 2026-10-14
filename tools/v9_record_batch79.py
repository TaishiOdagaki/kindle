"""Record PPP/practice/task review, partial QA and source limits."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');targets={'Q_4_035','Q_4_063','Q_4_064','Q_4_065','Q_4_066'}
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
for x,y in [('192問','197問'),('71問','69問'),('237問','234問'),('205問1658箇所','210問1704箇所'),('205問を','210問を')]:s=s.replace(x,y)
s+='''\n\n## 日本語描画QAの再構成
`tools/v9_render_checkpoint.py`は、元の作業DOCXを変更せず、Noto Sans JP Regular400を適用したQAコピーをdocumentsのrender_docx.pyへ渡す。`--input`、空の新しい`--output`、取得済みNoto Sans JP可変フォントの`--font`、書込み可能な実行環境同梱LibreOfficeの`--soffice`を明示する。既存PNGがある出力先は拒否し、古い描画と新しいPDFを混在させない。primary runtimeのPythonで実行し、作成前にはdocumentsスキルの指定マーカーを一度実行する。画像の学術的・視覚的判断は自動承認しない。日本語欠字のないことを確認し、最終版は全頁目視が必要。
'''
f.write_text(s)
report='''

## 第79バッチ（2026-10-14）

前回のローカル作業場がなかったため、専用監査ブランチをGitHubから再取得し、最新HEAD071fd132fe3bbd20349cf8767f76729e29881eb5の判断・変更・根拠・機械検査を引き継いだ。Richards（2006）の著者公開冊子全52頁を新規取得。印刷8・16〜17・31頁（PDF12・20〜21・35頁）の本文と画像を照合し、5問45箇所を改訂、画像精読後に解説の曖昧な係り受け1箇所を追補修正した。合計5問46箇所。順序付き変更はchanges_batch79.jsonとchanges_batch79b.jsonに分けて記録し、既存の初期判断生成スクリプトは再実行しない。

確認済み197・修正必要69・要追加確認234、残件303。累積210問1704箇所。全500問・500解説、正答番号、影響外原文、v8原本ハッシュを保持。問題を削除せず、全5問の設問・全4肢・独立正答・全4解説を取得した本文に独立照合した。

Q_4_063は「導入」一般にPPPを適用して他の授業方式を不適切とする説明から、指定モデルのPresentationの説明へ限定。Q_4_064は、制御された文脈から別文脈で自分の内容を使うProductionへの移行を問う。「認知負荷や言明の自由度は必ず上昇」「この順序で運用が自動化する」といった未立証の一般化は除いた。Q_4_065は監査で作った架空の三段階案をモデルに照らす問題とし、課題から始める別方式自体を否定しない。元の特定日本語形式の指導事例が原著で実証されたとは扱わない。

Q_4_066は、意味理解なしでも遂行できる機械的練習と、制御がある中で意味に即した選択をする有意味な練習を区別する。同書17頁は、自分の情報で文を完成させる活動も有意味な練習とするため、「個人情報を使うのはすべてコミュニケーション練習」という旧解説を撤回。意味理解や参加人数だけの乱暴な二分を避けた。画像精読後、解説1の「意味理解を必ずしも要するか」を「意味を理解せずに遂行できるか」へ整えた。

Q_4_035は、特定の文法形式が関与すれば必ずFocus on Formsでタスクではないという断定を除去。同書31頁が挙げる既存の言語資源、意味への焦点、言語学習だけに結びつかない成果という特徴を問う。実社会をそのまま再現しない教室用タスクも示されており、すべてのタスクを実社会の活動そのものに限定しない。Long、Ellis、Nunan、Willis等の他の原著も取得済みとはせず、Richards本人の整理を用いる。

機械検査と公開可否回帰8条件に合格。警告49件（従前46件）。追加3件を手動照合：Q_4_064のP1は効果保証を否定する正答解説末尾、Q_4_065のP1は原著の実証事例ではないという正答解説末尾、Q_4_066のA1は「必ずしも要さず」の否定を断定語として拾ったもの。全4肢・全4解説とタグ、独立正答の一致を直接確認。検出器は変更せず、従前の未解決警告も保持。

日本語フォントを復旧し、Noto Sans JP Static Regular400をQAコピーのみに適用。documentsのrender_docx.pyで、追補修正後の新しい出力先に全399頁を再描画。67・68・78・79・265・276・277頁の7頁を直接画像目視。最終45フィールドの変更文字列をPDFへ照合し、欠字・重なり・切れなし。Q_4_035の設問・選択肢67〜68頁、Q_4_065の設問・選択肢78〜79頁、Q_4_064解説276〜277頁の分割を最終改頁調整候補に残す。全399頁の最終画像目視と最終v9は未了。

再構成用の日本語QA描画補助をtools/v9_render_checkpoint.pyに保存。元原稿を変更せず、既存PNGが残る出力先を拒否する。台帳原文はv8スナップショットで、改訂後の本文はchanges.jsonと累積作業稿を参照する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第79バッチの取得資料（2026-10-14）

| ID | 資料・URL | 照合箇所 | 取得段階と限界 | 対象 |
|---|---|---|---|---|
| S144 | Jack C. Richards（2006）[Communicative Language Teaching Today 著者公開冊子](https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf)、[著者による無料公開告知](https://professorjackrichards.com/communicative-language-teaching-today/) | 印刷8頁：PPPの三段階と批判の併記。16〜17頁：機械的・有意味・コミュニケーション練習、個人情報を使う文完成の分類。31頁：タスクの特徴、教室用と実社会型の区別 | 全52頁取得、上記4頁を本文・画像照合。2006年著者冊子の説明に限定し、日本語教授法全般や全員の習得効果に一般化しない。引用されるSkehan、Willis等の原著も取得したとはしない。Q_4_065は監査で構成した架空のモデル適用例。 | Q_4_035・063・064・065・066 |

著者サイトには同名の47頁版（communicative-language-teaching-today-v2.pdf）もあるが、抽出文字がずれていた。今回採用したのは表紙・奥付付き52頁版で、印刷8頁＝PDF12頁、16〜17頁＝PDF20〜21頁、31頁＝PDF35頁。2006年の奥付も確認し、ダウンロードファイルの作成日時を刊年と誤認しない。PDF全文はリポジトリへ転載せず、URL・ハッシュ・照合範囲を記録する。
''')
pages=[67,68,78,79,265,276,277];render=Path('/tmp/batch79b-qa')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第79バッチ
日本語フォントを復旧し、Noto Sans JP Static Regular400をQAコピーだけに適用。追補の文言修正後、新しい空の出力先でdocumentsのrender_docx.pyによる399頁の再描画が終了してから、67・68・78・79・265・276・277頁を直接画像目視。対象5問の設問・全4肢・正答・全4解説に欠字・重なり・切れなし。変更46履歴を最終45フィールドへ畳み込んだ文字列は全てPDFに反映。Q_4_035の設問・選択肢67〜68頁、Q_4_065の設問・選択肢78〜79頁、Q_4_064解説276〜277頁は最終改頁調整候補。全399頁の最終目視は未了。旧バッチ頁番号はその時点の版に対する記録で、最新版全頁の検証を代替しない。
''')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
cs=json.loads((p/'changes_batch79.json').read_text())+json.loads((p/'changes_batch79b.json').read_text());assert len(cs)==46
effective={(e['id'],e['field'],e['index']):e for e in cs};assert len(effective)==45
text=re.sub(r'\s+','',Path('/tmp/batch79b.txt').read_text())
missing=[e['after'] for e in effective.values() if re.sub(r'\s+','',e['after']) not in text];assert not missing,missing
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==49
oldm=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newwarnings=[x for x in machine['issues'] if x not in oldm['issues']];assert len(newwarnings)==3
e={'batch':79,'base_commit':'071fd132fe3bbd20349cf8767f76729e29881eb5','questions':sorted(targets),'edits':46,'effective_changed_fields':45,'application_order':['tools/v9_apply_batch79.py','tools/v9_apply_batch79b.py'],'status_counts':{'確認済み':197,'修正必要':69,'要追加確認':234},'remaining':303,'independent_answers':{'Q_4_035':2,'Q_4_063':2,'Q_4_064':2,'Q_4_065':1,'Q_4_066':4},'sources':{'S144':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','sha256':sha('/tmp/richards2006-alt.pdf'),'pdf_pages':52,'edition':'2006著者公開冊子、別47頁版とは区別','image_verified_page_map':{'8':12,'16':20,'17':21,'31':35}}},'machine_warnings':49,'new_machine_warnings':newwarnings,'new_warning_manual_review':{'Q_4_064 P1':'全員の自動化という効果保証を否定する正答末尾。正答2と全肢タグ一致。','Q_4_065 P1':'原著の実証事例ではないとする正答末尾。正答1と全肢タグ一致。','Q_4_066 A1':'必ずしも要さずという否定を断定語として検出。正答4と全肢タグ一致。'},'readiness_gate':'8 cases passed','render_pages':399,'visually_reviewed_pages':pages,'full_visual_qa_completed':False,'changed_strings_missing_in_pdf':missing,'font':'Noto Sans JP Static Regular400 QA copy only','font_download':'https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf','font_sha256':sha('/tmp/lo-ja/libreoffice/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'page-{i}.png') for i in pages},'release_ready':False}
(p/'evidence/batch79_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
