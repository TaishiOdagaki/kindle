"""Record manual scholarly and changed-page review for batch116."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch116_qa');ids=['Q_4_060','Q_O_027','Q_O_029','Q_O_030']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':298,'修正必要':37,'要追加確認':165}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==80 and len(added)==2 and {x[1] for x in added}=={'Q_4_060','Q_O_027'} and all(x[0]=='P1' for x in added) and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch116.json').read_text());assert len(cs)==22
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];assert len(pages)==404
parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[76,149,276,352,353,354]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for item,name in zip(json.loads((p/'evidence/batch116_sources.json').read_text()),['cefr116.pdf','standards116.pdf','cmu_norm116.html']):
 f=Path('/workspace/scratch/01d7c3f9b818')/name;assert f.stat().st_size==item['bytes'] and sha(f)==item['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('294問','298問'),('169問','165問'),('298問2542箇所','302問2564箇所'),('298問を','302問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第116バッチ（2026-10-16）

Q_4_060、Q_O_027・029・030の設問・全4肢・独立正答・全4解説を一次本文へ照合、22箇所改訂。正答は2・1・3・3で維持。ケース6全2段落を確認。CEFR2001の9.3.5〜9.3.8（印刷186〜189頁、PDF195〜198頁）を本文・画像照合し、直接/間接、主観/客観、診断的利用という分類軸を区別。診断的評価を開始前だけに限る元解説、直接評価は必ず人間が採点するという一般化、間接評価なら常に採点コストが低いという断定を除去。2014 Testing Standardsの印刷79〜80頁（PDF89〜90）も本文・画像照合し、文章等の自動採点の記述を確認したが、その現行性能を承認していない。

Q_O_027はCMU公式教材の事前norming・基準解釈の討議に対応する会議の目的を問う。人数削減・時間短縮をケースに補わず、会議だけで完全一致すると保証しない。Q_O_030は根拠の記録と共通基準での複数教師の再確認を明示方針として、CEFR9.3.8を適用する本問の提案に限定。校内で利用目的・必要な許可・保管方法を確認した範囲という条件を置き、記録そのものの普遍効果や個別の法的適法性を主張しない。一人採点や妥当な基準改訂を無条件に誤りとはしない。

確認済み298・修正必要37・要追加確認165、残件202。累積302問2564箇所、500問維持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。取得原バイトのURL・ハッシュ・照合範囲を保存し資料全文は転載しない。CEFR全273頁・Standards全240頁の精読や引用先の全研究の取得を主張しない。

全500問の構造・正答対応・タグ・表・リンク・影響外本文・v8不変、公開可否回帰8条件を通過。警告78→80件。新規P1はQ_4_060の得点から運用能力全体を確定できないという留保、Q_O_027の完全一致保証の否定への誤検出で、正答の否定ではない。他78件保持。documents手順で日本語字形を確認したNoto Sans JPの新規404頁描画を使用。全22変更文字列を検出し、76・149・276・352・353・354頁を1800px画像で直接目視・完全読込み。変更部分に欠字・重なり・文字切れなし。Q_O_027の解説とQ_O_029解説4などの頁分割、Q_O_030のリンクの次頁分離、隣接未改訂問の分割を最終組版の改善対象に残す。全404頁の最終目視と残202問の学術照合は未完了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第116バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第116バッチ S179・S180とS142追加照合（2026-10-16）

- S179 Council of Europe, CEFR（2001）[公式公開本文](https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf)。273頁を通常取得、印刷186〜189頁（PDF195〜198）を本文・画像照合。9.3.5の総括的評価の診断的利用、9.3.6直接/間接、9.3.7運用/知識、9.3.8主観/客観と共通基準・複数判断・採点者訓練・データ分析までの全節を確認。Q_4_060・Q_O_029・030に使用。公式AssessmentページからのCEFR2001リンクでも本文を同定。PDFの2013年更新日を出版年と混同しない。全273頁や引用研究全体の承認ではない。
- S180 CMU Eberly Center [Grading and Feedback](https://www.cmu.edu/teaching/designteach/inclusiveexcellence/gradingandfeedback/index.html)。HTML本文取得、Grade anonymouslyのConsiderationsの採点前normingと解釈差の討議を精読。Q_O_027の会議目的へ対応づける。サイト全体や各科目実例の因果実証は承認対象外。
- S142 AERA/APA/NCME（2014）[Testing Standards公式全文](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf)を再取得。印刷79〜80頁（PDF89〜90）の採点仕様とその続き、複雑な文章応答へのアルゴリズム利用と検証の必要性を本文・画像照合。Q_4_060の人間採点必須という一般化を修正。2014年本文の記述であり、現在の製品性能やAI採点の妥当性を確認したものではない。

原バイト数・SHA256・範囲はevidence/batch116_sources.json。原資料全文は非転載。画像の初回196頁PNGに末尾欠損があったため廃棄して単頁再描画・完全読込み後に目視し、欠損画像を根拠に使っていない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第116バッチ\n新規Noto Sans JP描画404頁。全22変更文字列検出。76・149・276・352・353・354頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。解説やリンクの頁分割は最終組版改善対象。全頁最終目視は未完了。\n')
e=dict(batch=116,base_commit='5e7ba2e22798c87e2432ccb3a9540cc600f765d9',fully_rejudged=ids,edits=22,independent_answers=dict(zip(ids,[2,1,3,3])),sources=['S179','S180','S142'],status_counts=m['status_counts'],remaining=202,machine_warnings=80,new_warnings=added,new_warning_judgment='P1 false positives from qualifications on whole-competence inference and complete agreement, not denial of correct options',readiness_gate='8 cases passed',render_pages=404,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_image_review={'CEFR_printed':[186,187,188,189],'Standards_printed':[79,80]},pagination_todo='O027 explanations;O029 exp4;O030 link;neighboring questions',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch116_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('298 confirmed/202 remaining;22 edits/6 pages recorded')
