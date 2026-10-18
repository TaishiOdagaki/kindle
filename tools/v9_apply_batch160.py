"""Two source-bounded judgments; no diagnosis or guaranteed reflection effect."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3203
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
reason='S213 RFCDC第1巻（2018年）の取得済み89頁原PDFを第159バッチのSHA256・サイズと照合。41–43頁の開放性・尊重（注7–8含む）、47頁の批判的思考、52–53頁の自己の批判的理解、73頁の用語本文を精読し42・43・53頁を全頁画像照合。指定モデルの教育的適用に限定し、学習者の心理状態・適応段階の診断、過剰同化モデルの原著、自己点検や録画の因果的効果を承認しない。'
items={
'Q_1_002':dict(answer=4,stem='日本語学校の学習者Aさん（来日3か月）が、母国の習慣について尋ねられ、「自分の国は遅れているから、日本のやり方がすべて正しい」と話したとする。RFCDC第1巻（2018年）の開放性と尊重の説明に沿う教師の対応を一つ選べ。',opts=[
'発言の背景を尋ねず、母国の文化が日本より優れていると結論付けるよう指導する。',
'日本のやり方を全て正しいとする判断をそのまま肯定し、母国の習慣は全て捨てるよう勧める。',
'この発言だけで心理的な問題を確定し、本人の事情を聞かず、発言と他の学習者との交流を全面的に禁止する。',
'何を経験してそう感じたかを尋ね、自他の見方を具体的に検討しながら、本人の文化への帰属や考えを選ぶ権利を尊重して対話する。'],exps=[
'41頁は自分の見方の当然さを問い直し、判断をいったん保留する姿勢を示します。背景を確かめず、文化全体の優劣を逆転させた結論を教え込む対応は、この姿勢に合いません。',
'42頁は、他者を尊重することと、その人の考えへの同意・採用・転向を区別します。日本のやり方の無条件の正しさや、以前の習慣の全面放棄を教師が求める対応は、この区別に合いません。',
'本文だけでは心理状態や適応の段階は確定できません。41–43頁の開放性と尊重に照らし、事情を聞かず全面禁止する対応は支持されません。相談支援の必要性を本人の状況に応じて検討することまで否定する説明ではありません。',
'41頁は他者の見方への関心と判断の保留、42頁は本人の帰属や信念を選ぶ権利への尊重を示します。背景を尋ねて具体的に検討する対応は、この説明に沿います。全ての慣習を無条件に肯定する意味ではなく、42頁は他者の尊厳・人権・自由を侵す内容への尊重に限界を設けています。'],verdicts=['誤：判断保留を省き文化全体の優劣を逆転して教え込む','誤：尊重を同意・採用・全面転向と混同する','誤：未提示の心理状態を確定し本人の事情を聞かず全面排除する','正：開放性・判断保留・本人の選択権の尊重に対応'],detail='旧解説の過剰同化の相・適応を急ぐという心理的因果を撤回。自文化中心主義・文化相対主義という未取得の補助理論を誤答解説から除き、架空発言への対応を指定資料の原則へ限定。尊重が全慣習の無条件肯定という倫理的相対主義へ広がらない条件を注8と本文から明記。'),
'Q_O_005':dict(answer=3,stem='ケース1の教師が自分の訂正を点検する際、RFCDC第1巻（2018年）の批判的思考と自己の批判的理解の観点に沿う取り組みを一つ選べ。',overrides={2:'授業の発話記録を確かめ、自分の訂正の根拠や、質問・説明の内容を見直す'},exps=[
'47頁は自分の前提を認識して証拠と照らすこと、52–53頁は能動的な振り返りと自己の判断の点検を挙げます。経験が浅いことだけを理由に、点検そのものを不要とする肢は、この観点に合いません。気づきが成長に直結するという効果の保証ではありません。',
'ケース1では、教師自身が自分の訂正の適切さを疑っています。学習者の応答を初めから誤用と決めて無視するだけでは、47頁の証拠に基づく判断や53頁の自分の前提の点検になりません。',
'47頁は証拠と整合する評価や、自分の前提の偏りの認識を挙げます。52–53頁は能動的な振り返りと、自分の前提が判断に関わることの理解を示します。発話記録と訂正の根拠を照らし、質問や説明を見直す行為は、これらの観点に沿います。',
'52頁は批判的理解を自動的・無反省な解釈と区別します。やり方を今後一切変えないと初めから決める方針は、記録を調べて訂正や説明を点検するという今回の目的に合いません。'],verdicts=['誤：経験年数だけで点検を一括不要とする','誤：訂正の適否が論点なのに誤用と決めて無視する','正：証拠との整合性と自分の前提・判断を具体的に点検する','誤：一切変更しないと初めから決め能動的な点検を省く'],detail='初級経験者の成長へ直結するという未照合の因果効果を撤回。ケース1で教師の訂正が検討対象であることを尊重し、学習者の正用を誤用と決めない。録画を必須にせず発話記録の点検へ具体化。Schön等の省察理論原著や録画の効果の代用承認ではない。')}
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and int(a[ak]['ans'])==v['answer']
 opts=v.get('opts',[v.get('overrides',{}).get(i,t) for i,t in enumerate(q[k]['opts'])])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason+v['detail'],sources=['S213'],applied=True,before_version='第159バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==v['answer']-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['answer'],fixes_applied=True,sources=['S213'],reason=reason+v['detail'],option_verdicts=v['verdicts'],candidate_answers=[],stem_review='設問・全4肢を指定モデルの本文へ独立照合。Q1_002は架空発言、O005は累積改訂済みケース1の全3段落も精読。',explanation_review='全4解説を41–43・47・52–53頁本文へ照合。心理状態や段階の診断、文化全体の優劣、自己点検の効果を事実として追加しない。',unresolved='',multiple_correct_risk='なし：指定した観点に合うのは'+str(v['answer'])+'のみ',no_correct_risk='なし：独立正答'+str(v['answer']))
assert len(extra)==15,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch160.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'rfcdc150.pdf').read_bytes();prior=json.loads((b.OUT/'evidence/batch159_sources.json').read_text())[1];assert hashlib.sha256(raw).hexdigest()==prior['sha256']
e=[dict(source_id='S213',url=prior['url'],revalidated='2026-10-18',original_acquisition_record='evidence/batch157_sources.json',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),pdf_pages=89,read_scope='41–43頁（注7–8含む）・47・52–53・73頁の全本文を精読、42・43・53頁（PDF44・45・55頁）を1800px全頁画像照合。',limitations='取得済み同一原本の追加照合。全89頁通読ではない。心理診断・過剰同化の原著・省察理論原著・録画や自己点検の効果の実証ではない。原PDF非転載。',full_source_redistributed=False)]
(b.OUT/'evidence/batch160_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
attempt=dict(date='2026-10-18',pending_questions=['Q_2_022','Q_2_026','Q_2_027','Q_4_106'],urls=['https://www.mpi.nl/publications/item66744/politeness-some-universals-language-usage','https://www.scribd.com/doc/175689403/Brown-and-Levinson-1987-Politeness-Some-Universals-in-Language-Usage','https://pure.mpg.de/pubman/item/item_1719314_10/component/file_2152013/Brown_Politeness_2015.pdf'],result='MPI1987は書誌・概要のみ。Scribd13頁の表示は今回本文が取得できず推薦一覧のみ。Brown2015著者本人の解説PDFはWeb・curlとも403。抜粋・概要だけで承認せず全該当問の保留を維持。',full_task_blocked=False)
(b.OUT/'evidence/batch160_source_attempts.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2)+'\n')
print('2questions /15edits /keys4,3')
