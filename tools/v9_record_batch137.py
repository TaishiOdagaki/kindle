"""Record batch 137 after direct visual review of every changed page."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa137';targets={'Q_4_087','Q_MO_003'}
def oldfile(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(oldfile('ledger.csv'));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':340,'修正必要':19,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch137.json').read_text());assert len(cs)==18
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('338問','340問').replace('21問','19問').replace('337問2856箇所','339問2874箇所').replace('337問を部分修正','339問を部分修正');f.write_text(s)
report='''

## 第137バッチ（2026-10-17）

Q_MO_003とQ_4_087を全4肢・全4解説と設問の計18箇所改訂。独立正答はそれぞれ2・4で変更なし。S99の署名付きBritish Council記事を再取得・本文精読し、メニューの文字を解読することと、写真から場面の知識を活性化して会話内容を予測することを区別した。共通ケースは改変せず、当該設問に使用条件を明示。画像提示なら常にトップダウン処理という一般化を避け、実際の聴解の両処理の併用も説明。著作権法上の適法性の承認は行っていない。

S199は早稲田大学ライティング・センター教員スタッフ監修の記事本文。定義、レポート・論文作成上の注意点、六つのポイント、引用の作法を精読。学習領域を維持し、論証するレポートでの問い・主張・根拠と他者の言の区別を問う形に改訂。「私は思う」等の主観表現や丁寧体が一律不可との未照合一般化は撤回。記事中の引用分類の独自の説明は採用せず、分野を超える一律の書式規範にもしていない。参考文献の書籍は未取得であり取得済みとは扱わない。

確認済み340・修正必要19・要追加確認141、残160問。累積339問2874箇所。全500問を維持。台帳原文はv8のスナップショットで、改訂はchangesと作業稿を参照。v8不変、500問の構造・正解・タグ・早見表・リンク、影響外本文の不変を再検査。公開判定回帰8条件、置換回帰4条件を通過。警告98件は前回と完全一致。unittestの探索では関数形式の回帰を検出しなかったため、正規のスクリプト実行で明示的に再検査した。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全18変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。documentsと既存校正手順に従った変更範囲のQAであり、全頁の最終目視は未完了。残160問の学術照合も未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第137バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第137バッチ S99再取得 S199（2026-10-17）

- S99 Catherine Morley [Listening Top-down and bottom-up](https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/listening-top-down-and-bottom)。署名付き記事本文全体を再取得・精読。Q_MO_003の背景知識・写真による予測、音声解読との併用を照合。実証的な効果量や常時優位性は承認しない。参考文献原著は未取得。
- S199 早稲田大学 [アカデミック・ライティング力を磨こう](https://www.waseda.jp/inst/weekly/feature/2014/06/23/20860/)、2014年6月23日、ライティング・センター教員スタッフ監修。定義・作成上の注意・六つのポイント・引用作法を含む本文取得。Q_4_087の主張の根拠、構成、問いと答え、出典と自分の言の区別を照合。記事中の独自の引用分類や一般的な文体の禁止規範は採用していない。書誌のみの参考書は未取得、現在のセンターサービスも監査対象外。

取得原バイトのSHA256と照合範囲はevidence/batch137_sources.json。原文は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=137,base_commit='d88b464f87ca474589e174d9bc562937e3edfe71',fully_rejudged=sorted(targets),edits=18,independent_answers={'Q_4_087':4,'Q_MO_003':2},sources=['S99','S199'],status_counts=m['status_counts'],remaining=160,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch137_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('340 confirmed / 160 remaining',pages)
