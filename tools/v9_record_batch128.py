"""Record CLIL assessment/support and occupational burnout rejudgments."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa128';ids=['Q_O_069','Q_O_070','Q_M_019']
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in ids else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':331,'修正必要':28,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newflags=[i for i in machine['issues'] if i not in prior['issues']];assert len(machine['issues'])==98 and {i[1] for i in newflags}=={'Q_O_069','Q_M_019'} and all(i[0]=='P1' for i in newflags)
assert not [i for i in prior['issues'] if i not in machine['issues']]
cs=json.loads((p/'changes_batch128.json').read_text());assert len(cs)==27
matches=json.loads((r/'matches.json').read_text());assert len(matches)==27 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for n in [15,16]:
 with Image.open(root/f'tkt-clil-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('328問','331問'),('30問','28問'),('142問','141問'),('329問2770箇所','332問2797箇所'),('329問を','332問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第128バッチ（2026-10-17）

Q_O_069・Q_O_070・Q_M_019を27箇所改訂し、設問・全4肢・独立正答・全4解説を照合。独立正答は順に3・3・4を維持。Cambridge公式TKT:CLIL handbookの印刷14〜15/PDF15〜16、Coyleを含む著者の枠組み本文、WHO公式FAQの定義全文を取得した。検索抜粋ではなく根拠本文を用いた。

CLIL評価は、ケース14の内容と言語の両目標を持つ単元全体の計画に限定。公式資料はcontent and/or language等の焦点を認めており、「全個別課題で常に両面を同時に同じ重みで採点する」という義務にしない。内容・思考・意味伝達の目標を正確さだけで代用しない点と、目標・基準・支援の調整を問う。導入の意義は内容と思考と言語を結び付ける設計として記述し、「他方式より必ず効果が高い」「負担によって効果が下がる根拠はない」という未検証の実証的断定を撤回。言語支援・視覚的支援・課題調整を扱い、日本語で内容を提示するだけで支援不要とはしない。

バーンアウトはWHOのICD-11の説明に範囲を限定。職業場面の慢性的ストレスに関する三側面と、医学的疾患とは分類しない位置付けを確認。教師や学習者の一般的疲労を一律にWHO定義へ当てはめる原設問を改訂し、学習者バーンアウト研究・一般心理概念との比較・個人の診断/治療は承認対象にしていない。

TKT:CLILの最初のダウンロードはpdftotextで読めたが、pypdfの厳格読込みでEOF欠落が判明したため承認に使わず再取得。再取得ファイルは全31頁読込みと該当画像の完全展開を確認した。資料を部分的に読めることと原ファイルが完全であることを区別する。WHOは公式HTMLの本文全体を取得した。原資料は転載せずURL・取得範囲・バイト数・SHA256を記録。

確認済み331・修正必要28・要追加確認141、残169問。累積332問2797箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。500問の構造・キー/タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件、置換関数回帰4条件を通過。警告98件：Q_O_069の一律の採点規則ではないという留保、Q_M_019の個人診断ではないという留保をP1が検出した2件が追加。独立正答と留保は整合し、警告を消すために留保を削除していない。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画、27変更文字列を全検出。'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の改頁を含む全頁最終QAと残169問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第128バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第128バッチ S192・S193／S191再利用（2026-10-17）

- S192 Cambridge Assessment English [TKT:CLIL Handbook for teachers](https://www.cambridgeenglish.org/images/22191-tkt-clil-handbook.pdf)。再取得した全31頁原PDFを検証し、印刷14〜15/PDF15〜16の本文・画像を精読。内容と言語への足場掛け、語彙・文の枠組み・視覚的支援・課題分割、負担の調整、content and/or language等の評価焦点・基準・支援方略を使用。資料作成機関自身の教育枠組みとして用い、引用先の効果研究や全学習者への因果効果は未承認。S191の二重焦点・思考と言語を結び付ける設計も使用。
- S193 WHO [Burn-out an occupational phenomenon](https://www.who.int/standards/classifications/frequently-asked-questions/burn-out-an-occupational-phenomenon)。2026-10-17に公式HTMLの定義本文全体を取得。ICD-11での職業上の現象、medical conditionとは分類しない点、慢性的な職場ストレス、三側面、生活の他領域へ適用しない限定を照合。学習者研究、医療診断、治療・予防の有効性の承認ではない。

原バイトの範囲・SHA256はevidence/batch128_sources.json。原資料非転載。TKTの最初のEOF欠落ファイルは除外した。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第128バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全27変更文字列を検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=128,base_commit='66a196c15eaf6e208b86b6710908f0a4b26851ae',fully_rejudged=ids,edits=27,independent_answers=dict(zip(ids,[3,3,4])),sources=['S191','S192','S193'],status_counts=m['status_counts'],remaining=169,machine_warnings=98,new_warnings=newflags,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S192_PDF':[15,16]},excluded_source='first TKT CLIL download lacked EOF; retry validated 31 pages and used instead',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch128_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('331 confirmed/169 remaining;27 edits recorded',reviewed)
