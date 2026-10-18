"""Checkpoint five independent judgments, preserving unchanged CSV bytes."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from docx import Document
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa159';targets={f'Q_O_{n:03}' for n in range(61,66)}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':379,'修正必要':2,'要追加確認':119} and not m['release_ready']
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==113 and not removed and {x[1] for x in newwarnings}=={'Q_O_063','Q_O_064','Q_O_065'}
cs=json.loads((p/'changes_batch159.json').read_text());assert len(cs)==37 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
assert [a[f'A_O_{n:03}']['ans'] for n in range(61,66)]==['2','1','2','3','2']
paras=[x.text for x in Document(doc).paragraphs]
for c in cs:
 if c['field']=='case_text':assert paras.count(c['after'])==c.get('count',1);continue
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==37 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('374問','379問').replace('124問','119問').replace('369問3166箇所','374問3203箇所').replace('369問を部分修正','374問を部分修正');f.write_text(s)
report='''

## 第159バッチ（2026-10-18）

ケース13のQ_O_061–065を独立再判定し、全5問を確認済みへ更新。設問5件、選択肢10件、解説20件、ケース見出しと本文2件の計37件（見出しは問題・解説編2箇所同期）を改訂。独立正答は2・1・2・3・2で変更なし。確認済み379・修正必要2・要追加確認119、残121問。累積374問3203件の変更記録、500問維持。

S129は共同開発者Ralph Kilmannの公開解説を改めて取得し、二軸・全5様式・譲歩交換と中間案・全様式の利用可能性と状況依存性の本文を連続精読した。1974年初版用紙・原マニュアル、尺度の妥当性実験を取得したとはしない。S213は取得済み89頁原PDFのサイズ・SHA256を第158バッチ記録へ照合し同一性を確認。29–32・51–53頁本文を再精読し、51–52頁（PDF53–54頁）を1800px全頁画像照合。モデルを架空事例へ適用した判断であり、国籍別傾向、文化が単独の原因だという実証、予防効果・習得完了の証明ではない。

Q_O_061は4様式を英語名と対応させ、回避を先送りだけへ狭める解説を修正。Q_O_062は旧正答の「妥協または統合・協働」を解消した。背景確認だけでは両様式の判別ができないため、次回の仮定として「双方が一部譲り、希望が部分的にかなう中間案」を設問に明示し、妥協と協働を別肢へ分けた。元のケースの次回まで考える時間を、対応全体の回避と決めつけないことも明記した。

Q_O_063は文化が原因とする断定から、本人たちが述べた迅速さと全員の納得という重視点の相違へ限定。Q_O_064は未取得のメタコミュニケーション理論と対立予防効果の断定を撤回し、RFCDC51頁の発言・合意形成技能を用いる機会を作る工夫として設問を明確化。Q_O_065は教師の意図を推測で埋めず、架空ケースに目標を明記して具体的な視点理解・解決探索の力と対応させた。

旧3166件の履歴は不変のまま37件を追記。安全な累積再構成・500問台帳再生成、v8不変、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件を検査。台帳原文はv8スナップショットで、改訂後はchangesと作業稿を参照する。機械警告113件、P1が3件追加。O063の文化を単独原因としない留保、O064の予防保証ではない留保、O065の習得完了ではない留保が語尾で検出された。全4解説の論理とキーを本文へ照合し、正答の否定ではないことを確認。警告除去のために必要な留保を削らない。
'''
pagination=['Q_O_062の設問161頁と選択肢162頁の分割','Q_O_062の解説見出し・キーが368頁下端、本文369頁','Q_O_064の解説が369–370頁に分割']
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、変更後文字列37件を全件検出。'+ '・'.join(map(str,pages))+'頁のPNGをverify・loadし1800px画像を直接目視（138・343頁は共通の様式名に一致した文脈ページ）。日本語の欠字なし。ただし'+ '、'.join(pagination)+'を確認し、下端のキーの配置を含め最終改頁調整対象とする。未照合121問、既記録の改頁調整と全頁最終QAは未了。作業稿であり、最終v9・出版可能とはしない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第159バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第159バッチ S129再取得とS213追加照合（2026-10-18）

S129 [共同開発者KilmannのTKI解説](https://kilmanndiagnostics.com/a-brief-overview-tki/)の二軸・全5様式・譲歩と中間案・状況依存性の本文を再取得して精読。Q_O_061・062の全4肢と4解説を照合。1974年原マニュアル・心理測定資料の取得とは区別。S213 [RFCDC第1巻](https://rm.coe.int/16807bc66c)は取得済み原PDFを第158バッチのSHA256とサイズへ照合し一致、29–32・51–53頁を再精読、51–52頁を画像照合。Q_O_063–065と架空ケースの目標の根拠、Q_O_062の省察のための一時休止の区別に用いた。授業効果、国籍別傾向、原書全頁精読を承認したものではない。evidence/batch159_sources.json参照。本文非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
src=p/'evidence/batch159_sources.json';ev=json.loads(src.read_text());raw=root/'tki159.html';ev[0].update(bytes=raw.stat().st_size,sha256=sha(raw),acquisition='HTTPS HTML原バイト取得成功。Web取得本文とも照合。');src.write_text(json.dumps(ev,ensure_ascii=False,indent=2)+'\n')
e=dict(batch=159,base_remote_commit='669c2da26417ae9e6b181ea9ae58ebd9fbbd9d64',fully_rejudged=sorted(targets),edits=37,independent_answers={k:d[k]['independent_answer'] for k in sorted(targets)},sources=['S129','S213'],status_counts=m['status_counts'],remaining=121,machine_warnings=113,new_warnings=newwarnings,removed_warnings=removed,new_warning_review='P1の3件は正答の否定ではなく文化の単独原因・予防保証・習得完了ではないという留保を検出。全4肢解説と本文の論理照合済み。',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
e['pending_pagination']=pagination
(p/'evidence/batch159_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('379 confirmed /121 remaining',pages)
