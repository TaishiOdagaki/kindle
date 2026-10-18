"""Record source scope, cumulative checks and reviewed working pages."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa162';targets={'Q_O_008','Q_O_041'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':384,'修正必要':2,'要追加確認':114} and not m['release_ready']
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==114 and not removed and len(newwarnings)==1 and newwarnings[0][1]=='Q_O_041'
cs=json.loads((p/'changes_batch162.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
assert a['A_O_008']['ans']=='1' and a['A_O_041']['ans']=='2'
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns}|{345})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('382問','384問').replace('116問','114問').replace('377問3227箇所','379問3245箇所').replace('377問を部分修正','379問を部分修正');f.write_text(s)
report='''

## 第162バッチ（2026-10-18）

Q_O_008・Q_O_041の設問・全4肢・全4解説を独立照合し18件改訂。正答はそれぞれ1・2で変更なし。確認済み384・修正必要2・要追加確認114、残116問。累積379問3245件の変更記録、500問維持。

S190 Cummins2008の大学配架著者原稿を原バイトで再取得。PDF2–5頁の本文を精読し、2・3・5頁画像も確認。会話の流暢さと学習場面の口頭・書記の理解表現の概念的区分、評価の混同による問題事例、文脈支援と認知的要求の相対性を確認した。引用される全研究の原著を別途取得・検証したという記録ではない。URL・原バイトSHA256・サイズ・読了範囲をevidence/batch162_sources.jsonに保存。

Q_O_041の旧解説は、教科学習に困難を感じる状態から学習言語能力が十分育っていないことを示すと判断していた。ケースの観察だけでCALP不足や原因を確定する表現を撤回。会話と教科学習の言語使用を同一視せず、表現や内容のどこに困るかを確認する解釈に改訂した。CALPを書記だけに限定する肢と、理解時間だけで認知能力不足を診断する肢を明示的に否定。教科学習歴等の個人情報を架空に補って診断したものではない。

Q_O_008は、講義の概念・要点を理解し必要事項を記録するという、ケースに明記されたニーズに直接合う目標に限定。生活言語一般が学習に役立たないという読みを避け、日常会話だけで講義理解が保証されるという誤った推論を問う。特定ノート指導法の効果や習得年数をこの概念区分から実証したものではない。ケース本文は実在調査の報告とは扱わず変更していない。

旧3227件を不変のまま18件追記。安全な累積再構成・500問台帳再生成、v8 SHA256不変、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件を検査。機械警告は113から114件へ1件増加。追加はQ_O_041の正答解説が否定文で終わるという語尾検知であり、末尾の「観察だけで原因を確定するものではない」は適用限界として保持した。正誤タグ・独立正答の誤りではなく、警告を隠すための文言変更は行わない。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
pagination=json.loads((r/'pagination.json').read_text())
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画。変更後18文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接目視。欠字・重なりなし。改頁残件：'+ '、'.join(pagination)+'。全頁最終目視と未照合116問は未了。出版不可の作業稿であり最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第162バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第162バッチ S190再取得（2026-10-18）

[Cummins2008著者原稿](https://eclass.upatras.gr/modules/document/file.php/PDE1535/CumminsBICSCALPSpringer2007.pdf)を再取得し、PDF2–5頁本文を精読、2・3・5頁画像を照合。Q_O_008とQ_O_041の各4肢・各4解説を確認。会話の流暢さと、学習場面の口頭・書記の理解表現は概念的区分であり、個人の能力不足や困難の単一原因をこの観察だけで診断しない。大学講義・記録の目標はケースのニーズへの適用判断であり、特定の教授法効果を実証したという主張はしていない。引用文献全件の原著検証・普遍的習得年数の承認は範囲外。evidence/batch162_sources.jsonに原バイトSHA256・サイズ・取得日・読了範囲。原PDF非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=162,base_remote_commit='53a0fa07335dc86fc8046c6b407887fa9c83c52b',fully_rejudged=sorted(targets),edits=18,independent_answers={'Q_O_008':1,'Q_O_041':2},sources=['S190'],status_counts=m['status_counts'],remaining=116,machine_warnings=114,new_warnings=newwarnings,removed_warnings=removed,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False,pending_pagination=pagination)
(p/'evidence/batch162_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('384 confirmed /116 remaining',pages)
