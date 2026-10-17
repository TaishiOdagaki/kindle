"""One-time interpersonal-distance revision against an acquired original study."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2981
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_4_107';ak='A_4_107';assert d[k]['status']=='修正必要' and a[ak]['ans']=='4'
stem='非言語コミュニケーションに関わる対人距離について、Sorokowskaら（2017）の国際比較研究の方法と結果に合う記述を一つ選べ。'
opts=['質問紙は使わず、実際の会話中に参加者が移動した距離だけを観察した。','見知らぬ人に対する距離だけを測り、知人や親しい人に対する距離は扱わなかった。','希望する対人距離の平均には、調査対象の国の間で違いが認められなかった。','図を用いた質問紙で、見知らぬ人・知人・親しい人に希望する距離を尋ね、その平均に国の間で違いが認められた。']
exps=['参加者は図を用いた質問紙に回答しました。著者らは、希望する距離と実際に選ぶ距離は異なる可能性を限界として挙げています。実際の会話行動の観察だけを行った研究ではありません。','見知らぬ人・知人・親しい人の三つの相手区分について、会話の際に快適だと感じる距離を尋ねています。見知らぬ人だけに限定した調査ではありません。','結果では、希望する距離の平均に国の間で違いが認められています。各国の全員が同じ距離を望むと示したわけでもありません。','図上で希望する距離を回答する調査で、国の間の平均の違いが報告されました。実際の行動そのものの測定とは区別され、結果の一般化にも検討の余地があるとされています。国別の結果だけから、個々の相手の希望する距離を決め付けることはできません。']
reason='S210 Sorokowskaら（2017）の原論文Accepted Version全36頁を共著者所属大学Warwickの公開機関リポジトリから取得。本文番号9–18頁（PDF14–23頁）の方法・結果・考察・限界を全て精読し、方法9頁・結果11頁・限界17頁は画像でも照合。旧問題の沈黙・ジェスチャーの広範な補助主張と日本・北欧・ラテン系という一律な文化分類を撤回。非言語コミュニケーションの対人距離という同じ学習領域で、取得原論文の方法と平均の国間差に限定。希望と実際の行動を区別し、一般化の制約を明示。Hall原著の取得や全36頁精読、補足資料の取得とは扱わない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S210'],applied=True,before_version='第146バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S210'],reason=reason,option_verdicts=['誤：図を用いた質問紙による希望の測定を行動観察と混同','誤：相手の三つの区分のうち二つを除外している','誤：平均の国間差が認められた結果を逆転','正：方法・相手区分・平均の国間差に一致'],stem_review='非言語コミュニケーションの対人距離に限定し、特定原論文の方法・結果への理解を問う。',explanation_review='方法・結果・考察・限界本文全体に全4解説を照合。希望と実際の行動、平均と個人、国間差と文化の一律分類を区別。',unresolved='',multiple_correct_risk='なし：取得原論文の方法・結果に合うのは4のみ',no_correct_risk='なし：独立正答4')
for n,obj in [('changes.json',cs+extra),('changes_batch147.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'distances147.pdf').read_bytes()
e=dict(source_id='S210',title='Preferred Interpersonal Distances: A Global Comparison',authors='Agnieszka Sorokowska et al.',year=2017,journal='Journal of Cross-Cultural Psychology 48(4), 577–592',doi='10.1177/0022022117698039',version='Accepted Version with repository cover and author list; 36 PDF pages',url='https://wrap.warwick.ac.uk/100226/7/WRAP-preferred-interpersonal-distances-global-comparison-Realo-2017.pdf',landing_url='https://wrap.warwick.ac.uk/id/eprint/100226/',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=36,read_scope='本文番号9–18頁（PDF14–23頁）の方法・結果・考察・限界を全文精読。方法9頁・結果11頁・限界17頁の画像照合。',limitations='全36頁精読、補足資料の取得、Hall原著の取得ではない。希望の質問紙回答を実際の行動や全個人への予測に一般化しない。特定国の順位・温度や性差の因果的説明を新稿に使用しない。',full_source_redistributed=False)
(b.OUT/'evidence/batch147_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
