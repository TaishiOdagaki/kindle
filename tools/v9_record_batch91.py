"""Record batch91 after manual changed-page image inspection."""
from pathlib import Path
import json, hashlib, subprocess, re, csv, io
from PIL import Image
p=Path('audit/v9'); render=Path('/workspace/scratch/697c245d9771/batch91-qa')
targets={f'Q_5_{n:03}' for n in [96,97,98]}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':235,'修正必要':54,'要追加確認':211}
cs=json.loads((p/'changes_batch91.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');n=len(pages)-1
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs if c['after']};assert all(matches.values())
reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:Image.open(render/f'review-{x}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==57
f=p/'README.md';s=f.read_text()
for a,b in [('232問','235問'),('212問','211問'),('56問','54問'),('245問2030箇所','248問2057箇所'),('245問を','248問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第91バッチ（2026-10-15）

最新HEAD494d39c4b3cf869896587fddc761c6e4285076d7から継続。Thomas（1983）原論文の公開複製の本文を取得し、99〜101、104〜105、109〜110頁を照合。出版社で書誌も照合した。ScribdのAI説明・自動Q&Aは根拠に使用せず、頁番号・節見出し付きの論文本体を区別した。出版社PDFそのものを取得したとは扱わない。

Q_5_096は社会語用論を能力名と同一視した設問と、語用言語学を形態素接続だけに限定した説明を修正。Q_5_097は日本語での唯一の正しい断り方や、文体変更の効果の普遍断定を撤回し、意図・受け取り方を確認して学習者の選択を支える指導を問う。Q_5_098は褒めを肯定する応答が常に失敗との断定を撤回。社会的権利・義務の評価のずれと、形式に対応する語用的な力のずれを、原因を明示した架空事例で区別する。実際の原因が常に一つ、敬語・文法と社会的判断が無関係とはしない。原著の理論的区別と指導上の立場の照合であり、日本語固有の断り・褒め応答の頻度や指導効果を実証したという承認ではない。

3問27箇所、設問・全4肢・独立正答・全4解説を照合して改訂。独立正答1・3・3、番号変更なし。確認済み235・修正必要54・要追加確認211、残件265。累積248問2057箇所。500問・500解説、影響外本文、v8ハッシュを維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。

全問機械検査と公開可否回帰8条件に合格、警告57件は前回と同一。documentsのrender_docx.pyを用い日本語フォント適用QAコピーを{n}頁描画し、変更文字列のある{ '・'.join(map(str,reviewed)) }頁を完成PDFから150dpi再描画して直接目視。27変更文字列・全4正誤タグを確認。全頁の最終目視は未了で、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第91バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://www.scribd.com/document/258926296/Thomas-1983-Cross-Cultural-Pragmatic-Failure'
f=p/'sources.md';assert '| S150 |' not in f.read_text();f.write_text(f.read_text()+f'''

## 第91バッチ 原著本文の取得と照合

| ID | 資料 | 取得・使用範囲 | 対象 |
|---|---|---|---|
| S150 | Jenny Thomas（1983）Cross-Cultural Pragmatic Failure, Applied Linguistics 4(2),91–112。[出版社書誌](https://doi.org/10.1093/applin/4.2.91)／[公開本文複製]({url}) | 2026-10-15取得。99〜101頁の区別と図1の境界注記、104〜105頁の社会的条件、109〜110頁の原因の連続性と指導上の選択尊重を本文照合。公開HTMLの論文本体を取得。出版社PDFは未取得。AI説明・検索抜粋・付属Q&Aは根拠にしない。 | Q_5_096・097・098 |

分類条件を明示した教材用架空事例を使用。民族全体の慣習や日本語の断り・褒め応答の実態を調査したものではない。短い発話だけから母語転移・失礼な人格を診断しない。公開複製の本文と頁見出しに基づく照合であり、引用先原著の全取得でもない。HTML取得ファイルのハッシュ・本文取得段階はevidence/batch91_review.jsonに記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第91バッチ\n日本語フォント適用QAコピー{n}頁を描画。変更頁'+ '・'.join(map(str,reviewed))+f'を150dpi再描画・直接目視、27変更文字列と全4正誤タグを確認。全{n}頁の最終目視は未了。\n')
e={'batch':91,'base_commit':'494d39c4b3cf869896587fddc761c6e4285076d7','fully_rejudged':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':265,'independent_answers':dict(zip(sorted(targets),[1,3,3])),'sources':{'S150':{'url':url,'publisher_metadata':'https://doi.org/10.1093/applin/4.2.91','retrieved_format':'public original-article HTML transcription; publisher PDF not obtained','retrieved_html_sha256':sha('/workspace/scratch/697c245d9771/thomas91.html'),'body_verified_printed_pages':['99–101','104–105','109–110'],'excluded':'AI title, description, automatic Q&A, search snippets; empirical claims about Japanese refusal or compliment-response norms; cited original studies not obtained'}},'fictional_scenarios':['Q_5_097','Q_5_098'],'machine_warnings':57,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']='Q_5_096 explanation4 continues337–338; readable and tags intact. Final keep-together tuning pending.'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;f.write_text(f.read_text()+'\n第91バッチ改頁調整候補：問96の解説4が337〜338頁に分かれる。欠字・切れはないが、最終版の段落・設問単位の改頁調整は未了。\n')
(p/'evidence/batch91_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded3fullreviews/27edits;235confirmed/265remaining;pages',reviewed)
