"""Record only after direct inspection of all batch101 changed page images."""
import json,hashlib,subprocess,re,io,csv,bisect,gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch101-qa'
targets={'Q_4_122','Q_4_123','Q_O_048','Q_MO_011','Q_MO_012','Q_MO_013'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':260,'修正必要':44,'要追加確認':196}
cs=json.loads((p/'changes_batch101.json').read_text());assert len(cs)==56
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
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert added==[] and removed==[['P1','Q_O_048','(正)2の解説が否定で終わる/肯定の(誤)がある: [1, 3]']] and len(machine['issues'])==61
raw=(root/'egov101.xml').read_bytes();archive=p/'evidence/egov_batch101.xml.gz';archive.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(archive.read_bytes())==raw
f=p/'README.md';s=f.read_text()
for a,b in [('254問','260問'),('44問','44問'),('50問','44問'),('267問2229箇所','268問2285箇所'),('267問を','268問を')]:s=s.replace(a,b)
f.write_text(s)
sources={
'S26':{'url':'https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048','title':'e-Gov 著作権法 法令API','acquisition':'XML原応答945280バイト、Result Code 0。全応答を通常取得、本則の対象条項を抽出して精読。','scope':'第2条第1項第1号、第10条、第17条、第35条全3項、第48条、第59・60条。関連確認として第20〜27・32・47条の6・51条も取得本文を確認。','sha256':hashlib.sha256(raw).hexdigest(),'raw_archive':'evidence/egov_batch101.xml.gz','excerpt':'evidence/egov_batch101_excerpts.txt','limits':'附則の同番号条と区別。API1の応答に施行日メタデータが示されていないため、2026年改正全条項の施行・経過措置まで監査したとはしない。質問対象の条文本文を照合。個別事件への法的助言ではない。'},
'S161':{'url':'https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/seminar/2024/pdf/94089902_01.pdf','title':'SARTRAS 野方英樹 授業目的公衆送信補償金制度 活用のための基礎知識','date':'2023-07-31（表紙記載。URLの2024を刊年にしない）','acquisition':'文化庁掲載の全40頁PDFを通常取得。対象頁本文を取得しe-Govと照合。','scope':'PDF4頁の著作物定義、7〜8頁の複製・公衆送信、10頁の教育目的だけでの免除否定、12頁の人格的利益、15頁の第35条全項、16頁の原則・例外・出所明示。','sha256':sha(root/'S161-101.pdf'),'limits':'全40頁の精読・全主張の承認ではない。補償金の料金額・最新申込手続は本問の対象外。図中の単純化より第35条全項の条件を優先する。'}}
for v in sources.values():v['retrieved']='2026-10-16 JST'
report=f'''

## 第101バッチ（2026-10-16）

接続済みGitHubで最新HEAD 1ab42d6d6f91eb3aa2c52aac16f45f7868199b6fを確認し、新規作業場へfetchで復元。README・manifest・decisions・changes・sources・postfix_machineを引き継いだ。指定優先問題はMO2を含め照合済みを維持。初期スクリプトは再実行していない。

e-Gov著作権法APIのXML全文を新規取得し、本則の対象条項を精読。文化庁掲載のSARTRAS講習資料の該当頁とも照合した。第35条の非営利設置、授業過程、必要限度、不当に利益を害しないという条件、第2項の設置者の補償金負担と第3項の所定の同時受講への送信の例外を分けた。Q_4_123・Q_O_048・Q_MO_011・Q_MO_012を全4肢・全4解説ごとに独立再判定。録画の後日視聴や単にリアルタイムという情報だけを、第3項の免除にしない。ケース10と模擬応用の著作物ケースに適用前提を明記した。Q_MO_013は創作的な新聞コラムと第10条第2項の事実の伝達にすぎない報道の除外を区別。Q_4_122は著作物性に販売を要求しない定義、無方式性、著作者が存しなくなった後の第60条の保護と第59条の一身専属性を区別した。死後の人格権を遺族がそのまま承継するとは説明しない。

6問54項目とケース前提2段落、計56箇所。独立正答はQ_4_122=4、123=2、O48=2、MO11=2、MO12=3、MO13=2で番号変更なし。確認済み260・修正必要44・要追加確認196、残件240。累積268問2285箇所。ケースの前提を変えたからといって隣接するO46・O47・O50・MO14・MO15を承認せず、いずれも要追加確認を維持した。台帳の原文はv8スナップショットであり、改訂はchangesと作業稿を参照する。

全500問・解説500件、v8の不変ハッシュ、影響外の問題本文、リンク・早見表・正誤タグを機械検査し維持。公開可否回帰8条件合格。機械警告は62から61件へ、旧O48の否定文末P1が解消し、残61件は同一。長さ分布を検査結果に記録し、長さのため正誤を変えていない。documents手順でNoto Sans JP適用QAコピーを{len(pages)}頁描画し、56変更文字列をPDFで検出、{'・'.join(map(str,reviewed))}頁を150dpi画像で直接目視した。全頁最終目視と残240問の原資料照合は未了。作業稿は出版不可で最終v9ではない。

e-Govの原応答はgzipで原バイトを保存し、解凍後の同一性とSHA256を検証。API1の施行日メタデータ不表示、個別経過措置未照合、補償金額・最新手続未対象という限界を根拠一覧へ記録した。ウェブ検索のうち内容の一致しない結果は根拠に使用していない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第101バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';s=f.read_text()+'\n\n## 第101バッチ 著作権条文の再取得（2026-10-16）\n\n'
for k,v in sources.items():s+='- '+k+' ['+v['title']+']('+v['url']+')：'+v['acquisition']+' '+v['scope']+' '+v['limits']+'\n'
f.write_text(s+'\n対象：Q_4_122・123、Q_O_048、Q_MO_011・012・013。第35条全3項は文化庁資料PDF15頁と一致。S161の表紙日付は2023-07-31。原応答・対象抜粋・ハッシュ・範囲はevidence/egov_batch101.xml.gz、egov_batch101_excerpts.txt、batch101_review.jsonに保存。検索抜粋のみでの承認ではない。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第101バッチ\nNoto Sans JP適用コピー{len(pages)}頁を描画。56変更文字列のある'+ '・'.join(map(str,reviewed))+'頁を150dpi画像で直接目視。全頁最終目視は未了。\n')
e={'batch':101,'base_commit':'1ab42d6d6f91eb3aa2c52aac16f45f7868199b6f','fully_rejudged':sorted(targets),'question_field_edits':54,'case_premise_edits':2,'edits':56,'status_counts':m['status_counts'],'remaining':240,'independent_answers':{'Q_4_122':4,'Q_4_123':2,'Q_O_048':2,'Q_MO_011':2,'Q_MO_012':3,'Q_MO_013':2},'sources':sources,'machine_warnings':61,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']='変更箇所を含む11頁を直接確認。4_122解説は299〜300頁、O48解説は357〜358頁に続く。MO12の戻るリンクは189頁本文から190頁へ分離。改頁前後の欠字・本文クリッピング・重なりは見られないが、解説とリンクの改頁は最終組版で再確認する。隣接する未照合問の表示確認を学術的承認に流用しない。'
(p/'evidence/batch101_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 6 reviews/56 edits;260 confirmed/240 remaining;pages',reviewed)
