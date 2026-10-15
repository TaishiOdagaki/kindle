"""Record batch94 only after direct inspection of the latest changed-page images."""
from pathlib import Path
import json,hashlib,subprocess,re,io,csv,bisect
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch94-qa';targets={'Q_5_074','Q_M_016','Q_M_058'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':243,'修正必要':53,'要追加確認':204}
cs=json.loads((p/'changes_batch94.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];n=len(pages)
norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 if not c['after']:continue
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==60
f=p/'README.md';s=f.read_text()
for a,b in [('240問','243問'),('207問','204問'),('253問2103箇所','256問2130箇所'),('253問を','256問を')]:s=s.replace(a,b)
f.write_text(s)
url='https://escholarship.org/content/qt0sz9c8qh/qt0sz9c8qh_noSplash_9502f78e7451b3a9cbc24a68329e0890.pdf'
report=f'''

## 第94バッチ（2026-10-15）

最新HEAD0f7d01a8de4c6f290bf18d8bff4402baaebbbb25をGitHubから新規cloneして復元。旧作業場はgit管理ディレクトリの参照先が消失していたため正本とみなさず、最新ブランチから読み直した。元v8は不変。日本語フォントを再取得し、実行環境同梱LibreOfficeの書込み可能なコピーを復旧して使用。

Rosch（1978）「Principles of Categorization」原著の公開22頁PDFを取得。画像のみの資料なのでpdfスキルに従い、原著印刷27〜28、30〜43頁を版面で精読。印刷32頁表2.1、36頁の典型性評定、38〜41頁の実験結果とモデルの区別、42〜43頁の文脈の留保を照合。出版年は資料の作成日時2011年等から推測せず、著作の書誌を確認した。

Q_5_074は旧稿の「全多義語に一つの中心義」「かみ三語の歴史的語源」「唯一効率的な指導」を原著未照合のまま承認せず撤回。語彙・多義語指導へ原型の知見を援用する際の、カテゴリー構造と特定の処理・表象・学習モデルを混同しない留意点を問うよう改訂した。多義語の放射状ネットワーク一般や個別語の意味史を本章で実証したとは扱わない。

Q_M_016はスズメ・ペンギンの典型性が文化普遍的に同じだとする前提を撤回し、同一カテゴリー内の典型性評定差を考える架空調査を明示。包含階層と典型性、評定結果と心的表象モデルを区別した。Q_M_058は日本語の「犬」の日常使用頻度の普遍断定を撤回し、原著表2.1のfurniture―chair―kitchen chairという指定階層で基本レベルを判定する。

3問27箇所。設問・全4肢・独立正答・4解説を照合して改訂。独立正答3・3・1、番号変更なし。確認済み243・修正必要53・要追加確認204、残件257。累積256問2130箇所。500問・500解説、影響外本文、v8のSHA256を維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。

全問構造検査・公開可否回帰8条件に合格、機械警告60件は前回と同一。documentsのrender_docx.pyでNoto Sans JP適用QAコピーを{n}頁描画し、27変更文字列のある{ '・'.join(map(str,reviewed)) }頁を完成PDFからpdftocairoで150dpi再描画・直接目視。改頁をまたぐ文字列は隣接頁を連結して検査。全{n}頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第94バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';assert '| S153 |' not in f.read_text();f.write_text(f.read_text()+f'''

## 第94バッチ 原型と基本レベルの原著取得

| ID | 資料 | 取得・照合範囲と限界 | 対象 |
|---|---|---|---|
| S153 | Eleanor Rosch（1978）[Principles of Categorization 原著公開PDF]({url})、E. Rosch & B. B. Lloyd編Cognition and Categorization、27–48頁。[出版書誌](https://www.routledge.com/Cognition-and-Categorization/Rosch-Lloyd/p/book/9781032633381) | 2026-10-15全22頁取得。画像のみ、原著印刷27〜28・30〜43頁を版面精読。PDF頁=原著印刷頁−26。32頁表2.1、36頁典型性、38〜41頁の知見とモデルの区別、42〜43頁の文脈を照合。引用先Rosch等1976の原研究全体や、全多義語の意味史・語彙指導の普遍的効果を承認しない。 | Q_5_074・Q_M_016・Q_M_058 |

MIT掲載の再録PDFは404で未取得だったが、独立した公開先eScholarshipの原著PDFを通常取得できた。検索抜粋だけでは承認していない。原著の走査日時を刊年にしない。典型性の架空評定課題は原著の実験結果ではない。PDFハッシュと版面確認頁はevidence/batch94_review.jsonに記録し全文転載しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第94バッチ\nNoto Sans JP適用QAコピー{n}頁を描画。変更頁'+ '・'.join(map(str,reviewed))+f'を150dpiのCairo PNGで直接目視。全27変更文字列・全4正誤タグを確認。全{n}頁の最終目視は未了。\n')
e={'batch':94,'base_commit':'0f7d01a8de4c6f290bf18d8bff4402baaebbbb25','fully_rejudged':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':257,'independent_answers':{'Q_5_074':3,'Q_M_016':3,'Q_M_058':1},'sources':{'S153':{'url':url,'sha256':sha(root/'rosch-original94.pdf'),'pdf_pages':22,'retrieval':'Full scanned chapter PDF, text extraction empty; source images directly read','image_verified_printed_pages':[27,28]+list(range(30,44)),'page_mapping':'PDF page=printed page minus26','limits':'No full acquisition of cited1976 studies; no universal instructional effectiveness, polysemy etymology or mental representation model approval'}},'fictional_scenario':'Q_M_016 assessment example invented, not an observed experiment','machine_warnings':60,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'rasterizer':'pdftocairo','all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']={'Q_5_074':{'question':[127,128],'explanation':[329,330]},'Q_M_016':{'question':[171,172],'explanation':[372,373]},'note':'日本語は判読可能で欠字・重なりなし。選択肢4および解説4の次頁分離は最終組版で再確認する。全頁最終QAは未了。'}
(p/'evidence/batch94_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+'最終組版の残件：Q_5_074は選択肢4が128頁、解説4が330頁、Q_M_016は選択肢4が172頁、解説4が373頁へ分離。文字の欠落はないが、設問・解説のまとまりを最終版で再調整する。\n')
print('Recorded3fullreviews/27edits;243confirmed/257remaining;pages',reviewed)
