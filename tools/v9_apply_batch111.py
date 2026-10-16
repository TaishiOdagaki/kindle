"""One-time review of verbal-report procedures against Ericsson/Simon1980."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2469
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_078'
assert d[k]['status']=='要追加確認' and a['A_4_078']['ans']=='4'
stem='EricssonとSimon（1980）が論じる思考発話とその分析について、報告手続きの説明に合うものを一つ選びなさい。'
opts=q[k]['opts'].copy();opts[3]='課題に取り組む最中に、その時注意を向けている情報を声に出してもらい、得られた言語報告を分析データとする。'
exps=[
'217〜218頁と220頁は、指示に応じて参加者が口頭で報告する手続きを扱います。通常の授業の発言を記録し、単語の頻度だけを集計するという説明では、この思考発話の手続きを捉えていません。頻度集計そのものを研究方法として否定する趣旨ではありません。',
'220頁で説明するthink aloudの手続きは、注意を向けている情報を声に出してもらうものです。無言を強制し、後からも報告を得ないという肢には、分析対象となる言語報告を引き出す手続きがありません。',
'この肢は観察者が行動を二択で記録する方法です。それだけでは、217〜218頁と220頁で扱う参加者自身の言語報告を得ていません。観察記録を他のデータとして併用することまで否定するものではありません。',
'218頁の同時的言語化と220頁のthink aloudに対応します。回顧的報告は別の手続きで、記憶までの時間や質問の内容に注意が必要です。217頁では報告が内的過程を直接・完全に写すとは仮定せず、220頁では行動の動機・理由がそのまま報告可能とは限らないと述べています。']
reason='S170 Ericsson・Simon1980原論文の本文217〜220頁を版面照合。同時発話と回顧的報告を同一視せず、思考の透明な可視化や判断理由の完全な取得という未保証の主張を除く。本人の方法論上の区別を問う範囲で全4肢を独立判定。'
extra=[]
for field,old,new in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_4_078']['txt'],exps)]:
 for i,(o,n) in enumerate(zip(old,new)):
  o=html.unescape(o)
  if o==n:continue
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S170'],applied=True,before_version='第110バッチ反映後',block_context='A_4_078' if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(e)
assert len(extra)==6
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S170'],reason=reason,option_verdicts=['誤：口頭報告を引き出す手続きを単語頻度集計へ置換','誤：同時・回顧いずれの言語報告も得ない','誤：観察者の二択記録だけで参加者の報告を得ない','正：注意中の情報を同時に口頭報告させデータとして扱う'],stem_review='原論文の報告手続きへ範囲を限定。未変更の誤答3肢も含め全4肢を217〜220頁と独立比較。',explanation_review='全4解説を本文217頁の非直接観察、218頁の時間・同時/回顧の区別、220頁の手続きと動機・理由の可用性の留保に照合。引用先実証研究を別途取得・追試したとはしない。',unresolved='',multiple_correct_risk='なし：指定する思考発話手続きに合うのは4のみ',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',c+extra),('changes_batch111.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/01d7c3f9b818/ericsson111.pdf').read_bytes()
(b.OUT/'evidence/batch111_source.json').write_text(json.dumps(dict(id='S170',authors='K. Anders Ericsson and Herbert A. Simon',year=1980,title='Verbal Reports as Data',journal='Psychological Review87(3),215-251',doi='10.1037/0033-295X.87.3.215',url='https://acs.ist.psu.edu/ist597/papers/ericssonS80.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),obtained_pdf_pages=37,image_review_printed_pages=[215,216,217,218,220],ocr_read_pages=[218,219,220],high_resolution_verified_pages=[217,218,220],limits='Image-only scan. Relevant body pages visually verified, not abstract-only. Not full37-page reading; no blanket validation of all cited empirical studies or all educational contexts. PDF scan2004 not publication year.'),ensure_ascii=False,indent=2)+'\n')
print('1 full question/6 edits; key4 unchanged')
