"""Run once after direct review of all matched pages."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa184';k='Q_M_021'
BASE='f6590bdee47fe1fbc4837c1a0e8ce38794d110d7'
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':439,'修正必要':0,'要追加確認':61} and not m['release_ready']
cs=json.loads((p/'changes_batch184.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {key for key in d if d[key]!=d0[key]}=={k}
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500 and a['A_M_021']['ans']=='1'
for c in cs:
 got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_M_021']['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches184.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));assert machine['issues']==pre['issues'] and len(machine['issues'])==139
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
source=root/'cmu184.html';assert sha(source)=='83030644cee1b7faef64468b9742b455eb42451aea8afc2877d740c2b11c43f3'
url='https://www.cmu.edu/teaching/resources/teachingportfolios/index.html'
(p/'evidence/batch184_sources.json').write_text(json.dumps([dict(source_id='S249',title='Carnegie Mellon University Eberly Center Teaching Portfolios',url=url,checked='2026-10-19',bytes=source.stat().st_size,sha256=sha(source),body_read='公式ページ本文。定義、理念・責任・目標、資料の選択、研修参加と影響の区別、資料の意味・文脈説明、省察、更新・旧版保持。Seldin等の推薦原著は全文未取得で、その原著全体や概念の起源の承認ではない。',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
text=f'''

## 第184バッチ 2026-10-19

Q_M_021の設問・全4選択肢・全4解説を9件改訂。CMU Eberly Center公式Teaching Portfolios本文を取得し、教育理念・目標と根拠資料の関係、代表的資料の選択と省察、文脈説明を照合。単なる授業・研修記録の蓄積への還元を修正し、研修への参加記録と授業への影響を示す根拠を区別した。数値評価そのものを否定せず、数値だけへの限定を誤答とした。大学ガイドに照らした構成判断を問い、全大学の制度や効果の実証に一般化しない。旧誤答の情意フィルター・コーパス・ダイグロシアは各原典未取得で承認せず、同じ教授ポートフォリオ領域内で差替え。推薦されたSeldin等の原著全文は未取得。資料全体や翻訳全文は転載しない。

独立正答1、他の3肢は指定ガイドの選択・省察・説明を排除または参加と影響を混同するため誤り。キー変更なし。確認済み439・修正必要0・要追加確認61、500問を維持。累積432問3741件。全500問構造と正答タグ・早見表・リンク・改訂外不変を安全再構成で検査、v8 SHA256不変。公開判定8条件と置換・block-context回帰通過。機械警告139件、増減なし。台帳の原文はv8スナップショット、改訂後はchangesと作業稿を参照。

完全版Noto Sans CJK JPの既知ハッシュ一致と描画前の全CJK・非CJK代替フォント収録検査を通過。{pagecount}頁を新規描画し、全9改訂文字列を検出。影響{pages}頁の1800px画像を直接目視し、改訂箇所の欠字・切れ・重なりなし。最終の全頁画像QA・改頁調整・残61問の照合は未完了。作業稿は最終版ではなく出版不可。
'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第184バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+f'\n\n## 第184バッチ S249 2026-10-19\n\nS249 [CMU Eberly Center Teaching Portfolios]({url})。公式ページ本文取得。定義、Select your supporting materials、Consider where you are in your career、Write descriptions of your supporting materialsをQ_M_021の全肢全解説へ照合。単なる無選別の蓄積と区別し、選択・根拠・省察・文脈説明と研修参加／影響の違いを反映。原著の起源・全大学の制度・実証効果を承認しない。推薦原著は全文未取得。原資料非転載。取得ハッシュと範囲はevidence/batch184_sources.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('438問','439問').replace('62問','61問').replace('431問3732箇所','432問3741箇所').replace('431問を部分修正','432問を部分修正').replace('第183バッチの最新描画は355頁',f'第184バッチの最新描画は{pagecount}頁'))
e=dict(batch=184,base_remote_commit=BASE,fully_rejudged=[k],edits=9,independent_answers={k:1},sources=['S249'],status_counts=m['status_counts'],remaining=61,machine_warnings=139,added_warnings=[],removed_warnings=[],regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch184_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
