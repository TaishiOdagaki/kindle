"""One-time revision of conflict modes using the co-author's own definitions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1326
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
key='Q_5_105'; stem='Thomas–Kilmannのコンフリクト対処モデルについて、共同開発者Kilmannの公開解説に合う記述を一つ選べ。'
opts=[html.unescape(t) for t in q[key]['opts']]
opts[0]='「協働（collaborating）」は、自分の関心と相手の関心の双方を満たす解決策を、相手とともに探ろうとする対処様式である。'
exps=['協働は、自己主張と協力性の両面が高い様式です。双方の関心を十分に満たす解決策を探ります。ただし、あらゆる状況で最適という意味ではありません。',
'回避は、自分と相手の関心を直接追求せず、問題を先送りしたり距離を置いたりする様式です。Kilmannは状況に応じて様式を選ぶと説明しており、回避が常に最悪とはしていません。',
'受容・適応（accommodating）は、自分の関心を抑えて相手の関心を満たそうとする様式です。自分の主張を押し通すという肢の説明は逆です。',
'妥協（compromising）は、双方の関心を部分的に満たす受け入れ可能な解決を探る様式です。一方の完全勝利を目指すという肢の説明とは異なります。']
reason='統合と協働の用語混用を避けThomas–Kilmannのcollaboratingに統一し、協働を無条件に最善とする含みを除去。'
extra=[]
for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_5_105']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  if html.unescape(old)==new:continue
  e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S129','S130'],applied=True,before_version='第65バッチ反映後の累積作業稿')
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(e)
d[key].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S129','S130'],option_verdicts=['正：自己と相手の関心をともに満たそうとする協働の定義','誤：回避が常に最悪という評価が状況依存性と不一致','誤：受容は相手の関心を優先するため説明が逆','誤：妥協の部分的充足と一方の完全勝利を混同'],reason=reason,stem_review='共同開発者の公開定義を指定し全4肢を独立照合。',explanation_review='全4解説を開発者の五様式の定義と状況別選択の解説へ照合。心理測定特性や異文化間全般の有効性は主張しない。',unresolved='',multiple_correct_risk='なし：定義と限定条件に一致するのは1のみ',no_correct_risk='なし：独立正答1')
for name,obj in [('changes.json',c+extra),('changes_batch66.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
