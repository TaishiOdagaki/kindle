"""Record evidence and preserve untouched CSV record bytes."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa170';k='Q_M_042'
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[key].replace('\r\n','\n') if key==k else raw for key,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':399,'修正必要':2,'要追加確認':99} and not m['release_ready']
cs=json.loads((p/'changes_batch170.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {key for key in d if d[key]!=d0[key]}=={k}
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_M_042']['ans']=='4'
for c in cs:
 got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_M_042']['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches170.json').read_text());assert len(matches)==9 and all(matches.values())
pages=sorted({v for ns in matches.values() for v in ns});machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==122 and len(warnings)==1 and warnings[0][1]==k
assert all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第170バッチ 2026-10-18

Q_M_042の設問・全4肢・全4解説を9件改訂。S26 e-Gov著作権法APIの原XMLを再取得し、本則第32条と第48条全項を照合。応答は既取得の945280バイト・SHA256と一致。S227文化庁『令和8年度著作権テキスト』全119頁の原PDFを取得し、印刷75頁の引用全条件・注記、77頁の出所説明を本文と画像で照合した。独立正答4、キー変更なし。確認済み399・修正必要2・要追加確認99、残101問。累積394問3381件、500問維持。

公表、公正な慣行、目的上正当な範囲と出所を区別し、出所さえ示せば自由に掲載できるという誤解を防ぐ。文章の複製という条件に限定し、著作者名表示の例外、短い文芸作品等では全部引用もあり得る留保も残した。全文引用は常に不可という反対方向の過剰一般化もしていない。旧判断が挙げていたS10は第35条の別資料であり、本問の根拠としては用いず訂正した。

全119頁の精読、全法改正の施行・経過措置、具体的事件の適法性の検証ではない。e-Gov API1の施行日メタデータ不足を残し、今回の対象規則は令和8年度文化庁説明と突合した。法令本文と行政解説を区別する。出所だけで引用の全条件を満たすとはしていない。

v8不変、500問、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件が通過。機械警告121→122件。新規P1は、引用全体の適法性を出所表示だけで保証するものではないという正答解説の限定末尾、および誤肢解説が説明文であることによる誤検出。限定を削って警告数のみ減らさない。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifで{pagecount}頁を新規描画。新規9文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QAと未照合101問は未了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第170バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第170バッチ S26再取得 S227 2026-10-18\n\n- S26 [e-Gov著作権法API](https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048)。Result Code0、945280バイト、既取得原応答SHA256と一致。本則第32条全項・第48条全項を精読。API1の施行日メタデータ不足により全改正・経過措置の承認ではない。\n- S227 [文化庁令和8年度著作権テキスト](https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/pdf/94383901_01.pdf)。全119頁原PDF取得。印刷75頁の引用条件・注記、77頁の出所説明本文、PDF78・80頁画像を確認。出所だけでは不十分、全部引用が考えられる作品の留保も照合。全119頁精読・判例全件や個別事例の適法性判断ではない。\n\nQ_M_042の全4肢・全4解説を対応。S10は第35条の別資料のため本問根拠から除外。原バイトSHA256・範囲はevidence/batch170_sources.json。原資料全体非転載。\n''')
f=p/'README.md';f.write_text(f.read_text().replace('398問','399問').replace('100問','99問').replace('393問3372箇所','394問3381箇所').replace('393問を部分修正','394問を部分修正'))
e=dict(batch=170,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=[k],edits=9,independent_answers={k:4},sources=['S26','S227'],status_counts=m['status_counts'],remaining=101,machine_warnings=122,new_warnings=warnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},source_images={str(n):sha(root/f'bunka170-p{n:03}.png') for n in [78,80]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch170_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
