"""Record bounded history questions after direct changed-page image review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa190');BASE='6167d3e35f961c1e44de749952c89f73d973764d';keys={'Q_1_025':2,'Q_1_028':3}
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
def old(n):return subprocess.check_output(['git','show',BASE+':audit/v9/'+n])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[n].replace('\r\n','\n') if n in keys else raw for n,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':455,'修正必要':0,'要追加確認':45} and not m['release_ready']
cs=json.loads((p/'changes_batch190.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches190.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert not added
specs=[('S261','JASSO 国際学友会の沿革','https://www.jasso.go.jp/about/organization/history/gakuyu.html','jasso190-history.html','沿革表全項目を取得・精読。1935年12月・1936年2月・1940年12月・1943年1月を団体創立・会館/教室開設・法人設立許可・学校設置許可で区別。JASSOの公表沿革を問い、学校史の全一次史料や他の戦前機関の歴史を確認したとはしない。'),('S262','長沼スクール 標準日本語讀本の解説','https://www.naganuma-school.ac.jp/jp/japanese_teachers/reader.html','naganuma190-reader.html','標準日本語讀本とは・歴史の全本文と書影説明を取得・精読。自作教材、構文/語彙/漢字、オーラル・メソッド、試用改良、1931年巻一自費出版と全七巻、1948年改訂八巻完成と1950年一般向け出版、1964～67年再訂・1997年復刻の版区別。学校による教材史の説明に限定、原教材全巻の現物精読や教育効果・歴史的評価を承認したとはしない。')]
sources=[]
for sid,title,url,name,scope in specs:
 f=Path('..')/name;assert f.stat().st_size>10000
 sources.append(dict(source_id=sid,title=title,url=url,retrieved='2026-10-20',sha256=sha(f),bytes=f.stat().st_size,body_read=scope,method='公式HTML原バイト直接取得とWeb open本文の対応を確認・精読',full_source_redistributed=False))
(p/'evidence/batch190_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
text=f'''\n\n## 第190バッチ 2026-10-20\n\nQ_1_025・028の設問・全4肢・全4解説を18件改訂。S261 JASSO公表沿革とS262長沼スクール公式教材史の全本文を取得・精読、独立正答2・3、キー変更なし。確認済み455・修正必要0・要追加確認45、500問維持、累積448問3885件。\n\n国際学友会の1935年12月創立、1936年2月の会館・受入れ・教室、1940年12月法人許可、1943年1月の学校設置許可を区別。旧稿の宏文・東亜・松本・周恩来・魯迅・日仏会館の個別史を未取得原典のまま承認せず、同じ戦前日本語教育機関史で差替え。長沼読本は自作教材の構成・オーラル・メソッド取入れと試用改良、1931年初刊七巻と戦後の一般向け八巻の区別に限定。グアン・山口の教授法、直接法の決定版・国内外への影響という未照合の評価を撤回。各公表者が記す史実として範囲を明示し、全一次史料・原教材全巻・教育効果を検証したとはしない。\n\n安全再構成で全500問の構造・改訂外本文・v8ハッシュ不変を確認。公開判定8条件・置換4条件・block-context回帰は本実行で通過済み。機械警告{len(machine['issues'])}件、追加{len(added)}・解消{len(removed)}。完全版Noto Sans CJK JPと代替フォントの全文収録を検査、{count}頁新規描画。18改訂文字列全件検出、影響{pages}頁の1800px画像を直接確認し改訂箇所の欠字・重なり・切れなし。残45問・最終改頁調整・全頁最終QAは未完了。台帳原文はv8スナップショット、改訂後はchangesと作業稿参照。作業稿は出版不可。\n'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第190バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第190バッチ S261 S262\n\n'+'\n\n'.join(f'[{sid} {title}]({url})。{scope}' for sid,title,url,name,scope in specs)+'\n\n原HTML本文全体非転載。取得URL・SHA256・サイズ・精読範囲はevidence/batch190_sources.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('453問','455問').replace('47問','45問').replace('446問3867箇所','448問3885箇所').replace('446問を部分修正','448問を部分修正').replace('第189バッチの最新描画は355頁',f'第190バッチの最新描画は{count}頁'))
e=dict(batch=190,base_remote_commit=BASE,fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=[s[0] for s in specs],status_counts=m['status_counts'],remaining=45,machine_warnings=len(machine['issues']),added_warnings=added,removed_warnings=removed,regressions='readiness8; replacement4; block-context passed in this run',render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch190_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
