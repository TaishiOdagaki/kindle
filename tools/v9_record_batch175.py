"""Checkpoint three source-bounded replacement questions."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa175';keys={'Q_1_013':3,'Q_4_097':1,'Q_4_102':3}
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in keys else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':410,'修正必要':1,'要追加確認':89} and not m['release_ready']
cs=json.loads((p/'changes_batch175.json').read_text());assert len(cs)==27 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches175.json').read_text());assert len(matches)==27 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==130 and len(warnings)==3 and {x[1] for x in warnings}==set(keys) and all(x[0]=='P1' for x in warnings)
assert all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第175バッチ 2026-10-19

Q_1_013・Q_4_097・Q_4_102を各9件、計27件改訂。独立正答3・1・3、キー変更なし。確認済み410・修正必要1・要追加確認89、残90問。累積404問3480件、500問を維持。

Q_1_013は、既に暫定修正されていた1号／2号・ポイント制・親帯同・配偶者就労・永住の詳細を、本文未取得のまま承認することを避けた。出入国在留管理庁のQ&Aと優遇措置ページは本文403。検索に表示されたQ&Aの抜粋を本文取得に数えず、ブラウザによる迂回も行っていない。S236外務省の2026-01-22付高度専門職査証案内の本文・表・注1/2を原HTMLで取得し、同じ高度専門職領域の査証手続へ差替えた。5年、在留資格認定証明書の提示、電子証明書・写し、国籍ごとの必要書類、家族等の申請を全肢解説へ対応。旧残存主張の全てを確認できたという意味での修正必要解消ではなく、根拠のある同領域の問題への置換である。高度専門職2号やポイント全項目、年収・永住要件等の詳細は今回の承認対象から除外。

Q_4_097・102はS237 Weldon・Carlston・Rissman・Slobodin・Triandisの1974年技術報告書No.20をERICから43頁PDFとして取得。表紙、Triandisの序、本文1～6・25・32頁を精読し本文3頁の画像を確認。対立事例、行動原因の解釈選択、分岐フィードバック、両集団のパネルの反応による訓練目的上の正解選定を照合した。教材上の解釈と、国籍で全ての個人の行動原因を確定することを区別。「効率的に理解」「客観的に正しく理解」という無条件の効果・唯一原因の含みを撤回。1971原著や1970技術報告の取得とは区別し、旧1970報告PDFは404として記録。全ての訓練形式や行動効果をこの報告で実証したとは扱わない。

v8原本不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外の問題不変を再検査。公開判定回帰8条件と置換回帰4条件が通過。機械警告127→130件。新規P1の3件は、正答解説が適用範囲・普遍効果を否定して終わり、誤肢解説が正しい記載を示すための誤検出。既存127件は保持。台帳原文はv8スナップショット、改訂後本文はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifの収録検査後、{pagecount}頁を新規描画。27文字列全件を検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。問題・解説の頁またぎの調整と全頁最終QA、残90問は未了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第175バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第175バッチ S236 S237 2026-10-19

- S236 [外務省 高度専門職査証案内](https://www.mofa.go.jp/mofaj/toko/visa/chouki/visa16.html)。2026-01-22付の表・注1/2本文全体。滞在期間5年、在留資格認定証明書の提示と原本・写し・電子証明書、国籍による追加、家族等への認定証明書。Q_1_013を同じ高度専門職領域の査証手続へ差替え、全肢全解説へ対応。2号国内手続、ポイント項目、親帯同・配偶者就労・永住等の詳細は今回の照合外。ISA本文2ページは403。
- S237 [Weldon et al.1974 Technical Report20](https://files.eric.ed.gov/fulltext/ED095249.pdf)。A Laboratory Test of the Effects of Culture Assimilator Training、1974年3月、Illinois大学研究者の原報告43頁PDF。表紙・Triandis序、本文1～6・25・32頁、本文3頁画像。事例・解釈選択・分岐フィードバックと両集団パネルによる訓練目的上の正解選定をQ_4_097・102へ対応。1971原著・1970原報告本文や全実験の再検証ではない。

原バイトSHA256と精読範囲はevidence/batch175_sources.json。未取得はbatch175_source_attempts.json。原資料全体非転載。
''')
f=p/'README.md';t=f.read_text().replace('407問','410問').replace('| 修正必要 | 2問 |','| 修正必要 | 1問 |').replace('修正必要2問','修正必要1問').replace('91問','89問').replace('402問3453箇所','404問3480箇所').replace('402問を部分修正','404問を部分修正').replace('第174バッチの最新描画は353頁',f'第175バッチの最新描画は{pagecount}頁');f.write_text(t)
e=dict(batch=175,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=27,independent_answers=keys,sources=['S236','S237'],status_counts=m['status_counts'],remaining=90,machine_warnings=130,new_warnings=warnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch175_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
