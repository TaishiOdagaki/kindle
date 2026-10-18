"""Record batch153 only after changed-page images have been inspected."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa153';targets={'Q_2_003'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':364,'修正必要':4,'要追加確認':132}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues']
added=[i for i in machine['issues'] if i not in prior];removed=[i for i in prior if i not in machine['issues']]
assert len(machine['issues'])==106 and not removed and len(added)==1 and added[0][:2]==['P1','Q_2_003']
cs=json.loads((p/'changes_batch153.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
_,q,a=qa.audit(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'))
assert len(q)==len(a)==500
for k in targets:
 rows=[c for c in cs if c['id']==k]
 assert html.unescape(q[k]['stem'])==next(c['after'] for c in rows if c['field']=='stem')
 assert int(a['A_'+k[2:]]['ans'])==d[k]['independent_answer']==2
 for field,values in [('options',q[k]['opts']),('explanations',a['A_'+k[2:]]['txt'])]:assert [html.unescape(t) for t in values]==[c['after'] for c in rows if c['field']==field]
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns}|{221})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('363問','364問').replace('修正必要 | 5問','修正必要 | 4問').replace('修正必要5問','修正必要4問').replace('359問3089箇所','360問3098箇所').replace('359問を部分修正','360問を部分修正');f.write_text(s)
report='''

## 第153バッチ（2026-10-18）

Q_2_003の設問・全4選択肢・全4解説を9箇所改訂し、独立正答2を確定した。確認済み364・修正必要4・要追加確認132、残136問。累積360問3098箇所、500問維持。

S217 Cummins（1976）原論文の44頁PDFを取得し、書誌・標題・要旨と、印刷20–27頁（PDF21–28頁）の全本文を連続精読。印刷20・23・24・27頁は全頁画像でも照合した。閾値は絶対的な固定値として定義できず、第二言語を使う時間や表現する認知的操作により変わり得るという24頁、言語能力を媒介変数とし社会的・教育的要因等と区別する23頁、仮説の単純化と今後の研究を認める27頁を確認した。加算的・減算的な状況については、20頁でCumminsが紹介するLambertの区別に照合した。

旧正答は歴史的用語の説明と閾値仮説を混同し、解説は言語能力の不足を概念形成・思考能力の不足へ直接結び付けていた。原著の仮説内容を問う設問とし、旧ラベルを個人の能力診断に使う説明を撤回した。現在の呼称の普及度に関する未確認の記述、順次バイリンガルと継承バイリンガルを同義とする記述も除去した。新しい4肢は閾値の固定値化、媒介変数としての仮説、加算/減算の取り違えをそれぞれ判定できる構成。正答番号2は維持し、4解説を対応本文へ照合した。

1976年の仮説を現在の確定的な因果法則として承認したのではなく、引用先のLambert原著や各実験の独立検証でもない。原論文の全44頁を精読したとはせず、読了範囲と原バイトSHA256をevidence/batch153_sources.jsonに記録した。原資料本文は転載しない。

変更前に設問がWordの単独段落であることを確認。旧3089件の履歴を不変に保って追記し、安全な再構成・台帳再生成を実行した。v8不変、500問の構造・既存キー・正誤タグ・早見表・リンク・影響外の問の本文、公開判定回帰8条件・置換回帰4条件を検査した。機械警告は105→106件。新規P1は、正答解説末の「思考能力全体の不足を診断する基準ではありません」という留保の否定形を拾う誤検出である。正答肢2自体を否定しておらず、4肢・解説対応と原著23・27頁への照合で確認した。警告を削除・隠蔽せず一覧に残す。最初の回帰コマンドで複数形の不存在ファイルを指定したが、正しいtest_v9_replacement.pyで4条件の合格を確認した。

台帳の原文はv8スナップショットであり、改訂後本文はchangesと作業稿を参照する。未確認132問と他の修正必要4問は承認に変更していない。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列9件を全件検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。ただし設問は23–24頁に分割され、解説の見出し・正答表示が221頁末、本文が222頁へ分かれている。内容欠落ではないが、最終組版では見出しと本文をまとめる改頁調整が必要。今回の画像確認を最終レイアウト合格とはしない。残136問の照合と全頁最終QAは未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第153バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第153バッチ（2026-10-18）

- S217 James Cummins（1976年4月）[The Influence of Bilingualism on Cognitive Growth: A Synthesis of Research Findings and Explanatory Hypotheses](https://files.eric.ed.gov/fulltext/ED125311.pdf)、Working Papers on Bilingualism No.9、ERIC ED125311。44頁PDF取得。書誌・標題・要旨、印刷20–27頁（PDF21–28頁）の全本文を連続精読。印刷20・23・24・27頁を画像照合。Q_2_003の設問・4肢・4解説に用いた。23頁の媒介変数、24頁の絶対的な閾値の否定と変動条件、27頁の仮説の限界、20頁が紹介する加算/減算の区別に限定する。歴史的仮説を現在の確定的な因果法則や個人の知的能力診断として扱わない。引用先のLambert原著・個別実験は未独立取得であり、その再検証を承認したものではない。現在の呼称普及度の旧記述も根拠未確認のため撤回。取得ファイルの全44頁精読ではない。
- 原バイトSHA256と読了範囲はevidence/batch153_sources.json。原PDFは転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=153,base_remote_commit='3c3ed121006193f130300436888c250b0f6fabb6',fully_rejudged=sorted(targets),decision_rows_updated=sorted(targets),edits=9,independent_answers={'Q_2_003':2},sources=['S217'],status_counts=m['status_counts'],remaining=136,machine_warnings=106,new_warnings=added,new_warning_review='P1 is a false positive on the limitation sentence, not a negation of answer2. Retained in machine issue list.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch153_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('364 confirmed / 136 remaining',pages)
