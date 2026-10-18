"""Record restored edits after fresh source reading and fresh five-page QA."""
import json,hashlib,subprocess,csv,io
from pathlib import Path
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa165'
targets={'Q_1_034','Q_1_035','Q_1_008'}
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':392,'修正必要':2,'要追加確認':106}
cs=json.loads((p/'changes_batch165.json').read_text());assert len(cs)==27 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
matches=json.loads((r/'matches165.json').read_text());pages=sorted({v for ns in matches.values() for v in ns});assert pages==[8,19,205,216,217]
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==118 and len(warnings)==1 and warnings[0][1]=='Q_1_008'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
entries=[]
specs=[('S219','jlpt165.html','https://jlpt.jp/sp/faq/index.html','目的、会話・作文、解答方式、項目応答理論/配点、認定期限の各Q/A。'),('S220','eju165.html','https://www.jasso.go.jp/ryugaku/eju/about/eju_guide/2026.html','目的、出題科目等、備考1/5。'),('S220','score165.html','https://www.jasso.go.jp/ryugaku/eju/about/score/index.html','得点説明本文全体。'),('S220','syllabus165.html','https://www.jasso.go.jp/ryugaku/eju/examinee/syllabus/japanese.html','目的・構成・各領域説明全文。'),('S221','bjt165.html','https://www.kanken.or.jp/bjt/about/level_sample.html','冒頭の0～800点・6段階・非合否。'),('S222','opi165.html','https://www.actfl.org/assessments/postsecondary-assessments/opi','目的、自発的発話、面接4段階、レベルチェック/プローブ。列記された妥当性信頼性原著は未検証。')]
for sid,fn,url,scope in specs:
 f=root/fn;entries.append(dict(source_id=sid,url=url,bytes=f.stat().st_size,sha256=sha(f),checked='2026-10-18',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch165_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
text='''

## 第165バッチ 復旧と公式本文照合 2026-10-18

Q_1_034・Q_1_035・Q_1_008、3問27件を反映。独立正答4・2・1、キー変更なし。確認済み392・修正必要2・要追加確認106、残108問。累積387問3317件。

保存途中の作業場を失ったため、GitHub上のアップロード済みchanges blob cce17b0044ebbf3ae972af6cb6e5276f63367ef4とledger blob c53bbf3f6b5d7f2ce044746a56e052151835fca7から、追記27件と対象3問の判断を回収。基点7cd8470の旧3290件が完全な接頭辞であること、復元changesのGit blob SHA一致を検査し、他問の判断は変更していない。初期review/applyを再実行せず、安全な累積再構成と台帳生成を使用した。

実施機関公式本文を新たに取得し直し、全4肢・全4解説を再照合。JLPTの認定自体の無期限と提出先の期限を区別し、得点変動ゼロの絶対化を撤回。EJUの3領域とアカデミック・ジャパニーズ表記を確認し、読解等の尺度得点と記述の採点基準方式を区別。EJU全科目の一律受験という含意を避け、BJTの非合否・スコア/6段階とOPIの口頭面接の発話証拠を確認。OPIの妥当性信頼性原著群は未検証。

v8不変、500問、キー・タグ・早見表・リンク整合、公開判定回帰8条件・置換回帰4条件が通過。機械警告117→118件。新規P1はQ_1_008正答解説末尾の全科目受験を否定する注意書きによる誤検出と独立判定し、限定を消して警告数だけを下げていない。

Noto Sans JPを復旧し408頁を新規描画。27文字列全件を検出し、8・19・205・216・217頁の1800px画像を直接再確認。欠字・重なりなし、3問の各設問/4肢と各4解説はそれぞれ頁内に収まる。全頁最終QAは未了、最終版ではなく出版不可。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。
'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第165バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第165バッチ 公式試験本文 2026-10-18\n\n'+''.join(f'- {sid} [{fn}]({url})：{scope}\n' for sid,fn,url,scope in specs)+'\n原バイトSHA256と再取得範囲はevidence/batch165_sources.json。原文全体非転載。\n')
f=p/'README.md';f.write_text(f.read_text().replace('389問','392問').replace('109問','106問').replace('384問3290箇所','387問3317箇所').replace('384問を部分修正','387問を部分修正'))
e=dict(batch=165,base_remote_commit='7cd8470586e2f5b07408e49c0b67bef6a611a47e',fully_rejudged=sorted(targets),edits=27,independent_answers={'Q_1_034':4,'Q_1_035':2,'Q_1_008':1},status_counts=m['status_counts'],remaining=108,machine_warnings=118,new_warnings=warnings,render_pages=len(PdfReader(r/'qa.pdf').pages),visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansJP.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch165_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
