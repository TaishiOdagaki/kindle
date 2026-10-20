"""Record batch187 only after direct image review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa187');BASE='070919c39abc17d1d5d52c30e24dbc38e4cb48d9';k='Q_M_039'
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[n].replace('\r\n','\n') if n==k else raw for n,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':447,'修正必要':0,'要追加確認':53} and not m['release_ready']
cs=json.loads((p/'changes_batch187.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}=={k}
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_M_039']['ans']=='4'
for c in cs:
 got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_M_039']['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches187.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(old('postfix_machine.json'))['issues'] and len(machine['issues'])==140
source=Path('../hofstede187.pdf');source_sha=sha(source);assert len(PdfReader(source).pages)==26
url='https://pressbooks.bccampus.ca/knowinghome/wp-content/uploads/sites/1628/2021/06/module1dimenread03dimensionalizingcultures.pdf'
scope='原著者Geert Hofstede, Dimensionalizing Cultures: The Hofstede Model in Context, Online Readings in Psychology and Culture 2(1), 2011, DOI10.9707/2307-0919.1014。26頁PDF取得。本文6・8・11頁の画像を直接精読。国と個人の分析レベルの区別、8頁の次元一覧と個人類型化への警告、11頁の社会特性としての集団への統合の定義を照合。全26頁精読、現在の国別得点、表3の言語・教育等の一般化は承認していない。大学教材サイト上の原著者論文転載版で、教材の要約を根拠にしたものではない。'
(p/'evidence/batch187_sources.json').write_text(json.dumps(dict(source_id='S255',url=url,retrieved='2026-10-20',sha256=source_sha,bytes=source.stat().st_size,pages=26,body_read=scope,full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
text=f'''\n\n## 第187バッチ 2026-10-20\n\nQ_M_039の設問・4肢・4解説を9件改訂。S255の本文6・8・11頁を画像精読し独立正答4を確定。集団への統合の次元と、国・社会レベルの指標を個人の性格診断へ流用しない条件を明示。旧誤答の音韻論・言語学下位分野・文法カテゴリーは各原典未取得のため承認せず、同じ文化次元の比較へ差替え。現在の国別得点や表3の言語・教育一般化を承認したものではない。\n\n確認済み447・修正必要0・要追加確認53、500問維持。累積440問3813件。全500問構造・改訂外不変・v8ハッシュ不変、公開判定8条件・置換4条件・block-context回帰通過。機械警告140件増減なし。全文CJK収録確認後{count}頁を新規描画。9改訂文字列全件検出、影響{pages}頁の1800px画像を直接目視し改訂箇所の欠字・重なり・切れなし。全頁最終QA・改頁調整・残53問は未完了、作業稿は出版不可。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。\n'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第187バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+f'\n\n## 第187バッチ S255\n\n[S255 Hofstede原著者論文]({url})。{scope}\n\n原PDF・OCR全文非転載。ハッシュ・取得範囲はevidence/batch187_sources.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('446問','447問').replace('54問','53問').replace('439問3804箇所','440問3813箇所').replace('439問を部分修正','440問を部分修正').replace('第186バッチの最新描画は355頁',f'第187バッチの最新描画は{count}頁'))
e=dict(batch=187,base_remote_commit=BASE,fully_rejudged=[k],edits=9,independent_answers={k:4},sources=['S255'],status_counts=m['status_counts'],remaining=53,machine_warnings=140,added_warnings=[],removed_warnings=[],regressions='readiness8; replacement4; block-context',render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch187_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
