"""Record original-page review and the resulting bounded revisions."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa189');BASE='2ca1afad87cb60207430b7df06a327d95f87d453';keys={'Q_2_018':1,'Q_3_007':3}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':453,'修正必要':0,'要追加確認':47} and not m['release_ready']
cs=json.loads((p/'changes_batch189.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches189.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert added==[['D2','Q_3_007','解説の並びが入れ替わっている疑い (3, 1, 2, 4)']]
assert removed==[['A1','Q_3_007','正解選択肢3に断定語、他に断定語なし2つ以上']]
urls={1:'002',29:'030',30:'031',31:'032'};imgs=[]
from PIL import Image
for n,s in urls.items():
 f=Path('../canale189-'+str(int(s)).zfill(2)+'.webp');assert Image.open(f).size==(1159,1500)
 imgs.append(dict(printed_page=n,url='https://djvu.online/jpg2/c/G/l/cGlEHZTi5twtH/'+s+'.webp',sha256=sha(f),bytes=f.stat().st_size))
scope='Canale Michael and Swain Merrill 1980, Theoretical Bases of Communicative Approaches to Second Language Teaching and Testing, Applied Linguistics I(1),1–47, DOI10.1093/applin/I.1.1。第三者公開の原論文スキャンを掲載ページからたどり印刷1・29・30・31頁の原画像を通常直接取得し直接精読。学説の要約・検索抜粋ではない。本文29頁の文法能力、30頁の社会言語学的能力と談話規則・結束性/一貫性・ストラテジー能力、31頁への続き・3要素・理論段階の留保を照合。論文全47頁や1983年Canale原著、Halliday Hasan1976等の引用原著は未取得。'
(p/'evidence/batch189_sources.json').write_text(json.dumps(dict(source_id='S260',retrieved='2026-10-20',landing_url='https://djvu.online/file/cGlEHZTi5twtH',body_read=scope,images=imgs,full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch189_source_attempts.json').write_text(json.dumps([dict(result='出版社書誌・抄録と二次解説だけでは承認せず、公開原ページ画像まで取得。Web openで画像URLの一部はInternal Error、通常直接画像取得は成功。ダウンロードボタンの認証やCaptchaは操作せずWeb open掲載ページからたどれる表示用画像を読み取り。'),dict(result='landing HTMLの通常直接取得は6182バイトのJavaScriptとcookieを要求する案内で本文なし。検査実行や認証操作はしていない。Web openの掲載ページ情報と印刷頁・著者・題名の現物画像を対応。48画像の一覧は見たが原論文全47頁を取得・精読したとはしない。全画像・原論文本文は非転載。')],ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
text=f'''\n\n## 第189バッチ 2026-10-20\n\nQ_2_018・Q_3_007の設問・全4肢・全4解説を18件改訂。S260 Canale・Swain1980原論文の公開スキャン印刷1・29～31頁の原画像を直接取得・精読し、独立正答1・3を確定、キー変更なし。確認済み453・修正必要0・要追加確認47、500問維持。累積446問3867件。\n\nストラテジー能力は遂行要因や能力不足による伝達の破綻を補う言語的・非言語的方略という1980年定義へ限定。一般的な推進・効率化までを同定義に含める拡張、教師の介入が発達を阻害するという未実証の因果、1983年の追加史の未取得原著主張を撤回。談話規則は同論文30頁の結束性と一貫性の説明へ範囲を明示し、結束性が皆無という断定やノックと入浴の架空対話の推論を撤回。同論文全47頁・引用先原著・1983原著・全流派の定義を検証したとはしない。\n\n安全再構成で全500問の構造・改訂外本文・v8ハッシュ不変を確認。公開判定8条件・置換4条件・block-context回帰は本実行で通過済み。機械警告{len(machine['issues'])}件、追加{len(added)}・解消{len(removed)}。完全版Noto Sans CJK JPと代替フォントの全文収録を検査、{count}頁新規描画。18改訂文字列全件検出、影響{pages}頁の1800px画像を直接確認し改訂箇所の欠字・重なり・切れなし。残47問・最終改頁調整・全頁最終QAは未完了。台帳原文はv8スナップショットで改訂後はchangesと作業稿参照。作業稿は出版不可。\n'''
text+='\n新規D2はQ_3_007の対概念の文字列類似による疑い。肢1・2の逆転点を同じ番号の解説で訂正し、肢3の区別と肢4の焦点も対応していることを全肢照合。解説順序は正しく、警告を隠すための文章変更はしない。旧A1は解消。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第189バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第189バッチ S260\n\n[S260 Canale Swain1980原論文の公開ページ画像](https://djvu.online/file/cGlEHZTi5twtH)。'+scope+'\n\n画像ごとの取得URL・SHA256・サイズ・印刷頁はevidence/batch189_sources.json。原画像・原論文全体非転載。取得段階の区別はbatch189_source_attempts.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('451問','453問').replace('49問','47問').replace('444問3849箇所','446問3867箇所').replace('444問を部分修正','446問を部分修正').replace('第188バッチの最新描画は355頁',f'第189バッチの最新描画は{count}頁'))
e=dict(batch=189,base_remote_commit=BASE,fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S260'],status_counts=m['status_counts'],remaining=47,machine_warnings=len(machine['issues']),added_warnings=added,removed_warnings=removed,machine_warning_review='Q_3_007の新規D2を全4肢と全4解説で個別確認。1は結束性の誤定義、2は一貫性の誤定義をそれぞれ同じ番号で訂正し、3は両概念の区別、4は単一発話への限定を否定しており順序は正しい。対概念を誤答説明にも用いる文字列類似の疑いとして記録し、自動的に無視したり本文を警告回避目的で変更しない。',regressions='readiness8; replacement4; block-context passed in this run',render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),page_sha256={str(n):sha(r/(f'review-{n:03}.png' if n==25 else f'retry-{n:03}.jpg')) for n in pages},image_retry='25頁PNGを直接確認。33頁PNG読込失敗後、同一PDFの33・34・198・207頁を1800px JPEGで再生成し全4画像を直接目視確認。',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch189_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
