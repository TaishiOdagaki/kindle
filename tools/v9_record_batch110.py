"""Record scoped full-question review and inspected cumulative render."""
import json,hashlib,subprocess,io,csv,re,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');r=Path('/workspace/scratch/01d7c3f9b818/batch110_qa')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k=='Q_4_077' else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':283,'修正必要':39,'要追加確認':178}
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];assert len(machine['issues'])==70 and len(added)==1 and added[0][:2]==['P1','Q_4_077'];assert all(x in machine['issues'] for x in prior['issues'])
cs=json.loads((p/'changes_batch110.json').read_text());assert len(cs)==6
pages=subprocess.check_output(['pdftotext','-layout',str(r/'qa.pdf'),'-']).decode().split('\f')[:-1];parts=[re.sub(r'\s+','',s) for s in pages];whole=''.join(parts);bounds=[0]
for s in parts:bounds.append(bounds[-1]+len(s))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);at=whole.find(needle);assert at>=0
 matches[str((c['id'],c['field'],c['index']))]=list(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1))
reviewed=sorted({n for v in matches.values() for n in v});assert reviewed==[82,281,282]
for n in reviewed:
 with Image.open(r/f'review-{n}.png') as im:im.load()
f=p/'README.md';s=f.read_text()
for a,b in [('282問','283問'),('179問','178問'),('287問2463箇所','288問2469箇所'),('287問を','288問を')]:s=s.replace(a,b)
f.write_text(s)
report='''

## 第110バッチ（2026-10-16）

Q_4_077の設問・全4肢・独立正答・全4解説を、Burns・Khalifa2017第1章の実施者自身の説明へ照合し6箇所を改訂。出版社公開抜粋1〜10頁を取得・本文読了、4〜5頁を画像照合。4頁の現場での系統的検討、5頁の四段階の関連・反復と研究者・支援者との協働、7頁の計画の練り直しを根拠とする。教師主体を外部研究者の排除と混同せず、四段階は当該プログラムで採用されたモデルとする。原初のKemmis・McTaggart1988、Burns2010、引用先の全原著を取得済みとはしない。Figure1のプログラム運営サイクルと個別研究の四段階も区別した。未変更の誤答3肢も独立照合済み。

正答4を維持。確認済み283・修正必要39・要追加確認178、残件217。累積288問2469箇所、500問維持。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照。

全500問の機械検査と公開可否回帰8条件が合格。警告は69→70件、追加P1はQ_4_077の正解解説末尾が「唯一の固定手順・成功保証ではない」とする留保のためであり、正答否定ではないと目視確認。他69件は同一。Noto Sans JPによる累積稿401頁を新規描画し、全6変更文字列を検出、82・281・282頁を1800px画像で直接目視・完全読込み。対象部分の欠字・重なり・切れなし。解説の頁分割など最終組版の調整と全頁最終目視、残217問の学術確認は未了。作業稿は出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第110バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第110バッチ S169（2026-10-16）

Anne Burns・Hanan Khalifa（2017）Engaging action research to explore use of assessment for improving language ability, in Second Language Assessment and Action Research, 第1章。[出版社公開抜粋](https://assets.cambridge.org/97811084/36700/excerpt/9781108436700_excerpt.pdf)1〜10頁のみ取得・本文読了、4〜5頁画像照合。[前付け](https://assets.cambridge.org/97811084/36700/frontmatter/9781108436700_frontmatter.pdf)の著作権頁で2017初版を確認。Q_4_077を実施者本人が説明する当該プログラムの方法（4・5・7頁）に限定して承認。4頁は現場の系統的探究、5頁は四段階の相互関連と反復・研究者との協働、7頁は計画の練り直し。4段階モデルの原初文献Kemmis・McTaggart1988、Burns2010その他引用元の全原著は未取得。個別実証章の効果を抜粋の概要だけで承認しない。Figure1の事業運営サイクルとは区別。本文PDFは再配布せずハッシュと取得範囲をevidence/batch110_source.jsonへ記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+'\n\n## 第110バッチ\nNoto Sans JP適用累積稿401頁、全6変更文字列を検出。82・281・282頁を1800px画像で直接目視。対象部分に欠字・重なり・切れなし。解説の頁分割と全頁最終目視は未完了。\n')
e=dict(batch=110,base_commit='448e45f46da925dc3f9fd0804783659453f9b6e8',fully_rejudged=['Q_4_077'],edits=6,independent_answers={'Q_4_077':4},sources=['S169'],status_counts=m['status_counts'],remaining=217,machine_warnings=70,new_warnings=added,new_warning_judgment='P1 false positive: qualifying fixed procedure/success guarantee, not negating correct option',readiness_gate='8 cases passed',render_pages=len(pages),visually_reviewed_pages=reviewed,all_changed_strings_found=matches,docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(r/f'review-{n}.png') for n in reviewed},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch110_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('283 confirmed/217 remaining;6 edits/3 pages recorded')
