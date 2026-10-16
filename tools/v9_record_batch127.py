"""Record CLIL primary-framework audit and corrected-render QA."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa127-fixed';ids=['Q_4_037','Q_O_067','Q_O_068']
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in ids else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':328,'修正必要':30,'要追加確認':142}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
newflags=[i for i in machine['issues'] if i not in prior['issues']];assert len(machine['issues'])==96 and len(newflags)==1 and newflags[0][0:2]==['P1','Q_O_068']
assert not [i for i in prior['issues'] if i not in machine['issues']]
cs=json.loads((p/'changes_batch127.json').read_text());assert len(cs)==27
matches=json.loads((r/'matches.json').read_text());assert len(matches)==27 and all(matches.values());reviewed=sorted({n for vs in matches.values() for n in vs})
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
for n in [8,9,10]:
 with Image.open(root/f'clil-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();pagecount=len(text.split('\f')[:-1])
for c in cs:assert re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',text)
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}==set(ids)
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
f=p/'README.md';s=f.read_text()
for a,b in [('325問','328問'),('145問','142問'),('326問2743箇所','329問2770箇所'),('326問を','329問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第127バッチ（2026-10-16）

Q_4_037・Q_O_067・Q_O_068を27箇所改訂し、設問・全4肢・独立正答・全4解説を照合。独立正答は順に1・4・2を維持。Coyle本人を含む著者Bower/Cross/CoyleによるCLIL枠組みの本文を、出版社公開章抜粋の印刷9〜11/PDF8〜10で取得・本文/画像照合した。章の抜粋だが用いた箇所は定義・枠組みの本文であり抄録ではない。BICS/CALPの定義と課題の相対性は前バッチのCummins本人の著者稿も照合。

CLILの内容と言語の二重焦点、内容から言語要求を分析する設計、授業前の支援計画と授業中に生じる言語使用を区別。「すべての言語を先に学んでから内容」「初級者の思考活動は一切排除」「CALPは書き言葉専用」という誤った読みを排除。4CsはContent/Communication/Cognition/Cultureと明示し、日本語の「言語」だけでCommunicationを表す曖昧さを修正。応用問はケース14の資料読解・対話・国との比較レポートの設定に照合し、学習機会の設計と全員への効果保証を区別した。未取得の引用先介入研究や全CLIL実践の成果を承認したわけではない。

累積稿の再構成が、旧語を含む正当な展開「内容→内容（Content）」で停止した。既存の置換関数の「旧部分文字列が残っていない」アサートが原因で、旧作業稿は原子的保存により保護された。関数を「置換前の前後部分＋新本文」の完全一致検証へ修正し、分割run・旧語を含む新語・対象不存在・重複拒否の回帰検査を追加。初期applyの再実行ではなく、補助関数のみ修正して累積再構成を再実行した。失敗時に後続シェル命令が進んだ最初のqa127描画は旧稿なのでQAから明示的に除外し、qa127-fixedへ再構成済み稿を新規描画した。全変更文字列の存在も確認し、旧描画や台帳だけで改訂反映済みとは扱わない。

確認済み328・修正必要30・要追加確認142、残172問。累積329問2770箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。500問の構造・キー/タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件、置換関数回帰4条件を通過。警告96件：Q_O_068の正解解説の「全員の向上を保証する実験結果ではない」をP1が検出した1件追加。正答と効果保証の留保は整合し、誤検出を避けるための留保削除はしない。
'''
report+=f'\nNoto Sans JPで再構成後の新規{pagecount}頁描画、27変更文字列を全検出。'+ '・'.join(map(str,reviewed))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。隣接箇所の改頁を含む全頁最終QAと残172問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第127バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第127バッチ S191・S190再利用（2026-10-16）

S191 Bower, Cross and Coyle, *CLIL in Multilingual and English-Background Contexts*, in *Curriculum Integrated Language Teaching: CLIL in Practice*。[出版社公開章抜粋](https://assets.cambridge.org/97811087/29734/excerpt/9781108729734_excerpt.pdf)、ISBN9781108729734。印刷9〜11/PDF8〜10の定義・4Cs・Language Triptych本文と画像を精読。提唱者Coyleを含む著者による概念枠組みの一次説明として使用し、引用先個別実験の実証結果を独立に再検証したとはしない。抜粋以外の全章・全書籍・全学習者への効果は未承認。S190はCALPの口頭/書面と課題の相対性を再利用。取得範囲・原バイトSHA256はevidence/batch127_sources.json。原PDFは非転載。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第127バッチ\n'+f'qa127旧稿描画を除外、qa127-fixedでNoto Sans JP新規{pagecount}頁、全27変更文字列を検出。直接目視・完全読込み頁：'+ '・'.join(map(str,reviewed))+'。変更箇所の欠字・重なり・文字切れなし。全頁最終目視は未完了。\n')
e=dict(batch=127,base_commit='73a24c1f5086625e516ad3f4ab397bcbe1e729bb',fully_rejudged=ids,edits=27,independent_answers=dict(zip(ids,[1,4,2])),sources=['S190','S191'],status_counts=m['status_counts'],remaining=172,machine_warnings=96,new_warnings=newflags,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},source_images={'S191_PDF':[8,9,10]},excluded_render='qa127: old draft after replacement assertion failure; not used as QA',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch127_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('328 confirmed/172 remaining;27 edits recorded',reviewed)
