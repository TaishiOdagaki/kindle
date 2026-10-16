"""Record primary-author BICS/CALP rejudgments and changed-page QA."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa126';ids=['Q_2_004','Q_4_084']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':325,'修正必要':30,'要追加確認':145}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newflags=[i for i in machine['issues'] if i not in prior['issues']];removed=[i for i in prior['issues'] if i not in machine['issues']]
assert len(machine['issues'])==95 and {i[1] for i in newflags}==set(ids) and all(i[0]=='P1' for i in newflags)
assert len(removed)==1 and removed[0][0:2]==['A1','Q_2_004']
cs=json.loads((p/'changes_batch126.json').read_text());assert len(cs)==18
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for n in [1,2,3,5]:
 with Image.open(root/f'cummins-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('323問','325問'),('147問','145問'),('324問2725箇所','326問2743箇所'),('324問を','326問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第126バッチ（2026-10-16）

Q_2_004・Q_4_084の設問、全4肢、独立正答、全4解説をCummins本人の2008年著者稿に照合し、2問18箇所改訂。正答は双方3。大学が公開する原PDFを取得し、表紙とPDF2〜3・5頁の本文・画像を確認した。検索抜粋や出版社の抄録による承認ではない。

会話の流暢さだけで教科学習上の理解・表現を推定しないという教育的示唆を保持。CALPは口頭・書面の双方を含み、BICS/CALPは言語能力の全てを尽くす二分法ではない。課題の文脈的支えと認知的要求は既有知識・関心等によって相対的であり、「文脈が皆無」「認知能力そのものの不足」とはしない。原稿の一律の2年/5〜7年、全JSL児童の認知能力の不足や同じ支援が必須という読みを削除。著者が扱う英語圏集団での期間の議論を日本の全児童に一般化せず、引用された旧個別研究や言語間転移を今回独立検証したとは扱わない。

確認済み325・修正必要30・要追加確認145、残175問。累積326問2743箇所、全500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。全500問の構造、キー/タグ/表/リンク、影響外本文、v8不変を検査し公開可否回帰8条件を通過。警告は95件：Q_2_004の断定語警告1件が解消、2問の正解解説の留保表現をP1が誤検出した2件が追加。正誤ラベル・解説・単一正答性を本文照合しており、留保を削って警告を消す処理はしていない。

描画環境を再構成。LibreOffice複製で所有者保持のみ失敗したが、必要な実行ファイルと依存資産のコピー・実行は成功。日本語フォントはNoto Sans JPの字形収録を確認し、QA専用コピーに適用。原稿v8と作業稿の書体はこのQA操作で変更していない。
'''
report+=f'\n新規{pagecount}頁描画、全18変更文字列を検出。'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視し完全読込み確認。変更箇所の欠字・重なり・文字切れなし。隣接問題との改頁を含む全頁最終組版QAと残175問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第126バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第126バッチ S190（2026-10-16）

Cummins (2008), *BICS and CALP: Empirical and Theoretical Status of the Distinction*, Encyclopedia of Language and Education, Volume 2, pp.71–83。[大学公開著者稿PDF](https://eclass.upatras.gr/modules/document/file.php/PDE1535/CumminsBICSCALPSpringer2007.pdf)を取得。表紙の著者・書誌、PDF2〜3・5頁の本文・画像を精読。原稿頁には印刷頁番号がないためPDF頁を指定。会話と学術的言語の概念的区別、全能力の網羅理論ではない留保、口頭/書面の両側面、会話から教科学習を推定する危険、文脈と認知的要求の相対性を使用。日本の全JSL児童の期間・支援効果・認知能力不足、言語間転移、引用先の旧個別研究の再検証は承認対象外。全文ファイル取得は論文の全主張の承認を意味しない。URL・原バイトSHA256・範囲はevidence/batch126_sources.json。原PDFは非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第126バッチ\n'+f'Noto Sans JP新規{pagecount}頁、全18変更文字列検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=126,base_commit='ac56a89ab3e5eaf23d76e2fe2cf3a0896897e2e0',fully_rejudged=ids,edits=18,independent_answers=dict.fromkeys(ids,3),sources=['S190'],status_counts=m['status_counts'],remaining=175,machine_warnings=95,new_warnings=newflags,removed_warnings=removed,warning_review='P1 matches qualifications in correct explanations, not wrong key or multiple correct answers',readiness_gate='8 cases passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S190_PDF':[1,2,3,5]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch126_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('325 confirmed/175 remaining;18 edits recorded',reviewed)
