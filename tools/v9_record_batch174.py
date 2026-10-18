"""Checkpoint historical culture-shock explanations and explicit exclusions."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa174';keys={'Q_3_030':4,'Q_3_032':1}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':407,'修正必要':2,'要追加確認':91} and not m['release_ready']
cs=json.loads((p/'changes_batch174.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches174.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({213}|{v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']];gone=[x for x in pre['issues'] if x not in machine['issues']]
assert len(machine['issues'])==127 and len(warnings)==3 and len(gone)==1
assert {x[1] for x in warnings if x[0]=='P1'}==set(keys) and all(x[0]=='V1' for x in gone)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第174バッチ 2026-10-19

Q_3_030・032の設問・各4肢・各4解説を18件改訂。独立正答4・1、キー変更なし。確認済み407・修正必要2・要追加確認91、残93問。累積402問3453件、500問維持。

S235はOberg1960「Cultural Shock: Adjustment to New Cultural Environments」のcurare29(2006)2+3:142～146再録。第三者サイトの5頁PDFを取得、全英語本文と再録注記を精読し142～143頁画像を確認。Q_3_030の未取得Lysgaard原著への帰属や全員に生じる困難のピークは承認せず、同じ異文化適応領域の取得済み著者本文にある段階の説明へ改訂した。原誌1960との全字比較・1954講演本文は未了であり、再録であることを明示した。

日常の合図・手がかりの喪失と不安、生活上の実際の困難、個人差、文化理解と自己の行動様式の放棄の違いを照合。「乗り越える過程が必ず成長につながる」という旧説明を撤回。原著にある病気という比喩、性別・国籍による一般化、根拠の限定された助言は現行の診断基準や普遍的知見として採用しない。「正常反応」の一律宣言で医学的診断を代用することも避けた。歴史的な説明と個人の症状・原因の判定は別である。

v8不変、全500問、キー・正誤タグ・早見表・リンク、改訂外の問題不変を再検査。公開判定回帰8条件・置換回帰4条件通過。機械警告125→127件。新規P1の2件は、全員同一経過の診断や個人診断を否定して終わる正答解説による誤検出。V1のハネムーン期の出現数が3→2になり同じ表記ゆれ警告の記録が置き換わったもので、別の構造不良ではない。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。
'''
text+=f'\n完全版CJKと同梱Noto Serifの収録確認後に{pagecount}頁を新規描画。18文字列全件を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。問題や解説の頁またぎは最終組版で調整する。全頁最終QAと残93問は未了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第174バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第174バッチ S235 2026-10-19

[S235 Oberg原著のcurare2006再録](https://project-tree.net/wp-content/uploads/2019/10/Cultural_Shock_Adjustment_to_new_cultura.pdf)。全5頁の英語本文・再録注記を精読、142～143頁を画像照合。本文の出典注記はPractical Anthropology7:177–182(1960)。日常の合図、影響の個人差、第2段階の生活上の困難、自己のやり方を捨てない理解をQ_3_030・032の全肢全解説に対応した。1960原誌との全字比較、1954講演、Lysgaard原著、現在の医学的診断基準を取得したとはしない。病理的比喩や性別・国籍の一般化を現行知見として承認しない。取得原バイトSHA256と範囲はevidence/batch174_sources.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('405問','407問').replace('93問','91問').replace('400問3435箇所','402問3453箇所').replace('400問を部分修正','402問を部分修正').replace('第173バッチの最新描画は353頁',f'第174バッチの最新描画は{pagecount}頁'))
e=dict(batch=174,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S235'],status_counts=m['status_counts'],remaining=93,machine_warnings=127,new_warnings=warnings,replaced_warnings=gone,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch174_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
