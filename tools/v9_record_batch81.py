"""One-time checkpoint after academic and image review of batch81."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch81-qa';targets={'Q_4_036','Q_4_040','Q_4_046'}
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
manifest=json.loads((p/'manifest.json').read_text());assert manifest['status_counts']=={'確認済み':203,'修正必要':63,'要追加確認':234}
cs=json.loads((p/'changes_batch81.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==400
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs};assert all(matches.values())
reviewed=[68,69,70,72,266,268,270,271];assert sorted({n for v in matches.values() for n in v})==reviewed
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==52 and len(added)==1
f=p/'README.md';s=f.read_text()
for a,b in [('200問','203問'),('66問','63問'),('213問1732箇所','216問1759箇所'),('213問を','216問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第81バッチ（2026-10-15）

専用監査ブランチの最新HEAD3ec0f6337c5d3366f042d82ccfe77c84087a3e2cを取得し、既存判定を尊重。Jane Willis署名のTeachingEnglish記事全文を新規取得してS145として記録した。記事はPre-task、Task/Planning/Report、サイクル後の形式学習と、教科書の活動順序の変更を説明している。刊年の表示は確認できず、コメントの日付を記事の刊年としない。1996年書籍全体、Prabhu原著、教材アダプテーションの分類書を取得したとは扱わない。

Q_4_036はWillisとPrabhuを一つにした旧設問を本人の記事の説明に限定。Planningでは辞書や教師への相談、報告に向けた表現改善が可能で、Reportでは流暢さと正確さの双方に焦点がある。タスク・サイクル全体を形式注意ゼロとする読みを防ぎ、サイクル後の形式学習という提案を正答1とした。効果保証や全TBL授業への必須手順化はしない。

Q_4_040はRichards（2006）S144の印刷18頁を本文・画像で再照合。互いに絵を見せず、未知の情報を質問して違いの数を調べる条件を明示した。復唱をシャドーイングと同一視する解説を撤回。共有テキストを使う授業でも情報差は別途設計できるため、誤答にはそうした課題を含めないという限定を加えた。情報差だけで真正なやり取りや長期習得が必ず生じるとはしない。独立正答2。

Q_4_046は未照合の四つの分類名称を一括承認せず、教材順序の調整という同じ領域内で再配列の操作的定義を明示。Willis本人の教科書組替え案を参考に、準備課題の移動、Planningの位置変更、文法部分の後置と、順序を変えない配布部数の変更を比較する架空の適用問題へ改訂した。不適切な対応は4のみ。すべての教材でタスク先行が最善とする断定は除いた。

3問27箇所を順序付きchanges_batch81.jsonへ記録。設問・全4肢・独立正答・全4解説を取得本文と明示条件で照合し、確認済み203・修正必要63・要追加確認234、残件297。累積216問1759箇所。全500問と500解説、正答番号、影響外原文、v8原本ハッシュを維持した。

機械検査と公開可否回帰8条件に合格。警告は51から52。追加P1のQ_4_040は、情報差だけによる習得効果保証を否定する正答解説末尾が原因。全4肢と4解説、タグと独立正答2を直接確認し、検出器は変更しない。従前の警告も保持。

Noto Sans JP Static Regular400をQAコピーのみに適用し、documentsのrender_docx.pyで400頁を再描画。68・69・70・72・266・268・270・271頁の8頁を画像精読。27変更文字列はPDFに全て反映し、日本語欠字・重なり・切れなし。Q_4_040の設問・選択肢69〜70頁とQ_4_046解説270〜271頁は最終改頁調整候補。全400頁の最終画像目視は未了、最終v9は未制作。台帳の原文はv8スナップショットで、改訂本文はchanges.jsonと累積作業稿を参照する。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第81バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/priming-tasks-and-target-tasks-language-focus-and'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## 第81バッチの追加資料（2026-10-15）

| ID | 資料 | 照合範囲 | 取得段階と限界 | 対象 |
|---|---|---|---|---|
| S145 | Jane Willis [From priming tasks and target tasks to language focus and grammar]({url})、British Council TeachingEnglish。取得用の同一記事URL https://www.teachingenglish.org.uk/comment/1307 | Use the book but change the order、Pre-task/Priming、Task Cycle: Task - planning - report、Focus on Form: At the end of the task cycle。本人署名も確認 | HTML本文を直接取得し全記事を精読。刊年は未表示として扱い、コメント・クロール日を刊年にしない。提唱者本人の公開説明に限定し、1996年書籍全体・Prabhu原著・別の教材分類体系まで承認しない。Q_4_046は架空の適用案。 | Q_4_036・046 |

S144追加照合：著者公開52頁冊子の印刷18頁（PDF22頁）の説明と絵の差異探索例を本文・画像で再確認し、Q_4_040の全4肢・4解説に適用。全員が同じ文章を持つことだけであらゆる情報差を否定せず、今回の活動案に未知情報の取得課題がないことを明示。復唱をシャドーイングと同一視せず、情報差から長期習得効果を断定しない。資料のURL・ハッシュと取得範囲はevidence/batch81_review.jsonにも記録し、全文はリポジトリへ転載しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第81バッチ\n新しい出力先batch81-qaでNoto Sans JP Static Regular400を適用したQAコピーをdocumentsのrender_docx.pyにより400頁描画。完了後、68・69・70・72・266・268・270・271頁の8頁を直接目視。対象3問27変更文字列が全てPDFに存在し、欠字・重なり・切れなし。Q_4_040の設問・選択肢69〜70頁、Q_4_046解説270〜271頁は最終改頁調整候補。NotoSansJPStaticのPDF埋込みを確認。全400頁目視は未了、出版不可の作業稿。旧版の頁番号を最新版のQA完了の証拠と混同しない。\n''')
e={'batch':81,'base_commit':'3ec0f6337c5d3366f042d82ccfe77c84087a3e2c','questions':sorted(targets),'edits':27,'status_counts':manifest['status_counts'],'remaining':297,'independent_answers':{'Q_4_036':1,'Q_4_040':2,'Q_4_046':4},'sources':{'S145':{'url':url,'retrieval_url':'https://www.teachingenglish.org.uk/comment/1307','html_sha256':sha(root/'willis81.html'),'author':'Jane Willis 本文署名を確認','publication_year':None,'scope':'本人記事の本文全体を精読。コメントを根拠にしない。1996年書籍全体未取得。'},'S144':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','sha256':sha(root/'richards80.pdf'),'pdf_pages':52,'image_verified_page_map':{'18':22}}},'machine_warnings':52,'new_machine_warnings':added,'new_warning_manual_review':'Q_4_040 P1は習得効果の保証を否定する正答2の末尾による。4肢・4解説・タグを再確認。','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'full_visual_qa_completed':False,'all_changed_strings_found_in_pdf':matches,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(render/f'page-{i}.png') for i in reviewed},'release_ready':False}
(p/'evidence/batch81_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 questions / 27 edits; 203 confirmed / 297 remaining')
