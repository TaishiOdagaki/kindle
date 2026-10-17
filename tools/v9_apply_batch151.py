"""One-time Compass evidence-gated debriefing and classroom conflict repair."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3053
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_4_095':dict(key=2,
 stem='欧州評議会の人権教育手引きCompassにおける、体験活動後の「デブリーフィングと評価」の進め方に合うものを一つ選べ。',
 opts=['体験中の感情や学んだことには触れず、ゲームの勝敗の比較と表彰だけを行う。','何が起きてどう感じたか、自分自身や扱った課題について何を学んだか、学びを今後どう生かすかを振り返る。','進行役が唯一の答えを与え、参加者が互いの意見を聞いたり、自分で考えたりする機会を減らす。','活動の時間を延ばすため、振り返りや話合いの時間を優先的に削り、省略する。'],
 exps=['手引きは、活動中に起きたことと感情、自分自身や課題についての学びを振り返る問いを挙げています。ただし、本人が話したくない内容の発言や開示を強いないという運営条件も示しています。勝敗だけに限定する説明は合いません。','手引きのDebriefing and evaluation節が提案する問いの流れに対応します。活動の体験を振り返り、学びを自分の生活や地域、より広い世界と結びつけ、今後の活用を考える進め方です。','Facilitating discussions節は、参加者が互いに聞き合い、共有しながら自分たちの答えや判断を見いだす方針です。進行役の意見や助言を求めることはありますが、一方的な答えの提示へ置き換える説明ではありません。','Managing time節は、活動が予定より長引けば、話合いに十分な時間を残せるよう活動を短くすることを検討します。Debriefing and evaluation節も振り返りを活動の重要な部分としており、省略を優先する方針ではありません。'],
 verdicts=['誤：体験・感情・学びの振り返りを排除し、勝敗だけに限定する','正：当該節の問いの流れと生活・世界・今後の活用への関連づけに対応','誤：参加者が聞き合って判断する方針を一方的な答えへ置き換える','誤：話合いの時間を確保する時間管理と反対'],
 reason='S214欧州評議会Compass公式本文をHTMLで全頁取得。General tips on running activitiesの準備・時間管理・安全・基本ルール・話合い・振り返り・評価・フィードバック・抵抗・対立への対応を通読。Debriefing and evaluation等を精読し、4肢・4解説を個別照合。旧解説が示した感情→事実→原因→適用をKolbの4段階とする未取得原著への帰属を撤回し、手引きが実際に提案する問いへ限定。Kolb原著を取得・判定したものではない。感情の強制開示、全ての体験教育に唯一固定の手順があるという一般化、省略すれば必ず偏見を強化するという因果を残さない。'),
'Q_4_096':dict(key=3,
 stem='日本語教室で、Aさんが他の学習者の発話が終わる前に話し始めることがあり、学習者間で不満が出た。欧州評議会のCompassが示す話合いの運営や対立への対応を参考にする場合、それに合う教師の対応を一つ選べ。',
 opts=['Aさんの出身文化が劣っていると教師が決め、クラス全体の前で非難して従わせる。','周囲の学習者に、Aさんの発言を無視し、話合いから排除するよう指示する。','本人たちが話せる範囲で状況や考えを確かめ、互いに聞き合い、参加の機会をもてる話合いのルールを共に検討する。','状況や本人の考えを確認せず、身勝手な性格だけが原因だと断定し、発言機会を取り上げる。'],
 exps=['手引きは安全な場で多様な意見を引き出し、人への侮辱的な発言を避ける方針を示しています。出身文化を劣っていると決めて公然と非難する対応は、その方針に合いません。','基本ルールの節は、誰もが聞いてもらい、話し、参加する機会をもつことを重視します。特定の人の発言を無視して排除する指示は、この参加の方針と反対です。','基本ルールを共に話し合うこと、本人が話したくないことを強いないこと、立場や意見を明確にして互いに聞くことに対応します。事例の原因を国籍や文化、性格だけで確定せず、対話とルールの検討へつなぐ適用です。','手引きの対立への対応は、立場・意見・関心を明確にし、相互の傾聴や解決案の検討を促します。この記録だけから性格を単一の原因と断定し、参加の機会を奪う根拠にはなりません。'],
 verdicts=['誤：安全と尊重に反して文化の劣等性を断定・公然非難する','誤：全員に聞かれ話し参加する機会を設ける方針を否定する','正：本人の開示への配慮、基本ルールの共同検討、立場の明確化と傾聴に対応','誤：状況確認と傾聴を省き、単一原因を断定して参加を奪う'],
 reason='S214のCreating a safe environment、Setting ground rules、Facilitating discussions、Giving feedback、Resistance from the participants、Managing conflictを本文の前後とともに取得・精読。旧解説が国別の割り込みの解釈を実証なしに一般化し、事例の文化規範を原因として扱っていた部分を撤回。教室内の発言と不満という同じ領域の仮想事例を保ち、本人たちの視点・状況確認と話合いのルールの検討に限定して4肢・4解説を照合した。手引きの運営方針への適合であって、この教室事例の原因、ターンテイキングの国別実態、対応の効果を実証したものではない。')}
ps=[p.text for p in Document(b.DST).paragraphs]
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']!='確認済み' and q[k]['stem'] in ps and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=['S214'],applied=True,before_version='第150バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=['S214'],reason=v['reason'],option_verdicts=v['verdicts'],candidate_answers=[],stem_review='Compass公式手引きの運営方針への適合に対象を限定し、全4肢を独立判定。事例の原因や効果を推定で確定しない。',explanation_review='全4解説を該当節の本文と条件へ照合。参加者の開示を強いない条件を保ち、未取得原著への帰属・国別一般化・未実証因果を撤回。',unresolved='',multiple_correct_risk='なし：手引きの指定された方針に合うのは独立正答のみ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch151.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'compass151.html').read_bytes()
e=dict(source_id='S214',institution='Council of Europe',title='Compass — Using Compass for human rights education',url='https://www.coe.int/en/web/compass/using-compass-for-human-rights-education',retrieved='2026-10-18',format='official HTML full page acquired',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope='General tips on running activitiesからManaging conflict節末までの本文を通読。時間管理、安全、基本ルール、話合い、デブリーフィングと評価、フィードバック、抵抗、対立の各節を前後とともに精読。ウェブ表示全568行やCompass全書の通読ではない。',limitations='人権教育手引きの方針と仮想教室事例への適用。Kolb原著、国別規範、効果の実証研究は未取得・未承認。',full_source_redistributed=False)
(b.OUT/'evidence/batch151_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 18 edits; keys 2 and 3 retained')
