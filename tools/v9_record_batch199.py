"""Record batch199 after inspecting all affected pages of qa199."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa199');BASE='c9f5ec8580b0c2f543c2d2d7db2f32216e7c3bfe'
keys={'Q_2_002':2,'Q_4_076':1}
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
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[n].replace('\r\n','\n') if n in keys else raw for n,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':500,'修正必要':0,'要追加確認':0} and not m['release_ready'] and not m['full_visual_qa_completed']
cs=json.loads((p/'changes_batch199.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {n for n in d if d[n]!=d0[n]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches199.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert len(machine['issues'])==159 and len(added)==len(removed)==1 and added[0][1]==removed[0][1]=='Q_2_002'
specs=[('S300','真田信治 日本語とかかわるクレオールは存在しますか 国立国語研究所ことば研究館 2018年7月31日','https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-47/','ninjal199-creole.html','署名付き全記事本文を原HTMLとWeb取得で精読。研究者本人の調査報告を対象とし、接触・再編、台湾日本語との区別、子供・孫世代の担い手、日本語を上層とする報告を全肢全解説に照合。参考文献は未取得で承認根拠にしない。全クレオールの普遍的成立史や現在の話者数を問わない。'),('S149','Celce-Murcia Dörnyei Thurrell 1995 Communicative Competence A Pedagogically Motivated Model with Content Specifications','https://b9f19ceb-f720-4252-a2be-ccde56c0821f.filesusr.com/ugd/ba734f_1c905f1db74f488d924e158afdb63986.pdf?index=true','celce199.pdf','全16PDF頁を再取得。印刷26～29頁の全本文と表5原画像を直接精読。27頁の方略説明と28頁表5の四区分を全肢全解説に照合。Schachter1974の研究データ検証を完了したとはしない。')]
sources=[dict(source_id=sid,title=title,url=url,retrieved='2026-10-20',sha256=sha(Path('..')/name),bytes=(Path('..')/name).stat().st_size,body_read=scope,full_source_redistributed=False) for sid,title,url,name,scope in specs]
(p/'evidence/batch199_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
count=len(PdfReader(r/'qa.pdf').pages)
report=f'''\n\n## 第199バッチ 2026-10-20\n\n残るQ_2_002とQ_4_076を同領域差替えし、設問・全4肢・全4解説18件を改訂。Q_2_002は未取得Foley章からS300の研究者本人による宜蘭クレオール調査報告の全記事本文へ改訂。単なる抄録ではなく記事自身の報告を対象とし、2018年時点・当該事例に限定。Q_4_076は未取得Schachter論文からS149原著本文・Table 5の回避・縮小方略へ改訂。旧研究の参加者データの検証を完了したとは扱わない。両資料の全本文/原画像の取得・精読範囲はevidence/batch199_sources.json。独立正答2・1、全肢の誤りも指定資料で照合。キー変更なし。累積493問4314箇所、全500問維持、台帳は確認済み500・修正必要0・要追加確認0。\n\nこれは設問単位の学術判定の台帳上の到達点であり、最終全面監査完了・出版可を意味しない。前付け・ケース前提・索引・用語集等の横断根拠点検、159機械警告の分類処置、改頁修正、最終全頁画像QAが残る。manifestのacademic_audit_completeは全500問の判定完了を表す既存の集計フラグで、release_readyとfull_visual_qa_completedはfalseを保持。最終ファイル名は使用しない。\n\nv8ハッシュ・全500問・既存キーと正誤タグ・改訂外本文の不変を再構成で確認。18改訂文字列全件を新規PDFに検出、{count}頁の影響{pages}頁を直接画像確認。機械警告は159件、Q_2_002の文末極性警告の対象肢だけ更新。正答解説は普遍化への留保、誤答1は資料の区別を肯定して反証する文章であり、正誤タグの逆転ではない。CJK全字と非CJK代替の収録検査を通過。全頁QAは未完了。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。\n'''
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第199バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第199バッチ S300 S149\n\n'+'\n\n'.join(f'[{sid} {title}]({url})。{scope}' for sid,title,url,name,scope in specs)+'\n\nS279・S285の未取得原著を取得済みに変更せず、該当設問を同領域で差替え。本文のハッシュ・サイズ・精読範囲はevidence/batch199_sources.json。\n')
f=p/'README.md';s=f.read_text().replace('全面監査は未完了。','全面監査の最終検査は未完了。').replace('資料照合・改訂・再判定は継続中。','全500問の個別資料照合・改訂・再判定を台帳に記録済み。横断点検と最終検査は継続中。').replace('| 確認済み | 498問 |','| 確認済み | 500問 |').replace('| 要追加確認 | 2問','| 要追加確認 | 0問').replace('493問4296箇所','493問4314箇所').replace('学術的再判定・全頁QAが未了','横断点検・警告処置・全頁QAが未了').replace('第198バッチの最新描画は351頁',f'第199バッチの最新描画は{count}頁')
s+='\n第199バッチで旧学術残件2問を同領域差替えし、全500問の個別判定を記録済み。前段の再開手順3・4と第198バッチの残件記述は当時の履歴。現在は全159機械警告の処置、前付け・ケース・索引等の横断点検、改頁調整、最終全頁画像QAへ進む。全体の監査は未完了、作業稿は出版不可。\n';f.write_text(s)
e=dict(batch=199,base_remote_commit=BASE,fully_rejudged=list(keys),edits=18,independent_answers=keys,status_counts=m['status_counts'],remaining_question_holds=0,machine_warnings=159,added_warnings=added,removed_warnings=removed,render_pages=count,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch199_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
e['layout_pending']=['Q_4_076の解説見出し・正答が241頁、全4解説が242頁に分断。最終改頁調整が必要']
e['additional_context_pages_reviewed']=[241]
e['context_page_sha256']={'241':sha(r/'context-241.jpg')}
(p/'evidence/batch199_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
