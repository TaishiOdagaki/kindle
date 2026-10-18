"""Checkpoint task/accuracy design and reflective self-review decisions."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa164';targets={'Q_O_052','Q_O_055','Q_MO_004'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':389,'修正必要':2,'要追加確認':109} and not m['release_ready']
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==117 and not removed and {x[1] for x in newwarnings}==targets and all(x[0]=='P1' for x in newwarnings)
cs=json.loads((p/'changes_batch164.json').read_text());assert len(cs)==27 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
keys={'Q_O_052':4,'Q_O_055':3,'Q_MO_004':3}
assert all(a['A_'+k[2:]]['ans']==str(v) for k,v in keys.items())
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==27 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('386問','389問').replace('112問','109問').replace('381問3263箇所','384問3290箇所').replace('381問を部分修正','384問を部分修正');f.write_text(s)
report='''

## 第164バッチ（2026-10-18）

Q_O_052・Q_O_055・Q_MO_004の全4肢・全4解説を独立照合し、設問も含め27件改訂。独立正答4・3・3でキー変更なし。確認済み389・修正必要2・要追加確認109、残111問。累積384問3290件、500問維持。

S144 Richards2006著者公開冊子を52頁の原PDFとして再取得し、印刷14–16・31–35・45頁本文、15・31–33頁画像を照合。Q_O_052は、ロールプレイという活動名だけでタスクと同一視せず、使用表現を固定しないことと、依頼を伝え相手の応諾可否を確認するという成果目標を設問に追加した。これは元ケースに書かれていた事実として推定したのではなく、問いの追加条件である。既有資源・意味・成果を重視するRichards自身の説明と、PPPの提示先行との順序の違いに限定。気づきや習得を必ず生むという因果効果は承認していない。冊子に引用されたWillis等の全原著を独立取得したとは記録せず、Willisモデル全体の実施忠実性やTBIがPPPより優れるという主張は範囲外。

Q_O_055は、教授法を組み合わせること自体を有効性の根拠にする包括的説明を撤回。Richardsの正確さと流暢さの活動の区別、両者の関係付け、正確さの活動が前にも後にも置けること、観察された課題への事後練習の例に基づく活動選定へ改訂した。単なる折衷や無条件の学習効果を承認するものではない。ケース本文・他問のALMの理論帰属は変更せず、未確認を保っている。

Q_MO_004は取得済みS213 RFCDC第1巻52–53頁の批判的理解と自己理解6項目を本文・両頁画像で照合し、47頁の批判的思考本文も参照。原バイトSHA256は第156バッチと一致。旧問の包括的な技法名称当てを、同じ授業後の自己点検領域の行為選択へ改訂し、学習者の反応・教師の見立て・自分の前提と判断の限界を照らす行為に限定。RFCDCを「授業分析」という技法名の定義資料に代用せず、モデルの観点をケースへ適用する問いであることを明示した。旧肢にあるコーパス・誤用・対照分析の定義を未照合のまま承認せずこの問から除いたが、他の未確認問の定義や関連原著を一括承認してはいない。

旧3263件は不変で27件追記。安全な累積再構成、500問台帳、v8 SHA256不変、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件を検査。機械警告は114から117件へ増加。3件は正答解説末尾の効果保証を否定する限定文へのP1語尾検知であり、全選択肢・キーとの整合を読み直して誤検出と判断。限定を消して警告数だけを下げない。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
pagination=json.loads((r/'pagination.json').read_text())
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、変更後27文字列を全件検出。'+ '・'.join(map(str,pages))+'頁の1800px画像を直接目視、欠字・重なりなし。改頁所見：'+ '、'.join(pagination)+'。全頁最終QAと未照合111問は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第164バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第164バッチ S144再取得・S213本文検証（2026-10-18）

- S144 [Richards2006著者公開冊子](https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf)。印刷14–16・31–35・45頁本文、15・31–33頁画像。Q_O_052・055のタスクの意味・成果・既有資源、PPP順序、正確さと流暢さの活動の関係を照合。引用されるWillis等の全原著や介入効果の独立検証ではない。
- S213 [RFCDC第1巻](https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c)。取得済みPDFの原バイトSHA256を第156バッチと照合。52–53頁本文・自己理解全6項目・両頁画像、47頁批判的思考本文。Q_MO_004は観点のケース適用であり、授業分析という技法名の定義や相談効果の実証ではない。

取得範囲と原バイトのハッシュ・サイズはevidence/batch164_sources.json。原PDFは非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=164,base_remote_commit='e4eb0b113ba4324d29fe42636cc531f1e3a93d24',fully_rejudged=sorted(targets),edits=27,independent_answers=keys,sources=['S144','S213'],status_counts=m['status_counts'],remaining=111,machine_warnings=117,new_warnings=newwarnings,removed_warnings=removed,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False,pending_pagination=pagination)
(p/'evidence/batch164_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('389 confirmed /111 remaining',pages)
