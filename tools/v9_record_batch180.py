"""Record batch180 after manual inspection; one-time only."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa180';keys={'Q_1_006':4,'Q_O_001':1}
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in keys else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':421,'修正必要':0,'要追加確認':79} and not m['release_ready']
cs=json.loads((p/'changes_batch180.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches180.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));newwarnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==134 and len(newwarnings)==2 and {x[0] for x in newwarnings}=={'D2','P1'} and all(x[1]=='Q_1_006' for x in newwarnings) and all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第180バッチ 2026-10-19

Q_1_006・Q_O_001の設問・各4肢・各4解説を18件改訂。独立正答4・1、キー変更なし。確認済み421・修正必要0・要追加確認79、残79問。累積414問3579件、500問維持。修正必要ゼロは全問承認や最終完成を意味しない。

S244国史館台湾文献館の2013-09-30電子報114期「臺灣總督府首任學務部長伊澤修二來臺推展日語教育」の原HTML92184バイトを取得、template内の記事本文全体を精読。Web openが本文抽出に失敗したことと、原HTMLから実本文を取得したことを区別。李春生の提案、現地視察後の惠濟宮の選定、士林子弟、教授内容、台湾語研究・会話教材編集を全肢全解説へ照合。残る修正必要Q_1_006を同じ台湾日本語教育史領域で差替え。旧稿の松本亀次郎、満州、伊沢の教授法分類、最初の組織的教育等は未照合のまま撤回し、今回確認済みにした主張に混ぜない。2013年の公的史料機関の解説であり、記事が引用した1895年の史料全冊・任命画像を独立取得したとはしない。植民地教育政策全体の評価も承認していない。

S242 Larsen-Freeman・Anderson2011年第3版原著書を再取得し前回の原バイトSHA256と一致。直接法PDF52～53頁、文法訳読法39～40頁、デサジェストペディア110頁、CLL127～128頁の本文と39・52・110・127頁画像を照合。ケース1本文も確認。実物使用だけから授業全体の教授法を断定する問いを、同書の意味提示と母語・翻訳の利用に関する原則比較へ限定。CLLの初級母語会話と教師による訳、デサジェストペディア教材の母語訳併記、文法訳読法の翻訳を、それぞれの誤答理由として明示。音楽・安心感・教師の支援役割だけで分類しない。引用先Lozanov・Curran等の原典、脳機能説、授業効果は未検証であり掲載解説に導入しない。318頁電子再組版のPDF頁で印刷版頁を推定しない。

v8不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外文面の不変を再検査。公開判定回帰8条件・置換回帰4条件・block-context回帰通過。機械警告132→134件。新規D2はQ_1_006の3番・4番がともに地元子弟に言及するための類似度による交換疑いだが、3番は対象排除の否定、4番は場所・対象・内容の肯定で各肢に正しく対応。新規P1は4番正答解説末尾が出題範囲を限定する否定形であるための誤検出。全4肢・解説・タグを本文と再照合し、実際の解説交換・キー誤りでないことを確認。旧132件を保持。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifの文字収録検査後に{pagecount}頁を新規描画。18改訂文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QA・改頁調整・残79問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第180バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第180バッチ S242 S244 2026-10-19

- S242 [Larsen-Freeman Anderson2011年第3版原著書PDF](https://elearning.usm.md/pluginfile.php/190241/mod_resource/content/2/Larsen-freeman%203rd%20ed_techniques-in-language-teaching.pdf)。再取得SHA256一致。直接法PDF52～53、文法訳読法39～40、デサジェストペディア110、CLL127～128頁本文、39・52・110・127頁画像。Q_O_001の全肢全解説を母語・翻訳利用の原則で区別。引用先原典・脳機能・促進効果の承認ではない。
- S244 [國史館臺灣文獻館2013-09-30電子報114期の伊沢修二と日本語教育の解説](https://www.th.gov.tw/Epaper_Content/236/7518/)。原HTML取得、template内の記事本文全体を精読。Q_1_006全肢全解説を場所選定・対象・内容・学務部活動に限定。公的史料機関の2013年解説と1895年原史料全冊の取得を混同しない。旧稿の松本・満州・教授法分類等の未照合主張は撤回。

原資料サイズ・SHA256・範囲はevidence/batch180_sources.json、本文抽出失敗と代替本文取得の区別はbatch180_source_attempts.json。原資料全体非転載。
''')
f=p/'README.md';s=f.read_text().replace('419問','421問').replace('| 修正必要 | 1問 |','| 修正必要 | 0問 |').replace('80問','79問').replace('413問3561箇所','414問3579箇所').replace('413問を部分修正','414問を部分修正').replace('第179バッチの最新描画は354頁',f'第180バッチの最新描画は{pagecount}頁').replace('`decisions.json`の修正必要1問を、前提不成立・複数正答・正答不存在から優先して改稿する。','修正必要は現在0問。要追加確認79問の根拠取得と再判定を継続し、新たな不成立を見つけたら記録・改稿する。').replace('要追加確認79問と修正必要1問の全残存主張','要追加確認79問の全残存主張');f.write_text(s)
e=dict(batch=180,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S242','S244'],status_counts=m['status_counts'],remaining=79,machine_warnings=134,new_warnings=newwarnings,regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/('review299ppm.png' if n==299 else f'review-{n:03}.png')) for n in pages},image_retry='299頁の最初の表示に一部欠落の疑い、同バイトの再表示でも異常。最終PDFからpdftoppmで別PNGを生成し、正誤タグと全本文が正常なことを直接確認。299頁ハッシュはこの再生成画像。',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch180_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
