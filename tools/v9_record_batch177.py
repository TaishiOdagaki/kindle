"""Record source-scoped audit and manually reviewed changed pages."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa177';keys={'Q_1_017':3,'Q_1_030':4}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':414,'修正必要':1,'要追加確認':85} and not m['release_ready']
cs=json.loads((p/'changes_batch177.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches177.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));assert machine['issues']==pre['issues'] and len(machine['issues'])==131
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第177バッチ 2026-10-19

Q_1_017・030の設問・各4肢・各4解説を18件改訂。独立正答3・4、キー変更なし。確認済み414・修正必要1・要追加確認85、残86問。累積408問3516件、500問維持。

S188総務省自治行政局国際室の説明資料を文化庁掲載原PDFで再取得。表紙、2020年改訂の概要（PDF6／印刷5頁）、意識啓発と社会参画支援（PDF43／印刷42頁）を精読、43頁を画像確認。地域住民等の意識啓発、相互交流、主体的な活動へのネットワーク等の支援、災害時の担い手、自治会等の参画を全肢・全解説へ対応。旧稿の定義引用や同化の一般理論は本問の採用範囲から外した。資料自体が略と示す箇所の全文、原プラン全条項、施策効果・現行補助金要件を検証したものではない。

S72常用漢字表の告示原PDF164頁を再取得。第1頁の前書き1～5、表の見方1～6を本文・画像照合、第2頁の説明も参照。目安、個々人の表記、専門分野への留保、都道府県名等の例外、過去表記の非否定、運用の考慮、2136字を全肢・全解説へ対応。旧稿の「読むことが容易になったから字数が増加」という因果説明と手書き不要の一般化を撤回。追加削除字数・現代仮名遣いの別告示・改定原因・教育漢字制度の承認ではない。全164頁精読とはしない。

v8不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外問題の不変を再検査。公開判定回帰8条件・置換回帰4条件通過。機械警告131件は前回と完全一致、新規追加・削除なし。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifの文字収録検査後に{pagecount}頁を新規描画。18文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QA・改頁調整・残86問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第177バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第177バッチ S72 S188追加照合 2026-10-19

- S72 [常用漢字表告示原PDF](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf)再取得。第1頁前書き1～5・表の見方1～6本文と画像、第2頁本文。Q_1_030の全肢全解説。読み書きの容易さから字数増を説明する推測、手書き不要の一般化を撤回。全164頁精読、改定原因・教育漢字・別告示の現代仮名遣いの承認ではない。
- S188 [総務省説明資料 文化庁掲載PDF](https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/taikai/r02/pdf/92746701_03.pdf)再取得。表紙・PDF6頁概要と43頁の意識啓発と社会参画支援全本文、43頁画像。Q_1_017の全肢全解説。略の箇所、原プラン全条項・現行補助金要件や効果の実証は未確認。

原バイトSHA256・サイズ・取得範囲はevidence/batch177_sources.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('412問','414問').replace('87問','85問').replace('406問3498箇所','408問3516箇所').replace('406問を部分修正','408問を部分修正').replace('第176バッチの最新描画は353頁',f'第177バッチの最新描画は{pagecount}頁'))
e=dict(batch=177,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S72','S188'],status_counts=m['status_counts'],remaining=86,machine_warnings=131,new_warnings=[],regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch177_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
