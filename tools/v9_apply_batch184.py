"""One-time evidence-based teaching portfolio revision; do not rerun."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3732
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_M_021';key=1;ak='A_M_021';assert d[k]['status']=='要追加確認' and a[ak]['ans']=='1'
stem='カーネギーメロン大学Eberly Centerの公式ガイドに照らし、ティーチング・ポートフォリオの構成として適切なものを一つ選べ。'
opts=['教育理念や目標を示し、それらと関連する代表的な資料を選び、資料の文脈や意味を説明しながら自らの教育実践を省察する。','教育理念との関係や資料の意味は説明せず、授業関係の資料をすべて無選別に保存したものを提出する。','授業評価の数値だけを掲載し、教育理念、実践の説明、省察、質的な資料は含めない。','研修に出席した記録だけで授業への影響が実証されたと判断し、研修で得た知識を実践にどう生かしたかは説明しない。']
exps=['同ガイドは、教育理念・責任・目標を示す資料と、それらを実践する姿を示す量的・質的な根拠を組み合わせると説明しています。代表的で意味のある資料を選び、その文脈や意味を説明する構成に対応します。','同ガイドは、すべての資料を網羅する保管庫ではなく、代表的で意味のある資料を選ぶとしています。また、資料の意味と文脈の説明を求めており、無選別の保存だけではその構成に合いません。','同ガイドは、数値評価だけでは教育上の取組や成果を十分に表しにくいと述べ、理念・省察と量的・質的な根拠の組合せを示しています。数値の使用自体を否定する説明ではありません。','同ガイドは、研修への参加記録を教育への取組姿勢の根拠とし、影響を示すには研修で得た知識が実践にどう結びついたかを説明する必要があるとしています。参加した事実だけを授業への影響の実証とする判断は合いません。']
reason='S249 CMU Eberly Center公式Teaching Portfolios本文を取得精読。定義、Select your supporting materials、Consider where you are in your career、Write descriptions of your supporting materialsを全肢全解説へ照合。旧稿の単なる授業・研修記録の蓄積への還元を修正。旧誤答の情意フィルター・コーパス・ダイグロシアは各原典未取得のため承認せず、同じ教授ポートフォリオ領域内の構成判断へ差替え。Seldin等の原著全文を取得したとの扱いはしない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
  extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S249'],applied=True,before_version='第183バッチ後',block_context=ak if field=='explanations' else k,**kw))
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S249'],reason=reason,option_verdicts=['正：理念・選択資料・文脈説明と省察','誤：代表資料の選択と意味の説明を排除','誤：数値だけへ限定し理念や省察を排除','誤：参加の記録と授業への影響を同一視'],candidate_answers=[],stem_review='大学公式ガイドの構成判断へ範囲を明示。',explanation_review='全4肢・4解説を取得本文と照合。数値の全面否定ではなく数値だけへの限定を誤りとした。',unresolved='',multiple_correct_risk='なし：1のみ指定ガイドの構成に対応',no_correct_risk='なし：1の本文根拠を取得')
assert len(extra)==9
for n,obj in [('changes.json',cs+extra),('changes_batch184.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
