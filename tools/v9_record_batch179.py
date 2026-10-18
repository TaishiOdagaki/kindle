"""One-time checkpoint after direct inspection of changed page images."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa179';keys={'Q_4_034':4,'Q_O_051':1,'Q_2_032':3}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':419,'修正必要':1,'要追加確認':80} and not m['release_ready']
cs=json.loads((p/'changes_batch179.json').read_text());assert len(cs)==27 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches179.json').read_text());assert len(matches)==27 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));newwarnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==132 and len(newwarnings)==1 and newwarnings[0][:2]==['P1','Q_O_051'] and all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第179バッチ 2026-10-19

Q_4_034・Q_O_051・Q_2_032の設問・各4肢・各4解説を27件改訂。独立正答4・1・3、キー変更なし。確認済み419・修正必要1・要追加確認80、残81問。累積413問3561件、500問維持。

S242 Diane Larsen-Freeman・Marti Andersonの2011年第3版 Techniques and Principles in Language Teaching を大学公開PDFで取得。著者と奥付、直接法の導入・10原則・技法冒頭（PDF46・52～54頁）、ALM導入・10原則（59・70～72頁）を精読、52・53・59頁画像照合。直接法で数か月間文字を全面禁止するという誤答と、それをALM一般へ帰属する旧補助説明を区別し後者は撤回。直接法は口頭を基礎としつつ四技能を初めから扱うという同書の説明へ対応。Q_O_051はケースの手順からA教師本人の信念を断定せず、同書が述べるALMの構造主義と行動主義の関係・習慣形成・模倣反復・技能順序との比較へ限定。Skinner・Fries・Berlitz等の引用先原典、全教授法史、授業の習得効果を承認したものではない。電子的再組版318頁のPDF頁であり、印刷版頁を推定しない。全318頁精読ではない。

S243欧州評議会CEFR公式ページ Plurilingualism and pluriculturalism の概念説明3段落をWeb openで全体取得・精読し全肢全解説に照合。検索抜粋や文献抄録ではなく、発表機関自身の概念説明本文。個人の資源の全体性・相互関連・動的活用・部分的能力への価値づけと、多言語主義側の社会又は個人内の共存の説明を対応。旧稿の多言語主義を社会レベルだけとする単純化、別理論のトランスランゲージングの推奨を撤回。HTML原バイトとCEFR2020本体PDFの直接取得は403。迂回せず、原バイトSHA256なしと明記。CEFR2001/2020全原典取得や動画・リンク先論文の精読、各指導法の効果確認とは扱わない。

v8不変、500問、正答番号・正誤タグ・早見表・リンク・改訂外問題の不変を再検査。公開判定回帰8条件・置換回帰4条件通過。機械警告131→132件、新規P1はQ_O_051正答解説が教師の信念の断定を否定して終わることによる誤検出。全肢本文と正答タグの対応を再確認、既存131件は保持。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifの文字収録検査後に{pagecount}頁を新規描画。27文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QA・改頁調整・残81問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第179バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第179バッチ S242 S243 2026-10-19

- S242 [Larsen-Freeman Anderson2011年第3版原著書PDF](https://elearning.usm.md/pluginfile.php/190241/mod_resource/content/2/Larsen-freeman%203rd%20ed_techniques-in-language-teaching.pdf)。大学公開318頁電子再組版。著者・奥付、直接法PDF46・52～54頁、ALM59・70～72頁本文、52・53・59頁画像。Q_4_034・Q_O_051の全肢全解説。引用先原典・全318頁精読、教師本人の信念、授業効果の検証ではない。
- S243 [欧州評議会CEFR公式概念説明](https://www.coe.int/en/web/common-european-framework-reference-languages/plurilingualism-and-pluriculturalism)。Web openで概念説明本文3段落全体を取得・精読。Q_2_032の全肢全解説。HTML原バイト・CEFR2020本体PDFは直接取得403で未取得、本文取得と原バイト保存を区別。CEFR2001/2020の全原典・別のトランスランゲージング論文の承認ではない。

原PDFのSHA256・サイズ・精読範囲、HTML整形本文の取得方法はevidence/batch179_sources.json。403はbatch179_source_attempts.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('416問','419問').replace('83問','80問').replace('410問3534箇所','413問3561箇所').replace('410問を部分修正','413問を部分修正').replace('第178バッチの最新描画は353頁',f'第179バッチの最新描画は{pagecount}頁'))
e=dict(batch=179,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=27,independent_answers=keys,sources=['S242','S243'],status_counts=m['status_counts'],remaining=81,machine_warnings=132,new_warnings=newwarnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/(f'review{n}fresh.png' if n in [203,231,317] else f'review-{n:03}.png')) for n in pages},image_retry='203頁の初回画像表示が非対応データとして失敗。同じ最終PDFから203・231・317頁を新ファイル名で再描画し、3頁とも直接画像確認した。ハッシュは実際に確認した再描画画像。',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch179_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
