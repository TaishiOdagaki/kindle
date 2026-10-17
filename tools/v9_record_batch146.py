"""Record batch146 only after direct PNG review."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa146';target='Q_M_028'
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':353,'修正必要':11,'要追加確認':136}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(oldfile('postfix_machine.json'))['issues'];assert len(machine['issues'])==103
added=[x for x in machine['issues'] if x not in prior];assert len(added)==1 and added[0][:2]==['P1',target];assert all(x in machine['issues'] for x in prior)
cs=json.loads((p/'changes_batch146.json').read_text());assert len(cs)==9
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}=={target}
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns});assert pages==[175,382]
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
assert len(PdfReader(r/'qa.pdf',strict=True).pages)==406
f=p/'README.md';s=f.read_text().replace('352問','353問').replace('137問','136問').replace('349問2972箇所','350問2981箇所').replace('349問を部分修正','350問を部分修正');f.write_text(s)
report='''

## 第146バッチ（2026-10-18）

Q_M_028を9箇所改訂し、独立正答1を確定。S209 Larsen-Freeman（1987）From Unity to Diversityの2012年再掲全11頁PDFを米国国務省公式サイトから取得。印刷36–38頁本文・文献を精読し、36–37頁Conclusion全体を画像で照合。全11頁精読ではない。初回37頁画像は不正な画像データのため除外し、単頁再描画版を使用した。

折衷法という用語定義そのものは確認済み扱いせず、教授法の選択・組合せという同じ学習領域で、著者の結論を問う設問へ改訂した。目標・学習者・状況に基づく選択と目的との適合の点検、無作為な混合との区別、万能教授法への留保、教師による選択結果の評価を全4肢・全解説へ照合。著者の1987年の結論であり、2026年現在の効果研究を網羅する総括ではない。

機械警告102→103件。追加P1は正答1の解説末尾「複数の方法を無条件に混ぜればよいという意味ではありません」を正答の否定と取り違えたもの。無作為な混合を否定する限定であり、目的に基づく選択そのものを否定していない。誤答2・4の解説にある著者の正しい立場は、誤答肢を肯定したものでもない。既存102件とともに保持。

確認済み353・修正必要11・要追加確認136、残147問。累積350問2981箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。v8不変、500問の構造・キー・タグ・早見表・リンク・影響外本文、公開判定回帰8条件・置換回帰4条件を検査。Noto Sans JPで406頁を描画し、全9変更文字列を検出。175・382頁を1800px画像で直接目視し、変更箇所の欠字・重なり・文字切れなし。最終全頁QAと残147問の学術照合は未了。最終v9ではなく出版不可。
'''
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第146バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第146バッチ S209（2026-10-18）

- Diane Larsen-Freeman, From Unity to Diversity: Twenty-five Years of Language-Teaching Methodology。English Teaching Forum 25(4), 1987初出、50(2), 2012, 28–38再掲。https://americanenglish.state.gov/files/ae/resource_files/50_2_6_larsen-freeman-pp28-38_0.pdf から全11頁を取得。印刷36–38頁本文・文献を精読し、36–37頁Conclusion全体は画像でも照合。全11頁精読ではない。Q_M_028の目的・状況に基づく教授法選択と結果評価に限定して使用。折衷法の用語定義を確認したものではなく、2026年現在の効果研究の総括でもない。原バイトSHA256・読了範囲はevidence/batch146_sources.json。本文・頁画像は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=146,base_remote_commit='80186ca2b199f9ed43f0021da22a258551d31f08',after_local_batch145_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),fully_rejudged=[target],edits=9,independent_answers={target:1},sources=['S209'],status_counts=m['status_counts'],remaining=147,machine_warnings=103,new_warnings=added,new_warning_review='P1: the correct explanation rejects unconditional mixing, not informed selection; wrong-option explanations describe the author position in order to reject those options.',readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=406,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_page_sha256={'36':sha(root/'larsen145-review-09.png'),'37':sha(root/'larsen146-10.png')},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch146_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('353 confirmed / 147 remaining')
