"""One-time assessment audit. Never use to overwrite later decisions."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2542
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']=='要追加確認' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(o,n) in enumerate(zip(olds,news)):
   o=html.unescape(o)
   if o==n:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=sources,applied=True,before_version='第115バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢を取得済み一次本文の定義・判断条件と独立比較。ケース問は現行ケース6全2段落とも照合。',explanation_review='全4解説を資料本文に対応させ、直接/間接と主観/客観、評価の時期と目的、手順の推奨と効果保証を区別。原著の引用先全研究や実際のケース得点の妥当性を確認済みとはしない。',unresolved='',multiple_correct_risk='なし：明示した区別・目的で'+str(key)+'のみが適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_4_060';opts=q[k]['opts'].copy();opts[1]='間接テストでは、例えば文法の選択問題への解答から、実際に話したり書いたりする力を支える言語知識を推定する。';opts[3]='直接テストでは実際の発話や文章が得られるため、採点者による判断の影響は一切入らず、採点基準の共有や採点者の訓練も不要になる。'
review(k,'CEFR（2001）9.3.6の直接・間接評価の区別に照らし、適切な説明を一つ選びなさい。',opts,[
'9.3.6は実際に行う活動を評価する直接評価と、問題への応答から支える技能等をみる間接評価を区別します。話す力をロールプレイで、書く力を小論文で評価する設計は、直接評価の側に当たります。',
'9.3.6は間接評価が支える技能等を測ること、問題への応答から言語の範囲や制御を判断することを説明しています。発話・文章そのものを評価する課題とは区別できます。ただし、その得点だけで実際の運用能力全体が確定するという意味ではありません。',
'この肢は発話そのものを行わせず、文法・語彙の選択問題から話す力を推定する設計です。9.3.6の区別では間接評価の例となり、直接評価とする名称が合いません。',
'9.3.8は直接の運用評価にも採点者の判断が関わるとし、明確な基準、複数の判断、訓練等を挙げています。なお2014年Testing Standardsの79〜80頁は文章等の自動採点も扱うため、直接評価が常に人間の採点を要するとも言い切れません。直接・間接という区別だけで採点コストや信頼性は決まりません。'],2,['S179','S142'],
'CEFR2001印刷186〜189頁とTesting Standards2014印刷79〜80頁を本文・画像照合。直接/間接と主観/客観を混同せず、常に人間採点、間接なら常に低コストという元解説の過大な一般化を除去。対象を指定資料の区別へ限定。',
['誤：発話・作文課題を間接と命名','正：問題への応答から支える知識等をみる間接評価の例','誤：発話ではない知識問題を直接と命名','誤：直接評価から判断・訓練不要を導く'])
k='Q_O_027'
review(k,q[k]['stem'],q[k]['opts'],[
'CMUの採点教材は、採点前に学習者の成果例を用いて基準の解釈の違いを話し合う調整を挙げています。ケースの事前会議も共通の解釈を確かめ、ばらつきを抑えることを目指すと読めます。会議だけで全員の点が完全一致すると保証するものではありません。',
'ケースは複数の教師が採点を分担するため、観点と到達段階の内容をすり合わせたと記しています。CMUが挙げる基準解釈の調整に対応する目的であり、採点者を減らすという目的はこの記録からは読み取れません。',
'調整しているのは採点基準の内容・解釈です。テスト課題の実施時間を短くしたという記録はありません。採点者間の判断の調整と、受験に要する時間の短縮は別の目的です。',
'ケースに受験者数を減らす記録はありません。基準を共有して採点を分担するという文脈で、学習者を減らして採点を楽にする目的を選ぶ根拠はありません。'],1,['S180'],
'CMU公式教材Grade anonymouslyのConsiderations（事前normingと基準解釈の討議）を取得・精読。ケース全2段落と照合し会議の目的を再判定。人数や時間の削減という未記録事実を補わず、効果の完全保証に拡張しない。',
['正：基準解釈の調整・一貫性を目指す会議','誤：採点者削減は記録されず基準調整の目的と異なる','誤：試験実施時間短縮の記録がない','誤：受験者数削減の記録がない'])
k='Q_O_029'
review(k,'このケースでは、学習者に実際にロールプレイを行わせ、発話の質を評価している。CEFR（2001）9.3.6の直接・間接評価の区別で、この形式に当たるものを一つ選びなさい。',q[k]['opts'],[
'9.3.8は主観・客観の区別を別に扱い、運用の質を採点者が判断する場合にも、基準の明確化等によって主観性を抑えると説明します。この設問は実際の発話を評価するかという区別を問うため、客観テストのみという肢は答えになりません。',
'9.3.6の間接評価は、典型的には問題への応答から支える技能等をみるものです。このケースは発話そのものの質を判断しており、その区別では直接評価の側に当たります。',
'9.3.6は、学習者が実際に行っている活動を評価するものを直接評価とし、発話を観察して基準に照らす例を挙げています。ケースのロールプレイもこの設計に対応します。',
'診断的に情報を使うかどうかは、この設問が問う直接・間接の区別とは別です。9.3.5は総括的評価からのフィードバックも診断的・形成的になり得るとしています。診断的評価をコース開始前だけに限定して除外する説明は適切ではありません。'],3,['S179'],
'CEFR2001の9.3.5〜9.3.8を本文・画像照合。設問の分類軸を明示し、直接評価と客観採点を同一視しない。元解説4の診断評価＝開始前という単純化を除去し、評価結果の診断的使用と実施形式を区別。',
['誤：設問の直接/間接という軸への回答ではない','誤：発話そのものを評価する記録と不一致','正：実際の発話を観察して基準で評価','誤：診断的利用という別の軸であり直接/間接を示さない'])
k='Q_O_030';opts=q[k]['opts'].copy();opts[2]='学校で利用目的・必要な許可・保管方法を確認した上で発話の記録を残し、共通基準に沿って複数の教師が再確認できるようにする'
review(k,'評価の根拠を残し、必要に応じて採点者間で再確認する方針をとる。この方針に合う工夫を一つ選びなさい。',opts,[
'この設問は、判断の根拠を残して採点者間で再確認する方針です。根拠を一切記録しないとする肢は、その方針に反します。記録があるだけで採点の妥当性が保証されるという意味ではありません。',
'9.3.8は複数の判断や共通基準を挙げています。共有・再確認をしないと決める肢は、今回の方針に合いません。一人で採点することがどの試験でも誤りだと一般化するものではありません。',
'9.3.8の共通基準と複数の判断を参考に、発話と判断根拠を後から確かめられるようにする本問の提案です。記録の作成・共有は学校で目的、必要な許可、保管等を確認した範囲に限ります。記録するだけで公平性・信頼性が自動的に高まると保証していません。',
'基準を統一しないことを目的に毎回変更する肢は、共通基準に沿って再確認するという方針に合いません。問題のある基準を根拠に基づいて改訂することまで否定するものではありません。'],3,['S179'],
'CEFR2001の9.3.8の共通基準・複数判断を、根拠の記録と再確認という明示方針へ適用する編集上の提案に限定。録音録画の普遍的効果保証を除去し、目的・許可・保管等の校内確認を条件化。個別の同意取得や法的適法性を確認したものではない。',
['誤：根拠を残すという明示方針に反する','誤：共有・再確認を排除し方針に反する','正：条件を確認し記録と共通基準での再確認を行う','誤：基準の非統一を目的とし方針に反する'])
assert len(extra)==22,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch116.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path('/workspace/scratch/01d7c3f9b818');meta=[]
for sid,name,url,scope in [('S179','cefr116.pdf','https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf','CEFR2001 official body; printed186-189/PDF195-198 read and image reviewed; 9.3.5-9.3.8 complete, 9.3.9/9.3.10 start incidental; not all273 pages'),('S142','standards116.pdf','https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf','2014 Standards printed79-80/PDF89-90 read/image reviewed: scoring specifications and continuation, including human/computer scoring; whole240 pages not approved'),('S180','cmu_norm116.html','https://www.cmu.edu/teaching/designteach/inclusiveexcellence/gradingandfeedback/index.html','Grade anonymously Considerations: prior norming with sample work, interpretation across graders; author guidance not universal causal guarantee')]:
 f=root/name;raw=f.read_bytes();meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_read_scope=scope,retrieved='2026-10-16',full_source_redistributed=False))
(b.OUT/'evidence/batch116_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('4 questions /22 edits; independent keys2,1,3,3')
