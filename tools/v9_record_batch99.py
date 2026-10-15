"""Record after direct image inspection; do not rerun on later checkpoints."""
import json,hashlib,subprocess,re,io,csv,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch99-qa';targets={'Q_M_047','Q_M_048'}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':251,'修正必要':51,'要追加確認':198}
cs=json.loads((p/'changes_batch99.json').read_text());assert len(cs)==18
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
assert added==[['P1','Q_M_047','(正)4の解説が否定で終わる/肯定の(誤)がある: [1, 2, 3]']]
assert removed==[['P1','Q_M_047','(正)4の解説が否定で終わる/肯定の(誤)がある: [1, 3]']]
assert len(machine['issues'])==60
f=p/'README.md';s=f.read_text()
for a,b in [('249問','251問'),('200問','198問'),('264問2202箇所','264問2202箇所'),('262問2184箇所','264問2202箇所'),('262問を','264問を')]:s=s.replace(a,b)
f.write_text(s)
sources={
'S158':{'title':'鼻濁音の聞き取り','url':'https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/02-12-01.php','scope':'公開HTML全56行を取得・精読。52〜53行、語中の[g]/[ŋ]、鼻から息が抜ける発音と意味が変わらないという説明。','sha256':sha(root/'S158-99.html'),'targets':['Q_M_047']},
'S36':{'title':'アクセント基礎','url':'https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/01-08-01.php','scope':'公開HTML全58行を取得・精読。51〜56行の共通語例と核。「箸」の「は」直後、「あなた」の「な」直後で下降し、核はそれぞれ第1拍・第2拍。尾高と平板の注意も読み、全語に下降があるとはしない。','sha256':sha(root/'S36-99.html'),'targets':['Q_M_048']}}
for v in sources.values():v.update(retrieved='2026-10-16 JST',limits='指定教材の説明・例に限定。音声実測は未実施。全方言・全話者・全場面や使用率を承認しない。刊年不明、「最近」を2026年の統計と扱わない。')
report=f'''

## 第99バッチ（2026-10-16）

最新GitHub HEAD 74defd7ad03cbbdf59c90bcef110b2b4fd77535aから別作業場へ復元。未保存だったM47・M48を資料の全文再取得から独立再判定した。Q_M_047は東京外国語大学「鼻濁音の聞き取り」本文を照合し、語中の[g]/[ŋ]と意味不変を指定教材の範囲で問う形へ改訂。方言・個人・場面による分布の未照合主張を撤回し、教材の「最近」を現在の統計として扱わない。Q_M_048は同大学「アクセント基礎」の共通語例「箸」「あなた」に限定。アクセント核を下降そのものと同一視せず、下降直前の第1拍「は」・第2拍「な」を区別する。全4肢と各4解説を根拠本文に照らし、独立正答は4・2で番号変更なし。

2問18箇所。確認済み251・修正必要51・要追加確認198、残件249。累積264問2202箇所。全500問・解説500件、v8の不変ハッシュ、影響外本文、正解表・リンク・タグを検査し維持。公開可否回帰8条件合格。機械警告60件、M47の既存P1一件は誤答解説の検出番号だけが[1,3]から[1,2,3]へ変化。正答4の解説末尾が全方言への一般化を否定するための誤検出であり、肯定する教材の説明と矛盾しない。他59件は不変。台帳原文はv8スナップショット、改訂はchangesと作業稿を参照する。

documents手順でNoto Sans JP適用QAコピー{len(pages)}頁を描画し、18変更文字列をPDFで検出。該当{'・'.join(map(str,reviewed))}頁を150dpi画像で直接目視。全頁最終目視と残249問の学術照合は未了、出版不可。これで前回未保存の音声3問は第98・99バッチの別記録で再照合したが、未保存バッチ自体の成果は加算しない。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第99バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';s=f.read_text()+'\n\n## 第99バッチ 音声教材の再取得（2026-10-16）\n\n'
for k,v in sources.items():s+='- '+k+' 東京外国語大学 ['+v['title']+']('+v['url']+')：'+v['scope']+' '+v['limits']+' 対象：'+','.join(v['targets'])+'。\n'
f.write_text(s+'\nS36の既存Q_5_026判定を上書きしない。原バイトのハッシュはevidence/batch99_review.json。本文全文は転載しない。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第99バッチ\nNoto Sans JP適用コピー{len(pages)}頁。18変更文字列のある'+ '・'.join(map(str,reviewed))+'頁を150dpi画像で直接目視。全頁最終目視は未了。\n')
f=p/'evidence/recovery_20261016.md';f.write_text(f.read_text()+'\n## 第99バッチでの再照合\nM47・M48も本文再取得・18項目改訂・独立判定・機械検査・変更頁QAを実施。第98・99バッチのGitHub保存確認をもって音声3問の復旧分を採用する。未保存の第97バッチは加算しない。\n')
e={'batch':99,'base_commit':'74defd7ad03cbbdf59c90bcef110b2b4fd77535a','fully_rejudged':sorted(targets),'edits':18,'status_counts':m['status_counts'],'remaining':249,'independent_answers':{'Q_M_047':4,'Q_M_048':2},'sources':sources,'machine_warnings':60,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']='M47の設問・4肢・全4解説とM48の設問・4肢はそれぞれ同一頁内。M48の解説は383頁の見出し・正解・第1解説から384頁の第2〜4解説へ続き、両頁を直接確認した。欠字・重なり・クリッピングなし。解説の改頁は最終組版で再確認する。'
(p/'evidence/batch99_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded 2 full reviews/18 edits;251 confirmed/249 remaining;pages',reviewed)
