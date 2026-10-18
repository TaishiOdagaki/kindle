"""Record the recovered pending batch only after fresh image QA."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa155';targets={'Q_O_004'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':366,'修正必要':2,'要追加確認':132}
machine=json.loads((p/'postfix_machine.json').read_text());assert len(machine['issues'])==107 and machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues']
cs=json.loads((p/'changes_batch155.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
_,q,a=qa.audit(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'));assert len(q)==len(a)==500 and a['A_O_004']['ans']=='3'
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('365問','366問').replace('修正必要 | 3問','修正必要 | 2問').replace('修正必要3問','修正必要2問').replace('361問3105箇所','361問3114箇所');f.write_text(s)
report='''

## 第155バッチ（2026-10-18）

Q_O_004の設問・4選択肢・4解説を9箇所改訂し、独立正答3を確定。確認済み366・修正必要2・要追加確認132、残134問。累積361問3114箇所、500問維持。

S30 Schmidt（1990）原論文30頁PDFを大学から取得。131–133頁の2.1–2.2、138–141頁の第4節冒頭・4.1、149–150頁の結論を精読し、132・139・141・149頁を全頁画像照合した。132頁の気づきと理解・言語報告の条件、139頁のpreliminary intake、141頁の一時的な反復後に再使用しなかった例と実証上の留保、149頁の形式を目立たせる指導の役割を全4肢・4解説へ対応させた。

現行ケース1は既にwhat/whereの質問条件を区別する内容へ改訂済みで、今回はケース本文を変更しない。教師が検討する工夫の意図を問うと明記し、本人の気づきや授業効果を推測で確定しない。未照合の臨界期・文化変容・リンガフランカ各定義に依存した旧4択を、同じ学習領域の気づきの内容と限界を問う4択へ改訂した。教師の提示と本人の気づき、気づきと抽象規則の言語化、一時的な気づきと保持・習得を区別する。1990年の仮説を現在の全理論の合意や児童を含む全学習者の普遍法則として承認せず、原著の成人中心の範囲と研究の留保を尊重する。引用先のSchmidt/Frota1986等を独立取得したものではなく、全30頁精読でもない。原PDFは転載しない。

第154バッチf67b3a2までの保存は完了していたが、第155バッチの保存前にローカル環境が古い状態へ戻り、作業スクリプトと描画出力が失われていた。GitHubの最新HEADと6記録を再取得して正本から再構成し、取得原論文と会話に残る判定内容を用いて未保存バッチを復元した。以前の描画画像がないため、画像確認済みとは扱わず新規描画・目視を改めて実施した。

旧3105件の変更履歴を不変に保って9件追記。安全な再構成・台帳再生成、v8不変、500問の構造・既存キー・正誤タグ・早見表・リンク・影響外の問、公開判定回帰8条件・置換回帰4条件を検査。機械警告107件で第154バッチから一覧の増減なし。台帳原文はv8スナップショット、改訂後本文はchangesと作業稿を参照する。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列9件を全件検出。'+ '・'.join(map(str,pages))+'頁の1800px画像を直接目視。変更箇所の欠字・重なり・文字切れなし。未照合134問、全頁最終QAと既記録の改頁調整は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第155バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第155バッチ S30追加照合（2026-10-18）

S30 Richard W. Schmidt（1990）[The Role of Consciousness in Second Language Learning](https://www.nflrc.hawaii.edu/PDFs/SCHMIDT%20The%20role%20of%20consciousness%20in%20second%20language%20learning.pdf)、Applied Linguistics11(2),129–158を再取得。131–133頁の2.1–2.2、138–141頁の4冒頭・4.1、149–150頁の結論を精読。132・139・141・149頁（PDF4・11・13・21頁）を画像照合。Q_O_004の全4肢・全4解説を、気づきと理解、提示とpreliminary intake、一時的反復と保持・習得の区別へ対応させた。141頁の紹介研究の十分性・必要性の実証上の留保と、成人中心の範囲を重視。引用先原著の独立取得・現代の全理論の合意・当該日本語授業の効果の実測ではない。全30頁精読ではない。原バイトSHA256・読了範囲はevidence/batch155_sources.json。原PDF非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=155,base_remote_commit='f67b3a2f991a323b65d388be64ce2762e1dd06d3',fully_rejudged=sorted(targets),edits=9,case_changed=False,independent_answers={'Q_O_004':3},sources=['S30'],status_counts=m['status_counts'],remaining=134,machine_warnings=107,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),recovered_from_lost_local_work=True,full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch155_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('366 confirmed / 134 remaining',pages)
