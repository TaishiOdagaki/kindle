"""One-time record: one full academic approval and two explicitly partial checks."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch86-qa';targets={'Q_4_041','Q_4_016','Q_3_008'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':218,'修正必要':57,'要追加確認':225}
cs=json.loads((p/'changes_batch86.json').read_text());assert len(cs)==9
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==400
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=[70,268,269];assert sorted({n for v in matches.values() for n in v})==reviewed
for i in reviewed:Image.open(render/f'review-{i}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert len(machine['issues'])==55 and machine['issues']==prior['issues']
f=p/'README.md';s=f.read_text()
for a,b in [('217問','218問'),('226問','225問'),('230問1890箇所','231問1899箇所'),('230問を','231問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第86バッチ（2026-10-15）

最新HEAD 3911d93c026631d43eae27d6432e84ea1f2ff2a5を取得して継続。Krashen本人公開S13の全209頁PDFを再取得。原刊1982年、PDF奥付のインターネット版2009年7月と序文を区別し、検索の更新表示を刊年としない。印刷10・15〜16・21〜22・31〜32・83頁を本文と画像で照合した。全209頁を精読したとはせず、他の引用研究の原著全体や現在の理論的合意を承認しない。

Q_4_041は特定著書の仮説内の主張へ限定し、全4肢・独立正答1・全4解説を照合して9箇所改訂。理解可能インプット、低フィルターの状況、発話能力の出現、習得／学習の区別、モニターの条件を区別した。条件は必要であって十分とはしない。Krashen/Terrell共同著書全体の取得や、仮説の実証的妥当性・教授法の普遍的効果を保証する設問とはしない。

Q_4_016は全4肢・4解説を再読し、S13で照合できた選択肢1の高不安・高フィルター推奨の誤りと、未確認のラポール／心理的安全性の定義・不可欠性・ピア関係・指導効果を分けた。要追加確認を維持。Q_3_008も全4肢・4解説を再読し、成人の習得可能性と母語話者同等到達の非保証だけを追加照合。LADを普遍的確定事実とする問題、幼児L2を含む範囲不足、転移・個人差・明示的指導の全主張は未了のため修正必要を維持した。部分資料照合を問題全体の承認にしていない。

新規確認済みは1問、原稿改訂1問9箇所、ほか2問は資料照合の進展と未確認事項を具体化。確認済み218・修正必要57・要追加確認225、残件282。累積231問1899箇所。全500問・500解説、正答番号と影響外本文、v8ハッシュを維持。台帳の原文はv8スナップショットで、改訂はchangesと作業稿を参照。

全問機械検査と公開可否回帰8条件に合格。警告55件は前回と同一。documentsのrender_docx.pyでNoto Sans JP Static Regular400をQAコピーだけに適用して400頁描画し、対象3頁を完成PDFから150dpiで再描画。70・268・269頁を直接目視し、9変更文字列の反映と日本語表示、全4タグを確認。採用画像はPIL検査済み。Q_4_041の解説268〜269頁は最終改頁調整候補。全400頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第86バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://www.sdkrashen.com/content/books/principles_and_practice.pdf'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## 第86バッチ S13原著の追加照合（2026-10-15）

Krashen [Principles and Practice in Second Language Acquisition]({url})、原刊1982年・PDF奥付インターネット版2009年7月、全209頁を著者サイトから再取得。印刷10→PDF17、15→22、16→23、21→28、22→29、31→38、32→39、83→90頁を本文・画像照合。Q_4_041は全4肢・4解説と独立正答1を照合し改訂・確認済み。Q_4_016は選択肢1の情意フィルターに関する主張だけを照合し、ラポールの定義と指導効果は未確認のまま。Q_3_008は成人の習得可能性・到達保証なし・情意面の理論内の位置づけだけを照合し、比較全体は修正必要のまま。部分照合を全問承認や現在の実証的合意に拡張しない。Terrellとの共同著書、引用先の原研究全体は未取得。PDFハッシュと範囲はevidence/batch86_review.jsonに記録し全文を転載しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第86バッチ\nbatch86-qaへ400頁を描画し、70・268・269頁を完成PDFから150dpiで再描画して直接精読。採用3画像はPIL検査済み。9変更文字列をPDF内で確認、日本語欠字・切れ・重なりなし、Q_4_041の全4正誤タグを確認。NotoSansJPStatic埋込みあり。解説268〜269頁は最終改頁調整候補。全400頁の最終目視は未了。\n''')
e={'batch':86,'base_commit':'3911d93c026631d43eae27d6432e84ea1f2ff2a5','fully_rejudged':['Q_4_041'],'partial_checks_not_approved':{'Q_4_016':'要追加確認を維持。S13で選択肢1のみ照合、ラポール等の定義・効果は未確認。','Q_3_008':'修正必要を維持。成人の習得可能性・到達保証なしのみ追加照合。'},'edits':9,'status_counts':m['status_counts'],'remaining':282,'independent_answer':{'Q_4_041':1},'sources':{'S13':{'url':url,'sha256':sha(root/'krashen86.pdf'),'pdf_pages':209,'original_year':1982,'internet_edition':'July 2009 per colophon','image_verified_page_map':{'10':17,'15':22,'16':23,'21':28,'22':29,'31':38,'32':39,'83':90},'scope':'Author hypotheses only. Not a full209page close reading or current consensus verification.'}},'machine_warnings':55,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'review-{i}.png') for i in reviewed},'release_ready':False}
(p/'evidence/batch86_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 1 full review / 9 edits + 2 partial checks; 218 confirmed / 282 remaining')
