"""Record verified batch172 without changing unrelated CSV record bytes."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa172'
keys={'Q_3_009':4,'Q_3_010':4,'Q_3_011':1}
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in keys else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':403,'修正必要':2,'要追加確認':95} and not m['release_ready']
cs=json.loads((p/'changes_batch172.json').read_text());assert len(cs)==27 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches172.json').read_text());assert len(matches)==27 and all(matches.values())
pages=sorted({v for ns in matches.values() for v in ns});machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==124 and len(warnings)==1 and warnings[0][1]=='Q_3_009'
assert all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第172バッチ 2026-10-19

Q_3_009・010・011の設問・各4肢・各4解説を27件改訂。独立正答4・4・1、キー変更なし。確認済み403・修正必要2・要追加確認95、残97問。累積398問3417件、500問を維持。

S230 Anderson1982の原論文スキャン38頁を再取得し、369～370・373・381～383頁を照合、370・383頁画像を確認。手続き化と自動化を同義にせず、宣言的表象が必ず消えるという主張と、全第二言語処理が無意識・無誤りになる保証を承認しない。原論文は手続的形式になった後の調整・高速化を区別している。Q_3_010は明示した架空事例を用い、説明できた観察と会話中の誤用を区別する。単発誤用から唯一の原因・習得段階を診断しない。S232東京外国語大学のて形解説本文と全表で「かきます→かいて」を確認したが、誤用の心理原因を証明する資料とはしていない。

S231 Stanford公開のAtkinson・Shiffrin公刊前原稿194頁を再取得。表紙と原稿2・3・5～10頁、図1（6頁）と8頁画像を確認。貯蔵という構造とリハーサル等の制御過程を区別し、転送は元の情報を必ず除去する移動ではないこと、長期から短期への経路を照合。感覚登録から長期への直接経路は原稿自身が未確定としている。旧稿の7±2と4項目の混在・長期記憶の永久保存保証・情報流の固定化を撤回。出版版の頁・全引用原著の取得とは区別する。

前回の未保存作業はローカルに残っていなかったため、GitHub第171バッチから再構成し、資料の取得・本文照合・描画をやり直した。前回メモにあったAndersonのクエリなし取得の途中切れを今回の本文根拠に使わず、完全な38頁PDFをstrict検査して採用した。原資料全体は転載しない。

v8不変、500問、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件を検査。機械警告123→124件。新規P1は正答解説が万能性を否定して終わることによる誤検出。既存123件は維持。台帳原文はv8スナップショットで、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifで{pagecount}頁を新規描画。新規27文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接確認。日本語欠字・重なり・切れを認めず。ただしQ_3_011選択肢4、Q_3_009解説3～4、Q_3_012の解説開始が次頁になる改頁は残っており、最終組版で調整が必要。全頁最終QAと残97問は未了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第172バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第172バッチ S230 S231 S232 2026-10-19

- S230 [Anderson1982 Acquisition of Cognitive Skill 原論文スキャン](https://gwern.net/doc/iq/1982-anderson-2.pdf?download=1)。Psychological Review89(4)369–406、第三者保管の原論文38頁。369～370・373・381～383頁本文、370・383頁画像。命題ネットワーク／プロダクション、コンパイルの合成と手続き化、手続化後の学習、宣言的表象の必然的消失ではないこと。ACT1976書籍・Fitts1964原著・NevesAnderson1981は未取得。
- S231 [Atkinson Shiffrin Human Memory 著者公刊前原稿](https://web.stanford.edu/group/csli-suppes/techreports/IMSSS_110.pdf)。Stanford公開194頁。表紙、原稿2・3・5～10頁本文、図1（6頁）と8頁画像。貯蔵と制御過程、写す転送と検索、視覚の短い登録時間、未確定の直接経路。1968出版版の最終本文や頁との同一視、全194頁精読・引用先原著の検証とはしない。
- S232 [東京外国語大学 Vて 解説](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/043.html)。本文と全表。「かきます→かいて」の形を照合。架空事例の誤用原因の実証とは区別。

Q_3_009・010・011の全肢全解説を対応。取得原バイトのSHA256・精読範囲はevidence/batch172_sources.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('400問','403問').replace('98問','95問').replace('395問3390箇所','398問3417箇所').replace('395問を部分修正','398問を部分修正').replace('完全版での最新描画は354頁','完全版での第168バッチ描画は354頁、第172バッチの最新描画は353頁'))
e=dict(batch=172,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=27,independent_answers=keys,sources=['S230','S231','S232'],status_counts=m['status_counts'],remaining=97,machine_warnings=124,new_warnings=warnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},pending_pagination=['Q_3_011 option4 on next page','Q_3_009 explanations split','Q_3_012 heading and key before next page explanations'],full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch172_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
