"""Record batch188 after direct changed-page image review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa188');BASE='4fc1ee39fb3edee3c072369b320c8cae603f464e';keys={'Q_2_001':4,'Q_2_005':2,'Q_2_006':4,'Q_M_051':2}
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
def old(n):return subprocess.check_output(['git','show',BASE+':audit/v9/'+n])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[n].replace('\r\n','\n') if n in keys else raw for n,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':451,'修正必要':0,'要追加確認':49} and not m['release_ready']
cs=json.loads((p/'changes_batch188.json').read_text());assert len(cs)==36 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches188.json').read_text());assert len(matches)==36 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert not added and not removed and len(machine['issues'])==140
specs=[('S256','国語研 擬音語・擬態語にはどんな種類がある','https://www2.ninjal.ac.jp/Onomatope/column/nihongo_1.html','ninjal188-1.html','本文全体・5分類・全例・参考文献。金田一1978を紹介する公的教材として利用し原著1978全文取得とは区別。複数意味分類と文脈条件に限定。'),('S257','三井はるみ 方言というのはどのようなことばのことですか','https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-137/','ninjal188-definition.html','2021-07-13掲載、2003初出の修正版。本文全3節と留保・参考文献。ことば全体・東京方言・共通語との正誤関係・地域内の多様性。現在の全地域の使用率や原著全冊の検証ではない。'),('S258','小椋秀樹 方言には古語が残っているというのは本当ですか','https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-151/','ninjal188-archaic.html','2022-06-27掲載、2003初出修正版。本文全2節・図説明と柳田の著作への言及。周圏論という説明の条件と新旧の方向、古語残存に限定。柳田蝸牛考全文・引用史料全体は未取得。'),('S259','三井はるみ 日本語にはどうしていろいろな方言があるのですか','https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-190/','ninjal188-origin.html','2022-08-24掲載、2001初出修正版。本文全体・伝播と独自変化の二要因・複合要因・言語成立未定説の留保、図説明と参考文献。各地図の現物再解析や現行全話者の分布の確認ではない。')]
sources=[]
for sid,title,url,name,scope in specs:
 f=Path('..')/name;assert f.stat().st_size>7000
 sources.append(dict(source_id=sid,title=title,url=url,retrieved='2026-10-20',sha256=sha(f),bytes=f.stat().st_size,body_read=scope,method='公的HTML原バイト直接取得とWeb open全本文の対応を確認・精読',full_source_redistributed=False))
(p/'evidence/batch188_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch188_source_attempts.json').write_text(json.dumps([dict(url='https://spssi.onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-4560.1963.tb00447.x',result='通常直接取得HTTP403。Gullahorn1963原論文本文未取得、検索情報だけでWカーブ3問を承認せず今回の対象外。'),dict(result='Canale Swain1980は書誌とPDF候補を検索した段階。原著本文未取得、Q_2_018は要追加確認を維持。'),dict(result='オノマトペの方言記事qa236も本文取得したが本バッチ4問の承認根拠には不使用。LibreOfficeコピーの所有者保持警告が出たが実行ファイル・同梱フォントの存在と実際の新規描画成功を確認。')],ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
text=f'''\n\n## 第188バッチ 2026-10-20\n\nQ_2_001・005・006・Q_M_051を同じ地域方言・言語変異・オノマトペ領域で36件改訂。国語研公式教材・専門家解説4本文を取得し全肢全解説へ照合、独立正答4・2・4・2、キー変更なし。確認済み451・修正必要0・要追加確認49、500問維持、累積444問3849件。\n\n方言を独特な単語だけにせず地域のことば全体も扱い、東京方言と共通語の正誤関係を整理。地域内の年齢・場面・出身地の多様性に限定し、女性語成立史・役割語・隠語とレジスターの一括りの未照合主張を撤回。方言周圏論の伝播説明と各地の独自変化を区別し、旧稿のアクセント地域の分類と西日本全体での相の厳密区別、雨の例の一般化を撤回。オノマトペは文脈による複数意味分類に絞り、他言語との数量比較や豊富・生き生きという評価を承認しない。S256は金田一1978の分類を紹介する公的教材で、金田一原著全文の取得ではない。柳田原著・関連論文全体や現在の全地域分布を確認したとはしない。\n\n全500問の構造・改訂外本文・v8ハッシュ不変、安全再構成と公開判定8条件・置換4条件・block-context回帰通過。機械警告140件増減なし。完全版Noto Sans CJK JPの既知ハッシュと全文CJK・代替フォント収録を検査し{count}頁を新規描画。36改訂文字列を全件検出し、影響{pages}頁の1800px画像を直接確認、改訂箇所の欠字・重なり・切れなし。残49問・最終改頁調整と全頁最終QAは未完了。台帳原文はv8スナップショット、改訂後はchangesと作業稿参照。作業稿は出版不可。\n'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第188バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第188バッチ S256 S257 S258 S259\n\n'+'\n\n'.join(f'[{sid} {title}]({url})。{scope}' for sid,title,url,name,scope in specs)+'\n\n原HTML本文全体非転載。原バイトハッシュ・サイズ・精読範囲はevidence/batch188_sources.json、未取得はbatch188_source_attempts.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('447問','451問').replace('53問','49問').replace('440問3813箇所','444問3849箇所').replace('440問を部分修正','444問を部分修正').replace('第187バッチの最新描画は355頁',f'第188バッチの最新描画は{count}頁'))
assert sha(Path('../NotoSansCJKjp-VF.ttf'))=='240c9b83bf7b386edbae39995ae7e068ed4583f484d92e4a74c34158b5f27b1a'
e=dict(batch=188,base_remote_commit=BASE,fully_rejudged=list(keys),edits=36,independent_answers=keys,sources=[s[0] for s in specs],status_counts=m['status_counts'],remaining=49,machine_warnings=140,added_warnings=added,removed_warnings=removed,regressions='readiness8; replacement4; block-context',render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch188_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
