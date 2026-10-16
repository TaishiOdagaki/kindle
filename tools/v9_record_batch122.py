"""Record 2020 easy-Japanese source review and changed-page QA only."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa122';ids=['Q_1_005','Q_1_018','Q_1_021']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':318,'修正必要':32,'要追加確認':150}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==92 and len(added)==2 and {x[1] for x in added}=={'Q_1_018','Q_1_021'} and all(x[0]=='P1' for x in added) and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch122.json').read_text());assert len(cs)==22
matches=json.loads((r/'matches.json').read_text());assert len(matches)==22 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for name in ['easy-source-04.png','easy-source-06.png','easy-source-07.png','easy-single-8.png','easy-single-9.png','easy-single-10.png','easy-page11.png']:
 with Image.open(root/name) as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('315問','318問'),('150問（未精読','150問（未精読'),('153問','150問'),('316問2664箇所','319問2686箇所'),('316問を','319問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第122バッチ（2026-10-16）

Q_1_005・018・021の設問・全4肢・独立正答・全4解説を、出入国在留管理庁・文化庁の2020年8月「在留支援のためのやさしい日本語ガイドライン」の印刷3・5〜10頁に本文・画像照合。22箇所改訂し正答3・1・3を維持。書き言葉中心の作成提案に範囲を明示した。同資料は読み手の言語背景や日本語能力に応じた柔軟な調節を求め、あえて厳密な基準を置かないとする。旧日本語能力試験3〜4級/N4〜N5相当の語彙・文法への一律限定を撤回。短文・ですますは同資料の提案として維持するが全場面の絶対規則とはしない。重要な災害用語・日常語は説明を添えて残すこともある。意味や必要な条件を削ってよいとしない。

外来語の原語との意味・発音の違いへの注意と、バス等の例外を確認。未照合の和製英語の個別分類やオノマトペ全般、結論先置の一般規則を正当化せず、明示された情報整理・敬語等に誤答を改訂。二重否定・受身・使役を避ける作成提案は、正確な意味を犠牲にした機械的変換の義務ではない。多言語資料との使い分け、図・記号等の補助、日本語教師や対象者に伝わるかを確認する工程を照合。JIS/国際規格の個別仕様、全外国人・全障害種別に同じ配慮が有効という実証、要員コストや全翻訳の限界を未取得資料から承認しない。統計の数値や引用された一次調査は今回の承認対象外。

確認済み318・修正必要32・要追加確認150、残件182。累積319問2686箇所、500問維持。台帳の原文はv8スナップショットであり、改訂はchangesと作業稿を参照。全500問の構造、正答タグ/表/リンク、影響外本文、v8不変と公開可否回帰8条件を通過。警告90→92、新規P1はQ_1_018の一律試験級限定を否定する正答解説と、Q_1_021の全員保証・翻訳廃止を否定する留保の誤検出。正答を否定しておらず、他90件と検出器を保持。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全22変更文字列を検出、'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。既存の隣接問題・解説の改頁や見出し分離は最終組版確認へ残す。全頁最終目視と残182問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第122バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第122バッチ S189（2026-10-16）

出入国在留管理庁・文化庁[在留支援のためのやさしい日本語ガイドライン 2020年8月](https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/pdf/92484001_01.pdf)。文科省の[公開案内](https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/92484001.html)から原18頁を通常取得。印刷3・5〜10/PDF4・6〜11の本文・全画像を精読。用途・柔軟な調節・多言語との使い分け、情報整理、短文、外来語、二重否定・受身・使役、敬語、重要語説明、表記、読み手等の確認を使用。印刷4は追加本文参照にとどまり成立史の独立原著照合とはしない。印刷3の統計は注記・調査対象も読んだが引用一次調査未取得のため数値や全外国人への一般化を承認しない。参照先ツールの現行挙動も未承認。書き言葉中心の2020文書を全時代・全話し言葉の絶対基準にしない。

原バイトURL・SHA256・範囲はevidence/batch122_sources.json。原文PDFは非転載。途中の不正PNGはQAから除外し、単頁再描画で完全読込みを確認した有効画像だけを使用。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第122バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全22変更文字列検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=122,base_commit='1f725c69d7de27aece9ce83e5671373a10fcea6c',fully_rejudged=ids,edits=22,independent_answers=dict(zip(ids,[3,1,3])),sources=['S189'],status_counts=m['status_counts'],remaining=182,machine_warnings=92,new_warnings=added,new_warning_judgment='P1 false positives from qualified rejections of uniform test levels and universally guaranteed comprehension',readiness_gate='8 cases passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S189_PDF':[4,6,7,8,9,10,11]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch122_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('318 confirmed/182 remaining;22 edits recorded',reviewed)
