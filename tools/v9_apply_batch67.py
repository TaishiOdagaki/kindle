"""Remove a false error premise while retaining the kinship semantic domain."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1332
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
key='Q_5_004';stem='親族名称による意味の区別を考える。自分のきょうだいを表す「兄・姉・弟・妹」の通常の意味について、最も適当なものを一つ選べ。'
opts=['「兄」と「姉」は、きょうだいの性別を区別しない同じ意味の語である。','「兄・姉・弟・妹」は、きょうだいの性別と、自分から見た年齢の上下を組み合わせて区別する。','「妹」は、自分より年上の女性のきょうだいを表す。','「姉」は、自分より年下の男性のきょうだいを表す。']
exps=['兄は年上の男性、姉は年上の女性のきょうだいを表します。両者は性別の点で区別されます。','兄は年上の男性、姉は年上の女性、弟は年下の男性、妹は年下の女性のきょうだいを表します。これらの語では、性別と自分から見た年齢の上下の二つが意味の区別に関わります。','妹は、自分より年下の女性のきょうだいを表します。年上の女性のきょうだいは姉です。','姉は、自分より年上の女性のきょうだいを表します。年下の男性のきょうだいは弟です。']
reason='「兄弟と食事した」を誤用とする根拠のない前提を撤去。同じ親族語の意味分節を、公式教材の語義だけで判定できる問題へ改訂。'
extra=[]
for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_5_004']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  if html.unescape(old)==new:continue
  e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S131'],applied=True,before_version='第66バッチ反映後の累積作業稿')
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(e)
d[key].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S131'],option_verdicts=['誤：兄と姉の性別の区別を否定','正：四語の性別と相対年齢の組合せに一致','誤：妹の相対年齢が逆','誤：姉の性別と相対年齢がともに逆'],reason=reason,stem_review='公式語彙表の通常の親族義に限定。学習者の誤用原因や英語の概念体系は推測しない。',explanation_review='全4解説の四語の意味を国際交流基金語彙表29頁の定義と画像照合。',unresolved='',multiple_correct_risk='なし：性別と相対年齢の対応に一致するのは2のみ',no_correct_risk='なし：独立正答2')
for name,obj in [('changes.json',c+extra),('changes_batch67.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
