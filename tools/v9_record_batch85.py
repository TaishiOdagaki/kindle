"""One-time batch85 checkpoint after text verification and seven-page visual review."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch85-qa';targets={'Q_4_029','Q_4_049','Q_4_062'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':217,'修正必要':57,'要追加確認':226}
cs=json.loads((p/'changes_batch85.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==400
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=[65,73,78,263,264,272,277];assert sorted({n for v in matches.values() for n in v})==reviewed
imgs={i:render/('review277b.png' if i==277 else f'review-{i}.png') for i in reviewed}
for f in imgs.values():Image.open(f).verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==55 and len(added)==1 and added[0][1]=='Q_4_062'
f=p/'README.md';s=f.read_text()
for a,b in [('214問','217問'),('58問','57問'),('228問','226問'),('227問1863箇所','230問1890箇所'),('227問を','230問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第85バッチ（2026-10-15）

第84バッチのGitHub保存成功を確認し、最新HEAD fecc39c203a413bfcdcf01c216c91b00b155bf9dを取得して継続。S147印刷7頁の内容・方法・成果の区別、20・28頁の設計の説明と図10、30頁表2を本文・画像で追加照合した。S144の編成単位の説明も併用した。

Q_4_029はプロセスを重視する設計について、S147表2のセントラル・デザインという取得済みの比較に限定（独立正答1）。内容交渉・コース中の発展・教師と学習者の役割を全4肢・4解説に対応させた。未取得のBreen/Candlin原著を承認したとはせず、productを物理的成果物と訳して分類する旧説明を撤回した。

Q_4_049は、Can-doの文末だけで機能・場面シラバスと断定する説明を撤回（独立正答1）。実際の編成単位と、項目を扱うこと、主題名、目標の書式を分けて判断する問題に改訂。Q_4_062は普遍的な授業計画手順ではなく、S147図10の開発段階を指定（独立正答2）。著者の2013年の図をCEFRの現行必須手続きやすべての教案作成の唯一の順序とはしない。

3問27箇所を順序付きchangesに追加。確認済み217・修正必要57・要追加確認226、残件283。累積230問1890箇所。500問・500解説と正答番号、影響外本文、v8ハッシュを維持。台帳原文はv8スナップショットで、改訂はchangesと累積作業稿を参照する。

全問機械検査と公開可否回帰8条件に合格。警告は54から55。追加P1 Q_4_062は、すべての授業計画への一方向の固定を否定する正答解説末尾による。全4肢・4解説・タグ・独立正答2を直接確認。検出器は変更していない。

documentsのrender_docx.pyでNoto Sans JP Static Regular400をQAコピーだけに適用して400頁描画。対象7頁は完成PDFから150dpiで再描画し、65・73・78・263・264・272・277頁を画像精読。277頁の最初の150dpi PNGが破損していたため、別名review277b.pngへ再生成し確認した。採用7画像はPIL検査済み。27変更文字列が全てPDFに反映し、日本語欠字・切れ・重なりなし。Q_4_029解説263〜264頁は最終改頁調整候補。全400頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第85バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第85バッチ S147とS144の追加照合（2026-10-15）\nS147著者公開29頁論文の印刷7頁（PDF3頁）図1と学習成果の説明、20頁（PDF16頁）、28頁（PDF24頁）図10と結論、30頁（PDF26頁）表2を本文と画像で照合。Q_4_029・049・062の全4肢・4解説に適用。表2は著者がClarkを参照して構成した比較として扱い、Clark原著全体やBreen/Candlin原著を取得したとはしない。Q_4_049はS144印刷10〜11・28〜30頁の編成単位も併用。目標の書式からシラバス種別を決めず、2013年の著者図をCEFRの現行必須手続きと混同しない。URL・PDFハッシュ・頁対応はevidence/batch85_review.jsonへ記録。\n''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第85バッチ\n最新作業稿をbatch85-qaへ400頁描画後、対象7頁を150dpiで再描画して直接精読。65・73・78・263・264・272・277頁。277頁の破損した最初のPNGは採用せずreview277b.pngで再確認。採用画像は全てPIL検査済み。27変更文字列がPDFに存在。日本語欠字・切れ・重なりなし。NotoSansJPStatic埋込みあり。Q_4_029解説263〜264頁は最終改頁調整候補。全400頁の最終目視は未了。\n''')
e={'batch':85,'base_commit':'fecc39c203a413bfcdcf01c216c91b00b155bf9d','questions':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':283,'independent_answers':{'Q_4_029':1,'Q_4_049':1,'Q_4_062':2},'sources':{'S147':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Curriculum-Approaches-in-Language-Teaching.pdf','sha256':sha(root/'curriculum84.pdf'),'pdf_pages':29,'image_verified_page_map':{'7':3,'20':16,'28':24,'30':26},'scope':'Author comparison and figures; cited books not acquired.'},'S144':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','sha256':sha(root/'richards80.pdf'),'pdf_pages':52,'image_verified_page_map':{'10':14,'11':15,'28':32,'29':33,'30':34}}},'machine_warnings':55,'new_machine_warnings':added,'new_warning_manual_review':'Q_4_062 P1はすべての授業計画への固定順序化を否定する正答2の末尾による。全4肢・4解説・タグを直接確認。','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'render_recovery':'First review277.png invalid; regenerated review277b.png from same PDF. All accepted review images pass PIL verification.','full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(imgs[i]) for i in reviewed},'release_ready':False}
(p/'evidence/batch85_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 questions / 27 edits; 217 confirmed / 283 remaining')
