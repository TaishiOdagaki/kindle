"""Record the scoped AI guidance review after direct inspection of latest render."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch112_qa')
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_4_118' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':285,'修正必要':39,'要追加確認':176}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==72 and len(added)==1 and added[0][:2]==['P1','Q_4_118'];assert all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch112.json').read_text());assert len(cs)==7
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[98,99,298]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
f=p/'README.md';s=f.read_text()
for a,b in [('284問','285問'),('177問','176問'),('289問2475箇所','290問2482箇所'),('289問を','290問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第112バッチ（2026-10-16）

Q_4_118の全体を文科省ガイドラインVer.2.0（2024-12-26）の一次本文へ照合し、設問・全4肢・独立正答・全4解説を再判定、7箇所改訂した。公式PDF33頁を取得、7・17・18・20頁を本文精読、7・18・20頁を1800px画像で確認。対象を初等中等教育の日本語学習者に限定し、生成AIの修正をたたき台として本人が確認・推敲し過程と結果を示す活動例に対応させた。元解説の「非常に有効」「高い言語学習効果が得られる」、プロンプトによる学習効果が大きく変わる等の根拠不足の断定を除去。推奨・参考例と因果実証を混同せず、学齢・発達段階・利用上の留意点を条件に含めた。指定2024版の考え方を問うもので、成人日本語教育全般、現行法・個別規約の判断や全生成AI製品の性能を承認したものではない。

正答4維持。確認済み285・修正必要39・要追加確認176、残件215。累積290問2482箇所、500問維持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。

全500問の構造・正答番号・タグ・表・リンク・影響外本文・v8不変検査と公開可否回帰8条件が合格。警告71→72件、追加P1のQ_4_118は正答解説末尾の「全員への高い学習効果の実証ではない」という留保に反応した誤検出と確認。他71件は同一。documents手順でNoto Sans JPによる累積稿401頁を新規描画、全7変更文字列を検出、98・99・298頁を1800px画像で直接目視・完全読込み。対象部分に欠字・重なり・文字切れなし。ただしQ_4_118の選択肢4が次頁へ分かれているため、最終組版での改善対象として残す。全頁最終目視と残215問の学術照合も未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第112バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第112バッチ S171（2026-10-16）

文部科学省初等中等教育局「初等中等教育段階における生成AIの利活用に関するガイドライン」（2024-12-26、Ver.2.0）。[公式本文PDF](https://www.mext.go.jp/content/20241226-mxt_shuukyo02-000030823_001.pdf)33頁を取得、7・17・18・20頁を本文精読、7・18・20頁を画像照合。公式掲載案内も照合。7頁は課題・指示・真偽の判断と人間主体、17頁は発達段階・学習状況・リスク対策、18頁Box5・20頁Box6は自己の文章へのAI修正をたたき台に本人が推敲する例とそのまま提出する問題。推奨と因果実証を区別し、Q_4_118の対象を指定版の初等中等教育に限定して承認。全33頁の精読、成人教育への一般効果、現行法や個別利用規約、各製品性能は承認対象外。evidence/batch112_source.jsonに原バイトのハッシュと照合範囲を保存。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第112バッチ\nNoto Sans JPによる累積稿401頁、全7変更文字列を検出。98・99・298頁を1800px画像で直接目視。欠字・重なり・文字切れなし。Q_4_118の肢4の次頁分割は最終組版改善対象。全頁最終目視は未完了。\n')
e=dict(batch=112,base_commit='3a407d83121eece4bc67778a96b819ee568976a7',fully_rejudged=['Q_4_118'],edits=7,independent_answers={'Q_4_118':4},sources=['S171'],status_counts=m['status_counts'],remaining=215,machine_warnings=72,new_warnings=added,new_warning_judgment='P1 false positive: correct explanation qualifies unsupported causal effect, not correct option',readiness_gate='8 cases passed',render_pages=len(pages),visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},pagination_todo='Q_4_118 option4 on next page; improve final pagination',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch112_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('285 confirmed/215 remaining;7 edits/3 pages recorded')
