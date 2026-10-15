"""Checkpoint after direct image review; no automatic scholarly approval."""
import json,hashlib,subprocess,re,io,csv,bisect,gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch103-qa';targets={'Q_4_121','Q_4_127'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':265,'修正必要':41,'要追加確認':194}
cs=json.loads((p/'changes_batch103.json').read_text());assert len(cs)==18
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v});assert reviewed==[100,102,103,299,302]
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert removed==[] and len(machine['issues'])==63 and added==[['P1','Q_4_121','(正)3の解説が否定で終わる/肯定の(誤)がある: [1, 4]']]
raw=gzip.decompress((p/'evidence/egov_batch101.xml.gz').read_bytes());prior_ev=json.loads((p/'evidence/batch101_review.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior_ev['sources']['S26']['sha256']
f=p/'README.md';s=f.read_text()
for a,b in [('263問','265問'),('43問','41問'),('270問2312箇所','271問2330箇所'),('270問を','271問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第103バッチ（2026-10-16）

最新GitHub HEAD 16eb7ad596b286db438d5cf1d6954580f31db78aから別作業場へ復元。公式Creative CommonsのCC BY 4.0日本語リーガルコード全文とコモンズ証全文を取得し、拘束力のある条件はリーガルコードを優先して照合した。Q_4_121をCC BY 4.0のライセンスに基づく共有という対象に限定して改訂。「作者名だけで十分」を撤回し、提供された情報の保持、ライセンス情報・改変表示、合理的な表示方法、他の権利の留保を区別した。OER一般や別ライセンスへ同じ条件を一律適用しない。

Q_4_127は保護期間内の創作的な公表素材と、誤答肢では許諾・権利制限の根拠がない前提を明示。第32条第1項の公正慣行・引用目的上正当な範囲と、第48条の出所・著者名の表示を区別した。短さ・出所表示だけで引用の成立を承認しない。録音の複製と公衆送信は口述と分け、市販音源の実在事実や全ての無許諾公開利用への一般化を除いた。根拠は第101バッチ保存済みe-Gov応答を原SHA256一致で再利用した。

2問の設問・全4肢・独立正答・全4解説を照合、18箇所改訂。独立正答4_121=3・4_127=2、番号変更なし。確認済み265・修正必要41・要追加確認194、残件235。累積271問2330箇所。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照する。

全500問・解説500件、v8不変ハッシュ、影響外本文、正解表・タグ・リンクを維持し、公開可否回帰8条件合格。機械警告62→63件。新規4_121のP1は、正答解説末尾の「人格権・プライバシー等まで一律に許諾する規定ではない」という正確な限定を検知した誤検出。残る62件は同一。documents手順でNoto Sans JP適用QAコピー{len(pages)}頁を描画、18変更文字列を検出し、100・102・103・299・302頁を150dpi画像で直接目視。4_127の設問・選択肢1～2は102頁、選択肢3～4と戻るリンクは103頁へ分離しており最終組版で要調整。4_121は100頁に全4肢、両問の全4解説は299・302頁に収まり、欠字・重なり・クリッピングは見られない。全頁最終目視・残235問の根拠照合は未了、出版不可で最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第103バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第103バッチ S162 / S26（2026-10-16）

### S162 Creative Commons CC BY 4.0 日本語公式本文
- [リーガルコード全文](https://creativecommons.org/licenses/by/4.0/legalcode.ja) を取得・全文読了。Q_4_121は第2条a項1号の複製・共有・翻案、第2条a項2号の例外・権利制限、第2条b項の他の権利、第3条a項の提供情報保持・改変表示・ライセンス情報・合理的方法を中心に照合。
- [コモンズ証全文](https://creativecommons.org/licenses/by/4.0/deed.ja) も取得・読了。商用目的を含む共有・改変の説明を補助に用い、証自体がライセンスではないという留保を守る。
- 第3条a項1号Cはライセンス本文又はURI・ハイパーリンク。必ずURLの一方式だけとせず、第3条a項2号の合理的方法、第3号の情報除去要請も含めて本文を確認。旧版にある作品タイトル表示を第4.0版の一律必須条件としない。全OER・他CCライセンス・権利者が許諾権限を持たない権利へ一般化しない。取得HTMLのハッシュと範囲はevidence/batch103_review.json。

### S26 保存済みe-Gov本文の追加照合
[著作権法API](https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048) の第101バッチ保存応答をSHA256同一性検証の上再利用。本則第2条第1項第15号・第21・23・24・32・48条をQ_4_127と照合。第32条の実体要件と第48条の出所表示、録音による複製と公衆送信、口述を区別した。全裁判例・全法改正経過措置の監査とはしない。追加条文抜粋はevidence/egov_batch103_excerpts.txt。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第103バッチ\nNoto Sans JP適用QAコピー{len(pages)}頁。18変更文字列を検出し100・102・103・299・302頁を150dpi画像で直接目視。4_127は選択肢2/3間の改頁を最終組版で調整する。全頁最終目視は未了。\n')
e={'batch':103,'base_commit':'16eb7ad596b286db438d5cf1d6954580f31db78a','fully_rejudged':sorted(targets),'edits':18,'status_counts':m['status_counts'],'remaining':235,'independent_answers':{'Q_4_121':3,'Q_4_127':2},'sources':{'S162':{'urls':['https://creativecommons.org/licenses/by/4.0/legalcode.ja','https://creativecommons.org/licenses/by/4.0/deed.ja'],'retrieved':'2026-10-16 JST','legalcode_html_sha256':sha(root/'S162-103-legal.html'),'deed_html_sha256':sha(root/'S162-103-deed.html'),'scope':'Both complete texts read; legalcode sections 2,3 govern decision; not all OER or other licenses'},'S26':{'source_reuse_not_new_acquisition':True,'source_raw_sha256':hashlib.sha256(raw).hexdigest(),'archive':'evidence/egov_batch101.xml.gz','scope':['2.1.15','21','23','24','32','48']}},'machine_warnings':63,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'pagination_followup':'Q_4_127 stem/options1-2 page102; options3-4/link page103, requires final pagination adjustment. Full visual QA incomplete.','release_ready':False}
(p/'evidence/batch103_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 2 full reviews /18 edits;265 confirmed/235 remaining;400 pages rendered')
