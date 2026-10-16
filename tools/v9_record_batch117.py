"""Record batch117 independent judgments and directly inspected changed pages."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch117_qa')
ids=['Q_4_085','Q_4_086','Q_O_042','Q_O_043','Q_O_044','Q_O_045']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':304,'修正必要':36,'要追加確認':160}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==85 and len(added)==5 and {x[1] for x in added}==set(ids)-{'Q_4_085'} and all(x[0]=='P1' for x in added) and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch117.json').read_text());assert len(cs)==36 and sum(bool(c.get('remove_paragraph')) for c in cs)==1
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];assert len(pages)==404
parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for i,c in enumerate(cs):
 if c.get('remove_paragraph'):continue
 needle=re.sub(r'\s+','',c['after']);assert needle;at=whole.find(needle);assert at>=0,(c['id'],c['field'])
 matches[str(i)]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
assert len(matches)==35
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[85,154,155,286,287,359,360],reviewed
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for item,name in zip(json.loads((p/'evidence/batch117_sources.json').read_text()),['jsl117_basic.html','jsl117_subject.html','jsl117_math.html','jsl117_support.html']):
 f=Path('/workspace/scratch/01d7c3f9b818')/name;assert f.stat().st_size==item['bytes'] and sha(f)==item['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('298問','304問'),('37問','36問'),('165問','160問'),('302問2564箇所','307問2600箇所'),('302問を','307問を')]:s=s.replace(a,b)
f.write_text(s)
report="""

## 第117バッチ（2026-10-16）

Q_4_085・086、Q_O_042〜045の設問・全4肢・独立正答・全4解説を文部科学省JSL小学校編最終報告の一次本文と照合。正答1・3・4・4・3・1を維持。36箇所（本文35、旧段落の明示除去1）を記録。JSLの日本語で学ぶ力・授業参加・教科と言語の支援を、教科知識自体の習得や同一活動の全教科への機械的適用と混同しない。母語・文化の支援や取り出し指導を一律否定しない。過去の小学校編報告の概念照合であり、現在の制度・法的手続・学校統計は承認しない。

Q_4_086は観察資料なしに計算力や「持つ」の理解を除外し比較表現だけを原因と断定していた。誰と誰を比較し何枚少ないかを把握する指導の着眼点を問う明示目的へ改訂。算数の15−6=9、逆向きなら15+6=21を独立検算し、以前の解説1の正しい修正を保持（今回の新規計算修正として数えない）。元の2段落の設問を1段落へ統合し旧計算例段落を明示除去。初回再構成では新設問中にも旧文字列が存在し安全検査が複数一致を検出したため停止。直前段落・設問ブロックの文脈を記録して一意化し、最新判断を再適用せず再構成を成功させた。

ケース9全2段落を読み、Q_O_042は練習単独でJSL全体を認定せず、ケースの教科学習との統合方針に対応づける。Q_O_043は無出典の保護者同意・制度上禁止の主張を教材内の支援判断へ置換し、協働の自動的効果保証を除去。Q_O_044は必要に応じ教科別の言語支援を考える方針とし、常時完全分離の強制と正当な取り出し・個別支援を区別。Q_O_045は理解・参加を把握して指導を見直す目的とし、一要因の因果効果証明とはしない。同ケースQ_O_041はBICS/CALP原著照合が残るため未確認を維持。

確認済み304・修正必要36・要追加確認160、残件196。累積307問2600箇所、500問維持。台帳の原文はv8スナップショット、改訂はchangesと作業稿を参照。全500問機械検査、v8不変、正答タグ・表・リンク・影響外本文、公開可否回帰8条件を通過。警告80→85。新規P1の5件は、実際の原因診断・練習だけでのJSL認定・協働効果保証・同一活動の全教科適用・単独因果証明を否定する留保による誤検出。独立正答を否定する解説ではなく、以前の80件と検出器を保持した。

Noto Sans JPの字形を確認した新規404頁描画で全35変更文字列を検出。85・154・155・286・287・359・360頁を1800px画像で直接目視・完全読込み。初回155・359頁PNGの末尾欠損を検出して同一PDFから単頁再描画し、有効画像のみ確認・ハッシュ記録。変更箇所に欠字・重なり・文字切れなし。Q_O_043の正答肢の次頁分離、Q_4_086解説4、Q_O_044の見出し・正答と本文の分離、次ケース見出し等を最終組版課題に残す。全404頁の最終目視・残196問の学術照合は未完了。公開不可、最終v9ではない。
"""
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第117バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+"""

## 第117バッチ S23追加・S181・S182（2026-10-16）

- S23 文部科学省JSL小学校編最終報告 [基本的な考え方](https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/001.htm)、[教科志向型JSLカリキュラム](https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/006.htm)。基本構想の本文と教科志向型1〜2.3を取得・精読。教科と言語の統合、授業参加、母語・文化支援、個別の把握、取り出しと在籍学級支援を照合。
- S181 同報告 [算数科](https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/015.htm)。5.1.1〜5.2と5.4.1を精読。既習の算数や就学歴・言語理解等の複数の困難を視野に入れ、計算だけでなく活動への参加を支援する。Q_4_086の例は本問の算術例として独立検算し、報告に掲載された実験と称さない。
- S182 同報告 [JSLカリキュラムを支える支援体制](https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/1295288.htm)。1.1〜1.2本文を精読。教師間の共有・協働、家庭・母語支援。協働の因果効果や現在のインターネット普及率、個別の法的要件を承認しない。

取得原バイトのURL・SHA256・範囲はevidence/batch117_sources.json。登録日を報告出版年とみなさず、小学校編の過去の報告として扱う。原資料全文は非転載。関連概念の原著未取得問は未確認を維持。
""")
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第117バッチ\nNoto Sans JP新規404頁。35変更文字列検出、旧段落1明示除去。85・154・155・286・287・359・360頁を1800px画像で直接目視。155・359頁の初回欠損PNGは単頁再描画で置換し全画像完全読込み。変更部分に欠字・重なり・文字切れなし。選択肢・解説・見出しの頁分割は最終組版課題。全頁最終目視は未完了。\n')
e=dict(batch=117,base_commit='d343a77a2a0eed9ddd8e4dd7cf4becd3b801de89',fully_rejudged=ids,edits=36,content_edits=35,explicit_old_stem_removals=1,independent_answers=dict(zip(ids,[1,3,4,4,3,1])),sources=['S23','S181','S182'],status_counts=m['status_counts'],remaining=196,machine_warnings=85,new_warnings=added,new_warning_judgment='P1 false positives from explicit limits on causal diagnosis, JSL identification, collaboration effect, identical activities, and causal proof',readiness_gate='8 cases passed',render_pages=404,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},case9_other_question='Q_O_041 remains unverified',arithmetic='9 and21 independently checked; prior correction retained',rebuild_guard='Ambiguous old paragraph match rejected; explicit block and previous-paragraph context made removal unique',png_recovery='155/359 regenerated before accepted image review',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch117_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('304 confirmed/196 remaining;36 edits/7 pages recorded')
