"""Record body-based minority education and regulators audit."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa197');BASE='7fb429ba646d16242f68408a1adb09acafd02055';keys={'Q_2_034':3,'Q_2_030':4}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':496,'修正必要':0,'要追加確認':4} and not m['release_ready']
cs=json.loads((p/'changes_batch197.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches197.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert added==[['P1','Q_2_034','(正)3の解説が否定で終わる/肯定の(誤)がある: [2]']]
specs=[('S295','OHCHR Minority Rights 附属1992年少数者権利宣言','https://www.ohchr.org/Documents/Publications/MinorityRights_en.pdf','ohchr195-minority.pdf','宣言全前文・全9条（印刷45～48頁/PDF51～54頁）を精読。第4条第3・4項を全肢全解説に照合。PDF52～54頁画像も直接確認。母語教育の可能な限りという条件、少数者の歴史等と社会全体を知る機会を区別。規範と教育効果の実証を区別。Web openは403だが公式PDF原バイトは取得。'),('S296','Ekman & Friesen 1969 The Repertoire of Nonverbal Behavior','https://www.paulekman.com/wp-content/uploads/2013/07/The-Repertoire-Of-Nonverbal-Behavior-Categories-Origins-.pdf','ekman196.pdf','著者公式サイトの全51頁PDFを取得。Regulators節の印刷82～84頁/PDF35～37頁の原画像を直接精読。37頁PNGはツール読込不可のため同PDFからJPEG再描画して確認。会話の流れと進み方、形と機能、他分類の調節機能、意識性の区別を全肢全解説へ照合。著者は調節行動について自ら研究を実施していないと記すため、説明を新しい実証研究結果として扱わない。')]
sources=[]
for sid,title,url,name,scope in specs:
 f=Path('..')/name;sources.append(dict(source_id=sid,title=title,url=url,retrieved='2026-10-20',sha256=sha(f),bytes=f.stat().st_size,pdf_pages=len(PdfReader(f).pages),body_read=scope,method='原バイト取得、該当本文精読、原頁画像直接確認',full_source_redistributed=False))
(p/'evidence/batch197_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
layout='Q_2_034の選択肢が29～30頁に分かれ、Q_2_030解説の見出しと正答が198頁末に孤立するため最終改頁調整対象。200頁PNGの画像ツール表示で一部ラベルが欠けて見えたため、同じ最新PDFをJPEG再描画し、全ラベル・見出し・正答が正常に見えることを直接確認。198頁もJPEGで追加確認。'
text=f'''\n\n## 第197バッチ 2026-10-20\n\nQ_2_030・034の設問・全4肢・全4解説を18件改訂。S295国連宣言全文とS296著者サイトの原著を直接取得し、該当本文と原頁画像を精読。独立正答4・3、キー変更なし。確認済み496・修正必要0・要追加確認4、全500問維持、累積489問4260件。\n\nQ_2_034は母語教育機会の「可能な限り」と社会全体を知る機会を区別。相互依存仮説を実証された普遍法則とする旧解説を撤回し、同じ少数言語保持・教育機会の領域で宣言明文へ差替え。Q_2_030はうなずき等を形だけで固定分類せず、会話の流れを調節する機能と分類名を区別。必ず意識的な行為との誤解も排除。原著の提案を独自の実証研究結果とはしない。\n\n最新GitHubが作業中にaf72413から7fb429bへ進んだため、旧ローカル第195案・第196案はブランチへ適用せず保留。既に確認されたQ_2_009・Q_M_007の判定を上書きせず、なお未確認だった2問だけを最新稿から新規改訂した。安全再構成で全500問・改訂外本文・v8ハッシュ不変を確認。readiness8・replacement4・block-context回帰は本実行で通過済み。機械警告{len(machine['issues'])}件、追加{len(added)}・解消{len(removed)}。追加P1はQ_2_034の正答解説末尾が普遍的実証という過剰解釈を否定し、誤答解説が実在する措置を肯定して反証するためで、キー・タグ不整合ではない。警告は隠さず記録。\n\n完全版Noto Sans CJK JP・代替フォントの全文収録検査後、{count}頁を新規描画。18文字列全件検出、影響{pages}頁を1800px画像で直接確認し、改訂部分の欠字・重なり・切れなし。最終改頁調整・全頁最終QAは未完了。台帳原文はv8スナップショット、改訂後はchangesと作業稿参照。最終v9ではなく出版不可。\n'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第197バッチ' not in f.read_text();f.write_text(f.read_text()+text+'\n改頁・画像QAの留保：'+layout+'\n')
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第197バッチ S295 S296\n\n'+'\n\n'.join(f'[{sid} {title}]({url})。{scope}' for sid,title,url,name,scope in specs)+'\n\n取得URL・原バイトSHA256・サイズ・精読範囲はevidence/batch197_sources.json。原資料全体は転載しない。\n')
f=p/'README.md';f.write_text(f.read_text().replace('494問','496問').replace('要追加確認 | 6問','要追加確認 | 4問').replace('要追加確認6問','要追加確認4問').replace('487問4242箇所','489問4260箇所').replace('487問を部分修正','489問を部分修正').replace('第190バッチの最新描画は354頁',f'第197バッチの最新描画は{count}頁'))
e=dict(batch=197,base_remote_commit=BASE,fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S295','S296'],status_counts=m['status_counts'],remaining=4,machine_warnings=len(machine['issues']),added_warnings=added,removed_warnings=removed,render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
e['layout_and_image_note']=layout
e['additional_reviewed_images']={str(n):sha(r/f'retry-{n}.jpg') for n in [198,200]}
(p/'evidence/batch197_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
