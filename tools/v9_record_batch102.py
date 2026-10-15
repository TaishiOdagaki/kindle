"""Record after direct inspection of every batch102 changed page image."""
import json,hashlib,subprocess,re,io,csv,bisect,gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch102-qa';targets={'Q_O_046','Q_O_047','Q_O_049'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':263,'修正必要':43,'要追加確認':194}
cs=json.loads((p/'changes_batch102.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v}|{158})
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert removed==[] and added==[['P1','Q_O_047','(正)3の解説が否定で終わる/肯定の(誤)がある: [1, 2, 4]']] and len(machine['issues'])==62
raw=gzip.decompress((p/'evidence/egov_batch101.xml.gz').read_bytes());ev=json.loads((p/'evidence/batch101_review.json').read_text());assert hashlib.sha256(raw).hexdigest()==ev['sources']['S26']['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('260問','263問'),('44問','43問'),('196問','194問'),('268問2285箇所','270問2312箇所'),('268問を','270問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第102バッチ（2026-10-16）

最新GitHub HEAD ac9d5d97c59eb92814b927657de6c444fd2312cdから別作業場へ復元。第101バッチ取得のe-Gov原応答をgzipから解凍し、原SHA256の同一性を検証して追加照合した。Q_O_046は第35条第1項の非営利設置・利用主体・授業過程・公表作品・必要限度・ただし書を整理し、権利者自身の複製と同条の対象を曖昧に対比する旧肢を改訂。Q_O_047はただし書の適用範囲を同条に限定し、他の許諾・権利制限が使える可能性まで否定しない。Q_O_049は元の創作的表現を引き継ぐ要約・翻案を条件として明示し、第27条の原則、第47条の6第1項第1号の第35条を根拠とする翻案の特例、第50条の著作者人格権への留保、第20条の例外を区別した。全要約を翻案や無許諾利用と一律判定しない。

3問の設問・全4肢・独立正答・全4解説を照合し27箇所改訂。独立正答O46=4・O47=3・O49=2、番号変更なし。確認済み263・修正必要43・要追加確認194、残件237。累積270問2312箇所。ケース10の残るO50は教師の専門的資質に関する別資料照合が必要なため要追加確認を維持した。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照する。

全500問・解説500件、v8不変ハッシュ、影響外本文、正解表・リンク・タグを機械検査し維持。公開可否回帰8条件合格。機械警告は61から62件へ。新規O47のP1は、正答解説末尾が「他の許諾・例外まで否定しない」と範囲を限定するための誤検出で、正答を否定しているのではない。他61件は同一。documents手順でNoto Sans JP適用QAコピー{len(pages)}頁を描画、27変更文字列をPDFで検出し、{'・'.join(map(str,reviewed))}頁を150dpi画像で直接目視した。全頁最終目視・残237問の原資料照合は未了、出版不可で最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第102バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第102バッチ S26追加照合（2026-10-16）\n\n第101バッチ取得・保存した [e-Gov著作権法API本文](https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048) を原SHA256一致で再利用。Q_O_046・047は本則第35条第1項本文とただし書、Q_O_049は第20・27・35・47条の6・50条を照合。第47条の6の列挙は全項確認し、第35条に基づく翻案という設問の範囲を守る。第50条による人格権の留保を無条件の改変禁止とも、一律免除とも扱わない。新規取得とは数えず、全法令改正・経過措置・具体的要約の翻案該当性の判例判断を承認したとはしない。対象条文の追加抜粋はevidence/egov_batch102_excerpts.txt。S161の第35条説明もO46・047の補助として照合済み。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第102バッチ\nNoto Sans JP適用コピー{len(pages)}頁を描画。27変更文字列のある'+ '・'.join(map(str,reviewed))+'頁を150dpi画像で直接目視。全頁最終目視は未了。\n')
e={'batch':102,'base_commit':'ac9d5d97c59eb92814b927657de6c444fd2312cd','fully_rejudged':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':237,'independent_answers':{'Q_O_046':4,'Q_O_047':3,'Q_O_049':2},'source':'S26 acquired in batch101; S161 supplementary for O46/O47','source_raw_sha256':hashlib.sha256(raw).hexdigest(),'source_retrieved':'2026-10-16 JST (batch101)','source_reuse_not_new_acquisition':True,'scope':['2.1.1','20','27','35','47_6','50'],'machine_warnings':62,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']='O46の設問・4肢は156頁、戻るリンクは157頁。O49の設問・4肢は157頁、戻るリンクは158頁へ分離するため158頁も追加目視。解説はO46・047が357頁、O49が358頁に各4項目とも収まる。本文の欠字・重なり・クリッピングは見られない。リンクの改頁は最終組版で再確認する。'
(p/'evidence/batch102_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 full reviews/27 edits;263 confirmed/237 remaining;pages',reviewed)
