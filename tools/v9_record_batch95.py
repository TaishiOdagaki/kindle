"""Run only after directly reviewing the completed batch95 page images."""
import json,hashlib,subprocess,re,io,csv,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch95-qa';targets={'Q_M_025','Q_M_040'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':245,'修正必要':53,'要追加確認':202}
cs=json.loads((p/'changes_batch95.json').read_text());assert len(cs)==18
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({375}|{x for v in matches.values() for x in v})
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[i for i in machine['issues'] if i not in prior['issues']];removed=[i for i in prior['issues'] if i not in machine['issues']]
assert not added and not removed
f=p/'README.md';s=f.read_text()
for a,b in [('243問','245問'),('204問','202問'),('256問2130箇所','258問2148箇所'),('256問を','258問を')]:s=s.replace(a,b)
f.write_text(s)
url='https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf'
report=f'''

## 第95バッチ（2026-10-15）

GitHubの第94バッチ67290abc256a53c990b6a114a3ca1af4e19fc9bdをfetchし、新しい作業場へ反映。S144 Richards（2006）著者公開冊子52頁を再取得。印刷19・28・30頁の本文と版面を直接照合した。

Q_M_025は、内容中心教授法（CBI）という概念を維持して、内容からの編成と正確さ・評価という実施上の論点を問う記述へ変更。CBIとCLILを同義と扱う説明や、未取得の他教授法原著に依存する説明は撤回。Q_M_040はRichards19頁のジグソー活動に限定し、班が情報の一部を分有し、伝え合い全体を完成する条件を明示。意見共有・情報変換・推論差と、設問が明示した構成を比較する。ジグソー原案の専門家群を含む全手順を照合したとはしない。模式授業案は監査で構成し、原著の実証例とはしていない。

設問・全4肢・独立正答・4解説を照合し、2問18箇所を改訂。独立正答3・4は不変。確認済み245・修正必要53・要追加確認202、残件255。累積258問2148箇所。全500問・解説500件と元v8のSHA256は維持。台帳の原文はv8スナップショットで、改訂はchangesと作業稿を参照する。

全問構造検査および公開可否回帰8条件に合格。機械警告60件は前回と同一。documentsの描画手順で日本語フォント適用QAコピーを{len(pages)}頁描画。18変更文字列のある{'・'.join(map(str,reviewed))}頁を完成PDFから150dpiのCairo PNGにして直接目視。全頁最終QAと未確認問題の監査が残り、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第95バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+f'\n\n## 第95バッチ S144追加照合（2026-10-15）\n[S144 Richards2006著者公開52頁冊子]({url})を再取得。印刷19頁（PDF23頁）はジグソー、意見共有、情報変換、推論差の説明、28頁（PDF32頁）は内容を出発点とする編成と単元での利用、30頁（PDF34頁）は正確さ・専門性・評価の論点を本文・版面照合。Q_M_025・Q_M_040の全4肢・4解説に適用。CBIとCLILの完全同義性、Aronson原案全手順、引用先Krahnke等の著書全体、日本語授業での普遍効果は承認しない。全文転載せず取得PDFハッシュをevidence/batch95_review.jsonに記録。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第95バッチ\nNoto Sans JP適用コピー{len(pages)}頁を描画し、18変更文字列のある'+ '・'.join(map(str,reviewed))+f'頁を150dpi Cairo画像で直接確認。日本語欠字・重なり・クリッピングなし。全頁最終目視は未了。\n')
e={'batch':95,'base_commit':'67290abc256a53c990b6a114a3ca1af4e19fc9bd','fully_rejudged':sorted(targets),'edits':18,'status_counts':m['status_counts'],'remaining':255,'independent_answers':{'Q_M_025':3,'Q_M_040':4},'sources':{'S144':{'url':url,'sha256':sha(root/'richards95.pdf'),'pdf_pages':52,'image_verified_printed_pages':[19,28,30],'page_mapping':'PDF page=printed page plus4','limits':'No equivalence with CLIL; no full acquisition of Aronson original procedure or Krahnke1987; no universal effectiveness claim'}},'machine_warnings':60,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']={'Q_M_025':'375頁末尾に解説見出しと正解3、376頁に全4解説。欠字はないが最終組版で見出しの孤立を解消する。'}
(p/'evidence/batch95_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+'最終組版の残件：Q_M_025解説の見出し・正解3が375頁末尾、本文4肢が376頁へ分離。見出しの孤立を解消する。\n')
print('Recorded2 fullreviews/18 edits;245 confirmed/255 remaining;pages',reviewed)
