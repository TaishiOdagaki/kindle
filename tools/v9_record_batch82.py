"""One-time evidence checkpoint after batch82 text and image review."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch82-qa'
targets={'Q_4_022','Q_4_023','Q_4_038'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':206,'修正必要':60,'要追加確認':234}
cs=json.loads((p/'changes_batch82.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==400
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=[63,69,261,267];assert sorted({n for v in matches.values() for n in v})==reviewed
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==53 and len(added)==1
f=p/'README.md';s=f.read_text()
for a,b in [('203問','206問'),('63問','60問'),('216問1759箇所','219問1786箇所'),('216問を','219問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第82バッチ（2026-10-15）

最新HEAD d13649b29e6eb517fcedbb4d11cfd8e9a7663019を照合。Long本人の論考「Focus on form in Task-Based Language Teaching」の公開複製11頁版を取得し、Option 1〜3、図2とその本文を照合した。大学公式メタデータの1998年版本文とCOREの15頁版は403で取得できず、迂回しない。今回の複製は本文に1997年秋への言及があるが正式刊年は確定せず、設問にも年を付さない。1991年章や1998年章全体を取得したとは扱わない。

Q_4_022はコース設計一般の固定的な標準順序を問う旧設問から、取得論考の図2の七段階を指定する問題へ改訂。第1段階は現在・将来の目標タスクを特定するタスクに基づくニーズ分析（正答2）。他の肢は第6・2・3段階に対応し、全コース設計を一つの手順に固定しない。

Q_4_023は文法項目を配列単位とする構造シラバスという条件を明示（正答2）。話題・機能・達成作業の架空案を単位の違いで比較し、「口座開設」という語だけで場面シラバスと断定する曖昧さを解消。Richards2006の印刷10頁も本文・画像で再確認した。

Q_4_038は取得したLong論考のOption 3に限定し、意味中心の文脈で理解・産出の問題を契機とする一時的な形式への注意を正答3とした。外部項目配列、形式注意の排除、上位のform-focused instructionとの混同を区別。「過度のイマージョン」という未裏付けの価値判断を撤回し、意味中心授業一般の否定や習得効果保証をしない。

3問の設問・全4肢・独立正答・全4解説を照合し27箇所修正。確認済み206・修正必要60・要追加確認234、残件294。累積219問1786箇所。全500問と正答番号を維持、v8原本は変更なし。台帳原文はv8スナップショットであり、改訂はchangesと作業稿を参照する。

累積再構成と全問機械検査、公開可否回帰8条件に合格。警告は52から53。追加P1 Q_4_022は普遍的固定手順を否定する正答解説末尾によるもので、4肢・4解説とタグ・独立正答2を直接確認。検出器は変更しない。従前の警告も保持する。

documentsスキルのrender_docx.pyでNoto Sans JP Static Regular400をQAコピーだけに適用して400頁描画。63・69・261・267頁を直接画像目視し、日本語欠字・重なり・切れなし。27変更文字列が全てPDFに反映し、フォント埋込みも確認。全400頁の最終目視は未完了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第82バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://woucentral.weebly.com/uploads/7/4/6/9/7469707/long_1997_intro_focus_on_form.pdf'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## 第82バッチの追加資料（2026-10-15）

| ID | 資料 | 照合範囲 | 取得段階と限界 | 対象 |
|---|---|---|---|---|
| S146 | Michael H. Long [Focus on form in Task-Based Language Teaching]({url}) 公開複製11頁版 | PDF1頁Option 1、3頁Option 2、5頁Option 3とform-focused instructionとの区別、6頁図2の七段階と1〜3の説明、7頁タスク系列と文脈内形式指導例 | 本文を取得。該当1・3・5・6・7頁は画像照合。本文に1997年秋への言及があるが正式刊年は保証しない。大学公式1998年メタデータの本文とCORE15頁版は403で未取得。1991年章や1998年章全体の承認ではない。引用された実証研究全てを取得したとは扱わない。 | Q_4_022・023・038 |

S144追加照合：Richards2006著者公開52頁冊子の印刷10頁（PDF14頁）を本文と画像で確認。伝統的な文法項目・レベル配列の説明をQ_4_023の明示条件に適用する。すべての構造シラバスに語彙・音声を含める一律の定義や、話題名だけによる分類は採用しない。原著全文は転載せずURL・ハッシュと照合範囲をevidence/batch82_review.jsonに記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第82バッチ\n新しい出力先batch82-qaへ400頁を描画し、63・69・261・267頁の4頁を直接目視。3問27変更文字列は全てPDF内に存在し、日本語欠字・重なり・切れなし。NotoSansJPStatic埋込みを確認。適用はQAコピーのみで作業DOCXのフォントを勝手に変更しない。全400頁の最終画像目視は未了。途中稿であり出版不可。\n''')
e={'batch':82,'base_commit':'d13649b29e6eb517fcedbb4d11cfd8e9a7663019','questions':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':294,'independent_answers':{'Q_4_022':2,'Q_4_023':2,'Q_4_038':3},'sources':{'S146':{'url':url,'sha256':sha(root/'long82.pdf'),'pdf_pages':11,'image_verified_pages':[1,3,5,6,7],'scope':'Option 1〜3、図2と本文。正式刊年は未確定。公式15頁版・1991年章・1998年章の取得とはしない。'},'S144':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','sha256':sha(root/'richards80.pdf'),'pdf_pages':52,'image_verified_page_map':{'10':14}}},'machine_warnings':53,'new_machine_warnings':added,'new_warning_manual_review':'Q_4_022 P1は普遍的固定手順を否定する正答2の解説末尾による。全4肢・4解説・タグと単一正答性を直接確認。','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'full_visual_qa_completed':False,'all_changed_strings_found_in_pdf':matches,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'page-{i}.png') for i in reviewed},'release_ready':False}
(p/'evidence/batch82_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 questions / 27 edits; 206 confirmed / 294 remaining')
