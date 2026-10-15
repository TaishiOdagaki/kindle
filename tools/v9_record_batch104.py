"""Record direct changed-page QA and keep untouched ledger CSV rows verbatim."""
import json,hashlib,subprocess,re,io,csv,bisect,gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch104-qa';targets={'Q_4_124','Q_4_125'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':267,'修正必要':41,'要追加確認':192}
cs=json.loads((p/'changes_batch104.json').read_text());assert len(cs)==18
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v});assert reviewed==[101,102,300,301]
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==63
raw=gzip.decompress((p/'evidence/egov_batch101.xml.gz').read_bytes());prior_ev=json.loads((p/'evidence/batch101_review.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior_ev['sources']['S26']['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('265問','267問'),('194問','192問'),('271問2330箇所','273問2348箇所'),('271問を','273問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第104バッチ（2026-10-16）

最新GitHub HEAD 1b28c25de45a3d2fbabf3ceccdafd6f864ae90c6から別作業場へ復元。第101バッチ保存済みe-Gov原応答のSHA256同一性を確認し、本則第35条全3項、第32条・第48条全項を追加照合した。Q_4_124は、補償金の支払が第1項の要件を代替するという誤解、リアルタイム全般と第3項の限定的な同時授業送信の混同、曖昧な無償適用対象を改訂。指定団体の現行指定状況や年度特例まで確認したとはしない。

Q_4_125は、第32条第1項の公表済み・公正慣行・引用目的上正当な範囲と、第48条第1項第1号の引用複製時の出所表示を区別した条文対応問題へ改訂。未取得の裁判例に基づく主従・区別性を、条文そのものの固定的な独立要件として並べる旧解説を撤回した。各具体的利用の適法性を、出所表示や文章量だけで包括承認しない。

2問の設問・全4肢・独立正答・全4解説を照合し18箇所改訂。独立正答4_124=4・4_125=2、番号変更なし。確認済み267・修正必要41・要追加確認192、残件233。累積273問2348箇所。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照する。

全500問・解説500件、v8不変ハッシュ、影響外本文、正解表・タグ・リンクを維持。公開可否回帰8条件合格。機械警告63件は全て前回と同一。documents手順でNoto Sans JP適用QAコピー{len(pages)}頁を描画、18変更文字列を検出し、101・102・300・301頁を150dpi画像で直接目視した。4_124の設問・全4肢は101頁、解説4は301頁へ分離。4_125の見出し・設問は101頁、全4肢は102頁へ分離し、全4解説は301頁。欠字・重なり・クリッピングは見られないが、これらの改頁は最終組版で調整する。全頁最終目視・残233問の照合は未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第104バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第104バッチ S26追加照合（2026-10-16）

[e-Gov著作権法API](https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048) の第101バッチ保存済み原応答をSHA256一致で再利用し、本則第35条全3項をQ_4_124、第32条・第48条全項をQ_4_125と照合。対応本文はevidence/egov_batch101_excerpts.txt及びegov_batch103_excerpts.txtにも記録済み。第35条第3項の直接受講者への作品提供・提示等と別の場所で同時に同じ授業を受ける者への送信という限定を確認した。第32条第1項の条件と第48条第1項第1号・第2項の表示を別に扱った。新規取得とは数えず、全法改正経過措置・年度特例・指定団体の現行指定・未取得裁判例までの照合を意味しない。旧主張のうち根拠未取得のものは承認せず、同じ著作権領域の条文対応問題へ差替えた。\n''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第104バッチ\nNoto Sans JP適用QAコピー{len(pages)}頁。18変更文字列を検出し101・102・300・301頁を150dpi画像で直接目視。4_124解説4と4_125の設問/肢の改頁を最終組版で調整する。全頁最終目視未了。\n')
e={'batch':104,'base_commit':'1b28c25de45a3d2fbabf3ceccdafd6f864ae90c6','fully_rejudged':sorted(targets),'edits':18,'status_counts':m['status_counts'],'remaining':233,'independent_answers':{'Q_4_124':4,'Q_4_125':2},'source':'S26 original response acquired batch101, verified SHA256 reuse','source_raw_sha256':hashlib.sha256(raw).hexdigest(),'source_reuse_not_new_acquisition':True,'scope':['35 all three paragraphs','32 all paragraphs','48 all paragraphs'],'machine_warnings':63,'new_machine_warnings':[],'removed_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'pagination_followup':'Q4_124 exp4 split to301; Q4_125 stem101/options102. Review final pagination.','release_ready':False}
(p/'evidence/batch104_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 2 full reviews/18 edits;267 confirmed/233 remaining')
