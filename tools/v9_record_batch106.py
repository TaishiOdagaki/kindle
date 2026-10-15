"""Record the newly restored draft only after its own changed-page image review."""
import json,hashlib,subprocess,re,io,csv,bisect,gzip
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch106_restored_qa';targets={f'Q_MO_{x:03d}' for x in range(6,11)}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def image_path(x):return render/('review392_retry.png' if x==392 else f'review-{x}.png')
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':275,'修正必要':41,'要追加確認':184}
cs=json.loads((p/'changes_batch106.json').read_text());assert len(cs)==30
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:
 with Image.open(image_path(x)) as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert removed==[] and len(machine['issues'])==66 and added==[['P1','Q_MO_006','(正)1の解説が否定で終わる/肯定の(誤)がある: [3, 4]'],['P1','Q_MO_007','(正)3の解説が否定で終わる/肯定の(誤)がある: [1, 2, 4]']]
sources={}
for n in [164,165]:
 raw=gzip.decompress((p/f'evidence/S{n}_safety_education_notice.html.gz').read_bytes());assert raw==(root/f'S{n}_restore.html').read_bytes();sources[f'S{n}']={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'archive':f'evidence/S{n}_safety_education_notice.html.gz','retrieved':'2026-10-16 JST','url':f'https://www.mhlw.go.jp/web/t_doc?dataId={"00tc4244" if n==164 else "00tc2631"}&dataType=1&pageNo=1','scope':'2019 notice section1 body and A-D; full notice text read in prior unsaved review, key clauses reacquired and reread on restoration' if n==164 else 'Outline sections4(4),5(5); not all schedules or image appendices approved'}
f=p/'README.md';s=f.read_text()
for a,b in [('270問','275問'),('189問','184問'),('276問2375箇所','281問2405箇所'),('276問を','281問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第106バッチ（2026-10-16 復旧）

直前の未保存作業場が失われたため、最新GitHub HEAD 2ec2ab12f7393558370b114c132b3d6c565f7a5bから別作業場へ復元した。保存済み正本は確認済み270問・2375修正で、消失した5問を保存済みと数えない。厚労省2019年3月28日基発0328第28号通知と、公式掲載の安全衛生教育等推進要綱を再取得し、対応する本文を再照合した。S163・S26はGitHubに保存済みの原応答を使用。旧バッチ生成スクリプトの再実行で累積判断を上書きせず、新規の第106バッチとして復旧した。

Q_MO_006～010の全5問で設問・全4肢・独立正答・全4解説を照合。29箇所の設問・肢・解説とケース前提1段落、計30箇所を改訂した。文面が正確な肢は維持し、同一文の修正記録を加えない。MO6のニーズとMO8の分類は就労者・職場の指示理解という目的と対象から判断。MO7は視覚支援でも理解確認を省略しないことと、創作的な写真等の著作物性を区別。MO9は母語利用・文法テスト自体を否定せず、目標理解を確かめない方法を誤答とした。安全な模擬場面での確認に限定し、職場全体の安全・法定教育修了の保証とはしない。ケースにも事業場担当者との連携と、日本語学習支援が法定教育・設備対策の代替ではないことを追記した。

独立正答MO6=1・MO7=3・MO8=1・MO9=2・MO10=1、番号変更なし。確認済み275・修正必要41・要追加確認184、残件225。累積281問2405箇所。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照する。通知の旧特定技能14分野や在留制度の現行施行・経過措置、個別作業の安全技術まで確認したとはしない。

全500問・解説500件、v8不変ハッシュ、影響外本文、正解表・タグ・リンクを機械検査し維持。公開可否回帰8条件合格。警告64→66件で、新規MO6・7のP1は正答解説末尾の安全・効果の保証を否定する限定を検知した誤検出。他64件は同一。documents手順で、復旧稿そのものからNoto Sans JP適用QAコピー{len(pages)}頁を新しく描画し、全30変更文字列を検出、{'・'.join(map(str,reviewed))}頁を150dpi画像で直接目視した。消失した旧PNG・旧QA記録を今回の検査証拠に流用しない。頁をまたぐ見出し・設問・肢・解説のまとまりは最終組版の調整対象とする。欠字・重なり・クリッピングは検査頁に見られないが、全頁最終目視と残225問の根拠照合は未了。出版不可、最終v9ではない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第106バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''\n\n## 第106バッチ S164・S165（2026-10-16 再取得）

- S164 厚労省 [外国人労働者に対する安全衛生教育の推進等について](https://www.mhlw.go.jp/web/t_doc?dataId=00tc4244&dataType=1&pageNo=1)、2019-03-28基発0328第28号。未保存時に全文を取得・読了し、復旧時に原HTMLを再取得、1本文とイ（設備対策等）、ロ（母語・視聴覚教材）、ハ（理解度確認・反復）、ニ（必要な日本語・合図）を再照合。教育上の適用判断と因果的効果保証を区別する。旧14分野表や個別作業の安全技術を現在の網羅情報として使わない。
- S165 厚労省 [安全衛生教育及び研修の推進について・別紙安全衛生教育等推進要綱](https://www.mhlw.go.jp/web/t_doc?dataId=00tc2631&dataType=1&pageNo=1)、1991-01-21基発第39号の公式掲載本文。4(4)・5(5)を照合。元通知の日付と改正反映本文を区別し、全改正の経過措置・別表・画像別図を承認したとはしない。
- 原HTMLはevidence/S164_safety_education_notice.html.gz及びS165_safety_education_notice.html.gz。解凍一致・原バイト数・ハッシュを記録。HTML末尾と対象本文の存在を検査した。S163の必須内容〈31〉と目的・目標・評価の関係、S26本則第2・10条も対応箇所と照合。\n''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第106バッチ 復旧稿\nNoto Sans JP適用QAコピー{len(pages)}頁を新規描画。30変更文字列を検出し'+ '・'.join(map(str,reviewed))+'頁を150dpi画像で直接目視。392頁の最初のPNGは後の完全読込みで破損を検出したため使わず、review392_retry.pngを再描画して目視・完全読込みした。消失した旧描画は証拠に使用しない。見出し・設問・肢・解説の改頁調整と全頁最終目視は未了。\n')
e={'batch':106,'base_commit':'2ec2ab12f7393558370b114c132b3d6c565f7a5b','restored_after_unsaved_workspace_loss':True,'prior_saved_confirmed':270,'fully_rejudged':sorted(targets),'question_field_edits':29,'case_premise_edits':1,'edits':30,'status_counts':m['status_counts'],'remaining':225,'independent_answers':{'Q_MO_006':1,'Q_MO_007':3,'Q_MO_008':1,'Q_MO_009':2,'Q_MO_010':1},'sources':sources,'supplementary_sources':['S163 core curriculum goal31/objectives and evaluation','S26 statutory articles2,10'],'machine_warnings':66,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(image_path(x)) for x in reviewed},'png_retry':{'page':392,'corrupt_first_png_excluded':True,'used':'review392_retry.png'},'release_ready':False}
(p/'evidence/batch106_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded restored 5 reviews/30 edits;275 confirmed/225 remaining',reviewed)
