"""One-time checkpoint for six independently rejudged questions and latest render."""
from pathlib import Path
import json,hashlib,subprocess,io,csv,re
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch84b-qa';targets={'Q_4_002','Q_4_008','Q_4_009','Q_4_011','Q_4_014','Q_4_025'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':214,'修正必要':58,'要追加確認':228}
cs=json.loads((p/'changes_batch84.json').read_text());assert len(cs)==59 and sum(bool(x.get('remove_paragraph')) for x in cs)==5
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');assert len(pages)-1==400
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs if c['after']};assert len(matches)==54 and all(matches.values())
reviewed=[55,57,58,59,60,64,253,255,256,257,258,262];assert sorted({n for v in matches.values() for n in v})==reviewed
imgs={i:render/('check262.png' if i==262 else f'page-{i}.png') for i in reviewed}
for f in imgs.values():Image.open(f).verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==54 and len(added)==1 and added[0][1]=='Q_4_008'
f=p/'README.md';s=f.read_text()
for a,b in [('208問','214問'),('59問','58問'),('233問','228問'),('221問1804箇所','227問1863箇所'),('221問を','227問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第84バッチ（2026-10-15）

最新HEAD c9a1a4fb59e6b407d2d7bce98e1b309c758bce96を取得し、判断・累積変更を引き継いだ。Richards2013の著者公開論文全29頁を新規取得（S147）。抄録ではなく本文8・13・20・28頁と図2〜4を精読・画像照合し、設計に唯一の最善の出発点を置かない比較を確認。Wiggins/McTighe、Taba、Clark等の引用先原著全体を取得したとは扱わない。S144も印刷5・10〜12・28〜30頁の該当本文と画像を追加照合した。

Q_4_002はコミュニカティブな授業での協働と学習への責任を支える教師の役割へ限定（正答3）。訂正による不安の因果断定、9割以上という無根拠の講義比率を除去した。Q_4_008は普遍的な標準五段階を撤回し、S147図4のバックワード・デザインの出発点を問う問題へ改訂（正答3）。ニーズ分析を否定せず、モデルの違いを明示した。

Q_4_009は職務上の役割に必要な言語使用を観察・面接等で調べる架空の適用問題に改訂（正答1）。分類体系を指定しないLack・客観／主観ニーズの対応、再分析とレディネス分析の混同を残さない。Q_4_011は技能・機能・文法・タスクの編成単位の区別を明示（正答1）。使用目的とトピックの同一視や唯一の文法難易度順を除去した。

Q_4_014は主題を先に決め、それに活動や言語項目を結び付ける条件を明示（正答1）。主題名だけの分類や、未照合のサバイバル定義を撤回。CBI全体とトピック中心の編成が常に同義だとはしない。Q_4_025は電話・メールという単元名だけから場面とタスクの複合を断定する旧案を撤回。機能別の単元と文法項目・導入順の両方を明記した架空の編成へ改訂（正答2）。トピックを学術内容だけに限定せず、複合シラバスの普及頻度も断定しない。

初期の個別所見に、Q_4_002を省察、011をレディネス、014をTTT/STTとして扱う設問不一致があった。今回は実際の設問・全4肢・4解説を累積稿から再抽出し、その所見を根拠に正答を決めず再判定した。影響外の未照合問を一括承認していない。

6問54フィールド変更と、複数段落の設問の旧継続段落5つの明示削除、計59箇所を順序付きchangesへ記録。最初の再構成は連結された設問文字列の不一致で安全停止し、前の有効稿を維持。第84追補でQ_4_014・025の先頭段落置換と旧段落削除に分解し、再構成成功後に新しいbatch84b-qaへ描画した。失敗前のbatch84-qaは今回のQA根拠に使わない。

確認済み214・修正必要58・要追加確認228、残件286。累積227問1863箇所。全500問・500解説と正答番号、影響外本文、v8ハッシュを維持。台帳原文はv8スナップショットで、改訂はchangesと累積作業稿を参照する。

全問機械検査・公開可否回帰8条件に合格。警告54件。追加P1 Q_4_008は、正答解説がニーズ分析不要論と全コースへの固定順序化を否定する末尾による。タグ・全4肢・4解説と独立正答3を直接確認し、検出器は変更しない。

documentsスキルのrender_docx.pyによりNoto Sans JP Static Regular400をQAコピーのみに適用し400頁描画。55・57・58・59・60・64・253・255・256・257・258・262頁の12頁を直接目視し、54変更文字列と5旧段落除去を確認。262頁の元PNGは形式破損のため同じPDFから再描画し、100dpiで正誤タグの一部が不完全に見えたため150dpiのcheck262.pngでも再確認し4タグが揃うことを確認した。最終QAには解像度と画像健全性の確認も必要。本文の日本語欠字・切れ・重なりなし。Q_4_011の設問58〜59頁、009解説255〜256頁、014解説257〜258頁は最終改頁調整候補。全400頁目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第84バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://www.professorjackrichards.com/wp-content/uploads/Curriculum-Approaches-in-Language-Teaching.pdf'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## S147 第84バッチの新規原著（2026-10-15取得）

Jack C. Richards（2013）[Curriculum Approaches in Language Teaching Forward Central and Backward Design]({url})、RELC Journal 44(1), 5–33、DOI 10.1177/0033688212473293。著者公開の全29頁PDFを取得。本文の印刷8頁（PDF4頁）の三モデルと図2〜4、13頁（PDF9頁）のcentral design、20頁（PDF16頁）のbackward design、28頁（PDF24頁）の結論を本文・画像照合。Q_4_008の全4肢・4解説に適用。抄録だけの承認ではない。目標設定のためのニーズ分析を排除せず、他モデルより常に優れているとしない。引用先Wiggins/McTighe、Taba、Clarkの原著全体は未取得。全文転載せずURL・PDFハッシュ・確認頁をevidence/batch84_review.jsonに記録。

S144追加照合：著者公開52頁冊子の印刷5頁（PDF9頁）の教師・学習者の役割、10〜11頁（PDF14〜15頁）の編成単位、12頁（PDF16頁）の職務上のニーズ分析、28〜30頁（PDF32〜34頁）の主題・内容中心の編成を本文・画像で確認。対象Q_4_002・009・011・014・025。日本語教育一般への効果保証、機能・文法・テーマの単一排他的分類、題名だけの分類は承認しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'''\n\n## 第84バッチ\n安全停止後の再構成成功版を新しいbatch84b-qaへ400頁描画。55・57・58・59・60・64・253・255・256・257・258・262頁の12頁を直接目視。54変更文字列をPDFで確認。旧段落5つを明示除去。262頁は破損PNGを再生成し、タグを150dpiのcheck262.pngでも確認。NotoSansJPStatic埋込みあり。Q_4_011設問58〜59頁、009解説255〜256頁、014解説257〜258頁は最終改頁調整候補。失敗前のbatch84-qaや他版の画像を最新QAと混同しない。全400頁の最終目視は未了。\n''')
e={'batch':84,'base_commit':'c9a1a4fb59e6b407d2d7bce98e1b309c758bce96','questions':sorted(targets),'edits':59,'field_revisions':54,'old_stem_paragraphs_removed':5,'status_counts':m['status_counts'],'remaining':286,'independent_answers':{'Q_4_002':3,'Q_4_008':3,'Q_4_009':1,'Q_4_011':1,'Q_4_014':1,'Q_4_025':2},'sources':{'S147':{'url':url,'sha256':sha(root/'curriculum84.pdf'),'pdf_pages':29,'image_verified_page_map':{'8':4,'13':9,'20':16,'28':24},'scope':'Author article body and figures; cited original books not acquired.'},'S144':{'url':'https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf','sha256':sha(root/'richards80.pdf'),'pdf_pages':52,'image_verified_page_map':{'5':9,'10':14,'11':15,'12':16,'28':32,'29':33,'30':34}}},'machine_warnings':54,'new_machine_warnings':added,'new_warning_manual_review':'Q_4_008 P1はニーズ分析不要論・普遍固定順序を否定する正答3の末尾による。4肢・4解説・タグを照合。','readiness_gate':'8 cases passed','render_pages':400,'visually_reviewed_pages':reviewed,'all_changed_strings_found_in_pdf':matches,'render_recovery':'Rejected initial joined stems safely; explicit removal of5continuations; only new batch84b render accepted. PNG262 recovered from same PDF and checked again at150dpi for tag rendering.','full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(i):sha(imgs[i]) for i in reviewed},'release_ready':False}
(p/'evidence/batch84_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 6 questions / 59 edits; 214 confirmed / 286 remaining')
