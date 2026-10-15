"""Record batch88 only after its changed pages have been directly inspected."""
from pathlib import Path
import json,hashlib,subprocess,re,io,csv
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch88-qa';targets={'Q_4_032','Q_2_013','Q_2_018'}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');r=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(r)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':226,'修正必要':56,'要追加確認':218}
cs=json.loads((p/'changes_batch88.json').read_text());assert len(cs)==9
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');n=len(pages)-1
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:Image.open(render/f'review-{x}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==57 and added==[['P1','Q_4_032','(正)4の解説が否定で終わる/肯定の(誤)がある: [1, 2]']]
f=p/'README.md';s=f.read_text()
for a,b in [('| 確認済み | 225問','| 確認済み | 226問'),('| 要追加確認 | 219問','| 要追加確認 | 218問'),('要追加確認219問','要追加確認218問'),('238問1963箇所','239問1972箇所'),('238問を','239問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第88バッチ（2026-10-15）

最新HEAD f32739cda807f2dc850ed1ecdc2bfa14f82ee098を取得して継続。S144 Richards（2006）著者公開冊子の印刷7頁（PDF11頁）の全五手順を本文・150dpi画像で照合。Q_4_032の設問・全4肢・独立正答4・全4解説を照合して9箇所改訂。著者が記述した歴史的な典型授業の手順を問う形に限定。対話反復段階では教科書を参照しないが後続段階では参照する条件、文法説明を行う時点と最小限という条件、直接・即時訂正という歴史的記述を区別。旧解説の母語・翻訳を全面排除する一般化と、全現代授業への即時訂正推奨に読める表現を除いた。引用される2001年共著全体を取得したとはしない。

Q_2_013・018の原著取得も試行。Canale/Swain1980の出版社ページで正式書誌と有料アクセス表示を確認したが本文未取得。UEfAPの候補PDFはHTTP404、ResearchGateの表示された全文リンクも404。二次論文・検索抜粋の引用だけでは原著取得とせず、両問は要追加確認を維持し、不足経路をdecisionsへ追記。特に問18の教師介入が発達を阻害する因果主張、1980/1983の区分、問13のdesk/デスクを未照合のまま承認しない。

確認済み226・修正必要56・要追加確認218、残件274。累積239問1972箇所。500問・500解説、正答番号・影響外本文・元v8ハッシュを維持。台帳原文はv8スナップショットで改訂はchangesと作業稿を参照。

全問機械検査・公開可否回帰8条件に合格。警告56件は前回と同一。documentsのrender_docx.pyで日本語フォント適用QAコピーを{n}頁描画し、対象{ '・'.join(map(str,reviewed)) }頁を完成PDFから150dpi再描画して直接目視。9変更文字列と全4正誤タグ、日本語表示を確認。全{n}頁の最終目視は未了。最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第88バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第88バッチ S144追加照合と未取得原著（2026-10-15）

S144 [Richards2006著者公開冊子](https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf)印刷7頁（PDF11頁）の全五手順を本文・画像照合しQ_4_032の全4肢・4解説を改訂・確認済み。記述された歴史的授業手順に限定し普遍的教授効果・現代全授業への推奨としない。Richards/Rodgers2001著書全文は未取得。

Canale/Swain1980 [出版社書誌](https://doi.org/10.1093/applin/I.1.1)：Applied Linguistics I(1),1–47、1980-03-01、出版社は有料アクセス表示。本文未取得。[UEfAP候補](https://www.uefap.com/tefsp/bibliog/canale_swain.pdf)は404。[ResearchGate著者公開表示](https://www.researchgate.net/publication/31260438_THEORETICAL_BASES_OF_COMMUNICATIVE_APPROACHES_TO_SECOND_LANGUAGE_TEACHING_AND_TESTING)はMerrill Swainアップロードと表示されたが表示全文リンクのクリック先404。検索抜粋・他研究の引用で代用承認しない。Q_2_013・018は要追加確認を維持。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第88バッチ\n日本語フォント適用QAコピー{n}頁を描画し、対象'+ '・'.join(map(str,reviewed))+f'頁を150dpiで再描画・直接目視。9変更文字列・全4正誤タグを確認。採用画像はPIL検査済み。全{n}頁の最終目視は未了。\n')
e={'batch':88,'base_commit':'f32739cda807f2dc850ed1ecdc2bfa14f82ee098','fully_rejudged':['Q_4_032'],'edits':9,'independent_answers':{'Q_4_032':4},'status_counts':m['status_counts'],'remaining':274,'source':{'S144':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','sha256':sha(root/'richards80.pdf'),'pdf_pages':52,'body_and_image_verified_page_map':{'7':11},'limit':'2006 author account of historical procedure, not entire cited2001 book or universal teaching recommendation'}},'unretrieved_originals':{'Canale_Swain1980':{'doi':'10.1093/applin/I.1.1','publisher':'paid access; no body retrieved','UEfAP':'404','ResearchGate_displayed_fulltext_link':'404','questions_retained_unconfirmed':['Q_2_013','Q_2_018']}},'machine_warnings':56,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e.update(machine_warnings=57,new_machine_warnings=added,manual_warning_review='Q_4_032 correct4 explanation denies universal application; wrong1/2 explain actual historical steps. All four tags and independent key4 visually verified. Lexical P1 retained.')
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;s=f.read_text();prefix,batch=s.rsplit('## 第88バッチ',1);f.write_text(prefix+'## 第88バッチ'+batch.replace('警告56件は前回と同一。','警告56→57件。新規P1は正答解説が全教授法への一般化を否定し、誤答解説が実際の手順を肯定的に説明することによる字句警告。独立正答4と全4タグを再確認し警告を保存。'))
(p/'evidence/batch88_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded1 full review/9edits;226 confirmed/274remaining;pages',reviewed)
