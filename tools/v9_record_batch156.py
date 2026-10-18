"""Record only the new, independently adjudicated batch after image review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa156';targets={'Q_1_001','Q_M_038'}
def oldfile(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(oldfile('ledger.csv'));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':368,'修正必要':2,'要追加確認':130}
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==106 and not newwarnings and removed==[['A1','Q_1_001','正解選択肢1に断定語、他に断定語なし2つ以上']]
cs=json.loads((p/'changes_batch156.json').read_text());assert len(cs)==15 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
_,q,a=qa.audit(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'));assert len(q)==len(a)==500 and a['A_1_001']['ans']=='1' and a['A_M_038']['ans']=='2'
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
assert q['Q_1_001']['opts'][1:]==qa.audit(str(p.parent.parent/'登録日本語教員試験決定版問題集_v8_修正版.docx'))[1]['Q_1_001']['opts'][1:]
matches=json.loads((r/'matches.json').read_text());assert len(matches)==15 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('366問','368問').replace('132問','130問').replace('361問3114箇所','363問3129箇所').replace('361問を部分修正','363問を部分修正');f.write_text(s)
report='''

## 第156バッチ（2026-10-18）

Q_1_001・Q_M_038を15箇所改訂し、独立正答1・2を確定。確認済み368・修正必要2・要追加確認130、残132問。累積363問3129箇所、500問維持。

S213 RFCDC第1巻（2018年）全89頁PDFを公式サイトから再取得。書誌・著作権・著者チーム、47–49頁本文と注記、用語集73–74頁を精読し、48・49・73頁（PDF50・51・75頁）を1800px全頁画像で照合した。資料自身のモデルの説明として使い、心理学全分野の共通定義や、引用先Bennett等の原著を取得済みとして扱わない。

Q_1_001は自文化中心主義の定義を用語集に限定。正答の「無意識のうちに」「絶対的な基準」という必須条件化を除き、自文化を尺度にした評価と自集団優位の偏見を示した。誤答2–4の本文は維持し、定義と異なる理由を本文に直接対応させた。解説で別の未照合概念を定義する処理をやめ、「同化」「文化自卑」「文化コンプレックス」「文化相対主義」という名称による断定を削除した。これらの用語が不存在・一律誤りと判定したのではなく、今回それらの原著は取得・承認していない。

Q_M_038は共感を問う領域を保ち、共感の内容・範囲を問う4択へ改訂。モデルは自分の視点からの脱中心化、他者の考え・信念・感情を理解する技能を示し、認知的視点取得と情動面の視点取得、sympathyを含める。49頁注10の日常語・科学的用法の多様性を踏まえ、情動伝染だけへの限定やsympathyの排除を誤答として明確化した。他の理論でも必ず同じ分類をするとは説明しない。旧肢に含まれた言語計画・統語論の定義を、取得済みと見なして承認したものではない。

旧3114件の変更履歴を全て不変に保ち15件追記。安全な再構成・台帳再生成、v8不変、500問構造・キー・正誤タグ・早見表・リンク・影響外の問、公開判定回帰8条件・置換回帰4条件を検査。機械警告106件、前回から新規なし、Q_1_001のA1（正答だけに断定語）1件が解消。台帳の設問・選択肢・解説はv8スナップショットで、改訂後はchangesと作業稿を参照する。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列15件を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視。変更箇所の欠字・重なり・文字切れなし。Q_M_038の解説4は387頁へ続くため、最終版の改頁調整対象に追加する。未照合132問、全頁最終QAと既記録の改頁調整は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第156バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第156バッチ S213追加照合（2026-10-18）

[RFCDC第1巻（2018年）](https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c)を公式サイトから再取得。47–49頁の本文・注10、用語集73–74頁を精読。48・49・73頁（PDF50・51・75頁）を全頁画像で照合。Q_1_001の全4肢・4解説を73頁Ethnocentrism項、Q_M_038を48–49頁Empathy項・注10と73頁Empathy項へ対応。定義の流派・モデル依存性を明示し、心理学全般の合意、Bennett等の原著、旧解説の別概念を取得・承認したものとしない。全89頁精読ではない。原バイトSHA256・読了範囲はevidence/batch156_sources.json。原PDF非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=156,base_remote_commit='33a72651945436f2cf484f8585cfb9b4897a4223',fully_rejudged=sorted(targets),edits=15,independent_answers={'Q_1_001':1,'Q_M_038':2},sources=['S213'],status_counts=m['status_counts'],remaining=132,machine_warnings=106,new_warnings=newwarnings,removed_warnings=removed,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch156_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('368 confirmed / 132 remaining',pages)
