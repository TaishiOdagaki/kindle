"""One-time official-framework rejudgment of observation and identity items."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3034
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_2_031':dict(key=3,
 stem='非言語的な側面を含む会話の観察について、欧州評議会のRFCDC（2018）が述べる「聞く技能と観察する技能」に合うものを一つ選べ。',
 opts=['発話に使われた語句だけを捉え、声の調子や身体の動きには注意を向けない。','ことばと身体動作が一致しないように見えても、その不一致には注意を向けない。','声の調子や身体動作にも注意を向け、発言とその場の社会的文脈との関係を捉える。','同じ状況では人の反応に違いがないと考え、文化的所属が異なると捉えられる人同士の反応を比較しない。'],
 exps=['48頁は、何を言ったかだけでなく、どのように言ったかにも注意を向けると述べています。声の調子や身体の動きを一律に観察から外す説明は合いません。','48頁の技能の第2項は、言語メッセージと非言語メッセージの間にあり得る不一致にも注意を向けることです。不一致を無視する説明は、この記述と逆です。','48頁は、声の調子などの話し方と、視線・表情・身ぶりなどの身体動作への注意を含めています。第4項では、発言とその社会的文脈との関係にも注意を向けると述べています。','48頁の第6項は、同じ状況への人々の反応について類似点と相違点に注意を向けることです。個人差を排除したり、比較を不要としたりする説明ではありません。'],
 verdicts=['誤：語句以外の話し方と身体動作への注意を排除する','誤：第2項の言語・非言語間の不一致への注意を逆にする','正：話し方・身体動作への注意と第4項の社会的文脈に一致する','誤：第6項の反応の類似と相違の観察を排除する'],
 reason='S213印刷48頁の本文と列挙6項を全件精読・画像照合。うなずきという身体動作を音声と一括してパラ言語と呼び、日本語や他言語の相槌の頻度・解釈を一般化した旧問題は、その全経験的主張を承認できていない。同じ非言語的側面を含む会話の観察という学習領域で、公式枠組みに対象を明示して全4肢・4解説を改訂。語句以外の声と身体動作、言語・非言語間の不一致、社会的文脈、個人間の反応の類似・相違を本文に照合した。国別の身ぶりや視線の意味、相槌頻度、パラ言語という専門分類の境界をこの資料だけで実証・承認したとはしない。'),
'Q_3_034':dict(key=4,
 stem='留学生Cさんは、日本に滞在しながら、母国の家族、学校の友人、趣味のクラブの仲間とのつながりをそれぞれ大切にしている。また、相手や場面によって、自分のどのつながりを強く意識するかが変わると話した。欧州評議会のRFCDC（2018）におけるアイデンティティと文化的所属の捉え方に合う説明を一つ選べ。',
 opts=['文化的所属とは国家への所属だけを指し、家族や趣味の集団とのつながりは含まれない。','同じ文化的集団に属する人は、利用する文化的資源も、その文化に対する個人的な意味づけも全員同じである。','文化的アイデンティティをどれほど強く意識するかは、社会的な文脈や本人の関心が変わっても変動しない。','一人が複数の文化的集団とつながり、どの所属を強く意識するかが場面や時間に伴って変わることがある。'],
 exps=['30頁は、国家に限らず、家族や職業集団などさまざまな規模の集団に文化があり得ると述べています。29頁にも趣味のクラブなどの集団が社会的アイデンティティの例として挙げられています。','30頁は、各人が利用する文化的資源は集団全体の資源の一部であること、文化に対する意味や感情には個人の経歴や経験などが関わることを述べています。全員同じとする説明は合いません。','30頁は、社会的・文化的アイデンティティの主観的な重要性が、社会的文脈や関心・必要・目標・期待に関連して変動すると述べています。変動を排除する説明ではありません。','29〜30頁は、複数のアイデンティティと文化的所属、および文脈や時間に伴う所属の重要性の変化を述べています。Cさんの自己説明をその枠組みと対応づけたものであり、心理的な不適応や特定の症状を診断したものではありません。'],
 verdicts=['誤：国家だけへの限定は家族等の集団を含む本文に反する','誤：個人が利用する資源や意味づけの個別性を否定する','誤：文脈や関心等による主観的重要性の変動を否定する','正：複数の所属とその重要性の文脈・時間による変化に一致する'],
 reason='S213印刷29–33頁の本文を精読（今回は27–33頁も通読）、29・30頁を全頁画像照合。旧問題は帰国時の不適応とアイデンティティ変容が両立し得るのに、現在日本にいるというだけで帰国時の説明を排除していた。未取得のリエントリーショック理論の定義や心理症状の原因を推定して承認せず、同じアイデンティティと文化的所属という学習領域で、複数の所属と文脈による重要性の変化を問う事例へ改訂。4肢・全解説を29–30頁の定義と記述へ照合。単なる仮想例の対応であり、留学生一般の心理的変化の実証、葛藤の必然性、臨床診断を主張しない。')}
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='修正必要' and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=['S213'],applied=True,before_version='第149バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=['S213'],reason=v['reason'],option_verdicts=v['verdicts'],candidate_answers=[],stem_review='公式枠組みの対象と条件を設問に明示し、事例の推定診断や国別一般化を避けて全4肢を独立判定。',explanation_review='全4解説を取得本文の列挙項目・定義・限定へ照合。旧問題にあった未取得の経験的・理論的主張を承認せず改訂した。',unresolved='',multiple_correct_risk='なし：指定した枠組みの記述に一致するのは独立正答のみ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch150.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'rfcdc150.pdf').read_bytes()
e=dict(source_id='S213',title='RFCDC Volume 1 (Council of Europe, 2018)',url='https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c',read_scope='追加で印刷27–33頁（PDF29–35頁）の全本文を通読、29–33頁の概念定義を精読、29・30頁を画像照合。第149バッチで読了した48頁の本文・全6項を再照合。全89頁精読ではない。',image_pages_printed=[29,30,48],sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),limitations='公式枠組みに限定した記述。国別の相槌・身ぶり・視線の経験的主張、パラ言語の専門分類、リエントリーショック理論や症状の診断、葛藤の必然性を承認していない。',full_source_redistributed=False)
(b.OUT/'evidence/batch150_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 18 edits; keys 3 and 4 retained')
