"""One-time source-checked prompt and developmental peer-observation revisions."""
import json, html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text()); assert len(c)==1307
d=json.loads((b.OUT/'decisions.json').read_text()); _,q,a=qa.audit(str(b.DST)); extra=[]
items={
'Q_M_033':(1,
'LysterとMori（2006）の分類について問う。教師が学習者の誤用に気づき、正しい形を示さず、言い直しを求めるなどして自己修正の機会を与えるフィードバックの総称として、最も適当なものを選べ。',
None,
['原論文は、正しい形を与えず自己修正を促す働きかけをプロンプトと呼び、誘導、メタ言語的手がかり、明確化要求、反復を含めています。単なる聴取上の聞き返しと区別し、ここでは誤用への働きかけを問います。',
'対照分析は言語体系を比較する分析です。Wardhaugh（1970）が扱う強形・弱形も体系間の比較に関わり、設問の働きかけの名称ではありません。',
'リキャストでは教師が学習者の発話の全部または一部を暗示的に言い換えて、目標となる形を与えます。正しい形を与えないという設問の条件とは異なります。',
'学習者の誤用を系統的に分析することは、その時点の学習者の言語体系を知るための手がかりになります。ここで問う、正しい形を示さず自己修正を促すフィードバックの総称とは区別します。'],
['正：原著271–272頁のプロンプトの共通条件に一致','誤：体系比較の分析であり該当フィードバック名ではない','誤：正形式を供給するので設問条件と不一致','誤：誤用の分析と訂正フィードバックの分類を混同'],['S126','S115','S118'],
'単なる聞き返しを一律にプロンプトと断定しないよう、誤用への働きかけと自己修正機会を明記。'),
'Q_4_005':(4,
'Cambridge International Educationの公開手引きが示す、専門性の向上を目的とするピア・オブザベーションについて、最も適当なものを選べ。',
['観察した同僚の教案を、自分の学習者や授業条件を検討せずにそのまま写すことを目的とする。','経験の浅い新人教員だけを対象とし、経験豊富な教員は省察の対象から除外する。','教員を格付けすることを主目的とし、観察後には一方的に評価を告げる。','同僚の授業を観察し、記録した事実に基づく対話を通して、観察者と授業者がそれぞれの実践を振り返る。'],
['手引きは、他者の方法をそのまま写すのでなく、自分の文脈に合わせて検討・調整することを勧めています。',
'手引きは、勤務年数や校内の立場にかかわらず、どの教員にも実践を改善できる部分があると説明しています。',
'ここで指定した発達支援型のモデルでは、教員の格付けを目的としません。観察で得た根拠に基づく建設的な対話を行います。',
'このモデルは、授業改善を目的とする双方向の過程です。観察者も自分の実践を振り返り、授業者と観察後に対話します。すべての授業観察制度が人事評価と無関係だという意味ではありません。'],
['誤：文脈に合わせた調整を省くので手引きと不一致','誤：経験年数を問わないという対象条件と不一致','誤：指定したモデルの非格付け・対話の方針と不一致','正：双方向の省察と根拠に基づく対話に一致'],['S127'],
'ピア観察全般を人事評価と無関係と断定する旧解説を限定し、参照する発達支援型モデルを明示。'),
'Q_M_035':(2,
'授業改善を目的とするピア・オブザベーションを行う。Cambridge International Educationの公開手引きに沿う進め方として、最も適当なものを選べ。',
None,
['手引きは、改善すべき点だけでなく、授業の強みも振り返るよう勧めています。欠点だけに限定する方針ではありません。',
'事前に観察の焦点を合意し、その焦点に関係する事実を記録して、観察後の建設的な対話に用います。',
'このモデルでは、経験年数や立場にかかわらず教員が実践を振り返る機会をもちます。新人だけに対象を限りません。',
'手引きは、事前に観察の焦点を合意するよう勧めています。目的を共有せずに感想だけを述べる進め方とは異なります。'],
['誤：強みの省察を排除する','正：事前合意・事実記録・事後対話の手順に一致','誤：新人だけとする対象限定が不一致','誤：観察の焦点の事前合意を欠く'],['S127','S128'],
'一般的な動機づけへの因果断定を除き、公開手引きが推奨する手順の照合問題に限定。')}
for key,(ans,stem,opts,exps,verdicts,sources,reason) in items.items():
 if opts is None: opts=[html.unescape(v) for v in q[key]['opts']]
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new: continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第64バッチ反映後の累積作業稿')
   if field=='options': e['stem_context']=stem
   if field=='explanations': e['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==ans else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='設問が指定する分類・モデルの条件に全4肢を照合し独立判定。',explanation_review='全4解説を取得した根拠本文へ照合。一般的な指導効果への因果断定は採用しない。',unresolved='',multiple_correct_risk='なし：指定条件に一致する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch65.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
