"""Checkpoint after direct page-image QA of batch154."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa154';targets={'Q_O_012'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':365,'修正必要':3,'要追加確認':132}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues']
added=[i for i in machine['issues'] if i not in prior];removed=[i for i in prior if i not in machine['issues']]
assert len(machine['issues'])==107 and not removed and len(added)==1 and added[0][:2]==['P1','Q_O_012']
cs=json.loads((p/'changes_batch154.json').read_text());assert len(cs)==7
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
_,q,a=qa.audit(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'))
_,q0,a0=qa.audit(str(p.parent.parent/'登録日本語教員試験決定版問題集_v8_修正版.docx'))
assert len(q)==len(a)==500 and a['A_O_012']['ans']=='2'
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==7 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('364問','365問').replace('修正必要 | 4問','修正必要 | 3問').replace('修正必要4問','修正必要3問').replace('360問3098箇所','361問3105箇所').replace('360問を部分修正','361問を部分修正');f.write_text(s)
report='''

## 第154バッチ（2026-10-18）

Q_O_012を7箇所改訂し、設問・全4肢・独立正答2・全4解説をS04とS179の取得本文へ照合した。確認済み365・修正必要3・要追加確認132、残135問。累積361問3105箇所、500問維持。

現行ケース3の見出しと本文2段落は、第4バッチですでに会社Xの社員・自社の部長・社内の同僚・取引先という条件へ改訂されていた。Q_O_012の判定には古い「ケース前提の改稿が必要」という所見が残っていたため、現行ケースと後続Q_O_011–014の関係を再確認した。今回はケースを再変更せず、元の「このような誤り」という参照だけの問いを、聞き手とウチ・ソトによる表現選択と明示した。CEFR2001の5.2節を分類枠組みとして明記し、活用形、社会言語能力、音韻、正書法の各焦点を区別する。

S179公式CEFR2001 PDFを再取得。5.2冒頭、5.2.1.2の定義と列挙、5.2.1.4–5.2.1.5本文、5.2.2冒頭から5.2.2.4末を精読。社会的関係を示す表現、丁寧さの慣習、文脈による言葉遣いを扱うことを確認し、118・119頁を画像照合した。S04敬語の指針も再取得し、18頁の謙譲語II、22–23頁の立てる人物、43–44頁のウチ・ソトの具体例を精読。学校での呼称慣習を会社へ一律に広げず、会社内外と「部長の田中」の説明を画像で確認した。資料の分類を構成した事例へ適用する判断であり、CEFRにこの日本語事例が掲載されていると主張しない。未取得のCanale/Swain原著の検証ではない。

旧ケースの「本人への引用なら不自然」という前提は復元しない。新解説でも、本人への引用を一律に誤用とする判断と区別した。ケースに音声資料等はないため、発音全体の正誤や他能力の不足を診断しない。実際の発話に複数の能力が関与することと、設問が特定する主な焦点を区別し、正答2だけが焦点へ対応することを独立確認した。Q_O_013の原資料未照合・ケースにです/だの切替実例がないという既存の保留は維持し、周辺問を自動承認しない。

S04の今回の取得版では印刷44頁がPDF47頁であることを画像で確認した。sources.mdのcatalogにあった一律「2頁差」を、この取得版の検証済み対応へ更新した。歴史的な別ファイルのページ対応までは推定しない。原バイトSHA256と読了範囲をevidence/batch154_sources.jsonへ記録し、原資料は転載しない。

設問が単独のWord段落であることを変更前に確認し、旧3098件の累積履歴を保って7件追記した。安全な再構成・台帳再生成、v8不変、500問の構造・正答番号・正誤タグ・早見表・リンク・影響外の問、公開判定回帰8条件・置換回帰4条件を検査した。機械警告は106→107件。新規P1は正答解説末の「本人への引用を一律に誤用とする判断ではありません」という留保を拾う誤検出で、正答肢2自体の否定ではない。全肢・解説と根拠を再確認し、警告一覧を改変せず判断理由を残す。台帳原文はv8スナップショット、改訂後本文はchangesと作業稿を参照する。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画。最終変更文字列7件を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接目視した。変更箇所の欠字・重なり・文字切れなし。全頁最終QAと既記録の改頁調整は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第154バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';s=f.read_text();assert s.count('PDF頁と印刷頁は2頁差。')==1;s=s.replace('PDF頁と印刷頁は2頁差。','第154バッチ取得版では印刷44頁がPDF47頁であることを画像照合。');f.write_text(s+'''

## 第154バッチ S04・S179追加照合（2026-10-18）

- S179 [CEFR2001公式PDF](https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf)を再取得。5.2冒頭（108頁）、5.2.1.2の定義・列挙（112–113頁）、5.2.1.4–5.2.1.5本文（116–117頁）、5.2.2冒頭から5.2.2.4末（118–120頁）を精読。118・119頁（PDF127・128頁）を画像照合。Q_O_012の4肢・4解説へ使用。文法・音韻・正書法の焦点と社会的関係に応じた言葉遣いを区別。全273頁精読やCanale/Swain原著取得を意味しない。
- S04 [敬語の指針](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93927001_09.pdf)を再取得。18頁・22–23頁・43–44頁を本文精読し、43・44頁（今回のPDF46・47頁）を画像照合。会社内外のウチ扱い、学校の呼称との違い、謙譲語IIを現行ケースへ照合。今回の取得版のページ対応をcatalogへ明記。全書精読・現在の慣習頻度の再調査ではない。
- URL、原バイトSHA256、読了範囲と限界はevidence/batch154_sources.json。原PDFは転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=154,base_remote_commit='bf6f26a8ab16aa9333d4588bb6b2b7f9a1e27c78',fully_rejudged=sorted(targets),decision_rows_updated=sorted(targets),edits=7,case_changed=False,independent_answers={'Q_O_012':2},sources=['S04','S179'],status_counts=m['status_counts'],remaining=135,machine_warnings=107,new_warnings=added,new_warning_review='P1 false positive on the limitation about quoting an interlocutor; the correct option itself is not negated. Warning retained.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch154_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('365 confirmed / 135 remaining',pages)
