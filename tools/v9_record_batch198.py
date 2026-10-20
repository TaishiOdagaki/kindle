"""Record recovered batch198 after fresh render and direct affected-page review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa198_recovered');BASE='5c4071d924adf7745ee58a5589cafb15731dc221'
keys={'Q_O_015':2,'Q_M_029':1,'Q_M_009':1,'Q_1_015':3};holds={'Q_2_002','Q_4_076'}
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
changed=set(keys)|holds
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[n].replace('\r\n','\n') if n in changed else raw for n,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':498,'修正必要':0,'要追加確認':2} and not m['release_ready'] and not m['academic_audit_complete']
cs=json.loads((p/'changes_batch198.json').read_text());assert len(cs)==36 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}==changed
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches198.json').read_text());assert len(matches)==36 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert added==[['P1','Q_O_015','(正)2の解説が否定で終わる/肯定の(誤)がある: [1, 4]']] and not removed
specs=[
('S04','文化審議会 敬語の指針 2007年2月2日','https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93927001_09.pdf','bunka198-keigo.pdf','全82頁原PDF再取得。印刷9～12頁の手引と敬語教育を精読、10・11頁の画像確認。ケース整合として43～44頁の本文も照合。知識・複数表現の選択・経験と意図的学習の両立に限定。即時訂正・教育効果の普遍性を承認しない。'),
('S297','British Council Interactive Whiteboard IWB','https://www.teachingenglish.org.uk/professional-development/teachers/teaching-knowledge-database/d-h/interactive-whiteboard-iwb','bc198-iwb.html','機器説明、Example、In the classroomの全本文をHTML原バイトとWeb本文で取得・精読。コメントは除外。学習者操作と発音・発表・授業進行の例に限定。全製品仕様や機器導入の自動的効果としない。'),
('S298','Trudgill 1972 Sex covert prestige and linguistic change in the urban British English of Norwich','https://web.stanford.edu/~eckert/PDF/trudgill1972.pdf','trudgill198.pdf','全9PDF頁（原著179～195頁見開き）を大学研究者公開ページから取得。原著186～189頁/PDF5～6頁の原画像精読。過少申告・表立たない好意・連帯・非標準形の潜在的威信を全肢全解説照合。全社会・全男女の普遍的傾向へ一般化しない。'),
('S299','総務省 地域における多文化共生推進プラン 2020年改訂','https://www.soumu.go.jp/main_content/000706218.pdf','soumu198-plan.pdf','全23頁公式PDF取得。1～7頁本文と7頁原画像精読、3（1）①ア・ウとICT時の理解への配慮を全肢全解説に照合。2020年版の方針であり最新全制度・実現済みサービスとしない。改訂年はMEXT掲載総務省説明資料の本文5頁でも確認済み。')]
sources=[]
for sid,title,url,name,scope in specs:
 f=Path('..')/name;assert f.stat().st_size>10000;sources.append(dict(source_id=sid,title=title,url=url,retrieved='2026-10-20',sha256=sha(f),bytes=f.stat().st_size,body_read=scope,full_source_redistributed=False))
(p/'evidence/batch198_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
report=f'''\n\n## 第198バッチ 2026-10-20\n\nQ_O_015・Q_M_029・Q_M_009・Q_1_015の設問・全4肢・全4解説を36件改訂。S04公式答申、S297公式教材解説、S298原著、S299公式プラン本文に照合。独立正答2・1・1・3、キー変更なし。累積493問4296件、全500問維持。確認済み498・修正必要0・要追加確認2。\n\n待遇表現指導では形式の知識と場面ごとの複数表現選択・実践を組み合わせ、発話意欲への配慮や遅延訂正を一律に誤りとする曖昧な肢を除去。デジタル教材は即時応答を双方向性の必要条件とせず、学習者自身のIWB操作・発音活動・発表の具体例へ同領域差替え。威信は規範性だけへの限定を除き、原著が示す非標準形の潜在的威信へ改訂。政策は総務省2020年プランに限定し、多言語化・やさしい日本語・地域実情・NPO等連携・ICT時の理解への配慮を照合。参政権等の未照合の法的補助主張は除去。\n\n根拠資格の点検でQ_2_002（S285 Foley1988章導入要約）とQ_4_076（S279 Schachter1974著者要旨）を要追加確認に再開。要約・抄録を問う形へ範囲を狭めても、原著本文を取得・照合せず最終採用しないというユーザー基準は未充足。旧判定の前後をevidence/batch198_source_holds.jsonに保存。FoleyのPDF形式URLの応答実体はHTML、Schachter出版社PDFは403、ERIC ED105750はRichards1975の別論文であるため、いずれも該当原著取得に数えない。両問の原著本文照合または同領域で本文取得できる資料への改訂が次の学術残件。\n\n再構成で全500問・キー/正誤タグ・改訂外本文・v8ハッシュ不変を確認。readiness8・replacement4・block-context回帰通過。機械警告{len(machine['issues'])}件。追加P1はQ_O_015の正答解説が効果保証を否定する留保、誤答1・4の解説が肯定的根拠で反証するための文末極性警告。キー・タグ不整合ではないと本文照合し、警告は隠さず残す。完全版CJKと非CJK代替フォントの全文収録を検査し{count}頁新規描画、36文字列全件検出、影響{pages}頁を直接画像確認。最終改頁調整・全頁QA・全警告処置・前付け/ケース/索引/リンク等の横断点検は未完了。台帳原文はv8スナップショット、改訂後はchangesと作業稿参照。最終v9ではなく出版不可。\n\n一時作業場のロールバック後、GitHub正本5c4071dから再構成した。保存済み第197バッチは保持。未保存だった原稿案を回復し、原資料を再取得、今回の新しい描画のみを確認に使用した。\n'''
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第198バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第198バッチ S04 S297 S298 S299\n\n'+'\n\n'.join(f'[{sid} {title}]({url})。{scope}' for sid,title,url,name,scope in specs)+'\n\nS279・S285は原著本文未取得のため該当2問を再開。取得URL・SHA256・サイズ・精読範囲はevidence/batch198_sources.json。原資料全体は転載しない。\n')
f=p/'README.md';f.write_text(f.read_text().replace('496問','498問').replace('要追加確認 | 4問','要追加確認 | 2問').replace('要追加確認4問','要追加確認2問').replace('489問4260箇所','493問4296箇所').replace('489問を部分修正','493問を部分修正').replace('第197バッチの最新描画は351頁',f'第198バッチの最新描画は{count}頁')+'\n第198バッチの学術残件はQ_2_002・Q_4_076。抄録・導入要約のみの旧承認を再開し、原著本文照合または同領域改訂を待つ。\n')
e=dict(batch=198,base_remote_commit=BASE,fully_rejudged=list(keys),source_holds_reopened=sorted(holds),edits=36,independent_answers=keys,status_counts=m['status_counts'],remaining=2,machine_warnings=len(machine['issues']),added_warnings=added,removed_warnings=removed,render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch198_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
e['image_retry']={str(n):{'file':f'retry-{n}.jpg','sha256':sha(r/f'retry-{n}.jpg'),'reason':'PNG表示エラーまたは正誤ラベルの表示欠落を同じPDFからJPEG再描画して再確認'} for n in [179,324,330]}
e['layout_pending']=['Q_O_015の設問・選択肢が119～120頁で分断','Q_M_009の解説が323～324頁で分断。最終改頁調整が必要']
(p/'evidence/batch198_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
