"""One-time revised audit after remote concurrent commits; no prior batch rerun."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==4242
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=json.loads("[[\"Q_2_034\",3,[\"S295\"],\"少数言語の保持と教育機会について、1992年の国連少数者の権利宣言第4条第3項・第4項に合う説明を一つ選べ。母語学習の機会と社会全体について学ぶ機会を区別して考える。\",[\"母語を学ぶ機会を設けることを、社会全体についての知識を得る機会をなくすための措置として位置付けている。\",\"少数者の歴史・伝統・言語・文化を知るための教育上の措置は、宣言では取り上げられていない。\",\"可能な限り母語を学ぶか母語で教育を受ける十分な機会のための適切な措置を求め、社会全体についての知識を得る十分な機会も示している。\",\"すべての教育機関で全科目を各人の母語だけで教えることを、実施可能性に関係なく一律に求めている。\"],[\"第4条第3項は母語学習や母語による教育の機会を扱い、第4項は少数者に属する人が社会全体を知る機会も示します。一方の機会で他方をなくすという関係ではありません。\",\"第4条第4項は、適切な場合には、領域内の少数者の歴史・伝統・言語・文化についての知識を促す教育上の措置を取るべきだとしています。\",\"第4条第3項の可能な限りという条件と、第4項の社会全体を知る機会に対応します。母語学習の教育効果を普遍的に実証した条文ではありません。\",\"第4条第3項には可能な限りという条件があり、母語を学ぶ機会または母語で教育を受ける機会を挙げています。全機関・全科目・母語のみという一律の指定はありません。\"],[\"誤：第4条第4項の社会全体を知る機会を否定\",\"誤：第4条第4項の教育上の措置を否定\",\"正：第4条第3項の条件と第4項の機会に対応\",\"誤：第4条第3項にない全機関全科目母語のみの一律条件を追加\"]],[\"Q_2_030\",4,[\"S296\"],\"EkmanとFriesen（1969）が述べる非言語行動のレギュレーター（調節行動）について、適切な説明を一つ選べ。動作の形だけでなく、会話内での働きを考える。\",[\"他者の行動に影響を及ぼす非言語行動は、他の分類に当てはまる場合も含め、すべてレギュレーターだけに分類される。\",\"レギュレーターは会話の進行には関係せず、発話中の個々の語の強調や内容の描写だけを担う。\",\"レギュレーターは会話を管理するために毎回意識的に計画される行為であり、習慣的に行われることはない。\",\"話す・聞くというやり取りの流れや進み方を調節する行動であり、うなずきや視線などがその働きを担うことがある。\"],[\"原著82頁は、他の分類の行動も調節機能を持ちうると区別します。他者に影響するという理由だけで、すべてをレギュレーターのみに分類していません。\",\"原著82頁は、レギュレーターを会話の流れや進み方と結び付け、語の強調などを担う行動と区別しています。この肢はその関係を逆にしています。\",\"原著82～83頁は、必ずしも意識的・意図的ではなく、十分に学習された習慣として行われる面を述べています。毎回意識的に計画するという限定は合いません。\",\"原著82頁の説明と例に対応します。動作の形だけで機能を固定せず、ここでは会話のやり取りを調節する働きに着目します。\"],[\"誤：調節機能と分類名の区別を消す\",\"誤：会話の流れとの関係を否定\",\"誤：常に意識的な計画とする\",\"正：会話の流れの調節と例に対応\"]]]")
reasons=json.loads("{\"Q_2_034\":\"S295 宣言第4条第3項・第4項を設問・全肢・全解説へ照合。可能な限りの母語学習または母語による教育の機会、適切な場合の少数者の歴史等の知識促進、社会全体を知る機会を区別。旧稿の相互依存仮説を実証された普遍法則とする説明と多言語表示・やさしい日本語の未照合効果を撤回し、同じ少数言語保持・教育機会領域で改訂。規範文書の内容と教育効果の経験的実証を区別する。\",\"Q_2_030\":\"S296 著者公式サイトから原著全51頁を直接取得、画像でRegulators節（印刷82～84頁/PDF35～37頁）を精読。流れ・進み方、うなずき・視線、必ずしも意識的でない習慣、調節機能と分類名の区別を全肢全解説に照合。原著はこの節で自ら調節行動の研究を行っていないと明記しており、提案を新たな実証結果と扱わない。旧稿の未照合の近接空間学定義・エンブレム例の文化的普遍性は承認しない。同じ身体非言語行動の領域で調節行動に絞って改訂。\"}")
extra=[]
for k,key,sources,stem,opts,exps,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reasons[k],sources=sources,applied=True,before_version='第196バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reasons[k],option_verdicts=verdicts,candidate_answers=[],stem_review='著者・年・分類または宣言条項を明示。規範と実証、動作の形と機能を区別。',explanation_review='全肢全解説を取得本文に照合。普遍的教育効果・行政サービス一般・形だけによる固定分類は承認しない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定本文に整合',no_correct_risk=f'なし：{key}の本文根拠取得')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch197.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

