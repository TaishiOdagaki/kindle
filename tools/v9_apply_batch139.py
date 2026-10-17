"""One-time case audit: diagnostic limits and listening material support."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2883
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_MO_001':dict(stem='このケースで理解が進まなかった理由を検討する際、原因を決め付けずに確認する観点として、最も適切なものを一つ選べ。',opt='教材に含まれる語彙を学習者が知っているか、知っている語でも連続した音声の中で聞き取れているかを確かめる。',exps=['ケースの記述だけで、オンラインという形式を理解困難の唯一の原因と断定することはできません。','教材に問題がないとも、学習者だけが原因だとも断定できません。教材の語彙や音声と学習者の理解の実態を確かめます。','初級であることだけを理由に、聴解教材そのものを不適切とすることはできません。語彙の知識や音声中での語の認識などを踏まえて支援を検討します。','語を知らない場合と、知っていても連続した音声中で認識できない場合を区別して確認します。これは原因を確定した診断ではなく、教材と学習者の実態を調べる観点です。']),
'Q_MO_005':dict(stem='このケースで聴解の指導を継続するに当たり、教材・活動の改善として検討する方針のうち、最も適切なものを一つ選べ。',opt='学習者の語彙知識や音声理解の状況を確かめ、場面の知識を活性化する活動と、音声中の語を認識する活動の双方を検討する。',exps=['学習者の実態を調べずに上級者向けへ一律に統一するのは、理解状況を踏まえた改善ではありません。','オンラインであるという理由だけで、教材や活動への工夫が不要になるとはいえません。ケースでは理解の実態に応じた検討が必要です。','設問は聴解の指導を継続する場合の改善方針を問うています。聴解教材をすべて廃して読解だけにする方針は、その条件に合いません。','場面の背景知識を使うトップダウン処理と、音声を解読するボトムアップ処理の双方を考えます。どの活動を用いるかは学習者の実態に応じて検討し、一つの工夫による理解の保証とはしません。'])}
reason='再取得したS99の本文は、語彙知識の不足と既知語を連続音声中で認識できない場合を区別し、背景知識の活性化と音声の分割・解読の両処理を説明している。共通ケース全2段落と全4肢・全4解説を再点検。原因の断定や速度を遅くすればよいとの一般化を避け、学習者の実態を確かめる観点と両処理の支援を検討する方針に改訂。ふりがなのない文字提示を聴解困難の確定原因とはしない。資料の説明と当該ケースへの教育的な適用判断を区別し、効果量や成功の保証は承認しない。'
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']=='4'
 opts=q[k]['opts'].copy();opts[3]=v['opt']
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S99'],applied=True,before_version='第138バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S99'],reason=reason,stem_review='共通ケース全2段落と4選択肢を独立照合。原因の診断または成功の保証は問わず、実態を確認して指導を検討する条件に限定。',explanation_review='全4解説をケースの明示条件とS99の語彙知識・既知語認識・両処理の本文に照合。適用判断と資料の直接の主張は区別。',option_verdicts=(['誤：オンラインだけが原因と断定する根拠なし','誤：教材の問題を除外し学習者だけに帰責する根拠なし','誤：初級への聴解を一律に排除する根拠なし','正：語彙知識と音声中の語認識を区別して確認'] if k=='Q_MO_001' else ['誤：学習者の実態を無視した上級向け一律化','誤：オンラインを理由に教材検討を不要とする','誤：聴解指導の継続という明示条件に反する','正：実態を調べ、背景知識と音声解読の双方の支援を検討']),unresolved='',multiple_correct_risk='なし：明示した検討条件に合う正答4のみ',no_correct_risk='なし：独立正答4')
assert len(extra)==12
for name,obj in [('changes.json',cs+extra),('changes_batch139.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 12 edits; S99 acquisition metadata retained in batch137_sources.json')
