"""Record independently reviewed business Japanese item and changed-page QA."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');r=Path(__file__).resolve().parents[2]/'qa131'
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_M_036' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':334,'修正必要':25,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch131.json').read_text());assert len(cs)==9
oldcs=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']));assert json.loads((p/'changes.json').read_text())==oldcs+cs
d=json.loads((p/'decisions.json').read_text());old_d=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/decisions.json']));assert {k for k in d if d[k]!=old_d[k]}=={'Q_M_036'}
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text()
for a,b in [('333問','334問'),('26問','25問'),('334問2815箇所','335問2824箇所'),('334問を','335問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第131バッチ（2026-10-17）

Q_M_036の設問・全4肢・全4解説を9箇所改訂し、独立正答4を確定。BJT実施団体の公式説明と発言聴解セクション2の設問・解説本文を照合した。あいさつを初級生活場面の内容としてビジネス日本語から切り離した解説を撤回。職場の相手・場面に応じてやり取りするコースという条件を明示し、文学・旅行・あいさつの価値を一般的に否定せず、目標に必要な職場の練習を除く点で誤答を判定した。練習の効果保証、全職種の必須内容、BJTによる産出技能の直接測定は主張しない。

確認済み334・修正必要25・要追加確認141、残166問。累積335問2824箇所、500問維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。500問の構造・キー・タグ・表・リンク、影響外本文、v8不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。警告98件は前バッチと完全一致。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全9変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。全頁最終目視と残166問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第131バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第131バッチ S194（2026-10-17）

公益財団法人日本漢字能力検定協会のBJT公式 [特徴＆メリット](https://www.kanken.or.jp/bjt/about/feature_merit.html) 冒頭の測定対象説明と、[第1部聴解サンプル](https://www.kanken.or.jp/bjt/sample/sample01.html) の発言聴解セクション2の取引先初面会・商品紹介の設問および公開解説本文を取得・精読。Q_M_036のあいさつの位置付けと相手・場面に応じた表現選択の範囲に使用。音声・写真・全サンプル項目は未照合。個別敬語説明の全命題、就職効果、在留資格・点数の法的要件は承認対象に含めない。原資料の問題文は転載せず、学習内容について独自に改訂。原バイトSHA256と使用範囲はevidence/batch131_sources.json。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=131,base_commit='e3b3edc9f1a48353b179918951e537fde0a3826e',fully_rejudged=['Q_M_036'],edits=9,independent_answers={'Q_M_036':4},sources=['S194'],status_counts=m['status_counts'],remaining=166,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch131_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('334 confirmed / 166 remaining',pages)
