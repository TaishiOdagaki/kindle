"""Record teaching-method principles audit and changed-page inspection."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa144';target='Q_4_031'
def oldfile(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(oldfile('ledger.csv'));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k==target else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':351,'修正必要':11,'要追加確認':138}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==100
added=[x for x in machine['issues'] if x not in prior];assert added==[['P1','Q_4_031','(正)2の解説が否定で終わる/肯定の(誤)がある: [1, 4]']]
assert all(x in machine['issues'] for x in prior)
cs=json.loads((p/'changes_batch144.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={target}
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('| 確認済み | 350問 |','| 確認済み | 351問 |').replace('修正必要12問','修正必要11問').replace('| 修正必要 | 12問 |','| 修正必要 | 11問 |').replace('347問2954箇所','348問2963箇所').replace('347問を部分修正','348問を部分修正');f.write_text(s)
report='''

## 第144バッチ（2026-10-18）

Q_4_031を9箇所改訂し、独立正答2を確定。米国国務省公開のDiane Larsen-Freeman（1990）Language Teaching Methods教師用ハンドブック全65頁を取得。導入印刷1頁と、ALM2頁、TPR18–19頁、Silent Way32–33頁、Communicative Approach41–42頁の解説本文全体を精読し、各方法の開始頁を画像でも照合。全65頁精読や授業動画自体の視聴ではない。

教授法の理念・理論的観点という学習領域と正答2を維持し、広範な発展史・影響関係を問う旧問題から、取得本文で比較できる理念・指導上の特徴へ改訂。TPRの理解先行と身体反応、ALMの習慣形成・反復・正の強化、CAの場面に適切な使用と意味のやり取り、Silent Wayの学習者による自己修正を4肢・全解説へ照合。Hymesの提唱を社会言語学的能力だけと同一視する帰属を撤回。Skinner、Bloomfield、Hymes、CLIL、直接法の未取得原著の補助主張を新稿に残さず、創始者原著全冊の取得済みとは扱わない。方法の理念の紹介は普遍的な学習効果の実証ではないことも区別した。

機械警告は99→100件。追加P1は、正答2の解説末尾の「学習効果を無条件に保証するものではありません」を正答そのものの否定と誤認したもの。正答2はALMの取得本文の記述に一致し、解説末尾は効果の一般化を制限する注記。誤答1・4の解説中にあるTPRやSilent Wayの正しい補足記述を、誤答肢の肯定と扱うこともできない。誤検出理由を記録し、警告を消す目的の本文変更・機械判定の隠蔽はしない。既存99件も保持。

確認済み351・修正必要11・要追加確認138、残149問。累積348問2963箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。v8不変・500問構造・キー・タグ・早見表・リンク・影響外本文の不変検査、公開判定回帰8条件・置換回帰4条件を通過。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画し、全9変更文字列を検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。解説の頁またぎは残存し、最終全頁組版確認が必要。既存校正・documents手順で変更範囲を検査。全頁最終目視および残149問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第144バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第144バッチ S208（2026-10-18）

- S208 Diane Larsen-Freeman (1990), [Language Teaching Methods: Teacher’s Handbook for the Video Series](https://americanenglish.state.gov/files/ae/resource_files/language_teaching_methods_teachers_handbook.pdf)、米国国務省公式公開。全65頁PDFを取得。表紙と導入印刷1頁、ALM2頁、TPR18–19頁、Silent Way32–33頁、CA41–42頁の解説本文を精読し、4方法の開始頁は画像でも照合。Q_4_031の理念・指導上の特徴を全4肢・4解説へ照合。全65頁の精読、動画自体の視聴、1986年の著書や創始者原著全冊の取得ではない。理念の説明を、全対象での効果の実証へ一般化しない。

取得原バイトSHA256・読了範囲・制約はevidence/batch144_sources.json。本文・頁画像は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=144,base_commit='ebf46062d737e0a06ea9b4d1e7714b5019407b3d',fully_rejudged=[target],edits=9,independent_answers={target:2},sources=['S208'],status_counts=m['status_counts'],remaining=149,machine_warnings=100,new_warnings=added,new_warning_review='P1 false positive: the correct ALM explanation negates an unconditional effectiveness guarantee, not its own answer; descriptions of TPR/Silent Way in wrong-option explanations correct those options rather than affirming them.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_pdf_page_sha256={str(n):sha(root/f'teaching144-{n}.png') for n in [7,23,37,46]},candidate_not_used=dict(url='https://americanenglish.state.gov/files/ae/resource_files/50_2_6_larsen-freeman-pp28-38_0.pdf',sha256=sha(root/'larsen1987-144.pdf'),read_scope='2012年再掲の1987年論文、導入から印刷33頁途中、および35–38頁本文・文献。全11頁精読ではない。',reason='折衷的アプローチという用語自体の定義は取得読了箇所で確認できず。結論の状況に即した選択の議論のみから用語の確認済み判定をしない。Q_M_028は要追加確認を維持。'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch144_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('351 confirmed / 149 remaining',pages)
