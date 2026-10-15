"""One-time checkpoint for two source-gated communication strategy questions."""
from pathlib import Path
import json,hashlib,subprocess,re,io,csv
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch89b-qa';targets={'Q_2_013','Q_4_021','Q_2_018'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':228,'修正必要':56,'要追加確認':216}
cs=json.loads((p/'changes_batch89.json').read_text());assert len(cs)==18
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');n=len(pages)-1
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:Image.open(render/f'review-{x}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==57
f=p/'README.md';s=f.read_text()
for a,b in [('| 確認済み | 226問','| 確認済み | 228問'),('| 要追加確認 | 218問','| 要追加確認 | 216問'),('要追加確認218問','要追加確認216問'),('239問1972箇所','241問1990箇所'),('239問を','241問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第89バッチ（2026-10-15）

最新HEAD 9fdede3508aa5cf9a4055b114480e03d76a5f9ceを取得して継続。S149 Celce-Murcia・Dörnyei・Thurrell（1995）の原論文「Communicative Competence: A Pedagogically Motivated Model with Content Specifications」、Issues in Applied Linguistics6(2),5〜35の公開PDFを取得。PDFは16頁の見開きスキャンで、表題・著者・刊年はPDF1頁、印刷26〜29頁はPDF12〜13頁。全体取得と対象4印刷頁の精読・画像照合を区別する。著者ら自身の提案した分類の一次資料として使用し、同論文が紹介するCanale/Swain1980やCanale1983の原著本文取得とは扱わない。大学リポジトリ側のロボット確認画面は迂回せず、別途公開された同じ原論文スキャンを取得した。

Q_2_013は回避・縮小、達成・補償、時間稼ぎの区分を指定原論文27〜28頁と表5で照合。旧desk/デスクの例、母語話者・上級者の頻度や意図性を一般化する未照合の補助主張を撤回。コミット前の見直しでもデスクの語彙史・日本語語彙性への補足を除き、同論文が支える分類だけを残した。原稿の未保存中間案を最終成果として扱わず、再構成後のbatch89b描画で検証した。

Q_4_021は方略名と発話例を表5により全4肢・全4解説照合。反復要求、明確化要求、相手が何と言ったかの確認要求、話し手が聞き手の理解を確かめる理解チェックを区別。旧解説が反復と明確化を一括した箇所を修正し、未照合のリキャスト定義や辞書使用の説明は別の分類の例へ置換。台帳の旧理由「シラバスの構成単位」は実際の設問と主題が一致しないため撤回し、全4肢の独立判定を記録した。独立正答は問13が4、問21が3で旧キーを維持。

Q_2_018は要追加確認を維持。S149は著者ら自身のモデルの一次資料だが、1980/1983の歴史的区分については二次的紹介である。Canale/Swain1980の全文未取得を埋めたと扱わない。追加探索でDörnyei/Thurrell1991の旧著者サイト候補はHTTP410、CiteSeer候補は403のため同経路を迂回しなかった。この論文も取得済みとはしない。

2問18箇所改訂。確認済み228・修正必要56・要追加確認216、残件272。累積241問1990箇所。全500問・500解説、正答番号・影響外本文・元v8ハッシュを維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。

全問機械検査・公開可否回帰8条件に合格。警告57件は前回と同一。documentsのrender_docx.pyで日本語フォント適用QAコピーを{n}頁描画し、変更文字列のある対象{ '・'.join(map(str,reviewed)) }頁を完成PDFから150dpi再描画・直接目視。18変更文字列、全4肢と正誤タグ、日本語表示を確認。全{n}頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第89バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://b9f19ceb-f720-4252-a2be-ccde56c0821f.filesusr.com/ugd/ba734f_1c905f1db74f488d924e158afdb63986.pdf?index=true'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## S149 Celce-Murcia・Dörnyei・Thurrell（1995）原論文

[Communicative Competence: A Pedagogically Motivated Model with Content Specifications 公開スキャン]({url})、Issues in Applied Linguistics6(2),5〜35。全16PDF頁（見開きスキャン）を2026-10-15取得。題名・著者・刊年・誌名・頁はPDF1頁で画像確認。印刷26〜27頁→PDF12頁、28〜29頁→PDF13頁の本文・表5を画像照合。Q_2_013は回避縮小・達成補償・時間稼ぎ、Q_4_021は反復・明確化・確認要求・理解チェックを全4肢・4解説・独立正答まで照合。本人らの分類の一次資料として用い、引用先Canale/Swain1980、Canale1983、Varonis/Gass1985原著全文取得とはしない。Q_2_018は未確認を維持。母語話者での頻度、普遍的意図性、学習効果の保証まで承認しない。全論文を精読済みとはせず、SHA256と範囲をevidence/batch89_review.jsonへ記録。

取得経路の制約：[大学リポジトリ書誌](https://escholarship.org/uc/item/2928w4zj)はロボット確認画面のためそこでの取得を中止し、独立公開スキャンを使用。Dörnyei/Thurrell1991の旧著者サイト候補 https://www.zoltandornyei.co.uk/uploads/1991-dornyei-thurrell-eltj.pdf は410、CiteSeer候補は403のため迂回せず未取得。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第89バッチ\nコミット前に未照合の語彙的補足を除いて再構成し、batch89b-qaへ{n}頁を描画。対象'+ '・'.join(map(str,reviewed))+f'頁を完成PDFから150dpiで再描画・直接目視。18変更文字列・全4正誤タグと日本語表示を確認。採用画像PIL検査済み。全{n}頁の最終目視は未了。\n')
e={'batch':89,'base_commit':'9fdede3508aa5cf9a4055b114480e03d76a5f9ce','fully_rejudged':['Q_2_013','Q_4_021'],'edits':18,'status_counts':m['status_counts'],'remaining':272,'independent_answers':{'Q_2_013':4,'Q_4_021':3},'sources':{'S149':{'url':url,'sha256':sha(root/'celce89.pdf'),'pdf_pages':16,'printed_pages':'5–35; paired-page scan','title_author_year_image_verified_pdf_page':1,'body_and_image_verified_page_map':{'26–27':12,'28–29':13},'limit':'Original authors own classification; not cited1980/1983/1985 originals or current empirical consensus'}},'partial_check_not_approved':'Q_2_018 retains要追加確認. Secondary historical summary is not original Canale/Swain body.','old_decision_mismatch_corrected':'Q_4_021 original reason referred to syllabus organization rather than actual meaning-negotiation stem. Replaced with independent option-level judgments.','before_commit_scope_cleanup':'Removed desk lexical aside before commit; rebuilt and re-rendered to fresh batch89b-qa. No unverified lexical assertion retained.','machine_warnings':57,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
(p/'evidence/batch89_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded2fullreviews/18edits;228confirmed/272remaining;pages',reviewed)
