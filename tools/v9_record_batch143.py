"""Record metonymy and conjugation-form teaching-source audit after visual QA."""
import json,hashlib,subprocess,io,csv
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa143';targets={'Q_M_057','Q_M_052'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':350,'修正必要':12,'要追加確認':138}
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(oldfile('postfix_machine.json'))['issues'] and len(machine['issues'])==99
cs=json.loads((p/'changes_batch143.json').read_text());assert len(cs)==16
assert json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==16 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('| 確認済み | 348問 |','| 確認済み | 350問 |').replace('修正必要14問','修正必要12問').replace('| 修正必要 | 14問 |','| 修正必要 | 12問 |').replace('345問2938箇所','347問2954箇所').replace('345問を部分修正','347問を部分修正');f.write_text(s)
report='''

## 第143バッチ（2026-10-18）

Q_M_057・Q_M_052を16箇所改訂し、正答3・3を独立確定。国際交流基金ソウル日本文化センターの山口敏幸署名教材「日本語あれこれ(3) 換喩（メトニミー）」全4頁を取得。日本語本文全節・注記を抽出本文と全頁画像で精読し、定義と日常使用（1頁）、乗り物で警官を表す白バイの用例（3頁）、場所で政界を表す永田町の用例と部分全体の分類差の注3（4頁）を照合。韓国語対訳の独立監査ではない。引用元の佐藤信夫書籍全冊は未取得であり、取得済みとしない。

白バイは車両そのものの語義ではなく、文中でそれに乗る警官を表す用例と明確化。「部分や関連物で全体」を普遍的な分類基準として一括する前提は撤回。維持した選択肢3・解説3を含め全4肢・全4解説を本文へ照合した。別の原著候補の機関リポジトリは429で取得できず、当該原著未取得のまま承認したものではない。

連用形は東京外国語大学言語モジュール「普通形の体系」カードの全3表を取得・読了。表2の読む・食べるの行で辞書形・連用形・た形・て形を照合。元の語形成と連用形という学習領域および「読み方」「食べ物」の2例を保ち、動詞と連用形の語形対応を問う形へ変更。派生／複合の分類差を未取得理論で解決したと主張せず、2語を一律に複合語と分類する設問前提を撤回した。

確認済み350・修正必要12・要追加確認138、残150問。累積347問2954箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。v8不変・500問構造・キー・タグ・早見表・リンク・影響外本文の不変検査、公開判定回帰8条件・置換回帰4条件を通過。機械警告99件で増減なし。
'''
report+=f'\nNoto Sans JPで新規{pagecount}頁描画し、全16変更文字列を検出。'+ '・'.join(map(str,pages))+'頁を1800px画像で直接目視・完全読込み。変更箇所の欠字・重なり・文字切れなし。既存校正・documents手順で変更範囲を検査。全頁最終目視および残150問の学術照合は未完了。出版不可、最終v9ではない。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第143バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第143バッチ S206 S207（2026-10-18）

- S206 山口敏幸（国際交流基金ソウル日本文化センター日本語教育アドバイザー）「日本語あれこれ(3) 換喩（メトニミー）」『カチカチの声』119号、2017年2月。[公式PDF全4頁](https://www.jpf.or.kr/index/data/file/publish/3555240129_sHYuZjeG_201702.pdf)を取得し、日本語本文全節・注記を抽出本文と全頁画像で精読。1頁の定義・日常使用、3頁の白バイ、4頁の永田町・注3の分類差をQ_M_057全体へ照合。韓国語対訳の独立監査、引用元書籍全冊の取得ではない。本文中の男女差の推測や各国政治機関の現時点の呼称は監査対象の根拠に使わない。
- S207 東京外国語大学言語モジュール [普通形の体系：カード](https://www.coelang.tufs.ac.jp/modules/ja/gmod/courses/c01/lesson11/step1/card/038.html)。本文全3表を取得・読了。表2の読む・食べるの行の辞書形・連用形・た形・て形をQ_M_052全4肢・全4解説と照合。派生／複合の分類理論を証明する資料ではなく、設問も語形対応へ限定。

取得原バイトSHA256・読了範囲・制約はevidence/batch143_sources.json。資料本文・頁画像は転載しない。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=143,base_commit='5889de7e2c798ac5d0844d65c7f40a752ef79e27',fully_rejudged=sorted(targets),edits=16,independent_answers={'Q_M_057':3,'Q_M_052':3},sources=['S206','S207'],status_counts=m['status_counts'],remaining=150,machine_warnings=99,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),source_pdf_page_sha256={str(n):sha(root/f'metonymy143-{n}.png') for n in range(1,5)},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch143_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('350 confirmed / 150 remaining',pages)
