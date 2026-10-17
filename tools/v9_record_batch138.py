"""Record bounded historical-material audit after changed-page image review."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa138';target='Q_1_023'
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
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k==target else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':341,'修正必要':18,'要追加確認':141}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==98
cs=json.loads((p/'changes_batch138.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={target}
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 with Image.open(r/f'review-{n}.png') as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('340問','341問').replace('19問','18問').replace('339問2874箇所','339問2883箇所');f.write_text(s)
report='''

## 第138バッチ（2026-10-17）

Q_1_023を9箇所改訂し独立正答4を確定。S200渡邉俊彦（2015）の対訳教材の分析論文を含む紀要全312頁を取得し、当該論文の印刷170–178頁（PDF181–189頁）の本文・教材例を精読。印刷177–178頁では1895年教授書からの引用と前後の解釈を画像でも確認した。設問は取得した教材分析の説明を問う条件に限定し、台湾語の媒介利用、日本語理解の支援、日本語の語順・表現からの影響を全4肢・全4解説に照合した。台湾語を一切排除する直接法との混同を避けた。

1895年教授書の全冊そのものは未取得。書誌や論文中の引用だけを原著全冊の取得・精読とは扱わない。元問の学堂の設立年、事件の経緯、後続制度への発展などは今回の教材分析で全てを検証した扱いにはせず撤回。Q_1_006には中国留学生向けの機関・旧満州の言語政策・学堂史などの残存主張があり、同じ対訳法の根拠を得ただけで確認済みへ変更しない。大学博物館の所蔵資料紹介ページも閲覧したが、評価的な歴史叙述を無批判に採用せず、今回の全問承認根拠には使用していない。

確認済み341・修正必要18・要追加確認141、残159問。累積339問2883箇所。500問維持、v8不変、構造・正解・タグ・早見表・リンク・影響外本文の不変を再検査。公開判定回帰8条件と置換回帰4条件を通過。警告98件は前バッチと完全一致。台帳の原文はv8スナップショットで改訂本文はchangesと作業稿を参照。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画。全9変更文字列を検出し、'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所に欠字・重なり・文字切れなし。documentsと既存校正手順に従った変更範囲QA。全頁最終目視および残159問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第138バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第138バッチ S200（2026-10-17）

渡邉俊彦（2015年3月）「対訳日本語教材における伊沢修二の教育観とその台湾語の文体」『拓殖大学語学研究』132、169–193頁。[大学公開の第132号全文PDF](https://journal.takushoku-u.ac.jp/lcri/lcri_132.pdf)全312頁を取得・全頁テキスト読込み。精読範囲は印刷170–178頁（PDF181–189頁）：背景、対訳例、用途、台湾語の媒介利用と語順の影響、1895年教授書の引用とその解釈。印刷177–178頁は日本語の正常な画像描画でも確認。原文は転載しない。

Q_1_023はこの取得済み教材分析に合う説明を問う条件へ改訂し、全4肢・全4解説を照合。論文の他の章や他論文の全精読を完了したとはしない。1895年教授書全冊は未取得であり、原著全冊の全主張の承認に代用しない。引用される1900年資料の全冊や、学堂事件史の全照合もしていない。Q_1_006は残存主張未照合のため修正必要を維持。原バイトSHA256、取得頁数・精読範囲はevidence/batch138_sources.json。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=138,base_commit='75059be091618b69dcb836e97404889b89de4ee9',fully_rejudged=[target],edits=9,independent_answers={target:4},sources=['S200'],status_counts=m['status_counts'],remaining=159,machine_warnings=98,new_warnings=[],readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_page_sha256={str(n):sha(root/f'takushoku132-{n}.png') for n in [188,189]},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch138_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('341 confirmed / 159 remaining',pages)
