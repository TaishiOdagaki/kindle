"""Record batch181 only after fresh render and direct changed-page inspection."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa181b';keys={'Q_4_027':4,'Q_4_030':2,'Q_O_006':4,'Q_O_007':3}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':425,'修正必要':0,'要追加確認':75} and not m['release_ready']
cs=json.loads((p/'changes_batch181.json').read_text());assert len(cs)==36 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches181.json').read_text());assert len(matches)==36 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));newwarnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==135 and len(newwarnings)==1 and newwarnings[0][:2]==['P1','Q_4_030'] and all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第181バッチ 2026-10-19

Q_4_027・Q_4_030・Q_O_006・Q_O_007の設問・各4肢・各4解説を36件改訂。独立正答4・2・4・3、キー変更なし。確認済み425・修正必要0・要追加確認75、残75問。累積418問3615件、500問維持。未確認75問を確認済みとみなさない。

S197 Paul Nation What Should Every ESL Teacher Know? の出版社無料公開PDFを192頁取得。印刷/PDF12～15・23～25頁本文、12・13・14・25頁画像を精読。ケース2の本文も照合。第135バッチで取得した大学公開稿とはサイズ・原バイトSHA256が異なるため、同一バイトの再取得とはせず今回のハッシュ・精読範囲を記録。出版社商品ページの240p表示と現物192頁を区別し、ファイル名から刊年を推定しない。旧大学URL2種類は410、2000年論文リポジトリはWeb open403で、原典取得済みとしない。

ニーズ分析は現在の知識、必要となる知識、学びたいことを扱う。現稿の「ニーズ分析＝達成目標だけ、既習歴・時間等＝レディネス」という排他的分類を撤回。Q_O_006はケースの志望学部で必要となる知識技能に、Q_O_007は利用できる学習時間という環境要因にそれぞれ設問を限定し、既有知識をニーズから外さない。著者自身が環境分析をニーズ分析に含める場合もあると述べる点を踏まえ、同書で区別して説明される枠組みで問う。未取得Hutchinson/Waters1987のLack定義、主観／客観の単純な主体別区分は今回承認せず問題から撤回。

Q_4_027はテスト・課題・観察を含む資料と継続的分析を照合。Q_4_030は学習者の必要性・希望と、時間・資源等の実現条件を調べて途中でも見直す計画へ改訂。希望の無条件受入れではなく交渉・実現可能性を検討するという本文にも対応。特定シラバスの優越性、文法網羅による離脱の因果、国内の地域施策の規範をこのESL書から推測しない。原著書の指定範囲とケースへの応用であり、全192頁・引用先原典・授業効果の承認ではない。

v8不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外問題不変を再検査。公開判定回帰8条件・置換回帰4条件・block-context回帰通過。機械警告134→135件、新規P1はQ_4_030正答解説末尾の「常に最適だと保証する説明ではありません」という効果の限定による誤検出。全4肢・解説・タグと出典の対応を確認し、正答番号の誤りではないと記録。既存134件は保持。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。

描画前のフォント検査で残存NotoSansCJKjp-VF.ttfの破損を検出。14979072バイト・SHA256 9618497d8839d6fd23ba087804009d6bed2ae7787677561577516ae7d720aeeb、fontToolsのテーブル長検査で停止。失敗先qa181はQAに使用せず、公式notofontsから完全版36174296バイトを新規取得し、既知SHA256 240c9b83bf7b386edbae39995ae7e068ed4583f484d92e4a74c34158b5f27b1aとの一致を確認。新しいqa181bへ描画。部分フォント・破損フォントで画像確認済みとはしていない。
'''
text+=f'\n復旧した完全版と同梱Noto Serifの文字収録検査後に{pagecount}頁を新規描画。36改訂文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QA・改頁調整・残75問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第181バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第181バッチ S197出版社公開版 2026-10-19

[Paul Nation原著書 What Should Every ESL Teacher Know? 無料公開PDF](https://wjcompass.com/userfiles/downloads/20130213132738_DW11.pdf)、[出版社の商品説明](https://www.compasspub.com/eng/compass/level_view.asp?h_seq=1721)。現物192頁。印刷/PDF12～15・23～25頁本文、12・13・14・25頁画像。Q_4_027・Q_4_030・Q_O_006・Q_O_007の全肢全解説とケース2の必要性／利用時間の指定部分を照合。大学公開稿S197と同一著作だが原バイトハッシュ・サイズは異なり、出版社240p表示とも区別。既有知識もニーズの観点であること、環境要因、交渉・実現可能性、継続分析を確認。全書・引用先2000年論文、Hutchinson/Waters1987本文、国内施策、効果の検証ではない。

原資料サイズ・SHA256・範囲はevidence/batch181_sources.json。410・403・章要約しか得ていない資料はbatch181_source_attempts.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('421問','425問').replace('79問','75問').replace('414問3579箇所','418問3615箇所').replace('414問を部分修正','418問を部分修正').replace('第180バッチの最新描画は354頁',f'第181バッチの最新描画は{pagecount}頁'))
e=dict(batch=181,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=36,independent_answers=keys,sources=['S197'],status_counts=m['status_counts'],remaining=75,machine_warnings=135,new_warnings=newwarnings,regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-full181.ttf'),font_recovered=True,rejected_font_sha256='9618497d8839d6fd23ba087804009d6bed2ae7787677561577516ae7d720aeeb',page_sha256={str(n):sha(r/('review230ppm.png' if n==230 else f'review-{n:03}.png')) for n in pages},image_retry='230頁の初回画像表示に第2章の文字欠落の疑い。最終PDFからpdftoppmで再生成し、正常な全本文を直接確認。230頁は実際に確認した再生成画像のハッシュ。資料画像14頁も初回表示失敗後に再生成して確認。',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch181_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
