"""One-time evidence checkpoint after direct source and changed-page review."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch87-qa';targets={f'Q_3_{n:03}' for n in range(23,30)}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':225,'修正必要':56,'要追加確認':219}
cs=json.loads((p/'changes_batch87.json').read_text());assert len(cs)==64 and sum(bool(x.get('remove_paragraph')) for x in cs)==1
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==399
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs if c['after']};assert all(matches.values())
reviewed=sorted({n for v in matches.values() for n in v})
for i in reviewed:Image.open(render/f'review-{i}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==56 and added==[['P1','Q_3_028','(正)3の解説が否定で終わる/肯定の(誤)がある: [1, 2, 4]']]
f=p/'README.md';s=f.read_text()
for a,b in [('| 確認済み | 218問','| 確認済み | 225問'),('修正必要57問','修正必要56問'),('| 修正必要 | 57問','| 修正必要 | 56問'),('要追加確認225問','要追加確認219問'),('| 要追加確認 | 225問','| 要追加確認 | 219問'),('231問1899箇所','238問1963箇所'),('231問を','238問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第87バッチ（2026-10-15）

最新HEAD 7485bad2b1242583d6324a608034a18c166b0baeを取得して継続。Rebecca L. Oxford本人署名の25頁公開論文「Language Learning Styles and Strategies: An Overview」を大学サイトから取得。S148の8〜10・12〜14頁を本文・画像で確認した。ヘッダーにはGALA2003とあるが正式な刊年・掲載先の書誌同定は未確定のため、設問では年を断定しない。1990年著書全文、O'Malley/Chamot著書、引用された個別実験の全文取得とはしない。PDFにはxref再構成の警告が出たが、対象6頁は本文と直接描画画像が読めることを確認した。学習スタイルに関する前半の一般化や、指導効果の普遍的保証を承認したものではない。

Q_3_023〜029の7問を、設問・全4肢・独立正答・全4解説まで照合し改訂。Oxfordの6分類を明示し、別体系との混在を解消。文脈から未知語を推測する補償と、構造を分析する認知を区別した。問25は事前の内容予測という曖昧な肢を目標・時間の計画へ変更。問26は単に接触機会を増やす肢を相手への質問・確認に変更。問27は固定的学習者類型や文化背景から効果を一般化する問いをやめ、取得した著者本文の課題適合・方略連鎖・教師の支援を問う。問28は実際の活動で複数方略を併用できることを明示。問29は語構造分析と文脈推測の混在を解消し、選択肢4を文脈推測による補償に改稿。正答番号は全問維持した。

原稿改訂7問64箇所（63フィールドと問29の旧設問継続1段落の明示削除）。確認済み225・修正必要56・要追加確認219、残件275。累積238問1963箇所。全500問・500解説、正答番号・影響外本文・元v8のハッシュを維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。

全問機械検査と公開可否回帰8条件に合格。警告は55→56件。新規P1（問28）は、正答解説で「記憶と認知が実践上いつも完全に排他的という意味ではない」と限定したことと、誤答解説内に正しい分類を記したことによる字句警告。全4タグと独立正答3を再確認し、警告を隠さず保存。documentsのrender_docx.pyで日本語フォント適用済みQAコピーを400頁描画し、変更文字列のある全対象頁を150dpiで再描画・直接目視した。全400頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第87バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://web.ntpu.edu.tw/~language/workshop/read2.pdf'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## S148 Oxford本人「Language Learning Styles and Strategies: An Overview」公開25頁版

[大学サイトの公開PDF]({url})を2026-10-15に取得。著者Rebecca L. Oxfordの署名、題名、ヘッダーGALA2003を確認。正式な刊年・会議・掲載先は未同定でありヘッダーだけから確定しない。印刷頁とPDF頁は一致。8〜10頁は課題との適合、方略の連携、教師の支援、方略連鎖。12頁は認知・メタ認知、13頁は記憶関連・補償、14頁は補償を学習方略と認めるかの議論、情意・社会的方略。全6頁を本文・画像照合しQ_3_023〜029の設問・全4肢・全4解説と独立正答を再判定。1990年著書全文、別分類の原著、引用研究の全主張の承認ではない。前半の学習スタイル論や固定的な型に基づく指導効果は本バッチで検証しない。xref再構成警告を記録し、対象頁の可読性を確認。全文転載せず、SHA256と照合範囲はevidence/batch87_review.jsonへ記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第87バッチ\n399頁を日本語フォント適用QAコピーから描画。変更文字列がある対象頁'+ '・'.join(map(str,reviewed))+'を完成PDFから150dpiで再描画し直接目視。採用画像はPIL検査済み。63変更文字列、全4肢・正誤タグの日本語表示と切れ・重なりを確認。問24・27の肢や問27の解説が頁をまたぐため、46〜48・245〜246頁は最終改頁調整候補。全399頁の最終目視は未了。\n')
e={'batch':87,'base_commit':'7485bad2b1242583d6324a608034a18c166b0bae','fully_rejudged':sorted(targets),'edits':64,'explicit_old_stem_removals':1,'status_counts':m['status_counts'],'remaining':275,'independent_answers':dict(zip(sorted(targets),[4,1,3,4,3,3,4])),'sources':{'S148':{'url':url,'sha256':sha(root/'oxford87.pdf'),'pdf_pages':25,'author':'Rebecca L. Oxford','bibliographic_limit':'GALA2003 running header; formal publication year/venue not independently identified','body_and_image_verified_pages':[8,9,10,12,13,14],'parser_warning':'xref num101 not found; Poppler reconstructed; six relevant pages visually verified','limits':'Author summary primary text, not entire 1990 book or alternative taxonomy originals or current empirical consensus.'}},'machine_warnings':56,'new_machine_warnings':added,'manual_warning_review':'Q_3_028 key3 correctly rejects always-mutually-exclusive interpretation; all four tags verified. P1 lexical heuristic retained.','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'review-{i}.png') for i in reviewed},'release_ready':False}
e['render_pages']=399
e['pagination_followup']='Q_3_024/Q_3_027 options cross pages46–48; Q_3_027 explanations cross245–246. Final keep-together tuning pending.'
# Correct page total in this batch only; earlier reports describe their own PDFs.
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;s=f.read_text();prefix,batch=s.rsplit('## 第87バッチ',1);f.write_text(prefix+'## 第87バッチ'+batch.replace('400頁','399頁')+'\n改頁調整候補：問24・27の肢（46〜48頁）、問27の解説（245〜246頁）。\n')
(p/'evidence/batch87_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 7 reviews /64 edits;225 confirmed /275 remaining; reviewed pages',reviewed)
