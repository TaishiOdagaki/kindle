"""One-time record after inspection of every changed page image."""
import json,hashlib,subprocess,re,io,csv,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch100-qa';targets={'Q_M_045','Q_M_049','Q_M_050'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':254,'修正必要':50,'要追加確認':196}
cs=json.loads((p/'changes_batch100.json').read_text());assert len(cs)==27
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
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[x for x in machine['issues'] if x not in prior['issues']];removed=[x for x in prior['issues'] if x not in machine['issues']]
assert removed==[] and len(machine['issues'])==62 and len(added)==2 and {x[1] for x in added}=={'Q_M_045','Q_M_049'} and all(x[0]=='P1' for x in added)
f=p/'README.md';s=f.read_text()
for a,b in [('251問','254問'),('51問','50問'),('198問','196問'),('264問2202箇所','267問2229箇所'),('264問を','267問を')]:s=s.replace(a,b)
f.write_text(s)
sources={
'S159':{'title':'文化審議会 公用文作成の考え方（建議）・解説','url':'https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf','date':'2022-01-07','acquisition':'文化庁から63頁のPDF原本全体を取得。検索抜粋でなく本文を抽出。','scope':'建議本文の表記原則、解説の見方、解説2頁の読み手に応じた工夫、8頁の漢字使用の原則全体、17頁の句読点の符号原則、33頁の係り受け・読点位置による意味変化と書き換えの節を精読。','sha256':sha(root/'S159-100.pdf'),'targets':['Q_M_049','Q_M_050'],'limits':'2022年建議の明示内容を対象にする。法令は直接の対象ではないとの資料自身の留保を守り、全文章ジャンルの唯一規則や著作権法上の適法性を承認しない。全63頁の全主張を照合したとはしない。'},
'S160':{'title':'国際交流基金 教科書を作ろう BTS00126 Ａく／ＡＮに／Ｎになります','url':'https://www.kyozai.jpf.go.jp/kyozai/material/BTS00126/ja/render.do','acquisition':'公開HTML本文全55行を取得・精読。','scope':'18〜43行の構造図、変化の結果の状態、状態変化、例文、するとの着目点の区別、なりましたの含意の但書。','sha256':sha(root/'S160-100.html'),'targets':['Q_M_045'],'limits':'指定教材の文型解説の範囲。使用頻度の高さ・指導効果の実証や最新試験級別との対応は承認しない。刊年は推定しない。'}}
for v in sources.values():v['retrieved']='2026-10-16 JST'
report=f'''

## 第100バッチ（2026-10-16）

最新GitHub HEAD 65dac7e887d3fef67fc07ea2e6d8f3d77b4bdcbfから別作業場へ復元。国際交流基金「教科書を作ろう」の文法解説全文と文化庁の文化審議会建議・解説PDF原本を取得した。Q_M_045は「なる」の使用頻度が高いとする未実証の主張を撤回し、状態変化とその結果、するとの着目点の違いを問う。Q_M_049は振り仮名についての一律の著作権判断を撤回し、解説・広報等で読み手に配慮した表記の工夫を問う。Q_M_050は全文章の読点の慣習を曖昧に一般化せず、指定建議解説の読点位置と意味、必要時の書き換えに限定した。各設問・全4肢・独立正答・各4解説を取得本文と照合し、正答3・4・3を確認、番号変更なし。

3問27箇所。確認済み254・修正必要50・要追加確認196、残件246。累積267問2229箇所。全500問・解説500件、v8不変ハッシュ、影響外本文、正解表・リンク・タグを検査し維持。公開可否回帰8条件合格。機械警告は60から62件へ。新規2件はM45とM49のP1で、正答解説末尾がそれぞれ「頻度や教授効果の実証ではない」「著作物の適法性判定ではない」と範囲を限定するための誤検出。冒頭の肯定と根拠本文を独立照合し、正誤の反転ではないと判断した。既存60件は同一。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照する。

documents手順でNoto Sans JP適用QAコピー{len(pages)}頁を描画。27変更文字列をPDFで検出し、該当{'・'.join(map(str,reviewed))}頁を150dpi画像で直接目視した。全頁最終目視と残246問の学術照合は未了。最終v9は未制作で出版不可。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第100バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';s=f.read_text()+'\n\n## 第100バッチ 変化表現・公用文表記（2026-10-16）\n\n'
for k,v in sources.items():s+='- '+k+' ['+v['title']+']('+v['url']+')：'+v['acquisition']+' '+v['scope']+' '+v['limits']+' 対象：'+','.join(v['targets'])+'。\n'
f.write_text(s+'\n原バイトのハッシュはevidence/batch100_review.json。資料全文は転載しない。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第100バッチ\nNoto Sans JP適用コピー{len(pages)}頁。27変更文字列のある'+ '・'.join(map(str,reviewed))+'頁を150dpi画像で直接目視。全頁最終目視は未了。\n')
e={'batch':100,'base_commit':'65dac7e887d3fef67fc07ea2e6d8f3d77b4bdcbf','fully_rejudged':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':246,'independent_answers':{'Q_M_045':3,'Q_M_049':4,'Q_M_050':3},'sources':sources,'machine_warnings':62,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']='M45の設問・全4肢は180頁、解説は382〜383頁。M49・M50の設問・全4肢は182頁、M49解説は384頁、M50解説は384〜385頁。改頁前後を直接確認、欠字・本文クリッピングなし。M50第4解説のタグ右端107.65pt、本文左端117.65ptもPDF座標で確認し10ptの間隔を確保。解説の改頁は最終組版で再点検する。'
(p/'evidence/batch100_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 3 full reviews/27 edits;254 confirmed/246 remaining;pages',reviewed)
