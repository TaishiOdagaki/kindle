"""One-time classroom arrangement and PDCA source audit. Do not rerun."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3741
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_4_018',3,['S250'],
'イェール大学Poorvu Centerの公式ガイドが示す教室の座席配置の用途について、説明に合うものを一つ選べ。',
['列型の固定席では全員が互いに向き合うため、教師の方を向く配置とは区別される。',
'円卓型は互いの顔が見えない構造なので、全体での対話にも隣同士の対話にも使えない。',
'グループ型やペア型の配置は、授業時間の多くを共同作業に充てる場合の選択肢となる。',
'U字型は前方の教材を投影して議論する活動には使えないため、ガイドはその用途を除外する。'],
['同ガイドの列型は、学習者が教師の方を向き、互いには背を向ける配置です。固定席であっても、隣同士で行う活動を取り入れる案は別途示されています。',
'同ガイドの円卓型では教師と学習者が互いに向き合います。全体での対話や相手と組んでの対話を支える配置として説明されています。',
'同ガイドのGroup and Pair Podsの用途に対応します。座席配置は授業の活動や目標に合わせて選び、必要に応じて変えるという推奨と合わせて理解します。',
'同ガイドのHorseshoe or Semicircleは、前方の教材を投影しながら議論する場合にも適する配置として説明されています。その用途を除外する記述は逆です。'],
['誤：列型で向く方向を逆転','誤：円卓型の対面と対話の用途を否定','正：共同作業中心の場合の用途に一致','誤：U字型の投影と議論の用途を否定']),
('Q_M_023',2,['S250'],
'前方の画面に教材を投影し、それを見ながら全体で議論する教室を計画する。イェール大学Poorvu Centerの公式ガイドに照らした配置の検討として適切なものを一つ選べ。',
['投影機器を置けば活動と座席配置の関係を考える必要はなくなるので、授業の目標は配置の検討から外す。',
'U字型や半円型を候補にし、前方の教材の投影と参加者間の議論という活動に合わせて配置を検討する。',
'U字型は学習者間の議論を妨げるための配置なので、教材の議論を行わないことを目的に採用する。',
'固定席の教室では隣同士で行う活動もできないため、配置を動かせなければペアで考える活動をすべて取りやめる。'],
['同ガイドは、座席配置を授業の目標や活動に合わせることを推奨しています。投影機器の存在を理由に、その検討を不要とする案は合いません。',
'同ガイドは、U字型や半円型について、参加者間の議論と前方の教材の投影を扱っています。指定された活動に応じて候補とする案であり、特定機器の導入効果を保証する判断ではありません。',
'同ガイドは、U字型を学習者同士や教師との議論を促す配置として説明しています。議論を妨げることを採用目的とする案は、その説明と逆です。',
'同ガイドは、配置を変えられない列型の教室でも、隣同士で行うThink-Pair-Shareなどの活動を挙げています。固定席であることだけで相互活動を全面的に排除する案は合いません。'],
['誤：活動と配置の整合を検討しない','正：投影と議論に合わせた配置の検討','誤：U字型の議論の用途を逆転','誤：固定席での隣同士の活動を不可能と断定']),
('Q_M_022',1,['S251','S252'],
'ASQ（米国品質協会）の公式説明に照らし、PDCAサイクルの各段階の扱いとして適切なものを一つ選べ。',
['変更を計画して小規模に試し、結果を分析して学んだことを確かめ、それに基づいて対応し、次の改善へつなげる。',
'Checkは変更を試す前だけに行い、試行後の結果の分析はPDCAの手順には含めない。',
'Actでは試行から学んだ内容を使わず、変更がうまくいかなかった場合も同じ計画だけを繰り返す。',
'PDCAは一度だけで終了する手順であり、結果を使って新しい改善を計画したりサイクルを繰り返したりしない。'],
['ASQは、Planで変更を計画し、Doで小規模に試し、Checkで試行結果を検討・分析して学びを確かめ、Actでそれに基づき対応すると説明しています。継続的な改善のために繰り返す手順です。',
'ASQのCheckは、試行の結果を検討し、分析して学んだことを確かめる段階です。試行前だけに限定し、その後の分析を排除する説明は合いません。',
'ASQは、変更がうまくいかなければ別の計画で再び進め、成功した場合は得た学びをより広い変更へ生かすとしています。学びを使わず同じ計画だけを繰り返す案は逆です。',
'ASQはPDCAを継続的な改善のために繰り返すと説明しています。なお、Deming Instituteが説明するPDSAのSはStudyです。PDCAのCheckという語をそのままPDSAの展開語にしないよう区別します。'],
['正：計画・小規模試行・分析・学びに基づく対応と反復','誤：試行後のCheckを排除','誤：学びに基づくActを否定','誤：継続的改善のための反復を否定'])]
reasons={
'Q_4_018':'S250 Yale Poorvu Center公式Classroom Seating Arrangements本文を取得。各配置の説明とAlign Arrangement with Activity、Be Intentional about Engagementを全肢全解説へ照合。旧稿の円形配置による緊張緩和・ラポール形成の一律効果、島型の集中低下を根拠不足のまま承認せず、大学ガイドの用途説明に限定。引用研究原著は未取得で因果効果の実証には用いない。',
'Q_M_023':'S250同公式ガイド本文を取得。U字・半円の投影と議論、活動目標に合わせた配置、固定席でも隣同士のThink-Pair-Shareが可能との説明を全肢全解説へ照合。同じICTを含む教室環境の領域で、投影と議論という活動を明示。特定機器・サービスの現行仕様や導入効果の保証は問わない。',
'Q_M_022':'S251 ASQ公式PDCA Cycle本文の4段階・反復とS252 Deming Institute公式PDSA Cycle本文を取得照合。Checkにも結果分析と学びが含まれるASQの説明を保持し、PDSAのStudyと展開語を区別。PDCAは学びを含まないという一般化をしない。旧誤答のCLIL・PPP・TBLTは今回各原著を取得していないため承認せず、同じ改善サイクル領域内の段階判断へ差替え。Deming本人の原著全文・発祥史や授業効果の実証を承認したものではない。'}
extra=[]
for k,key,sources,stem,opts,exps,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   assert html.unescape(old)!=new
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reasons[k],sources=sources,applied=True,before_version='第184バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reasons[k],option_verdicts=verdicts,candidate_answers=[],stem_review='指定した公式説明と活動条件の範囲を明示して再判定。',explanation_review='全4肢・4解説を取得本文と照合。一般的因果効果・機器仕様・原著起源史へ拡大しない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定資料・活動条件に対応',no_correct_risk=f'なし：{key}の本文根拠を取得')
assert len(extra)==27
for n,obj in [('changes.json',cs+extra),('changes_batch185.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
