"""Record two complete question reviews after review of the final batch109b render."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/697c245d9771/batch109b_qa');targets={'Q_4_003','Q_4_007'}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');reader=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(reader)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==69
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':282,'修正必要':39,'要追加確認':179}
cs=json.loads((p/'changes_batch109.json').read_text());assert len(cs)==15
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[54,56,252,253,254]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
f=p/'README.md';s=f.read_text()
for a,b in [('280問','282問'),('181問','179問'),('285問2448箇所','287問2463箇所'),('285問を','287問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第109バッチ（2026-10-16）

Q_4_003とQ_4_007の設問・全4肢・独立正答・全4解説を一次本文へ照合し、計15箇所を改訂した。Q_4_003はRichards・Farrell2005の出版社公開第1章抜粋1〜10頁を読了し、特に2〜4頁の知識更新・協働・個人と機関の支援へ対応させた。アクション・リサーチ第12章を未取得のまま特定サイクルや主要性まで承認せず、同じ専門性開発領域の本文に即して改訂。Q_4_007はBorg本人の2003年総説81〜82頁の枠組みと図1、91頁の要約を版面照合。信念が全行動を一方向に規定する断定、理論を聞くだけでは変わらないという一律化、省察すれば無意識の偏見から解放されるという未裏付けの効果主張を除いた。総説に引用される各実証研究や1997年図の初出を別途取得済みとは扱わない。

独立正答Q_4_003=2・Q_4_007=1、番号変更なし。確認済み282・修正必要39・要追加確認179、残件218。累積287問2463箇所、500問維持。台帳原文はv8スナップショットであり、改訂本文はchangesと作業稿を参照する。

全500問の構造・正答番号・タグ・早見表・リンク・影響外本文・v8不変ハッシュを検査。公開可否回帰8条件合格、機械警告69件は前回と同一。documents手順で全15修正を反映した新しいNoto Sans JP適用QAコピー401頁を描画し、全変更文字列を検出、54・56・252・253・254頁を直接画像目視・完全読込み。前半だけの旧batch109_qaは最終検査証拠に使わない。対象部分に欠字・重なり・切れなし。Q_4_007解説の頁分割など最終組版の調整、全頁最終目視、残218問の学術確認は未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第109バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第109バッチ S167・S168（2026-10-16）

- S167 Richards・Farrell（2005）, Professional Development for Language Teachers Strategies for Teacher Learning。[出版社公開抜粋](https://assets.cambridge.org/97805218/49111/excerpt/9780521849111_excerpt.pdf)全10頁を通常取得・本文読了、2〜4頁を画像照合。[出版社書誌](https://www.cambridge.org/core/books/professional-development-for-language-teachers/6CD2038A178603982F4FFE8AFC44A22D)で印刷版2005-04-04とオンライン2010-02-01を区別。第1章全22頁のうち1〜10頁だけの取得であり全書・第12章・引用先研究の取得ではない。Q_4_003の承認範囲は継続的学習・知識更新・共有・個人と機関の支援。ハッシュはbatch109_source.json。
- S168 Simon Borg（2003）, Teacher cognition in language teaching A review of research on what language teachers think know believe and do, Language Teaching36(2),81–109。[所属大学リポジトリ公開原文](https://eprints.whiterose.ac.uk/1652/1/borgs1_language_teaching_36-2.pdf)、DOI10.1017/S0261444803001903。全30PDF頁を取得、原著81〜82頁（PDF2〜3）の定義・枠組み・図1と91頁（PDF12）の要約を本文・画像照合。Q_4_007はBorgが提示する整理に限定。研究史全体・全論文・全30頁を精読承認したとはしない。図1の1997年初出、引用先の全個別実証研究は未取得。原著者自身による総説の枠組みと、個別の因果・介入効果の証明を区別。ハッシュ・範囲はbatch109_source_borg.json。

資料本文は再配布せず、取得バイト数・ハッシュ・URL・照合範囲を保存する。検索抜粋だけでの承認ではない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第109バッチ\n最終batch109b稿のNoto Sans JP適用QAコピー401頁。全15変更文字列を検出、54・56・252・253・254頁を直接画像目視。対象部分に欠字・重なり・切れなし。前半稿のQAは使用しない。解説の頁分割と全頁最終目視は未完了。\n')
e=dict(batch=109,base_commit='ef39dfa649297d8373104fe337e30059b343d0e3',fully_rejudged=sorted(targets),edits=15,independent_answers={'Q_4_003':2,'Q_4_007':1},sources=['S167','S168'],status_counts=m['status_counts'],remaining=218,machine_warnings=69,machine_warnings_unchanged=True,readiness_gate='8 cases passed',render_pages=len(pages),visually_reviewed_pages=reviewed,image_scale_to_pixels=1800,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch109_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('282 confirmed/218 remaining;15 edits/5 pages recorded')
