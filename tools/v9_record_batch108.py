"""Record scholarly and visual review of the three Schon questions."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');render=Path('/workspace/scratch/697c245d9771/batch108_qa');targets={'Q_4_001','Q_4_004','Q_4_083'}
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
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']))
added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert not removed and len(machine['issues'])==69 and added==[['P1','Q_4_001','(正)4の解説が否定で終わる/肯定の(誤)がある: [1, 2]'],['P1','Q_4_083','(正)4の解説が否定で終わる/肯定の(誤)がある: [2, 3]']]
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':280,'修正必要':39,'要追加確認':181}
cs=json.loads((p/'changes_batch108.json').read_text());assert len(cs)==28 and sum(x.get('remove_paragraph',False) for x in cs)==1
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1]
norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 if not c['after']:continue
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[53,54,55,84,251,252,284]
for n in reviewed:
 with Image.open(render/f'review-{n}.png') as im:im.load()
f=p/'README.md';s=f.read_text()
for a,b in [('277問','280問'),('40問','39問'),('183問','181問'),('282問2420箇所','285問2448箇所'),('282問を','285問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第108バッチ（2026-10-16）

Schön原著の公開複製380頁PDFを通常取得し、21・40・61〜63頁を本文・版面照合した。Q_4_001・004・083の設問・全4肢・独立正答・全4解説を改訂して再判定。技術的合理性を「固定教案の機械的適用」と同一視する誤説明を、科学的理論・技術を適用する問題解決モデルと、問題設定を含む省察との区別へ修正した。行為の中の省察を常に瞬時の判断に限らず、実践に応じた時間幅を明示。Q_4_004は変更だけで省察・成功を決めず、理解の捉え直しと試行を架空事例に明記。経験や科学的知識の利用を全面否定しない。効果の実証・知識を得る唯一の方法という断定も避けた。

3問の27フィールド修正と旧設問継続段落1件の明示削除、計28箇所。独立正答はいずれも4、番号変更なし。確認済み280・修正必要39・要追加確認181、残件220。累積285問2448箇所、全500問を維持。台帳原文はv8のスナップショットで、改訂本文はchangesと作業稿を参照する。原著の当該範囲の照合であり、全380頁の精読・全主張の承認ではない。

全500問・解説500件、正答番号・タグ・早見表・リンク、影響外本文、v8不変ハッシュを検査。公開可否の回帰8条件合格。機械警告67→69、新規Q_4_001・083のP1は、正答解説末尾の効果保証等を否定する留保を検出した誤検出。他67件は同一。documents手順でNoto Sans JP適用QAコピー401頁を新規描画、27変更後文字列をPDFで検出し、53・54・55・84・251・252・284頁を直接画像目視。対象部分に欠字・重なり・切れなし。Q_4_001の問題が頁をまたぐ等の最終組版調整、全頁最終目視、残220問の学術確認は未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第108バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第108バッチ S166（2026-10-16）

Donald A. Schön, The Reflective Practitioner How Professionals Think in Action（著作権表記1983、Basic Books後刷の公開複製）[原著PDF](https://www.socialworkerskills.eu/uploads/1/4/4/7/144711219/sch%C3%B6n_d._a.__1983_._the_reflective_practitioner.pdf)。全380頁・28811364バイトを通常取得。Web抽出は容量上限だったがローカルで原PDFを取得して本文と画像を照合。印刷21頁（PDF30）の技術的合理性、40頁（PDF49）の問題設定、61〜63頁（PDF70〜72）の過度の習熟による固定・振り返り・action-present・対象・試行を精読。表題PDF3頁も画像確認。周辺49〜60頁の本文も参照したが、全冊・周辺全頁の完全精読とは扱わない。原著の他研究への言及を、その引用元研究の取得と混同しない。2018年スキャン日を刊年にしない。本文は再配布せず、ハッシュ・頁対応・照合範囲をevidence/batch108_source.jsonに保存。

対象Q_4_001・004・083。日本語授業の変更例は本問独自の適用例で、原著掲載の実験事例ではない。省察の唯一性や教授効果を普遍的に承認しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第108バッチ\nNoto Sans JP適用QAコピー401頁。27変更後文字列を検出し、53・54・55・84・251・252・284頁を直接画像目視・完全読込み。対象部分に欠字・重なり・切れなし。旧設問継続段落1件の削除も再構成で検査。問題の頁分割等は最終組版で調整し、全頁最終目視は未完了。\n')
e={'batch':108,'base_commit':'d813798f55576d4f372a1fe56196a594e0371399','fully_rejudged':sorted(targets),'edits':28,'field_edits':27,'removed_stem_continuations':1,'independent_answers':{k:4 for k in targets},'sources':['S166'],'status_counts':m['status_counts'],'remaining':220,'machine_warnings':69,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'image_scale_to_pixels':1800,'all_changed_strings_found':matches,'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(n):sha(render/f'review-{n}.png') for n in reviewed},'full_visual_qa_completed':False,'release_ready':False}
(p/'evidence/batch108_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('280 confirmed;220 remaining;28 edits/7 pages recorded')
