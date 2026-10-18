"""Checkpoint two independent judgments; preserve other CSV record bytes."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa163';targets={'Q_O_066','Q_4_099'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':386,'修正必要':2,'要追加確認':112} and not m['release_ready']
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==114 and not removed and not newwarnings
cs=json.loads((p/'changes_batch163.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
assert all(a['A_'+k[2:]]['ans']=='1' for k in targets)
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('384問','386問').replace('114問','112問').replace('379問3245箇所','381問3263箇所').replace('379問を部分修正','381問を部分修正');f.write_text(s)
report='''

## 第163バッチ（2026-10-18）

Q_O_066・Q_4_099を再判定し、設問・各4肢・各4解説の18件を改訂。独立正答はともに1、キー変更なし。確認済み386・修正必要2・要追加確認112、残114問。累積381問3263件の変更記録、500問維持。

Q_O_066は、Coyleを含むBower・Cross・Coyleの出版社公開章抜粋S191を再取得。印刷9–11頁（PDF8–10頁）の本文を読み、9・10頁画像を照合した。内容に基づく目標から必要な言語を検討する二重焦点を、ケース14の環境資料の読解・対話・比較レポートに具体化する目標設定へ改訂。単に環境を話題にする活動と内容自体を学ぶ設計を区別した。ケース本文は変更していない。旧肢の文法訳読法・サイレントウェイ・ALMは、各原著を未取得のまま解説を承認せず、この問からその説明を除いた。別の未確認問にある教授法の理論帰属・定義を一括確認済みにはしていない。引用先の介入研究原データや全章・全書籍は未確認であり、二重目標の設定を全員の成果保証としない。

Q_4_099はS213 RFCDC第1巻41–43頁（注7・8含む）と用語集73頁の全文、42・73頁の画像を照合。既取得の全89頁PDFのSHA256が第156バッチ記録と一致することを検証した。Webの再取得はタイムアウトしたため、今回新規取得に成功したとは記録せず、検証した既取得本文を使用した。旧解説の「無意識の正解」「歪曲・蔑視」を自民族中心主義の必須条件に見せる表現と、文化相対主義的視点から柔軟な適応へ一律につながるという効果の断定を撤回。設問をRFCDC自身の定義・開放性・尊重へ明示限定し、自分の文化を参照基準とする見方、他者の尊重と同意・採用の違い、自分の前提を問い直す姿勢、人権・尊厳を侵害する慣行の内容を無条件肯定しない限界を全4肢・4解説へ照合した。文化相対主義の哲学的全学説やBennett等の引用先原著を代わりに承認したものではない。

旧3245件は不変で18件追記。安全な累積再構成と台帳再生成、v8 SHA256不変、500問・正答・正誤タグ・早見表・内部リンク、公開判定回帰8条件・置換回帰4条件を検査。機械警告114件で増減なし。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照する。
'''
pagination=json.loads((r/'pagination.json').read_text())
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、変更後18文字列を全件検出。'+ '・'.join(map(str,pages))+'頁の1800px画像を直接目視、欠字・重なりなし。改頁所見：'+ '、'.join(pagination)+'。既記録の改頁調整と全頁最終QA、未照合114問は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第163バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第163バッチ S191再取得・S213取得済み本文検証（2026-10-18）

- S191 [Bower・Cross・Coyleの出版社公開章抜粋](https://assets.cambridge.org/97811087/29734/excerpt/9781108729734_excerpt.pdf)。印刷9–11/PDF8–10頁本文、9・10頁画像。Q_O_066の内容と言語の二重目標・意味を伝える言語を照合。全書籍・引用先介入研究・教授法効果の承認ではない。
- S213 [RFCDC Volume1](https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c)。Web再取得はタイムアウト。既取得PDF原バイトのSHA256を第156バッチと照合し、41–43頁本文・注7/8、73頁用語集本文、42・73頁画像を再確認。29–30頁本文も参照。Q_4_099をRFCDC自身の定義・姿勢に限定し、哲学的文化相対主義の全学説や適応効果へ拡張しない。

原バイトハッシュ・サイズ・読了範囲はevidence/batch163_sources.json。PDF本文は非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=163,base_remote_commit='7b0365aecc81c11dcfdaf40fa3b5f3299a975755',fully_rejudged=sorted(targets),edits=18,independent_answers={k:1 for k in sorted(targets)},sources=['S191','S213'],status_counts=m['status_counts'],remaining=114,machine_warnings=114,new_warnings=newwarnings,removed_warnings=removed,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False,pending_pagination=pagination)
(p/'evidence/batch163_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('386 confirmed /114 remaining',pages)
