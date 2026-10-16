"""Record batch107 only after direct inspection of its six changed pages."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');render=Path('/workspace/scratch/697c245d9771/batch107_qa');targets={'Q_4_013','Q_4_026'}
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
assert not removed and len(machine['issues'])==67 and added==[['P1','Q_4_026','(正)3の解説が否定で終わる/肯定の(誤)がある: [1, 4]']]
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':277,'修正必要':40,'要追加確認':183}
cs=json.loads((p/'changes_batch107.json').read_text());assert len(cs)==15
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1]
norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[58,63,64,256,257,262]
for n in reviewed:
 with Image.open(render/f'review-{n}.png') as im:im.load()
f=p/'README.md';s=f.read_text()
for a,b in [('275問','277問'),('41問','40問'),('184問','183問'),('281問2405箇所','282問2420箇所'),('281問を','282問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第107バッチ（2026-10-16）

Q_4_013・026の設問・全4肢・独立正答・全4解説を、S11国際交流基金の公式HTML本文3ページと照合した。活動Can-doを問う設問と、文法等を含む能力Can-doの区別を明示。文法や語彙を不要とする一般化、Can-doをそのままルーブリックとする表現、必ず自己評価能力を高めるという効果の断定を避けた。Q_4_026の注文例は本問独自であり、公式引用・レベル認定とはしない。正答番号は2・3で変更なし。変更していないQ_4_013の3肢も、暗記量のみ・正確さのみ・教授順の固定が活動目標と対応しないことを本文に照合した。

2問15箇所を改訂。確認済み277・修正必要40・要追加確認183、残件223。累積282問2420箇所、全500問を維持。台帳原文はv8スナップショットで、改訂本文はchangesと作業稿を参照する。公式ページの当該概念・活用例の範囲を照合し、CEFR全巻、全レベルの各例、効果検証研究を取得・承認したとはしない。

全500問の構造・キー・タグ・早見表・リンク、影響外本文、v8不変ハッシュを検査。公開可否の回帰8条件合格。機械警告66→67で新規P1はQ_4_026の正答解説末尾「公式引用・レベル認定ではない」という留保を検出した誤検出。その他66件は同一。documents手順でNoto Sans JP適用QAコピー402頁を描画、全15変更文字列をPDFで検出し、58・63・64・256・257・262頁の画像を直接目視。対象部分に欠字・重なり・切れは見られない。Q_4_026の肢やQ_4_013の解説は頁をまたいでおり、最終組版で調整する。全頁最終目視と残223問の学術確認は未完了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第107バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第107バッチ S11追加照合（2026-10-16）

国際交流基金公式 [Can-doとは](https://www.jfstandard.jpf.go.jp/cando/about/summary/ja/render.do) の定義、種類（活動・テクスト・方略・能力）、言語構造的能力、留意点の言語材料・目標と評価の使い分け・MY Can-doを本文取得・照合。[活用方法](https://www.jfstandard.jpf.go.jp/course/ja/render.do) 全62行の目標・授業・評価の一貫性と必要な語彙・文法の準備、[JFスタンダードとは](https://www.jfstandard.jpf.go.jp/summary/ja/render.do) の目標共有・現場に応じた利用・自己評価（52〜108行）も本文照合。対象Q_4_013・026。検索抜粋だけの承認ではない。画像内の全表や他リンク先、CEFR全冊、実証的効果研究を承認したとはしない。刊年・更新日をフッターのcopyrightや取得日から推定しない。

再取得HTML原バイトをevidence/S11_batch107_about.html.gz・course.html.gz・summary.html.gzに保存、バイト数・SHA256はbatch107_sources.json。注文例は独自作成で公式引用・認定レベルを付与しない。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第107バッチ\nNoto Sans JP適用QAコピー402頁。15変更文字列を検出し、58・63・64・256・257・262頁を直接画像目視・完全読込み。対象部分に欠字・重なり・切れなし。問題・解説の頁分割は最終組版で調整し、全頁最終目視は未完了。\n')
e={'batch':107,'base_commit':'76e7cce7e150c637fa5f0ef01a45c8f0804ada61','fully_rejudged':sorted(targets),'edits':15,'independent_answers':{'Q_4_013':2,'Q_4_026':3},'sources':['S11'],'status_counts':m['status_counts'],'remaining':223,'machine_warnings':67,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'image_scale_to_pixels':1800,'all_changed_strings_found':matches,'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(n):sha(render/f'review-{n}.png') for n in reviewed},'full_visual_qa_completed':False,'release_ready':False}
(p/'evidence/batch107_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('277 confirmed;223 remaining;15 edits/6 pages recorded')
