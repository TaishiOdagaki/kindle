"""Checkpoint an independently bounded Barnga implementation question."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa171';k='Q_4_094'
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':400,'修正必要':2,'要追加確認':98} and not m['release_ready']
cs=json.loads((p/'changes_batch171.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {key for key in d if d[key]!=d0[key]}=={k}
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_4_094']['ans']=='4'
for c in cs:
 got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_4_094']['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches171.json').read_text());assert len(matches)==9 and all(matches.values())
pages=sorted({v for ns in matches.values() for v in ns});machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==123 and len(warnings)==1 and warnings[0][1]==k
assert all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第171バッチ 2026-10-18

Q_4_094の設問・全4肢・全4解説を9件改訂。S228ニューハンプシャー大学Institute on Disabilityが公表した2019-02-19付バーンガ実施報告の本文全体を取得・精読。S229開発者側のGameletter2006年8月の編集者名・Barnga紹介全節も取得し、目的と、形式・人数に応じた変更があることを確認。独立正答4、キー変更なし。確認済み400・修正必要2・要追加確認98、残100問。累積395問3390件、500問維持。

出典の実施主体と日付を指定し、話さずに対戦すること、勝者が他の卓へ移ること、後の振り返りで文化・言語の違いとその際の気持ちを話し合ったという、直接記録された事実を問う形へ限定した。対戦中の制約と振り返りの対話を混同しない。旧稿の筆談を含む言語使用の一律禁止は今回取得本文から確認できず、採用文から外した。原マニュアルの全冊や全版の唯一手順を取得したとは扱わない。

葛藤・心理ストレスが全員に必ず生じる、長期的な異文化適応能力の向上が実証されたという主張もしていない。開発者の目的説明、実施大学自身の活動報告、統制された効果研究はそれぞれ異なる証拠として扱う。参照先Michigan旧URLは404、マニュアル全文は未取得。

v8不変、500問、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件が通過。機械警告122→123件。新規P1は、正答解説が効果実証の範囲を限定して否定で終わること、および誤肢解説が報告内容を説明することによる誤検出。留保を削って警告だけ減らさない。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifで{pagecount}頁を新規描画。新規9文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QAと未照合100問は未了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第171バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第171バッチ S228 S229 2026-10-18\n\n- S228 [UNH Institute on Disability Barnga実施報告](https://iod.unh.edu/blog/2019/02/barnga-simulation-game-cultural-clashes)。2019-02-19付本文全体を取得・精読。無言の対戦、勝者の卓移動、異なるルールへの気づき、言語・文化と感情に関する振り返り。実施機関自身の一次記録であり効果を比較した統制研究ではない。\n- S229 [Thiagi Gameletter2006年8月](https://thiagi.net/archive/www/pfp/IE4H/august2006.html)。編集者名とGame Announcement Barnga:25th Anniversary Edition全節。異なる解釈を理解・調整するという開発者側の目的説明。マニュアルや振り返りガイドの存在の説明は、その全冊取得と区別。全版の唯一手順・普遍的効果を承認しない。\n\nQ_4_094の全4肢・全4解説を対応。原バイトSHA256・範囲はevidence/batch171_sources.json。Michigan旧参照URLは404、マニュアル全冊未取得。原資料全体非転載。\n''')
f=p/'README.md';f.write_text(f.read_text().replace('399問','400問').replace('99問','98問').replace('394問3381箇所','395問3390箇所').replace('394問を部分修正','395問を部分修正'))
e=dict(batch=171,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=[k],edits=9,independent_answers={k:4},sources=['S228','S229'],status_counts=m['status_counts'],remaining=100,machine_warnings=123,new_warnings=warnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch171_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
