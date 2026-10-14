"""Record source-limited academic judgments and partial visual QA, once."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch80-qa'
targets={'Q_4_042','Q_4_044','Q_4_045'}
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
manifest=json.loads((p/'manifest.json').read_text());assert manifest['status_counts']=={'確認済み':200,'修正必要':66,'要追加確認':234}
cs=json.loads((p/'changes_batch80.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs}
assert all(matches.values());reviewed=[70,71,72,268,269];assert sorted({n for v in matches.values() for n in v})==reviewed
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==51 and len(added)==2
f=p/'README.md';s=f.read_text()
for a,b in [('197問','200問'),('69問','66問'),('210問1705箇所','213問1732箇所'),('210問を','213問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第80バッチ（2026-10-15）

専用監査ブランチの最新HEAD5c940975d2f8d9630f590252a35083c9b8c7bae4を取得し、既存の判断を引き継いだ。著者公開のRichards（2006）全52頁冊子S144を再取得。印刷18・20〜21・31頁（PDF22・24〜25・35頁）の全文と画像を照合し、Q_4_042・044・045の3問27箇所を改訂。各問の設問、全4肢、独立正答、全4解説を再判定した。正答は順に2・4・3で変更なし。引用される別著者の原著を読んだとは扱わない。

Q_4_042は、初級全般で何が最善かという問いから、Richardsのタスクの特徴への架空の適用案の判定へ限定。案内係だけが時刻表を持ち、観光客だけが到着条件を持つ情報差を明記し、乗り継ぎ案という非言語的成果を設定した。文型使用自体をタスク失格とせず、誤答では音声・例文再現だけが成果という条件を明示。シャドーイングをすべてALMとする分類も除去。

Q_4_044は、生教材を母語話者向けだけに限定した定義や無条件の効果比較ではなく、Richards本人が20〜21頁で示す真正性をめぐる議論の両面を問う。文化情報と実際の言語使用に触れられるという利点、難解で関係のない言語が含まれる場合、作成教材も動機づけになりうるという対論を全肢・全解説で対応させた。引用されたClarke/Silberstein1977・Widdowson1987の原著取得やその全主張の承認へ広げない。

Q_4_045は、案内に地区別曜日・対象品目・場所が記載される条件と情報読取りという目標を明示。漢字検索、音読、形式抽出が常に無価値・挫折の原因・Focus on Formsだから不適切とする旧解説を撤回し、今回の目標に対応するかに限定した。設問の地区と傘は架空の適用例であり、実在自治体の分別規則や特定の中級授業での実証的効果とはしない。

確認済み200・修正必要66・要追加確認234、残件300。累積213問1732箇所。全500問と500解説、正答番号、影響外原文、v8ハッシュを維持。機械検査と公開可否回帰8条件に合格。警告は49から51へ増えたが、追加P1の2件はQ_4_044の効果比較ではないという正答末尾とQ_4_045の実在規則ではないという正答末尾が原因。全4肢と全4解説を照合しタグ・独立正答の一致を確認。従前の警告を消したり、検出器を緩めたりしていない。

Noto Sans JP Static Regular400をQAコピーだけに適用し、documentsのrender_docx.pyで399頁を再描画。変更の載る70・71・72・268・269頁を直接画像目視し、欠字・重なり・切れなし。27変更文字列はすべてPDFに反映。Q_4_045の選択肢が71〜72頁、Q_4_044の解説が268〜269頁に分かれる箇所は最終改頁調整候補。全399頁の最終画像目視は未了で、作業稿は出版不可。台帳の原文はv8スナップショット、改訂本文はchanges.jsonと累積作業稿を参照する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第80バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第80バッチ S144の追加照合（2026-10-15）

Jack C. Richards（2006）[Communicative Language Teaching Today 著者公開52頁冊子](https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf)を再取得。印刷18頁の鉄道案内での情報差、20〜21頁の真正性をめぐる賛否、31頁のタスクの特徴と教室用タスクを全文・画像照合した。印刷頁とPDF頁は18→22、20→24、21→25、31→35。対象Q_4_042・044・045。PDFのSHA256はevidence/batch80_review.jsonに記録。

2006年の本人による説明・議論の紹介を根拠とし、引用されるClarke/Silberstein1977やWiddowson1987、Littlewood1981の原著取得とは扱わない。Q_4_042・045は監査で作った架空の適用案で、初級・中級日本語授業の効果を実証した事例ではない。生教材の普遍的優越、音読や文法抽出の全面否定、自治体の実在規則は承認範囲に含めない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第80バッチ\nNoto Sans JP Static Regular400をQAコピーに適用。新しい出力先batch80-qaでdocumentsのrender_docx.pyによる399頁の描画完了後、70・71・72・268・269頁の5頁を直接画像目視。3問27変更文字列がPDFに全て存在し、正答と4肢タグの対応、欠字・重なり・切れのないことを確認。Q_4_045選択肢71〜72頁、Q_4_044解説268〜269頁は最終改頁調整候補。PDFにNotoSansJPStaticの埋込みを確認。全399頁の最終目視は未了、最終v9は未制作。\n''')
e={'batch':80,'base_commit':'5c940975d2f8d9630f590252a35083c9b8c7bae4','questions':sorted(targets),'edits':27,'status_counts':manifest['status_counts'],'remaining':300,'independent_answers':{'Q_4_042':2,'Q_4_044':4,'Q_4_045':3},'source_id':'S144','source_url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','source_sha256':sha(root/'richards80.pdf'),'source_pdf_pages':52,'source_image_verified_page_map':{'18':22,'20':24,'21':25,'31':35},'source_limits':'本人2006年の議論整理。引用元別原著は未取得。日本語授業例は架空の適用案。','machine_warnings':51,'new_machine_warnings':added,'new_warning_manual_review':{'Q_4_044 P1':'普遍的な優越の比較ではないという留保を正答末尾で述べるため。独立正答4に一致。','Q_4_045 P1':'架空例を実在自治体規則としないという留保を正答末尾で述べるため。独立正答3に一致。'},'readiness_gate':'8 cases passed','render_pages':399,'visually_reviewed_pages':reviewed,'full_visual_qa_completed':False,'all_changed_strings_found_in_pdf':matches,'font':'Noto Sans JP Static Regular400 QA copy only','font_sha256':sha(root/'lo80/share/fonts/truetype/NotoSansJPStatic.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'page-{i}.png') for i in reviewed},'release_ready':False}
(p/'evidence/batch80_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 questions / 27 edits; 200 confirmed / 300 remaining')
