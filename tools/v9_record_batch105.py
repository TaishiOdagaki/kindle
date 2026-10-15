"""Record source verification and changed-page visual inspection for batch105."""
import json,hashlib,subprocess,re,io,csv,bisect,gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch105-qa';targets={'Q_O_050','Q_MO_014','Q_MO_015'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':270,'修正必要':41,'要追加確認':189}
cs=json.loads((p/'changes_batch105.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v});assert reviewed==[158,190,191,360,394,395]
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert removed==[] and len(machine['issues'])==64 and added==[['P1','Q_O_050','(正)4の解説が否定で終わる/肯定の(誤)がある: [1, 2, 3]']]
raw=gzip.decompress((p/'evidence/S163_core_curriculum_20240401.pdf.gz').read_bytes());assert len(raw)==514031 and hashlib.sha256(raw).hexdigest()==sha(root/'S163-105-retry.pdf')
f=p/'README.md';s=f.read_text()
for a,b in [('267問','270問'),('192問','189問'),('273問2348箇所','276問2375箇所'),('273問を','276問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第105バッチ（2026-10-16）

最新GitHub HEAD cd6b7809b3ebfb4ca8ac1caf611789c7befd1f6cから別作業場へ復元。文科省公式登録案内の現時点のリンク先から、令和6年4月1日日本語教育部会決定「登録日本語教員実践研修・養成課程コアカリキュラム」全15頁を取得・全文読了。初回ダウンロードは末尾欠損で描画不能だったため使用せず、再取得した514031バイトの15頁PDFを検証した。PDF3頁（表1）・14頁（印刷13頁の〈35〉〈36〉）は画像も直接確認し、表の列と到達目標の対応を確認した。原PDFはgzipで原バイトのまま保存し、解凍一致を検査した。

Q_O_050は必須内容〈36〉の著作権・情報資源の扱い方の理解と照合。Q_MO_014は担当者との確認を知識の実践活用として位置付ける適用判断に限定し、事前確認による適法性・トラブル回避の保証を除いた。Q_MO_015は授業目標との適合と権利の確認を両方求め、独自教材という名称だけで権利処理不要と扱わず、CC BY 4.0の作者名以外の条件を明記。CC公式本文S162と保存済みe-Gov本則S26も利用条件に照合した。

3問の設問・全4肢・独立正答・全4解説を照合し27箇所改訂。独立正答O50=4・MO14=2・MO15=2、番号変更なし。確認済み270・修正必要41・要追加確認189、残件230。累積276問2375箇所。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照する。

全500問・解説500件、v8不変ハッシュ、影響外本文、正解表・タグ・リンクを維持。公開可否回帰8条件合格。機械警告63→64件。新規O50のP1は、正答解説末尾で「確認だけで個々の利用が必ず適法になるという意味ではない」と限定したための誤検出。他63件は同一。documents手順でNoto Sans JP適用QAコピー{len(pages)}頁を描画、27変更文字列を検出し、158・190・191・360・394・395頁を150dpi画像で直接目視した。O50は設問と4肢が158頁、全4解説が360頁。MO14は190頁に全4肢、解説1は394頁、2～4は395頁。MO15は190頁の設問・肢1～3と191頁の肢4に分離し、全4解説は395頁。欠字・重なり・クリッピングは見られないが、選択肢と解説の分離は最終組版で調整する。全頁最終目視・残230問の照合は未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第105バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第105バッチ S163（2026-10-16）

文科省 [登録機関の登録等に関する公式案内](https://www.mext.go.jp/a_menu/nihongo_kyoiku/mext_02667.html) のリンク先を確認し、[令和6年4月1日決定・登録日本語教員実践研修・養成課程コアカリキュラム](https://www.mext.go.jp/content/20240321-ope_dev02-000034812_4.pdf) 全15頁を取得・全文読了。PDF3頁の表1（知識・技能・態度）、PDF10頁の一般目標⑫、PDF14頁（印刷13頁）の必須教育内容〈35〉〈36〉を対象3問と照合し、表1と〈36〉は画像でも確認。情報資源の扱い方の理解と、表1の技能（3）の知識の現場への活用を区別し、ケースへの適用判断を明記した。全カリキュラム項目の学説を実証的に承認したとはしない。指定日版を対象とし、未掲載の将来改訂まで推測しない。

原PDFはevidence/S163_core_curriculum_20240401.pdf.gz。初回取得は末尾欠損のため廃棄候補の一時ファイルとしてのみ残し監査に不使用。再取得後pdfinfoで15頁・514031バイトを確認、gzipの解凍一致とSHA256を記録。令和7年10月22日実務説明会資料も探索時に本文の関連頁を参照したが、判定の正本は本決定本文とし、説明会の検索抜粋だけで承認していない。Q_MO_015の利用許諾はS162公式CC BY 4.0第2・3条、オンデマンドは保存済みS26本則第35条も追加照合。\n''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第105バッチ\nNoto Sans JP適用QAコピー{len(pages)}頁。27変更文字列を検出し158・190・191・360・394・395頁を150dpi画像で直接目視。MO14解説1/2とMO15肢3/4間の改頁を最終組版で調整する。S163原資料PDF3・14頁の表も直接目視。全頁最終目視未了。\n')
e={'batch':105,'base_commit':'cd6b7809b3ebfb4ca8ac1caf611789c7befd1f6c','fully_rejudged':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':230,'independent_answers':{'Q_O_050':4,'Q_MO_014':2,'Q_MO_015':2},'sources':{'S163':{'url':'https://www.mext.go.jp/content/20240321-ope_dev02-000034812_4.pdf','discovery_page':'https://www.mext.go.jp/a_menu/nihongo_kyoiku/mext_02667.html','date':'2024-04-01','retrieved':'2026-10-16 JST','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'full_text_read':True,'pages':15,'source_table_visually_reviewed_pdf_pages':[3,14],'focused_scope':'Table1 practical use of learned knowledge; general goal12; mandatory content36 information-resource handling','first_download_truncated_not_used':True},'S162':'Official full legalcode acquired batch103; sections2,3','S26':'Original response acquired batch101; article35 reuse'},'machine_warnings':64,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'source_table_image_sha256':{str(x):sha(root/f'S163-105-page{x}.png') for x in [3,14]},'pagination_followup':'MO14 exp1/2 split394/395; MO15 options3/4 split190/191. Review final pagination.','release_ready':False}
(p/'evidence/batch105_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 full reviews/27 edits;270 confirmed/230 remaining')
