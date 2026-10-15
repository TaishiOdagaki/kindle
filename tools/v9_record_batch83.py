"""One-time evidence record after batch83 academic review and six-page image QA."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch83-qa';targets={'Q_4_020','Q_4_024'}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');r=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(r)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':208,'修正必要':59,'要追加確認':233}
cs=json.loads((p/'changes_batch83.json').read_text());assert len(cs)==18
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==400
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=[62,63,64,260,261,262];assert sorted({n for v in matches.values() for n in v})==reviewed
for i in reviewed:Image.open(render/f'review-{i}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
assert len(machine['issues'])==53 and machine['issues']==prior['issues']
f=p/'README.md';s=f.read_text()
for a,b in [('206問','208問'),('60問','59問'),('234問','233問'),('219問1786箇所','221問1804箇所'),('219問を','221問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第83バッチ（2026-10-15）

専用監査ブランチ最新HEAD 3ef0834fba77018217a626d1c82d94c75ef184d5を取得し、既存判定を引き継いだ。Richards2006の著者公開52頁冊子S144をWebでも再取得・同定し、印刷11頁（PDF15頁）と19頁（PDF23頁）を取得本文と画像で照合した。原提唱者のジグソー原著や、引用された別研究を取得したとは扱わない。

Q_4_020は、ジグソー活動の情報交換の仕組みを問う架空の適用問題へ改訂。各人の部分情報を伝えて全体を完成させる案のみが条件に合い、独立正答は4。一人で完結する作業、同じ完成回答の音読、情報交換を設けない個別作業を対照とする。音読・個別作業自体の全面否定や、「ポジティブな相互依存」という名称だけから全員参加・習得効果を保証する説明は撤回した。

Q_4_024は、機能に応じて語彙・文法を選ぶというS144の定義に限定して全4肢・4解説を改訂（独立正答4）。文法項目・タスク・技能を編成単位とする案との違いを明示。「タスクは成果物だけを評価し過程を軽視する」という旧誤答解説と、機能シラバスなら即効性がある／必ず文法理解が後回しになるという未裏付けの説明を撤回した。機能シラバスが文法を扱わないとの誤読も防いだ。

2問18箇所を順序付きchangesへ追加。確認済み208・修正必要59・要追加確認233、残件292。累積221問1804箇所。500問・500解説と正答番号、影響外の本文を維持し、v8原本ハッシュ不変。台帳原文はv8スナップショット、改訂本文はchangesと累積作業稿を参照する。

全問機械検査と公開可否回帰8条件に合格。警告53件は前回と同一で、検出器は変更していない。Noto Sans JP Static Regular400をQAコピーのみに適用し、documentsのrender_docx.pyで400頁を描画。元PNGの63・262頁はPIL検査でTruncated File Readとなったため、破損画像をQA根拠にせず、同じ完成PDFから対象6頁をPopplerで再描画し、全6画像の形式健全性と表示を確認した。

62・63・64・260・261・262頁を直接画像目視。18変更文字列は全てPDFに存在し、日本語欠字・切れ・重なりなし。Q_4_024の設問・肢は63〜64頁、解説は261〜262頁に分かれ、最終改頁調整候補として残す。全400頁の最終目視は未完了。最終v9は未制作、出版不可。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第83バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## 第83バッチ S144の追加照合（2026-10-15）

[Richards2006著者公開52頁冊子]({url})をWebでも再取得・同定し、印刷11頁（PDF15頁）の機能・技能・タスクの編成基準、19頁（PDF23頁）のジグソー活動の定義と例を本文・画像で確認した。対象Q_4_020・024。部分情報を交換して全体を完成させる仕組みと、実際の発話参加・習得効果を区別し、ジグソー原提唱者の原著まで読んだとは扱わない。Q_4_020の活動案は架空の適用例。機能シラバスの普遍的な利点・欠点や、タスクは成果物のみ評価するという主張は承認しない。PDF全文は転載せず、ハッシュと確認頁をevidence/batch83_review.jsonへ記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第83バッチ\n新しいbatch83-qaへ400頁を描画。63・262頁の元PNGは形式破損があったため、完成PDFから対象6頁をPopplerでreview-N.pngへ再描画しPIL検査後に62・63・64・260・261・262頁を直接目視した。日本語欠字・切れ・重なりなし。18変更文字列は全てPDFに反映。NotoSansJPStatic埋込みを確認。Q_4_024設問63〜64頁と解説261〜262頁は最終改頁調整候補。全400頁の最終目視は未了。\n''')
e={'batch':83,'base_commit':'3ef0834fba77018217a626d1c82d94c75ef184d5','questions':sorted(targets),'edits':18,'status_counts':m['status_counts'],'remaining':292,'independent_answers':{'Q_4_020':4,'Q_4_024':4},'sources':{'S144':{'url':url,'sha256':sha(root/'richards80.pdf'),'pdf_pages':52,'image_verified_page_map':{'11':15,'19':23},'scope':'本人の編成単位・活動定義に限定。原提唱者の原著取得や効果保証ではない。'}},'machine_warnings':53,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'full_visual_qa_completed':False,'all_changed_strings_found_in_pdf':matches,'font':'Noto Sans JP Static Regular400 QA copy only','render_recovery':'Original PNG63 and262 failed PIL verification with Truncated File Read. Regenerated six reviewed pages from same completed PDF using pdftoppm; all review-N.png verified and visually read.','pagination_followup':'Q_4_024 stem/options63-64 and explanations261-262; final pagination adjustment pending','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'review-{i}.png') for i in reviewed},'release_ready':False}
(p/'evidence/batch83_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 2 questions / 18 edits; 208 confirmed / 292 remaining')
