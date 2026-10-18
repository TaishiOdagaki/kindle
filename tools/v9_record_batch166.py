"""Checkpoint the JF four-question audit after direct page review."""
import json,hashlib,subprocess,csv,io,html
from pathlib import Path
from pypdf import PdfReader
from PIL import Image
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa166';targets={'Q_1_038','Q_M_005','Q_1_026','Q_M_001'}
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':396,'修正必要':2,'要追加確認':102} and not m['release_ready']
cs=json.loads((p/'changes_batch166.json').read_text());assert len(cs)==36 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
keys={'Q_1_038':2,'Q_M_005':1,'Q_1_026':3,'Q_M_001':3}
assert all(a['A_'+k[2:]]['ans']==str(v) for k,v in keys.items())
for c in cs:
 v=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=v['stem'] if c['field']=='stem' else v['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches166.json').read_text());assert len(matches)==36 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
for n in pages:
 with Image.open(r/f'review-{n:03}.png') as im:im.verify()
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==120 and len(warnings)==2 and {x[1] for x in warnings}=={'Q_1_026','Q_M_005'}
assert all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第166バッチ 2026-10-18

Q_1_038・Q_M_005・Q_1_026・Q_M_001の設問、全4肢、独立正答、全4解説を原表と公式紹介本文へ照合し、4問36件改訂。独立正答2・1・3・3、キー変更なし。確認済み396・修正必要2・要追加確認102、残104問。累積391問3353件、500問維持。

S223国際交流基金2021年度調査第1章の原PDFを取得。印刷7頁の対象、10～13頁の地域表・国順位、18頁の教育段階、22頁の学習目的を本文照合し、11・18・22頁画像も直接確認。東アジアと東南アジアは76.4％、中等教育49.6％・初等教育8.7％。学習目的59.9％は機関の回答であり、学習者本人の回答比率ではない。年度を固定し、独習者除外の回答機関集計を世界の全学習者推計と同一視しない。Q_M_005の地理的・経済的近さを原因とする未検証の因果説明を撤回。2024年度調査の公開は把握しているが、この2問を2026年現在の最新統計として扱わず、明示した2021年度の資料を読む問題に限定した。

S224基金公式紹介本文の1972年外務省所管特殊法人設立・2003年10月1日独法化を確認。Q_1_026の戦後普及自粛や再開の広範な政策史解釈を、沿革だけで承認しない。設立史の範囲で取得本文に限定した。公式拠点紹介の国内外の基盤と在外公館・日本語教育機関・文化交流機関の連携も確認。Q_M_001は個々の権限の網羅的否定ではなく、同じ海外拠点領域の連携のあり方を問う形にした。全拠点一律の事業は承認していない。

旧3317件は不変で36件追記。他問の判断は変更せず、v8不変、500問、正答・タグ・早見表・リンク、公開判定回帰8条件と置換回帰4条件を検査。機械警告118→120件。新增P1の2件は、正答解説末尾の政策史一般化・因果確定を避ける限定文による検知であり、4肢と正答を再読して誤検出と判定。注意書きを削って警告数だけを減らしていない。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。
'''
text+=f'\nNoto Sans JPで{pagecount}頁を新規描画、36文字列全件を検出。'+ '・'.join(map(str,pages))+'頁の1800px画像を直接目視。改頁所見は証跡のpending_paginationに記録。全頁最終QAと未照合104問は未了、最終版ではなく出版不可。\n'
pagination=json.loads((r/'pagination.json').read_text())
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第166バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第166バッチ 原表と公式紹介 2026-10-18

- S223 [国際交流基金2021年度調査第1章](https://www.jpf.go.jp/j/project/japanese/survey/result/dl/survey2021/overview.pdf)。印刷7・10～13・18・22頁本文、11・18・22頁画像。対象は回答機関、独習者除外。Q_1_038・Q_M_005。最新2024年度値の承認ではない。
- S224 [基金公式紹介](https://www.jpf.go.jp/j/about/)の沿革本文、[世界の拠点紹介](https://www.jpf.go.jp/j/world/)の導入と一覧。Q_1_026・Q_M_001。政策史全般、全拠点の全業務・法的権限の独立検証ではない。

原バイトSHA256と照合範囲はevidence/batch166_sources.json。原資料全文は非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('392問','396問').replace('106問','102問').replace('387問3317箇所','391問3353箇所').replace('387問を部分修正','391問を部分修正'))
e=dict(batch=166,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=sorted(targets),edits=36,independent_answers=keys,sources=['S223','S224'],status_counts=m['status_counts'],remaining=104,machine_warnings=120,new_warnings=warnings,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansJP.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},source_page_sha256={n:sha(root/f'jf166-{n}.png') for n in ['table','school','goals']},full_visual_qa_completed=False,release_ready=False,pending_pagination=pagination)
(p/'evidence/batch166_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('396 confirmed /104 remaining',pages)
