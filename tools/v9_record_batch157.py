"""Record the new fictional-case batch after direct page-image review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from docx import Document
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa157';targets={f'Q_O_{n:03}' for n in range(16,21)}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':373,'修正必要':2,'要追加確認':125}
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==109 and {x[1] for x in newwarnings}=={'Q_O_017','Q_O_018','Q_O_019','Q_O_020'} and all(x[0]=='P1' for x in newwarnings)
assert removed==[['A1','Q_O_017','正解選択肢2に断定語、他に断定語なし2つ以上']]
cs=json.loads((p/'changes_batch157.json').read_text());assert len(cs)==30 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
assert [a[f'A_O_{n:03}']['ans'] for n in range(16,21)]==['2','2','2','1','3']
ps=[v.text for v in Document(doc).paragraphs]
for c in cs:
 if c['field']=='case_text':assert ps.count(c['after'])==c.get('count',1);continue
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==30 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('368問','373問').replace('130問','125問').replace('363問3129箇所','368問3159箇所').replace('363問を部分修正','368問を部分修正');f.write_text(s)
report='''

## 第157バッチ（2026-10-18）

ケース4の全5問Q_O_016–020を独立再判定し、設問・選択肢・解説とケースを30件改訂（見出し1件は問題編・解説編の2箇所に同期）。独立正答2・2・2・1・3を確定。確認済み373・修正必要2・要追加確認125、残127問。累積368問3159件の変更記録、500問維持。

S213 RFCDC第1巻（2018年）全89頁PDFを公式サイトから再取得。29–32頁の文化の内部多様性、文化的アイデンティティ、異文化間対話と能力の概念、51–53頁の協働技能・対立解決全12項目・自己の批判的理解全6項目を精読。51・52・53頁（PDF53・54・55頁）を1800px全頁画像で照合した。全89頁の精読ではなく、このモデルの説明の架空事例への教育的適用である。

ケース4を架空事例と明記し、「二人が互いの考えを聞き合う時間を設けず」という条件を追加。教師の「日本ではくじ引きで決めるのが普通」という発言は批判対象で、日本の一般的慣習と承認しない。本文に本人が述べた年上優先・くじ引き等の前提の相違と、国籍からの推測を分けた。文法・音声・語彙の問題をないと実証したわけではなく、本文にその証拠がないと説明する。

Q_O_017は「唯一の正解を示した」という強い推定を避け、当事者相互の視点理解・合意形成の過程の不足を問う。Q_O_018は対話をすれば必ず解決・納得するという保証を避け、52頁8が認める一時休止を永久分離と区別。Q_O_019は学習者が意見を出し合う機会という目的を明示し、集団討議の常時義務化・グループワークの一律優位・対立予防の効果の実証を承認しない。Q_O_020は未取得の省察理論の定義・効果保証に依存せず、52–53頁が示す自分の前提・偏りと判断の関係を点検する具体的行為を問う。国籍別傾向、授業効果、対立の再発率、Schön等の省察理論原著の独立確認ではない。

旧3129件の変更履歴を全て不変に保ち30件追記。安全な再構成・500問台帳再生成、v8不変、キー・正誤タグ・早見表・リンク・影響外の問、公開判定回帰8条件・置換回帰4条件を検査。台帳の設問・選択肢・解説はv8スナップショットで、改訂後はchangesと作業稿を参照する。

機械警告は106件から109件。Q_O_017のA1が1件解消し、Q_O_017–020にP1が4件増えた。全て正答解説末尾が「事実承認ではない」「効果の保証ではない」「特定理論の実証ではない」と留保するための検出で、正答内容の否定ではない。肯定表現を含む誤答解説も、その肢の誤りと根拠を明記している。各キーと全4解説を本文へ再照合し、警告を消すために留保を削らず誤検出として記録する。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列30件を全件検出（ケース見出し両箇所も検出）。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視。351・352頁の初回PNGは欠損して表示できなかったため再生成し、全7枚のPNGをverifyとloadで検査後、正常画像を直接目視した。変更箇所の欠字・重なり・文字切れなし。ただし349頁末尾にケース4解説見出しが孤立し、Q_O_018解説が350–351頁、Q_O_020解説が351–352頁に分かれる。最終版では見出しと本文の改頁調整が必要であり、レイアウト完成とは扱わない。未照合127問、全頁最終QAと既記録の改頁調整は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第157バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第157バッチ S213追加照合（2026-10-18）

[RFCDC第1巻（2018年）](https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c)全89頁PDFを再取得。29–32頁全文、51–53頁全文を精読。51・52・53頁（PDF53・54・55頁）を全頁画像照合。ケース4と全5問Q_O_016–020の全4肢・4解説を、本人の発言に基づく文脈の把握、相互の視点理解、合意形成、一時休止、協働、自己の前提と判断の点検へ対応させた。ケース本文を証拠とする論理的判断と、指定モデルへの教育的適用を区別。日本の慣習、国籍別傾向、授業効果、対立再発率、引用先原著の承認ではない。全89頁精読ではない。原バイトSHA256・読了範囲はevidence/batch157_sources.json。原PDF非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=157,base_remote_commit='440fb7a4abb0691518e0dce48df2644346cf62ed',fully_rejudged=sorted(targets),edits=30,case_entries=2,case_heading_occurrences=2,independent_answers={k:d[k]['independent_answer'] for k in sorted(targets)},sources=['S213'],status_counts=m['status_counts'],remaining=127,machine_warnings=109,new_warnings=newwarnings,removed_warnings=removed,new_warning_review='P1は正答末尾の事実承認・効果保証・未取得理論原著の承認を否定する留保を検出。正答自体の否定でないことと誤答解説の否定対象を全肢対照。',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,regenerated_corrupt_review_pngs=[351,352],pending_pagination=['349頁末尾ケース4解説見出し孤立','Q_O_018解説350–351頁','Q_O_020解説351–352頁'],all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch157_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('373 confirmed / 127 remaining',pages)
