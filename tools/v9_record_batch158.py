"""Record one complete source-bounded audit; keep failed-source question pending."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa158';targets={'Q_1_003'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':374,'修正必要':2,'要追加確認':124}
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==110 and not removed and len(newwarnings)==1 and newwarnings[0][:2]==['P1','Q_1_003']
cs=json.loads((p/'changes_batch158.json').read_text());assert len(cs)==7 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets and d['Q_2_032']==d0['Q_2_032']
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_1_003']['ans']=='1'
for c in cs:
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==7 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns}|{203})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('373問','374問').replace('125問','124問').replace('368問3159箇所','369問3166箇所').replace('368問を部分修正','369問を部分修正');f.write_text(s)
report='''

## 第158バッチ（2026-10-18）

Q_1_003の設問・選択肢2件・全4解説を7箇所改訂し、独立正答1を確定。確認済み374・修正必要2・要追加確認124、残126問。累積369問3166件の変更記録、500問維持。

S213 RFCDC第1巻（2018年）は今回の公式サイト再取得がタイムアウトしたが、手元の取得済み89頁原PDFの4154359バイト・SHA256 a93866bccc575a825b4cc9e9b5f25c115d7c1ffd29dc677a1acc0aa226daa612が、GitHub第157バッチの取得記録と一致することを確認できた。その原PDFの29–32頁を精読し、29・30頁（PDF31・32頁）を1800px全頁画像で照合。新規取得成功と、取得済み原本の再検証・追加読了を混同しない。

文化的アイデンティティを、指定モデルが示す文化集団への所属、同時の複数帰属、状況・時間に応じた主観的重要さの変動に限定した。旧解説の「ハイブリッド化」、CEFR・加算的バイリンガリズム・滅失的同化への補助的な理論帰属を削除し、「双方のアイデンティティの共存・拡張が一般的」という頻度断定を撤回。旧肢4の第二言語習得に伴う因果的な完全置換を、同じ文化的アイデンティティ領域の複数帰属の必要条件を問う肢へ改訂。宗教・地域の文化を除外する肢、幼少期固定・成人後不変とする肢も本文から独立に判定した。全89頁精読や引用先原著、同化の頻度・言語学習の因果効果の実測ではない。

Q_2_032はS179 CEFR2001の必要本文を再取得できず保留維持。長い公式URLと短縮URLを試し、短縮URLのcurlは45秒・受信0バイト、exit28。Webで273頁PDFの概要は一度得られたが、必要箇所の本文取得・find・画像確認がタイムアウトした。概要や検索抜粋だけで全4肢・解説を承認しない。取得失敗はevidence/batch158_source_attempts.jsonに記録。個別資料の一時的な取得障害であり、監査全体の完全停止条件とはしない。

旧3159件の変更履歴を不変に保ち7件追記。安全な再構成・500問台帳再生成、v8不変、既存キー・正誤タグ・早見表・リンク・影響外の問、公開判定回帰8条件・置換回帰4条件を検査。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照する。機械警告110件でP1が1件追加。Q_1_003の正答解説末尾の「特定の変容が起こる頻度を測定した説明ではありません」という留保と、誤答解説の原資料の肯定的説明を検出したもの。正答自体の否定ではなく、各誤答の誤りの箇所も説明している。キー・全4解説を原資料へ対照し、留保を削って警告だけを消さず誤検出として記録する。
'''
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、最終変更文字列7件を全件検出。'+ '・'.join(map(str,pages))+'頁（変更2頁と直前の解説見出しを含む文脈1頁）のPNGをverifyとloadで検査し、1800px画像を直接目視。変更箇所の欠字・重なり・文字切れなし。ただしQ_1_003の解説見出し・キーが203頁末尾、解説本文が204頁に分かれるため最終版の改頁調整対象とする。未照合126問、全頁最終QAと既記録の改頁調整は未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第158バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第158バッチ S213の原本再検証とS179取得保留（2026-10-18）

S213 [RFCDC第1巻（2018年）](https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c)の取得済み原PDFをGitHub第157バッチのバイト数・SHA256と照合し一致。今回の再取得はタイムアウトのため、新規取得成功とは記録しない。29–32頁本文を精読、29・30頁（PDF31・32頁）を全頁画像照合。Q_1_003の全4肢・4解説を、複数帰属・主観的重要さの変動・文化集団の多様性へ対応。未取得理論や同化の頻度・言語習得の因果効果を承認しない。全89頁精読ではない。evidence/batch158_sources.jsonに原本再検証と範囲を記録。原PDF非転載。S179 CEFR2001は必要本文の再取得・画像確認に失敗、Q_2_032の要追加確認を維持。evidence/batch158_source_attempts.json参照。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=158,base_remote_commit='e1505318f944faaf489bd3f075c38787ea343b58',fully_rejudged=sorted(targets),edits=7,independent_answers={'Q_1_003':1},sources=['S213'],status_counts=m['status_counts'],remaining=126,pending_unchanged=['Q_2_032'],machine_warnings=110,new_warnings=newwarnings,removed_warnings=removed,new_warning_review='P1は変容頻度を実測した説明ではないという留保を検出。正答の否定でなく、全4解説と原本文を対照済み。',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,additional_context_pages=[203],pending_pagination=['Q_1_003の解説見出し・キー203頁末尾、本文204頁'],all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch158_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('374 confirmed / 126 remaining',pages)
