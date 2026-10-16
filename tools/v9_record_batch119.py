"""Record recovered batch119 after fresh machine and changed-page review."""
import json,hashlib,subprocess,io,csv,re
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path(__file__).resolve().parents[2]/'qa119'
ids=['Q_1_039','Q_O_010','Q_M_030']
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':311,'修正必要':35,'要追加確認':154}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']]
assert len(machine['issues'])==88 and len(added)==1 and added[0][:2]==['P1','Q_1_039'] and all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch119.json').read_text());assert len(cs)==12
matches=json.loads((r/'matches.json').read_text());assert len(matches)==12
changed=sorted({n for vs in matches.values() for n in vs});assert changed==[21,176,219,347,381]
reviewed=sorted(changed+[22])
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
text=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode();assert len(text.split('\f')[:-1])==404
whole=re.sub(r'\s+','',text)
for c in cs:assert re.sub(r'\s+','',c['after']) in whole
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']))
assert {k for k in d if d[k]!=old_d[k]}==set(ids)
f=p/'README.md';s=f.read_text()
for a,b in [('308問','311問'),('36問','35問'),('156問','154問'),('311問2625箇所','314問2637箇所'),('311問を','314問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第119バッチ（2026-10-16）

保存済み第118バッチ72fb1ffから、消失した一時作業場の未保存3問12箇所を会話の判断履歴に基づき再構成。過去の全500問判定や初期applyは再実行しない。CEFR原PDFとTKT公式用語集を再取得し、第116・118バッチのSHA256と一致。Q_1_039・Q_O_010・Q_M_030の設問・全4肢・独立正答・全4解説を照合。正答4・1・2を維持。

Q_1_039はCEFR2001年版1.3（印刷4〜5頁）、2.1（9〜10頁）、3.2図1・3.3・3.4冒頭（23〜25頁）へ対応。母語話者を唯一の最終モデルとせず、社会的行為者・具体的な言語活動とA1〜C2を説明。2001年版の共通参照レベルを明示し、下位区分・記述調整や文法に焦点を当てる学習・評価を全面禁止する説明にしない。原著の当該頁は前の作業場で本文と画像を直接精読済み。今回同一原バイトを再取得して同定した。全冊や引用先研究の承認ではない。

Q_O_010はケース2全3段落と設問の仮定を確認。診断を開始前に限定する解説4を直し、弱点等の診断的情報を途中の指導調整に使う形成的利用との併存を認める。Q_M_030はTKT AssessmentのPeer/Self/Diagnostic/Summativeへ全肢・全解説を照合。診断の時期限定を除去し、評価目的と評価主体を分ける。総括・診断とピア評価が併存し得る。未照合の対照分析の補助定義は同じ評価領域の自己評価へ差し替えた。

確認済み311・修正必要35・要追加確認154、残件189。累積314問2637箇所、500問維持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。全500問の構造・正答タグ/表/リンク・影響外本文・v8不変、公開可否回帰8条件を再検査して通過。警告87→88。新規P1はQ_1_039の下位区分・記述調整を禁じない留保への誤検出で、正答4の否定ではない。他87件と検出器を維持。

documents手順で日本語字形を確認したNoto Sans JPを用い、新規404頁を描画。全12変更文字列を検出し、21・176・219・347・381頁および正答肢を含む22頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。Q_1_039の正答肢の次頁分離、Q_O_010の見出し/正答と解説の分離を最終組版課題に残す。前の消失した描画はQA根拠に流用しない。全404頁最終目視と残189問の学術照合は未完了。公開不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第119バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第119バッチ S179・S183再取得と追加照合（2026-10-16）

S179 [CEFR2001公式原著](https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf)の印刷4〜5/PDF13〜14、9〜10/PDF18〜19、23〜25/PDF32〜34を本文・画像照合。3.2図1・3.3・3.4冒頭と1.3・2.1の範囲を使用。途中の欠損PNGは除外し、単頁再描画やpdftocairoで有効画像を読んだ。9.3.2と9.3.5は既取得範囲を再利用。S183 [Cambridge TKT公式用語集](https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf)の印刷4〜5/PDF5〜6のAssessment各定義（Peer/Self/Diagnostic/Formative/Summative）を第118バッチ本文・画像照合から再利用。今回両原PDFを再取得して保存済みSHA256と一致を確認。刊年・現行仕様を推定しない。本文の全転載・全冊翻訳や引用先研究の取得ではない。原バイトURL・ハッシュ・範囲はevidence/batch119_sources.json。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第119バッチ\n作業場消失後に新規Noto Sans JP描画404頁。全12変更文字列検出。21・22・176・219・347・381頁を1800px画像で直接目視・完全読込み。変更箇所に欠字・重なり・文字切れなし。Q_1_039正答肢、Q_O_010見出し/正答と本文の頁分割は最終組版課題。全頁最終目視は未完了。\n')
e=dict(batch=119,base_commit='72fb1ff0b41e42e0816b784ac40f7d1b59c17b83',recovered_after_workspace_loss=True,fully_rejudged=ids,edits=12,independent_answers=dict(zip(ids,[4,1,2])),sources=['S179','S183'],status_counts=m['status_counts'],remaining=189,machine_warnings=88,new_warnings=added,new_warning_judgment='P1 false positive: permission for finer levels not denial of correct option4',readiness_gate='8 cases passed',render_pages=404,visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch119_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('311 confirmed/189 remaining;12 edits/6 reviewed pages recorded')
