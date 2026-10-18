"""Checkpoint the repaired multi-paragraph writing guidance question."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from docx.oxml.ns import qn
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa167b';k='Q_4_089'
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[key].replace('\r\n','\n') if key==k else raw for key,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':397,'修正必要':2,'要追加確認':101} and not m['release_ready']
cs=json.loads((p/'changes_batch167.json').read_text());assert len(cs)==10 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {key for key in d if d[key]!=d0[key]}=={k}
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_4_089']['ans']=='2'
assert q[k]['stem']==cs[0]['after']
assert not [para for para in Document(doc).paragraphs if para.text==cs[1]['before']]
for c in cs[2:]:assert html.unescape((q[k]['opts'] if c['field']=='options' else a['A_4_089']['txt'])[c['index']])==c['after']
matches=json.loads((r/'matches167.json').read_text());assert len(matches)==10 and matches['1']==[] and all(v for key,v in matches.items() if key!='1')
pages=sorted({v for ns in matches.values() for v in ns});machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==121 and len(warnings)==1 and warnings[0][1]==k
assert all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagination=json.loads((r/'pagination.json').read_text());pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第167バッチ 2026-10-18

Q_4_089をS225名古屋大学の大学教材『レポート課題に備える』（笠木雅史作成、教養教育院・高等教育研究センター発行、2019-03-01改訂）の全文へ照合し10件改訂。独立正答2、キー変更なし。確認済み397・修正必要2・要追加確認101、残103問。累積392問3363件、500問維持。

旧稿の「と思う」を「と考えられる」へ替えることで客観化する説明を撤回し、問い・結論・理由根拠・資料の調査過程と対象範囲を吟味する指導へ改訂。観察や個人の経験を学術文章から一律排除せず、限られた車内観察から一般傾向を主張できるかを吟味するという、取得教材の方針の具体的適用として問う。引用内の「読書離れ」を社会的事実として独立承認してはいない。推薦文献2冊も未取得である。

旧設問は2段落だったため、第1段落を引用を含む新設問に置換し、旧引用段落を明示的に除去する2件を記録。最初の再構成は引用が新段落にも残るため候補2件となり安全アサートで停止し、作業DOCXは上書きされなかった。削除に直前段落条件を追加して旧独立段落だけを特定し、再構成後に新設問一致・旧独立段落不存在をOOXMLで検査した。旧3353件は変えていない。

v8不変、500問、キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件が通過。機械警告120→121件。新規P1は、文末形式だけで根拠が確かになるわけではないという正答解説末尾の限定による誤検出と判断。限定を削って警告数だけを下げない。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\nNoto Sans JPで{pagecount}頁を新規描画。新規9文字列を全件検出し、旧独立段落1件の削除を別途検査。'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認、改頁所見は証跡へ記録。全頁最終QAと未照合103問は未了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第167バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第167バッチ S225 大学教材 2026-10-18\n\n[S225 名古屋大学 レポート課題に備える](https://web.cshe.nagoya-u.ac.jp/resources/asg/prepareessay.html)の本文全節と作成者・発行者・改訂日を確認。問いへの回答・理由根拠の吟味、資料の調査過程、自分の考察と資料の区別。Q_4_089の具体的適用。推薦書籍・社会的読書統計は未取得。原バイトSHA256と範囲はevidence/batch167_sources.json、原文全体非転載。\n''')
f=p/'README.md';f.write_text(f.read_text().replace('396問','397問').replace('102問','101問').replace('391問3353箇所','392問3363箇所').replace('391問を部分修正','392問を部分修正'))
e=dict(batch=167,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=[k],edits=10,new_text_passages=9,explicit_paragraph_deletions=1,deleted_standalone_paragraph_absent=True,independent_answers={k:2},sources=['S225'],status_counts=m['status_counts'],remaining=103,machine_warnings=121,new_warnings=warnings,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansJP.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False,pending_pagination=pagination)
(p/'evidence/batch167_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
