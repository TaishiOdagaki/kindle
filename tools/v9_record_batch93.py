"""One-time record after manual review of the latest changed-page PNGs."""
from pathlib import Path
import json,hashlib,subprocess,re,io,csv,bisect
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch93-qa';targets={'Q_4_006','Q_M_017','Q_O_074'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':240,'修正必要':53,'要追加確認':207}
cs=json.loads((p/'changes_batch93.json').read_text());assert len(cs)==28 and sum(bool(x.get('remove_paragraph')) for x in cs)==1
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');n=len(pages)-1
normalized=[re.sub(r'\s+','',t) for t in pages[:-1]];joined=''.join(normalized);bounds=[0]
for t in normalized:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 if not c['after']:continue
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=joined.find(needle,start))>=0:
  first=bisect.bisect_right(bounds,at);last=bisect.bisect_right(bounds,at+len(needle)-1)
  found.update(range(first,last+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values())
reviewed=sorted({x for v in matches.values() for x in v})
def review_image(x):return render/('review-373-cairo.png' if x==373 else f'review-{x}.png')
for x in reviewed:Image.open(review_image(x)).verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));nw=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==60 and len(nw)==1 and nw[0][0:2]==['P1','Q_4_006'] and all(x in machine['issues'] for x in prior['issues'])
f=p/'README.md';s=f.read_text()
for a,b in [('237問','240問'),('54問','53問'),('209問','207問'),('250問2075箇所','253問2103箇所'),('250問を','253問を')]:s=s.replace(a,b)
f.write_text(s)
url='https://www.scribd.com/document/807250266/Council-of-Europe-Modern-Languages-Project-Henri-Holec-Autonomy-and-Foreign-Language-Learning-Pergamon-Press-1981'
report=f'''

## 第93バッチ（2026-10-15）

最新HEAD4cbc8dc4a26aa251c49f1a5c7401c7e9b13f93a4から継続。Holec『Autonomy and Foreign Language Learning』の1981年Pergamon版表示のある公開複製本文を取得。初版1979年と1981年版を奥付で区別。3〜4頁の定義・能力と行動・支援の有無、および23〜24頁の教師の支援を本文照合した。取得は公開HTMLで閲覧できる範囲であり、59頁全体のPDF取得・全読とは扱わない。

Q_4_006は学習者本人が丁寧体でまとめたいと相談した条件を明記し、文体混在の無条件の誤用前提を撤回。目標・方法・自己評価の検討を支える助言を問う。反復練習が必ず情意フィルターを高める、明示的訂正では自律性が育たないという未照合の一律因果は残さない。旧設問の継続1段落も明示削除した。

Q_M_017は自律性という能力と、自己主導で学ぶ行動・学習形態を区別。教師不在だけでは自律性とは言えず、教師の支援を受けることも自律性と矛盾しないという原著の条件で全4肢を判定した。旧肢の他理論の略記を本問から除き、原著未取得の臨界期理論などを同時承認したとは扱わない。

Q_O_074はケース15の全前提を読み、本人が方法を選び実践したという事例内の事実と対応させた。ケースは教材用の架空事例だと設問に明示し、数週間後の成績を指導効果の実証や全学習者への普遍保証にしない。ケース共有本文や他問の既存確定分類は変更していない。

3問28箇所（27フィールド＋旧継続段落1削除）を改訂し、設問・全4肢・独立正答・4解説を照合。独立正答はQ_4_006=2、Q_M_017=1、Q_O_074=1、番号変更なし。確認済み240・修正必要53・要追加確認207、残件260。累積253問2103箇所。500問・500解説、影響外本文、v8ハッシュを維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。

構造検査と公開可否回帰8条件に合格。機械警告60件（従来59件を維持、新規は問6のP1字面警告1件）。正答解説の「保証するものではありません」と誤答解説の説明的肯定文を検出したもので、全4肢・タグの直接照合で正誤の不整合ではないと記録。警告は消去していない。documentsのrender_docx.pyで日本語フォント適用QAコピーを{n}頁描画し、27変更文字列のある{ '・'.join(map(str,reviewed)) }頁を完成PDFから150dpi再描画・直接目視。全頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第93バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';assert '| S152 |' not in f.read_text();f.write_text(f.read_text()+f'''

## 第93バッチ 自律性の原著本文照合

| ID | 資料 | 取得・使用範囲 | 対象 |
|---|---|---|---|
| S152 | Henri Holec（1981）[Autonomy and Foreign Language Learning、Council of Europe／Pergamon版公開複製]({url}) | 2026-10-15公開HTMLの原著本文取得。奥付の初版1979／当該Pergamon版1981を区別。印刷3〜4頁の定義・能力と行動・支援、23〜24頁の教師の助言を本文照合。59頁のPDF全体を取得したとは扱わない。OCRの誤読が見られる導入の歴史記述など、対象外の主張は承認しない。 | Q_4_006・Q_M_017・Q_O_074 |

特定の作文訂正法が自律性・情意面へ及ぼす普遍的効果を実証したとは扱わない。ケース15の成績変化は教材用架空事例の記述で、原著の実験結果ではない。出典本文の取得範囲とHTMLハッシュはevidence/batch93_review.jsonに記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第93バッチ\n日本語フォント適用QAコピー{n}頁を描画。変更頁'+ '・'.join(map(str,reviewed))+f'を150dpi再描画・直接目視、全27変更文字列・全4正誤タグを確認。全{n}頁の最終目視は未了。\n')
e={'batch':93,'base_commit':'4cbc8dc4a26aa251c49f1a5c7401c7e9b13f93a4','fully_rejudged':sorted(targets),'edits':28,'explicit_old_stem_removals':1,'status_counts':m['status_counts'],'remaining':260,'independent_answers':{'Q_4_006':2,'Q_M_017':1,'Q_O_074':1},'sources':{'S152':{'url':url,'retrieved_html_sha256':sha(root/'holec93.html'),'format':'Public original-text HTML preview; not whole59-page PDF','edition':'Title and imprint show1979first edition/1981Pergamon edition','body_verified_printed_pages':['3–4','23–24'],'limits':'Not empirical correction-effect study, critical-period original, entire cited originals, or endorsement of OCR historical introduction'}},'case15':'Shared case read, not modified; fictional nature and no causal universal inference explicit in Q_O_074','machine_warnings':60,'new_machine_warnings':nw,'manual_warning_disposition':{'Q_4_006':'P1 lexical heuristic. Correct explanation rejects guaranteed completion of autonomy, not correct option2. Wrong explanation1 affirmatively describes why learner-goal exclusion fails. 1wrong/2correct/3wrong/4wrong consistent.'},'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['page_sha256']={str(x):sha(review_image(x)) for x in reviewed}
e['image_validation']='A truncated253PNG was rejected and regenerated. For373, PDF text and DOCX runs retained all tags; pdftocairo150dpi was additionally used and its page image directly verified for answer1 and all four tags. Adopted373image hash refers to Cairo PNG.'
e['pagination_followup']='Q_4_006 stem crosses55–56. Exact changed-string check joins normalized adjacent PDF pages and records both pages, rather than assuming every paragraph fits one page. Final keep-together tuning pending.'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;f.write_text(f.read_text()+'\n第93バッチ改頁調整候補：問6の設問が55〜56頁に分かれる。変更全文は隣接頁を連結して照合し、両頁を目視した。欠字・切れはないが最終改頁調整は未了。253頁の不完全PNGは棄却して再描画。373頁はDOCX・PDFのタグ保持を照合し、pdftocairoによる150dpi画像も作成して正解1・全4タグを直接再確認した。採用画像のハッシュは当該Cairo画像を記録。\n')
(p/'evidence/batch93_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded3fullreviews/28edits;240confirmed/260remaining;pages',reviewed)
