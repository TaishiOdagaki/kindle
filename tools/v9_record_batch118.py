"""Record batch118 independent judgments and directly inspected changed pages."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch118_qa')
ids=['Q_4_010','Q_4_012','Q_4_051','Q_4_059']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':308,'修正必要':36,'要追加確認':156}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==87 and len(added)==2 and {x[1] for x in added}=={'Q_4_012','Q_4_059'} and all(x[0]=='P1' for x in added) and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch118.json').read_text());assert len(cs)==25 and sum(bool(c.get('remove_paragraph')) for c in cs)==1
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];assert len(pages)==404
parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for i,c in enumerate(cs):
 if c.get('remove_paragraph'):continue
 needle=re.sub(r'\s+','',c['after']);assert needle;at=whole.find(needle);assert at>=0,(c['id'],c['field'])
 matches[str(i)]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
assert len(matches)==24
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[57,58,73,75,76,256,257,273,276],reviewed
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for item,name in zip(json.loads((p/'evidence/batch118_sources.json').read_text()),['tkt118.pdf','mext118_faq.html','cefr116.pdf']):
 f=Path('/workspace/scratch/01d7c3f9b818')/name;assert f.stat().st_size==item['bytes'] and sha(f)==item['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('304問','308問'),('160問','156問'),('307問2600箇所','311問2625箇所'),('307問を','311問を')]:s=s.replace(a,b)
f.write_text(s)
report="""

## 第118バッチ（2026-10-16）

Q_4_010・012・051・059の設問・全4肢・独立正答・全4解説を一次本文に照合。正答2・3・4・3維持。25箇所（本文24、旧設問の別段落除去1）改訂。Cambridge TKT公式用語集のAssessmentとTestの各定義、CEFR2001の9.3.1〜9.3.2および取得済み9.3.5〜9.3.8を使用。熟達度を無限定な全能力の測定とせず、未照合のJLPT例は除去。配置・到達度・熟達度・診断の目的を区別し、実際のテストに複数の機能があることまで否定しない。

Q_4_012は文法・語彙の知識と会話の両方を把握し、開講後必要に応じ配置を見直す学校の架空方針を明示。課題・評価基準を目的に対応させる案を正答とし、筆記と面接の併用だけで迅速さ・客観性・妥当性が保証されるとはしない。根拠のない「一般に数日〜1週間」の変更期間を除去。元の複数段落の設問を一つへ統合し、旧第2段落の除去を明示記録。Q_4_051は診断を開始前・途中だけに限定せず、総括評価の結果を診断に利用できることも確認。成績算出だけが目的で強弱の特定を排除する誤答に改訂し、時期だけで分類しない。

Q_4_059は平均点70と本人85だけから「上位20%」と推定する不成立な説明を85−70=15点という検算可能な比較へ修正。標準偏差だけから偏差値55とする条件欠落の例は、同じテストの受検集団内の順位という明確な事例に置換。未照合のCEFR B1記述子は架空のコース内基準へ置換。文科省の過去のFAQから個人内評価の概念定義のみ照合し、本人の過去からの進歩という設問の範囲を明示。旧学習指導要領の「現在」や現行の法的義務は承認しない。四つの例は説明用の架空事例で、実証結果ではない。

確認済み308・修正必要36・要追加確認156、残件192。累積311問2625箇所、500問維持。台帳の原文はv8スナップショット、改訂はchangesと作業稿を参照。全500問機械検査・v8不変・正答タグ/表/リンク・影響外本文・公開可否回帰8条件を通過。警告85→87。新規P1はQ_4_012の方法併用だけによる保証の否定、Q_4_059の他の評価との併用を否定しない留保による誤検出。独立正答を否定しておらず、他85件・検出器は保持。

日本語字形を確認したNoto Sans JPの新規404頁描画で24変更文字列を検出。57・58・73・75・76・256・257・273・276頁を1800px画像で直接目視し全画像完全読込み。変更箇所に欠字・重なり・文字切れなし。Q_4_059の選択肢4、Q_4_010の見出し/正答と解説、Q_4_012解説4、Q_4_051の見出し/正答と解説の頁分割は最終組版改善対象。全404頁の最終目視、残192問の照合は未完了。公開不可、最終v9ではない。
"""
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第118バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+"""

## 第118バッチ S183・S184とS179追加照合（2026-10-16）

- S183 Cambridge English [TKT Glossary](https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf)。通常取得59頁、印刷4〜5頁/PDF5〜6のAssessment、印刷47頁/PDF48のTest各項目を本文・画像精読。配置・診断・形成・総括・到達度・熟達度の区別に使用。版年を推定せず、全用語集や引用研究の確認を主張しない。
- S184 文部科学省 [確かな学力FAQ](https://www.mext.go.jp/a_menu/shotou/gakuryoku/faq/001.htm)。通常HTML取得。「目標に準拠した評価」「集団に準拠した評価」「個人内評価」の質問と全回答のみ概念定義に使用。平成10/11年改訂を現在とする過去のページであり、現行制度や観点数・漢字数等の周辺記述を根拠にしない。2019年通知も参照したが、本バッチの個人内評価の定義の根拠と混同しない。
- S179 CEFR2001公式PDFの印刷183〜185頁/PDF192〜194を新たに本文・画像精読。9.3.1到達度/熟達度、9.3.2規範/基準の区別を使用。9.3.3〜9.3.4の隣接本文も読んだが関連全問を自動承認しない。9.3.5〜9.3.8の第116バッチ取得・照合を再利用。S142採点仕様の既取得照合もQ_4_012に使用。

原資料URL・原バイトSHA256・範囲はevidence/batch118_sources.json。資料全文は非転載。例の順位や算数は編集上の独立確認であり原資料の実験ではない。
""")
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第118バッチ\nNoto Sans JP新規404頁。24変更文字列検出、旧設問段落1明示除去。57・58・73・75・76・256・257・273・276頁を1800px画像で直接目視し全画像完全読込み。変更箇所に欠字・重なり・文字切れなし。Q_4_059選択肢4・Q_4_010/051の見出しと解説・Q_4_012解説4等の頁分割を最終組版改善対象に残す。全頁最終目視は未完了。\n')
e=dict(batch=118,base_commit='4113ee267c0ce1aaeb00bca99c69f99e35a854dc',fully_rejudged=ids,edits=25,content_edits=24,explicit_old_stem_removals=1,independent_answers=dict(zip(ids,[2,3,4,3])),sources=['S183','S184','S179','S142'],status_counts=m['status_counts'],remaining=192,machine_warnings=87,new_warnings=added,new_warning_judgment='P1 false positives: denies automatic guarantee and permits combination with other evaluations',readiness_gate='8 cases passed',render_pages=404,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'TKT_printed':[4,5,47],'CEFR_printed':[183,184,185]},arithmetic='85-70=15; mean alone does not determine percentile',initial_apply='Edit-count assertion expected26 but actual25; aborted before writes, corrected count then applied once',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch118_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('308 confirmed/192 remaining;25 edits/9 pages recorded')
