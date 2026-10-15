"""One-time recording after human inspection of batch92 page images."""
from pathlib import Path
import json,hashlib,subprocess,re,io,csv
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch92-qa';targets={'Q_5_103','Q_5_104'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':237,'修正必要':54,'要追加確認':209}
cs=json.loads((p/'changes_batch92.json').read_text());assert len(cs)==18
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');n=len(pages)-1
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:Image.open(render/f'review-{x}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
new_warnings=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==59 and len(new_warnings)==2
assert {x[1] for x in new_warnings}==targets and all(x[0]=='P1' for x in new_warnings)
assert all(x in machine['issues'] for x in prior['issues'])
f=p/'README.md';s=f.read_text()
for a,b in [('235問','237問'),('211問','209問'),('248問2057箇所','250問2075箇所'),('248問を','250問を')]:s=s.replace(a,b)
f.write_text(s)
url='https://siptulearn.ie/wp-content/uploads/2018/01/Fisher-Urry-Getting-to-yes.pdf'
report=f'''

## 第92バッチ（2026-10-15）

最新HEAD2ccdd1f8c1a2271af3e21b515dd4b6dd10ecba2cの保存を確認して継続。Fisher・Ury・Patton『Getting to Yes』第2版と表示された公開再組版PDFを全90頁取得。PDF11〜14、20〜24、31、42〜43、50頁の原著本文を照合し、11・21・23頁を画像でも確認。参照頁はこのPDFの通し頁であり、商業出版版の頁番号と同一視しない。要約資料や書誌だけでは承認していない。

Q_5_103の「原理的交渉術が最も効果的」という無条件の実証的順位を撤回。同書の利害・ニーズへの着目、複数案、客観的基準、人への配慮を問う形に改訂し、方法が合意を保証しないという原著の留保も含めた。旧稿の文化類型の定義・国別慣習は本問から除き、Hallの原著を照合したとは扱わない。

Q_5_104は原著の意味・認識・制約の相互確認を、会場の開場条件を明示した架空会話に適用。視線や「ちょっと」だけから意図を一義的に決めず、Bの意図は後の説明という事例内の事実として明示した。Aだけの察する義務やBだけへの批判ではなく、双方が意味・制約を共有して相談する対応を正答とした。教材用の例であり、日本語の間接表現の頻度や民族全体の特性を実証したものではない。

2問18箇所の設問・全4肢・独立正答・4解説を改訂・照合。独立正答2・4で番号変更なし。確認済み237・修正必要54・要追加確認209、残件263。累積250問2075箇所。500問・500解説、影響外本文、v8ハッシュを維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。

全問構造検査と公開可否回帰8条件に合格。機械警告は59件（従来57件維持、新規P1が問103・104に各1件）。新規2件は解説の文末否定や肯定文を拾う字面検査であり、誤答の理由を肯定文で説明する箇所と、正答解説内で普遍断定を否定する箇所を検出したもの。全4肢とタグの対応を直接照合し、新たな正誤不整合ではないと個別記録した。警告自体は消去していない。documentsのrender_docx.pyで日本語フォント適用QAコピーを{n}頁描画。変更文字列のある{ '・'.join(map(str,reviewed)) }頁を完成PDFから150dpiで再描画して直接目視し、全18文字列と全4肢・正誤タグを確認。全{n}頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第92バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';assert '| S151 |' not in f.read_text();f.write_text(f.read_text()+f'''

## 第92バッチ 交渉原著の本文照合

| ID | 資料 | 取得・使用範囲 | 対象 |
|---|---|---|---|
| S151 | Roger Fisher・William Ury・Bruce Patton, [Getting to Yes、第2版表記の公開再組版PDF]({url})。SIPTU研修サイト掲載。 | 2026-10-15全90頁取得。PDF11〜14頁の原則、20〜24頁の伝達・意味確認・利害、31頁の複数案、42〜43頁の基準、50頁の非保証を本文照合。PDF11・21・23頁は画像も確認。PDF独自通し頁、商業出版版の頁とは区別。原著本文の複製であり、国別効果の実証研究ではない。 | Q_5_103・104 |

文化類型の原著を未取得のまま承認しない。会場準備の会話は本問題集の教材用創作で、原著掲載の実例ではない。合意の強制・成功の保証をしない。PDFハッシュと照合範囲はevidence/batch92_review.jsonに記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第92バッチ\n日本語フォント適用QAコピー{n}頁。変更頁'+ '・'.join(map(str,reviewed))+f'を完成PDFから150dpi再描画・直接目視し、全18文字列と全4正誤タグを確認。全{n}頁の最終目視は未了。\n')
e={'batch':92,'base_commit':'2ccdd1f8c1a2271af3e21b515dd4b6dd10ecba2c','fully_rejudged':sorted(targets),'edits':18,'status_counts':m['status_counts'],'remaining':263,'independent_answers':{'Q_5_103':2,'Q_5_104':4},'sources':{'S151':{'url':url,'sha256':sha(root/'fisher92.pdf'),'pdf_pages':90,'format':'Public re-typeset original book text, second edition attribution on title page; commercial-edition pagination not asserted','body_verified_pdf_pages':['11–14','20–24','31','42–43','50'],'image_verified_pdf_pages':[11,21,23],'limit':'Principled negotiation as authors approach, not universal effectiveness ranking, Hall original, or empirical national-culture claims'}},'fictional_scenario':'Q_5_104 invented; B intention supplied as subsequent statement, not inferred from gaze','machine_warnings':57,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e.update(machine_warnings=59,new_machine_warnings=new_warnings,manual_warning_disposition={'Q_5_103':'P1 lexical heuristic: wrong option4 promises success; explanation4 correctly states no guarantee; affirmative narrative is not endorsement of option4.','Q_5_104':'P1 lexical heuristic: explanation4 ends with rejection of a universal meaning claim; explanations1–3 contain affirmative reasons why the wrong choices fail. Tags1–3wrong/4correct are consistent with scenario and source.'})
e['pagination_followup']='Q_5_104 explanation4 continues340–341; readable and tags intact. Final keep-together tuning pending.'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;f.write_text(f.read_text()+'\n第92バッチ改頁調整候補：問104の解説4が340〜341頁に分かれる。欠字・切れはないが最終版の改頁調整は未了。\n')
(p/'evidence/batch92_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded2fullreviews/18edits;237confirmed/263remaining;pages',reviewed)
