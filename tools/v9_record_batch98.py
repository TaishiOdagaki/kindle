"""Run only after directly inspecting completed batch98 review images."""
import json,hashlib,subprocess,re,io,csv,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch98-qa-restored';k='Q_M_046'
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[key].replace('\r\n','\n') if key==k else raw for key,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':249,'修正必要':51,'要追加確認':200}
cs=json.loads((p/'changes_batch98.json').read_text());assert len(cs)==9
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==60
f=p/'README.md';s=f.read_text()
for a,b in [('248問','249問'),('52問','51問'),('261問2175箇所','262問2184箇所'),('261問を','262問を')]:s=s.replace(a,b)
f.write_text(s)
source={'id':'S76','url':'https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/03-03-01.php','title':'東京外国語大学言語モジュール 無声化母音の産出','retrieved':'2026-10-16 JST','acquisition':'公開HTML全56行を再取得・精読。検索抜粋ではない。','scope':'51〜54行：い・うの声帯振動の消失、無声子音間の語中例、です・ますの文末例、アクセント核があると起こりにくい傾向。','limits':'教材の説明との対応に限定。音声ファイル未測定。全方言・全話者・必発性や2026年の頻度を承認しない。刊年不明を推定しない。','sha256':sha(root/'S76-98.html')}
report=f'''

## 第98バッチ（2026-10-16）

最新GitHub HEAD 510ed169439dbc5f715722019ee8d96eedaa2b10から復旧。未保存の第97バッチ3問は加算せず、Q_M_046だけを資料再取得から独立再判定した。東京外国語大学「無声化母音の産出」の公開HTML全文を再取得し、設問・全4肢・独立正答・全4解説を本文と照合。「です」の語末例を無声子音に挟まれた例として扱う混同を撤回し、無声化を声帯振動の消失として定義。語中・文末の条件とアクセント核による起こりにくさを指定教材の範囲で区別した。必発性や全方言への一般化はしない。

1問9箇所。独立正答3、番号変更なし。確認済み249・修正必要51・要追加確認200、残件251。累積262問2184箇所。全500問・解説500件、元v8ハッシュ、影響外本文、正解表・リンク・正誤タグを機械検査で維持。公開可否回帰8条件に合格。既存警告60件は内容まで不変。正答長の分布は検査結果に記録し、長さ調整のため学術的判断を変更していない。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照する。

documents手順でNoto Sans JP適用QAコピーを{len(pages)}頁描画。9変更文字列をPDFで検出し、該当する{'・'.join(map(str,reviewed))}頁を150dpi画像で直接目視した。旧LibreOfficeコピーが終了135で失敗したため、同梱ランタイムから新規コピーを構築し描画を復旧した。失敗した描画をQA根拠に使っていない。全頁最終目視と残251問の学術照合は未了、作業稿は出版不可。M47・M48の前回未保存分は未解決として維持する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第98バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第98バッチ S76追加照合（2026-10-16）\n\n既存S76 [無声化母音の産出]('+source['url']+')を全文再取得し、Q_M_046の全9項目を照合。'+source['scope']+' '+source['limits']+' 既存Q_5_019の判定を上書きしない。原バイトのハッシュはevidence/batch98_review.json参照。本文全文は転載しない。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第98バッチ\nNoto Sans JP適用コピー{len(pages)}頁。9変更文字列のある'+ '・'.join(map(str,reviewed))+'頁を150dpi画像で直接目視。旧描画環境の終了135から同梱ランタイム新規コピーで復旧。全頁最終目視は未了。\n')
f=p/'evidence/recovery_20261016.md';f.write_text(f.read_text()+'\n## 第98バッチでの再照合\nQ_M_046はS76本文再取得・9項目改訂・独立正答3・機械検査・変更頁画像QAを実施。M47・M48は未確認のまま。件数は本バッチのGitHub保存確認後に249問を採用する。前回の251問という未保存値とは区別する。\n')
e={'batch':98,'base_commit':'510ed169439dbc5f715722019ee8d96eedaa2b10','fully_rejudged':[k],'edits':9,'status_counts':m['status_counts'],'remaining':251,'independent_answers':{k:3},'sources':[source],'machine_warnings':60,'machine_issues_unchanged':True,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
(p/'evidence/batch98_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 1 full review/9 edits;249 confirmed/251 remaining;pages',reviewed)
