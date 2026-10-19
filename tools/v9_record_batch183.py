"""Record batch183 after source reading and direct review of all affected pages."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa183'
keys={'Q_1_020':2,'Q_1_022':4,'Q_M_006':1,'Q_M_008':2,'Q_M_037':2}
BASE='c3c681e2eddf4ffa5ea0853af0962fecf4d6d1c2'
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
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in keys else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':438,'修正必要':0,'要追加確認':62} and not m['release_ready']
cs=json.loads((p/'changes_batch183.json').read_text());assert len(cs)==45 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches183.json').read_text());assert len(matches)==45 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns});assert pages==[11,12,144,145,152,153,184,185,327,328,337]
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in pre['issues']];removed=[x for x in pre['issues'] if x not in machine['issues']]
assert len(machine['issues'])==139 and len(added)==1 and added[0][:2]==['P1','Q_1_022'] and not removed
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
source_specs=[
 ('S246','文部科学省 日本語教育コンテンツ共有システム 生活Can do説明本文','https://www.nihongo-ews.mext.go.jp/information/framework_of_reference','ews183.html','生活Can do節全文。日本語教育の参照枠の説明節との関係も確認。'),
 ('S246','生活Can doについて 説明資料','https://www.nihongo-ews.mext.go.jp/information/download/370','cando183.pdf','全3頁の本文と全頁画像。定義、分野別Can do、検証手順、利用時留意事項。'),
 ('S247','文化審議会国語分科会 地域における日本語教育の在り方について 報告 2022-11-29','https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93798801_01.pdf','region183-full.pdf','全114頁PDFを取得。印刷35・58～62頁（PDF38・61～65頁）の本文と全該当画像を精読。標題の年月日を確認。全114頁精読ではない。'),
 ('S248','静岡県 地域日本語教育体制構築事業トップページ','https://www.pref.shizuoka.jp/kurashikankyo/1049844/tabunkachiiki/1044858/1015564.html','shizuoka183.html','本文全文。更新日2025-09-05。対話交流型の定義、双方の学び、初期教室の設置運営。R2～R6旧方針とR7以降の方針を区別。')]
sources=[dict(source_id=s,title=t,url=u,checked='2026-10-19',bytes=(root/f).stat().st_size,sha256=sha(root/f),body_read=scope,full_source_redistributed=False) for s,t,u,f,scope in source_specs]
assert len(PdfReader(root/'region183-full.pdf').pages)==114 and (root/'region183-full.pdf').stat().st_size==11480319
assert len(PdfReader(root/'cando183.pdf').pages)==3
(p/'evidence/batch183_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch183_source_attempts.json').write_text(json.dumps([
 dict(url=source_specs[2][2],result='Web openは11480319バイトでサイズ上限。通常直接取得の初回40秒制限で部分ファイルとなり、再開ファイルは11672831バイトでPDF構造不正。いずれも本文承認や画像QAに使わず、新しい別ファイルへ最初から通常取得。11480319バイト・114頁・本文抽出成功と該当頁画像を確認。'),
 dict(url='https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/94029601_01.pdf',result='文化庁案内ページの旧別冊リンクは404。別冊全文・現行全Can do一覧は未取得で承認根拠に使わず、公式説明本文・3頁資料と2022報告の指定範囲を用いた。'),
 dict(url=source_specs[0][2],result='検索システム1の結果が不適合だったため引用せず、システム2で公式ページを特定し本文を取得。検索抜粋では判定していない。')],ensure_ascii=False,indent=2)+'\n')
text='''

## 第183バッチ 2026-10-19

Q_1_020・Q_1_022・Q_M_006・Q_M_008・Q_M_037の設問・各4肢・各4解説を45件改訂。独立正答2・4・1・2・2、キー変更なし。確認済み438・修正必要0・要追加確認62、残62問。累積431問3732件、全500問を維持。

S246文科省EWSの生活Can do説明本文と説明PDF3頁を取得し全3頁画像を精読。生活Can doは生活分野の言語活動の例示であり、全員が日本語で必ず達成すべき行為の網羅的一覧ではない。学習者の状況に応じた選択、新たな現場Can doの作成、安全や生命に関わる場合の多言語情報、他の学びや振り返りとの組合せを全肢全解説に反映。旧稿の評価指標だけという還元、直接の開発根拠をJF標準とする未照合の説明、未照合のゴミ・役所例を撤回。尺度の質的・量的検証を、全授業・全対象者の効果保証とはしない。旧別冊リンク404は取得できたことにせず、現行全Can do一覧の項目数・各尺度の完全監査は行っていない。

S247文化審議会国語分科会2022年11月29日報告114頁を通常取得。サイズ超過でWeb取得できなかった資料を、直接取得で確保した。途中ファイル・再開後の構造不正ファイルは採用せず、新規ファイル11480319バイトの完全PDFを検証。印刷35・58～62頁（PDF38・61～65頁）の本文と全該当頁画像を精読。全114頁を精読したとはしない。生活者の中に留学生・就労者も含まれるとの明記とニーズに応じた内容検討を確認。Q_M_006は改定後の目的・目標を問う問題、Q_M_008は生活者・留学・就労を互いに重ならない区分としない問題へ改訂。法的な在留資格や現在の在留要件をこの報告だけで承認しない。

Q_M_037は同じ高齢学習者支援の領域で文字指導の背景配慮を問う内容へ限定。59頁の習得段階の個人差、62頁の漢字圏・非漢字圏、識字、高齢者などの背景と言語間距離、内容・方法・進度・クラス分けの検討に対応。見やすさや生活経験の利用による学習意欲・理解の効果については個別の原典を取得しておらず、今回承認せず撤回。旧稿に感覚・記憶機能低下の明示はなく、そのような誤りを指摘したものではない。年齢だけで能力を断定せず、医学的な年齢効果の実証とも区別した。

S248静岡県公式ページ全文を取得。更新2025年9月5日、確認2026年10月19日。Q_1_022は対話型全般の万能な定義から、県が説明する対話交流型の特徴へ範囲を明示。対等な交流と双方の学び、初期日本語教室での採用を照合。講義型一般が生活定着に不向きとする評価、交流によるネットワーク・ソーシャルキャピタル形成の効果保証、未取得の初級支援方法の具体例は撤回。県の事業の特徴を全地域の実態へ一般化しない。

全500問、v8不変、正答番号・正誤タグ・早見表・リンク・改訂外問題不変を機械検査。公開判定8条件・置換回帰4条件・block-context回帰通過。警告138→139件、新規P1はQ_1_022正答解説末尾の「効果が必ず生じることを保証する記述ではありません」という限定による誤検出。全肢・解説・タグと資料本文を再照合し、キー不整合ではないことを確認。既存138件は保持。台帳の原文はv8スナップショットであり、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPの既知SHA256一致を確認。CJK1448文字欠落0、非CJKの同梱Noto Serif収録も検査し、355頁を新規描画。45改訂文字列を全件検出。'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認し、改訂箇所に欠字・重なり・切れを認めず。153頁の初回PNG表示失敗は同じ最終PDFからpdftoppm JPEGで再描画し全文表示を確認、実際に確認した画像のSHA256を記録。設問・選択肢の頁またぎを含む最終改頁調整、全頁最終画像QAと残62問は未完了。作業稿は出版不可。\n'
assert pagecount==355
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第183バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第183バッチ S246 S247 S248 2026-10-19

S246 [文科省EWS生活Can do説明本文](https://www.nihongo-ews.mext.go.jp/information/framework_of_reference)と[説明資料3頁](https://www.nihongo-ews.mext.go.jp/information/download/370)。全説明・全3頁画像。例示・状況による選択・現場Can do・多言語情報・他の学びとの組合せ。Q_1_020全肢全解説を照合。尺度検証を授業効果の保証へ一般化しない。

S247 [文化審議会国語分科会 地域における日本語教育の在り方について 報告](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93798801_01.pdf)、2022年11月29日。114頁を取得、印刷35・58～62頁（PDF38・61～65頁）を本文・画像で精読。Q_M_006・008・037全肢全解説と目的・目標、対象の重なり、個人の習得段階・文字指導の背景配慮を照合。全書精読、在留要件、医学的年齢効果や特定方法の実証ではない。

S248 [静岡県 地域日本語教育体制構築事業](https://www.pref.shizuoka.jp/kurashikankyo/1049844/tabunkachiiki/1044858/1015564.html)。更新2025年9月5日、確認2026年10月19日、本文全文取得。Q_1_022全肢全解説と県の対話交流型の定義・双方の学習・初期教室の実施を照合。R2～R6旧方針とR7以降の方針を混同せず、全地域への一般化や効果実証には用いない。

資料のサイズ・SHA256・精読範囲はevidence/batch183_sources.json。サイズ超過、404、途中・不正PDFの不採用と完全な新規取得をbatch183_source_attempts.jsonへ記録。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('433問','438問').replace('67問','62問').replace('426問3687箇所','431問3732箇所').replace('426問を部分修正','431問を部分修正').replace('第182バッチの最新描画','第183バッチの最新描画'))
e=dict(batch=183,base_remote_commit=BASE,fully_rejudged=list(keys),edits=45,independent_answers=keys,sources=['S246','S247','S248'],status_counts=m['status_counts'],remaining=62,machine_warnings=139,added_warnings=added,removed_warnings=removed,regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/('retry-153.jpg' if n==153 else f'review-{n:03}.png')) for n in pages},image_retry='153頁の初回PNG表示エラー。pdftoppm JPEGで全字表示を直接確認。',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch183_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
