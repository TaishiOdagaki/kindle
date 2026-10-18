"""Source/QA checkpoint after manual page inspection; one-time run."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa178';keys={'Q_1_007':4,'Q_1_029':2}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':416,'修正必要':1,'要追加確認':83} and not m['release_ready']
cs=json.loads((p/'changes_batch178.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches178.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));assert machine['issues']==pre['issues'] and len(machine['issues'])==131
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第178バッチ 2026-10-19

Q_1_007・029の設問・各4肢・各4解説を18件改訂。独立正答4・2、キー変更なし。確認済み416・修正必要1・要追加確認83、残84問。累積410問3534件、500問維持。

S240文化庁「文化審議会について」の原HTML本文全体（設置経緯、所掌事務、構成表、答申一覧）を取得精読。2001年1月6日の文部科学省への文化審議会の設置と、国語分科会の国語の改善・普及の調査審議を区別。旧稿の当用漢字表を過度の制限主義と評価する説明、全戦後のローマ字化政策、国語分科会の日本語教育所管の現在形を撤回。全法令原文の改正経緯や現在の全所管の独立検証ではない。

S241文化審議会2022年1月7日建議「公用文作成の考え方」の原63頁PDFを取得。表紙、PDF3～4／本文1～2頁の前書き・基本的な考え方・分類例、PDF7／本文5頁の用語1～4を精読、7頁画像照合。定着した外来語を使う、言い換える、説明を付けるという条件別の選択と、文書の目的・種類・読み手別の工夫、正確さと意味保持を全肢・全解説へ対応。漢字追加の原因や手書き不要の旧補助説明を撤回。全63頁精読や引用先別告示・別法令の全改正、言い換えの介入効果の実証ではない。検索先の旧PDF URLは404で、公式建議ページの実リンクをたどり取得した。

v8不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外問題の不変を再検査。公開判定回帰8条件・置換回帰4条件通過。機械警告131件は前回と完全一致、新規追加・削除なし。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifの文字収録検査後に{pagecount}頁を新規描画。18文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QA・改頁調整・残84問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第178バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第178バッチ S240 S241 2026-10-19

- S240 [文化庁 文化審議会について](https://www.bunka.go.jp/seisaku/bunkashingikai/about/)原HTML。設置経緯・主な所掌事務・構成表・主な答申一覧本文全体。Q_1_029の全肢全解説。現在の全行政所管・法令全改正や旧稿の歴史評価を独立検証したとはしない。
- S241 [文化審議会2022年建議原PDF](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf)。全63頁のうち、表紙、PDF3～4頁基本的な考え方と分類例、7頁用語の扱い本文・画像、8～10頁本文参照。Q_1_007の全肢全解説。目的・読み手に応じた工夫、外来語の条件別対応、意味保持と正確さ。全63頁精読、別告示全体や介入効果の承認ではない。

原バイトSHA256・サイズ・精読範囲はevidence/batch178_sources.json。旧URL404はbatch178_source_attempts.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('414問','416問').replace('85問','83問').replace('408問3516箇所','410問3534箇所').replace('408問を部分修正','410問を部分修正').replace('第177バッチの最新描画は353頁',f'第178バッチの最新描画は{pagecount}頁'))
e=dict(batch=178,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S240','S241'],status_counts=m['status_counts'],remaining=84,machine_warnings=131,new_warnings=[],regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch178_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
