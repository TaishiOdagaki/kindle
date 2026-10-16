"""Record two rubric judgments after source-body acquisition and changed-page QA."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch115_qa');ids=['Q_O_026','Q_O_028']
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in ids else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':294,'修正必要':37,'要追加確認':169}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==78 and len(added)==2 and {x[1] for x in added}==set(ids) and all(x[0]=='P1' for x in added) and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch115.json').read_text());assert len(cs)==10
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];assert len(pages)==403
parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[149,352,353]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
srcpath=p/'evidence/batch115_sources.json';src=json.loads(srcpath.read_text())
for item,name in zip(src,['cmu_rubric','cornell_rubric','coe_elp','coe_dossier','ninjal_corpus','cornell_syllabus']):
 raw=Path('/workspace/scratch/01d7c3f9b818')/(name+'115.html');assert sha(raw)==item['sha256'] and raw.stat().st_size==item['bytes']
 item['archive']=None;item['archival_limit']='full source HTML cached privately for inspection, not redistributed in repository'
srcpath.write_text(json.dumps(src,ensure_ascii=False,indent=2)+'\n')
f=p/'README.md';s=f.read_text()
for a,b in [('292問','294問'),('38問','37問'),('170問','169問'),('296問2532箇所','298問2542箇所'),('296問を','298問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第115バッチ（2026-10-16）

Q_O_026・028の設問・全4肢・独立正答・全4解説とケース6全2段落を照合し、10箇所改訂。Q_O_026は正答2を維持し、4選択肢と設問は変更せず全解説を改訂。CMUのルーブリック定義に加え、ELPの公式説明、国語研のコーパス開発者自身の定義、Cornellのシラバス教材本文を取得。「コーパスは評価に関する用語ではない」という全面否定を除去。評価基準表とは機能が異なると説明し、シラバスを学習項目の一覧だけに狭めず、評価に関する情報を含むことも認める。ポートフォリオはELPを例として区別し、ルーブリックとの併用を否定しない。

Q_O_028は正答1を維持。Cornellのルーブリック教材の定義・段階記述・基準明確化・利用者の意見による見直しへ照合。保護者の納得を得やすくなるという未照合効果を正答と解説から除き、基準と実際の発話の根拠を対応させる説明方針を明示した。大学の一般教材を架空ケースへ適用する編集上の判断であり、保護者対象の実証研究や法令上の説明義務を確認したものではない。元ケースは評価表の実物や発話記録を提示していないため、実際の得点の妥当性・公平性は認定しない。ケース6の他問を一括承認していない。

確認済み294・修正必要37・要追加確認169、残件206。累積298問2542箇所、500問維持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。一次HTML6件を通常取得して本文を精読し、ハッシュ・URL・範囲を記録。検索抜粋だけの承認ではない。権利条件の異なる資料全文はリポジトリへ転載せず、独立した日本語の説明と取得情報を保存。

全500問の構造・正答対応・タグ・表・リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告76→78件。新規P1の2件は正答解説末尾の妥当性・一致の保証否定と、対保護者効果の実証ではないとの留保への誤検出で、正答の否定ではない。他76件保持。documents手順でNoto Sans JPによる新規403頁を描画、全10変更文字列を検出。149・352・353頁を1800px画像で直接目視・完全読込み。改訂箇所に日本語欠字・重なり・文字切れなし。隣接未改訂問の選択肢や解説が頁をまたぐ箇所を含み、最終組版・全403頁最終目視は未完了。残206問の学術照合も未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第115バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第115バッチ S174〜S178（2026-10-16）

- S174 CMU Eberly Center [Creating and Using Rubrics](https://www.cmu.edu/teaching/assessment/assesslearning/rubrics.html)。本文取得、冒頭の定義・criteria/descriptors/performance levelsを精読。Q_O_026の表の構成に照合。全効果・全課題での保証ではない。
- S175 Cornell CTI [Using rubrics](https://teaching.cornell.edu/teaching-resources/assessing-student-learning/using-rubrics)。本文取得、定義・Why use・Considerations・Getting Startedを精読。Q_O_028全体の基準明確化・段階記述・説明方針への適用判断に使用。利用者との確認・改訂を含み、保護者の納得の実験や法的説明義務を根拠づけない。
- S176 Council of Europe [What is the ELP?](https://www.coe.int/en/web/portfolio/introduction)、[The Dossier](https://www.coe.int/en/web/portfolio/the-dossier)。両本文取得・主記事全文を精読。ELPの記録と省察・三構成要素、作品の選択・蓄積と過程/展示ドシエ、形成的評価等の用途をQ_O_026のポートフォリオ具体例に使用。全ポートフォリオをELPと同一視しない。
- S177 国立国語研究所「[鼎談 プロジェクトリーダーが語る 日本語の個性 ②](https://kotoba.ninjal.ac.jp/digest/03/d-03-02/)」（2018-04-18）。本文取得、最初のコーパス定義への小木曽氏の回答を精読。開発者本人によるデータの収集・検索・研究情報の説明をQ_O_026へ使用。記事全体の全事実・個々のコーパスの最新規模や現行仕様は承認対象外。
- S178 Cornell CTI [Write a Course Syllabus](https://teaching.cornell.edu/teaching-resources/preparing-teach/designing-your-course/write-course-syllabus)。本文取得、導入とFunctions of a Syllabus全体を精読。学習内容・時期・方法、成績評価の方針、課題・試験の日程などを伝える機能をQ_O_026へ照合。個々の大学の法的義務・全シラバスの記載項目を認定しない。

6原HTMLの取得日・バイト数・SHA256・照合範囲はevidence/batch115_sources.json。資料全文は非転載。上記以外のリンク先研究・実例は未取得であり、それらの内容を承認していない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第115バッチ\n新規Noto Sans JP描画403頁。全10変更文字列検出。149・352・353頁を1800px画像で直接目視・完全読込み。改訂箇所の欠字・重なり・文字切れなし。隣接未改訂問の頁またぎを含め最終組版・全頁最終目視は未完了。\n')
e=dict(batch=115,base_commit='a5b58ab030e0cc19a6327a5f8a397b85845eafed',fully_rejudged=ids,edits=10,independent_answers=dict(zip(ids,[2,1])),sources=['S174','S175','S176','S177','S178'],status_counts=m['status_counts'],remaining=206,machine_warnings=78,new_warnings=added,new_warning_judgment='P1 false positives from explicit limits on guarantees and empirical evidence, not rejection of correct options',readiness_gate='8 cases passed',render_pages=403,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},limits='case6 actual scoring validity/fairness and parent satisfaction effect not established; other case6 questions not automatically approved',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch115_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('294 confirmed/206 remaining;10 edits/3 pages recorded;source metadata only')
