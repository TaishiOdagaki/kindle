"""One-time JSL elementary-report audit; ordered changes preserve past fixes."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2564
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));blocks,_=qa.blocks(qa.load(str(b.DST))[0]);extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 def entry(field,i,o,n,**kw):
  c=dict(id=k,field=field,index=i,before=html.unescape(o),after=n,reason=reason,sources=sources,applied=True,before_version='第116バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
  c.update(kw);extra.append(c)
 if q[k]['stem']!=stem:
  ps=[x['t'] for x in blocks[k][1:-1] if not x['ind']]
  entry('stem',None,ps[0],stem)
  for old in ps[1:]:entry('stem',None,old,'',remove_paragraph=True,previous_paragraph=stem)
 for field,olds,news in [('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(o,n) in enumerate(zip(olds,news)):
   if html.unescape(o)==n:continue
   kw={'stem_context':stem} if field=='options' else {'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'}
   entry(field,i,o,n,**kw)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢を現行小学校編報告の本文と独立比較。ケース問は現行ケース9の全2段落と照合し、記録にない原因や結果を補わない。',explanation_review='全4解説を公的報告本文へ照合。理念・提案と因果実証、個々の児童の既習内容・言語理解・支援条件を区別。算数例は与えられた数値と比較の向きを独立検算。',unresolved='',multiple_correct_risk='なし：明示した目的・報告の考え方で'+str(key)+'のみが適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_4_085';opts=q[k]['opts'].copy();opts[0]='教科の学習活動に参加するための「日本語で学ぶ力」を、一人一人の実態に応じた学習支援と日本語支援を通して育成する。'
review(k,'文部科学省「学校教育におけるJSLカリキュラムの開発について」小学校編の考え方に合う説明を一つ選びなさい。',opts,[
'基本構想は日本語指導と教科指導を統合し、学習活動に参加する力を育てるとしています。教科志向型の説明も、内容の習得だけを直接の目的とせず、具体物や体験、既有知識を支えに学ぶ過程を重視します。',
'基本構想は、学習項目を固定した順序で配列するのでなく、教師が子どもの実態に応じて組み立てるツールと説明しています。文法項目の積み上げを最も推奨される唯一の編成原理のように扱う肢は合いません。',
'日本語指導と教科指導を統合し、教科の学習活動への参加を支える考え方です。初期指導の語彙・文型だけを扱い、教科から完全に切り離す目的ではありません。取り出し指導そのものを否定する説明でもありません。',
'基本構想は母語や母文化の支えも必要と述べています。母語習得を抑制するという肢の目的はこれに合いません。ここでは同報告の目的を問うもので、イマージョン教育全般を母語抑制と定義するものではありません。'],1,['S23'],
'小学校編の基本構想・教科志向型本文を再取得して照合。教科知識と日本語の同時達成という説明を、学習活動に参加する日本語で学ぶ力と個別支援へ精密化。中学校編・付加的バイリンガリズム理論の未照合主張を除去。',
['正：実態に応じた支援で学習参加を目指す','誤：固定順序の文法積み上げを基本原理とする','誤：教科から完全に切り離した初期指導のみとする','誤：母語抑制という目的は母語の支えを認める本文に反する'])
k='Q_4_086';mathpara=html.unescape([x['t'] for x in blocks[k][1:-1] if not x['ind']][1]);opts=q[k]['opts'].copy();opts[2]='比較する人物と、どちらが何枚少ないかという数量関係を、文章や図を使って確かめること。';exps=a['A_4_086']['txt'].copy()
exps[1]='児童の計算の解答や既習内容は、この設問に示されていません。文科省のJSL算数科5.1.2も日本語の習得状況と算数の既習内容の両方の把握を求めています。計算力不足を唯一の原因と断定する根拠はありません。'
exps[2]='この設問は、だれとだれを比べ、どちらが何枚少ないかを確かめる指導を問うています。あきらの枚数は、あおいの15枚から6枚を引いた9枚です。比較する人物と差を文章や図で対応させる着眼点が合います。実際の児童のつまずきの原因を特定したものではありません。'
exps[3]='「もっています」の意味を理解しているかどうかについて、この設問には児童の反応がありません。その理解を確かめることも必要になり得ますが、理解していないと認定して比較関係の確認に置き換える根拠はありません。'
review(k,'次の文章題で、だれとだれを比較し、どちらが何枚少ないかを確かめる指導を考える。その着眼点として適切なものを一つ選びなさい。'+mathpara,opts,exps,3,['S181'],
'JSL算数科5.1.1〜5.2の個別の既習内容・日本語理解の把握を照合。「最もつまずきやすい原因」をデータなしに断定せず、明示した比較関係を確かめる指導へ改訂。過去の第2バッチで正しく直された解説1の9/21の計算は維持し独立検算。設問を統合したため旧文章題の別段落は明示的に削除。',
['誤：語だけで常に正解という一般化は比較の向きが逆の例で成り立たない','誤：計算力不足が唯一という根拠がない','正：明示された比較する人物・数量差を確認する着眼点','誤：所有動詞未理解は記録されず比較関係という問いへの答えではない'])
k='Q_O_042'
review(k,q[k]['stem'],q[k]['opts'],[
'ケースは日本語の表現を練習し、教科内容と日本語指導を切り離さない方針としています。母語だけに完全に切り替えたとは記されていません。母語による支援を活用することまで否定するものではありません。',
'基本構想は日本語指導と教科指導の統合をねらいとしています。ケースも算数の文章題に結びつけた取り組みであり、教科から完全に切り離すという肢とは合いません。別の時間や取り出しで日本語を指導すること自体を誤りとするものではありません。',
'ケースには算数の文章題で使う日本語表現を練習すると明記されています。日本語指導を一切行わないという肢は、この事実と合いません。',
'教科志向型の説明は、教科の内容に即した学習活動と日本語支援を関連づけます。ケースの明示方針はこの考え方に沿います。ただし、表現を取り出して練習するという一事だけで、JSLカリキュラムの全内容を実施したと認定するものではありません。'],4,['S23'],
'基本構想・教科志向型の本文をケース9全2段落へ照合。教科との関連という明示条件で4肢を比較し、表現練習だけで全カリキュラムの実施を認定せず、母語支援や取り出し指導を全面否定しない。',
['誤：母語だけへの完全切替という事実がない','誤：教科から切り離さないという明示方針に反する','誤：日本語表現の練習という記録に反する','正：教科学習と日本語支援を関連づける考え方'])
k='Q_O_043';opts=q[k]['opts'].copy();opts[0]='児童の学習歴や理解の状況を確かめず、全員に同じ支援を適用するため';opts[2]='教科の学習と日本語の学習は関係しないので、互いに情報を共有する必要がなくなる';opts[3]='教科の理解と日本語での表現の両面から状況を共有し、必要な支援を検討できる'
review(k,'教科の学習と日本語支援を結びつける方針に照らし、ケースの担任教師と日本語指導担当の教師の連携の意義に合う説明を一つ選びなさい。',opts,[
'サポート・システムの説明は、子どもの状況を見極め、教師同士が協力して困難を解決する考え方を示します。実態を確かめず一律の支援を適用する肢は、この連携の目的に合いません。',
'指導方針の違いが生じる可能性はあっても、ケースには連携によって効果が低下したという結果は示されていません。サポート・システムは相互支援と連携を重視しており、情報を共有して必要な支援を検討する意義があります。',
'教科志向型の説明では、学習支援と日本語支援は密接に関連するとされています。教科と日本語は関係せず、情報共有が不要になるとする肢は、この考え方に合いません。',
'学習支援と日本語支援を関連づけ、教師同士が協力して課題を検討する考え方をケースに適用した説明です。教科の理解と日本語での表現の両面から支援を考えます。連携すれば必ず高い効果が出るという保証ではありません。'],4,['S23','S182'],
'小学校編教科志向型の学習/日本語支援とサポート・システム1.1の連携を照合。未照合の保護者同意必須・制度上禁止という法制度の誤答主張を同じ連携領域の説明へ差替え、普遍的効果保証も除去。現行法上の同意や連携手続の適法性は承認対象外。',
['誤：個々の状況の把握を排除','誤：ケースに効果低下の結果はなく相互支援の意義と不一致','誤：教科と日本語支援の関連を否定','正：教科理解・日本語表現の両面を共有して支援を検討'])
k='Q_O_044';opts=q[k]['opts'].copy();opts[3]='すべての授業で他の児童から常に完全に分離し、所属学級の学習への参加は検討しない'
review(k,'JSLカリキュラム開発の基本構想に沿って、学校生活の中でこの児童の学習参加を支える方針をとる。この方針に合う工夫を一つ選びなさい。',opts,[
'基本構想は母語や母文化の支えも必要と述べています。学校生活全体で母語使用を禁止するという肢は、その考え方に合いません。ここでは個々の児童への心理的影響を実証したとは主張していません。',
'教科志向型は、それぞれの教科に固有の活動・語彙・表現への支援を扱います。他教科で困難があるかを確かめず、一切支援しないと決める肢は、学校生活で学習参加を支える方針に合いません。',
'教科志向型が示す教科ごとの活動・語彙・表現への支援を、児童の実態に応じて検討する説明です。すべての教科で同じ練習を一律に行うという意味ではありません。',
'基本構想は取り出し・個別指導を想定しつつ、所属学級で他の子どもと学ぶことも念頭に置いています。常に完全に分離し学級参加を検討しないという肢は合いません。必要な取り出し指導そのものを否定しているわけではありません。'],3,['S23'],
'基本構想の母語・母文化の支え、所属学級と取り出しの両方の位置づけ、教科志向型の教科ごとの支援を照合。元解説の心理効果一般化を除去し、個別指導自体を誤りにせず永久全面分離と区別。',
['誤：母語・母文化の支えを否定','誤：他教科の支援を無条件に排除','正：実態に応じて他教科の表現・語彙の支援を検討','誤：所属学級への学習参加を常に排除'])
k='Q_O_045';opts=q[k]['opts'].copy();opts[0]='文章題の理解や学習への参加状況を、課題や日々の観察で継続的に確かめる'
review(k,'取り組みを見直すため、児童の理解と学習参加の変化を把握したい。この目的に合う方法を一つ選びなさい。',opts,[
'基本構想は、学習の過程で日本語の力と内容の理解を把握し、次の学習課題につなげる形成的な評価を挙げています。課題や観察で変化を確かめ、指導の見直しに使う方法が合います。変化があっても、その原因がこの支援だけだと確定するものではありません。',
'基本構想は授業後にも内容の理解を確かめる方法を提案しています。把握できないものと決めて確認を行わない肢は、この設問の見直しという目的に合いません。単一のテストだけで支援の因果効果全体を証明できるという意味ではありません。',
'基本構想は教師・指導者が学習過程で理解を把握することを挙げています。保護者にのみ任せ教師は一切関与しないという肢は合いません。家庭から情報を得ることを否定するものではありません。',
'基本構想は児童の実態に応じて表現や活動を工夫し、理解を確かめながら進める考え方です。開始後は一切確認しないという肢は、継続的な把握と見直しの目的に反します。'],1,['S23'],
'基本構想の日本語力・学習内容理解の把握と形成的評価を照合。観察や課題で把握する変化と支援の因果効果の証明を区別し、元設問の効果確認の過大な解釈を防ぐ。教師・家庭の役割も一方を排除しない。',
['正：継続的に理解と参加を把握し見直す','誤：見直しに必要な確認を排除','誤：教師自身による把握を排除','誤：開始後の確認・見直しを排除'])
assert len(extra)==36,len(extra)
assert sum(bool(c.get('remove_paragraph')) for c in extra)==1
assert 15-6==9 and 15+6==21 and 21-15==6
for name,obj in [('changes.json',cs+extra),('changes_batch117.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
meta=[];root=Path('/workspace/scratch/01d7c3f9b818')
for sid,name,url,scope in [('S23','jsl117_basic.html','https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/001.htm','elementary final report basic conception main body: integration, participation, mother language/culture, individual assessment, topic/subject types, pull-out and regular class'),('S23','jsl117_subject.html','https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/006.htm','main body1-2.3: subject learning participation, support integration, development principles and subject-specific expressions'),('S181','jsl117_math.html','https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/015.htm','5.1.1-5.2 and5.4.1: language and prior subject learning, multiple possible difficulties, individual context; arithmetic examples independently calculated, not reported experiments'),('S182','jsl117_support.html','https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/1295288.htm','1.1-1.2: collaboration and shared practice, mother-language support; no current internet-access statistics or legal procedures')]:
 raw=(root/name).read_bytes();assert len(raw)>10000;meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_read_scope=scope,retrieved='2026-10-16',full_source_redistributed=False))
(b.OUT/'evidence/batch117_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('6 questions/36 edits including1 obsolete paragraph removal; arithmetic9/21 verified')
