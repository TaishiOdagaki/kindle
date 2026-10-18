"""Checkpoint five independent judgments, preserving unchanged CSV bytes."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from docx import Document
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa160';targets={'Q_1_002','Q_O_005'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':381,'修正必要':2,'要追加確認':117} and not m['release_ready']
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==113 and not removed and not newwarnings
cs=json.loads((p/'changes_batch160.json').read_text());assert len(cs)==15 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
assert a['A_1_002']['ans']=='4' and a['A_O_005']['ans']=='3'
paras=[x.text for x in Document(doc).paragraphs]
for c in cs:
 if c['field']=='case_text':assert paras.count(c['after'])==c.get('count',1);continue
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==15 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('379問','381問').replace('119問','117問').replace('374問3203箇所','376問3218箇所').replace('374問を部分修正','376問を部分修正');f.write_text(s)
report='''

## 第160バッチ（2026-10-18）

Q_1_002・Q_O_005を改訂し、全4肢・全4解説から独立正答4・3を確定。設問2件、選択肢5件、解説8件の計15件を追記。確認済み381・修正必要2・要追加確認117、残119問。累積376問3218件の変更記録、500問維持。

Q_1_002は一度の発言と来日3か月という情報から「過剰同化の相」「適応を急いだアイデンティティの抑圧」と心理状態・段階・因果を決める旧説明を撤回。架空発言への教育的対応をRFCDCの開放性・尊重に限定し、事情を尋ねて本人の選択権を尊重する対応を正答とした。文化全体の優劣を逆転して教える肢、日本のやり方を全て正しいと肯定する肢、心理状態を確定して全面禁止する肢は、それぞれの誤りの箇所を本文へ照合。尊重は全ての慣習の無条件肯定ではなく、他者の尊厳・人権・自由を侵す内容に限界を設ける42頁本文・注8も明記した。相談支援の必要性まで一律否定しない。

Q_O_005は累積改訂済みケース1の全3段落を再確認。教師の訂正が検討対象なのに、学習者の正用を初めから誤用とする読みを防いだ。旧解説の自己点検が成長に直結するという効果の断定を撤回し、発話記録と自分の訂正の根拠・前提の点検へ具体化。録画を必須とせず、Schön等の未取得原著や自己点検の因果効果を承認したものではない。

S213の取得済み原PDFの4154359バイト・SHA256を第159バッチ記録へ照合して同一性を確認。41–43頁（注7–8含む）、47・52–53・73頁本文を精読、42・43・53頁（PDF44・45・55頁）を1800px全頁画像で照合。取得済み原本の追加精読であり、新規取得成功や全89頁通読とはしない。モデルの架空事例への適用と、心理診断・適応モデルの実証を区別する。

ポライトネス関連4問は今回の取得で必要本文に到達できず保留維持。MPI1987は書誌・概要のみ、Scribd13頁表示は今回本文が取得できず推薦一覧のみ。理論共同開発者Brown自身の2015年解説PDFもWeb・curlとも403となった。検索抜粋や概要だけを根拠にせず、evidence/batch160_source_attempts.jsonへ記録。個別資料の取得障害であり監査全体の完全停止条件とはしない。

旧3203件の順序付き履歴を不変のまま15件追記。安全な累積再構成・台帳再生成、v8 SHA256不変、500問・キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件を検査。機械警告113件で増減なし。台帳原文はv8スナップショットで、改訂後はchangesと作業稿を参照する。
'''
pagination=['Q_1_002の設問・肢1–2が5頁、肢3–4が6頁','Q_O_005の解説が344–345頁に分割','既記録Q_1_003の解説見出し・キーは今回202頁下端、本文203頁']
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、変更後文字列15件を全件検出。'+ '・'.join(map(str,pages))+'頁のPNGをverify・loadし1800px画像を直接目視。345頁画像は初回表示で破損を検出しPDFから再生成、verify・load後に再表示して確認した。日本語の欠字・重なりなし。ただし'+ '、'.join(pagination)+'を改頁調整の残件に記録。全頁最終QA、既記録の改頁調整、未照合119問は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第160バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第160バッチ S213追加照合とポライトネス資料取得保留（2026-10-18）

S213 [RFCDC第1巻](https://rm.coe.int/16807bc66c)の取得済み原PDFを第159バッチのサイズ・SHA256へ照合し一致。41–43頁（注7–8含む）、47・52–53・73頁本文を精読し42・43・53頁を全頁画像照合。Q_1_002の開放性・尊重、Q_O_005の証拠に基づく評価と自分の前提・判断の点検へ対応。全89頁精読、心理診断、過剰同化モデル原著、自己点検・録画の因果効果の実証ではない。evidence/batch160_sources.json参照。原PDF非転載。Brown・Levinson関連の検索抜粋やMPI書誌・概要は学術的承認に不使用、必要本文取得失敗はevidence/batch160_source_attempts.json参照。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=160,base_remote_commit='3e6f4a3d961177808bbe3ba79b2fee43f2b7cae0',fully_rejudged=sorted(targets),edits=15,independent_answers={k:d[k]['independent_answer'] for k in sorted(targets)},sources=['S213'],status_counts=m['status_counts'],remaining=119,machine_warnings=113,new_warnings=newwarnings,removed_warnings=removed,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
e['pending_pagination']=pagination
e['render_repair']='345頁PNGの初回表示で破損を検出。PDFから再生成しverify・load・直接表示後に確認。'
(p/'evidence/batch160_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('381 confirmed /119 remaining',pages)
