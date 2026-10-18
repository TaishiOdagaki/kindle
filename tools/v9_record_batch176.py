"""Checkpoint institutional language-policy source comparisons."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa176';keys={'Q_2_010':3,'Q_2_012':1}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':412,'修正必要':1,'要追加確認':87} and not m['release_ready']
cs=json.loads((p/'changes_batch176.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches176.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==131 and len(warnings)==1 and warnings[0][0]=='P1' and warnings[0][1]=='Q_2_010' and all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第176バッチ 2026-10-19

Q_2_010・012の設問・各4肢・各4解説を18件改訂、独立正答3・1、キー変更なし。確認済み412・修正必要1・要追加確認87、残88問。累積406問3498件、500問維持。

S238国立国語研究所「外来語」委員会の2006年総集編の概要・利用の手引き全節・インフォームドコンセントの項目全体を原HTMLで取得して精読。提案主体・日付、受け手への配慮、文脈に応じた使い分け、日本語の外来語と原語の範囲の違い、専門語と正確な説明の併用を照合。「納得診療」だけでなく「説明と同意」と意味説明があることを確認。一語への機械的な置換に還元しない。旧稿の公用文・法令のルビや仮名遣い、やさしい日本語の多様な受け手に対する効果は別の主張であり、この提案本文だけで一括承認せず、本問は2006年提案の利用へ限定。資料当時の理解度の星印や数値を現在の理解度とは扱わず、医療の法的要件を検証したとはしない。

S239文化庁の危機言語の説明本文、掲載8言語・危機度一覧、言語／方言の呼称の注記、被災地方言への言及と事業一覧を取得精読。Q_2_010の「指定」を「掲載」へ修正し、文化庁が紹介する2009年発表資料の説明へ時点を限定した。8言語だけが日本国内の危機的なことばであるとはしない。旧稿の共通語普及やメディア全国化を継承断絶の主因と断定する説明は今回の本文で確証できず撤回。UNESCO Atlas原本文や最新話者数、各言語の現在の危機度を独立に再確認したとは扱わない。

v8不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外問題の不変を再検査。公開判定回帰8条件・置換回帰4条件通過。機械警告130→131件。新規P1は、正答解説が8言語への網羅性を否定して終わることによる誤検出。既存130件は保持。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifの収録検査後に{pagecount}頁を新規描画。18文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。問題や解説の頁またぎの調整、全頁最終QA、残88問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第176バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第176バッチ S238 S239 2026-10-19

- S238 国立国語研究所「外来語」委員会の[2006年総集編概要](https://www2.ninjal.ac.jp/gairaigo/Teian1_4/index.html)、[利用の手引き全節](https://www2.ninjal.ac.jp/gairaigo/Teian1_4/tebiki.html)、[インフォームドコンセント項目全体](https://www2.ninjal.ac.jp/gairaigo/Teian1_4/Words/informed_consent.gen.html)のHTML原文を取得。受け手・文脈別の言い換えと説明、原語との区別、納得診療／説明と同意をQ_2_012の全肢・全解説へ対応。資料当時の理解度を現在値としない。医療の法的要件・別の公用文政策の承認ではない。
- S239 [文化庁 消滅の危機にある言語・方言](https://www.bunka.go.jp/seisaku/kokugo_nihongo/kokugo_shisaku/kikigengo/)の本文・8言語と危機度一覧・注記・事業一覧を取得精読。文化庁が紹介する2009年発表資料の掲載をQ_2_010の全肢全解説へ対応。UNESCO Atlas原本文・最新話者数・全危機言語を独立検証したとはしない。

原バイトSHA256と範囲はevidence/batch176_sources.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('410問','412問').replace('89問','87問').replace('404問3480箇所','406問3498箇所').replace('404問を部分修正','406問を部分修正').replace('第175バッチの最新描画は353頁',f'第176バッチの最新描画は{pagecount}頁'))
e=dict(batch=176,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S238','S239'],status_counts=m['status_counts'],remaining=88,machine_warnings=131,new_warnings=warnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch176_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
