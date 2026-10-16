"""One-time source-bounded review of coursebooks and reflective timing."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2686
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S183'],applied=True,before_version='第122バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S183'],reason=reason,option_verdicts=verdicts,stem_review='Cambridge公式TKT GlossaryのBook/Adapt/Supplementary material/Reflect on teaching/Reflective/Timingの本文と画像を独立照合。全4肢の排他性を資料内定義と具体例に限定して判断。',explanation_review='全4解説を照合。教材の分類と調整、時間の見積りと改善の省察を区別。用語集の定義を、特定調整が必ず学習効果を向上させる実証や日本語教育全体での統一用語の証拠にしない。',unresolved='',multiple_correct_risk='なし：独立正答'+str(key)+'のみ適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_4_043';opts=q[k]['opts'].copy()
opts[0]='コースブックは授業で継続的に使う教材で、通常はシラバスに沿って語彙・文法や技能を扱う。副教材は、それに加えて用いる教材であり、発音練習を補う教材などが例となる。'
opts[2]='教材を学習者に合うように調整するadaptationとは、クラスの違いにかかわらず、教材の内容を一切変更せずに使うことである。'
opts[3]='副教材とはコースブックそのものだけを指し、コースブックに加えて練習を補う教材は含まれない。'
review(k,'CambridgeのTKT公式用語集におけるcoursebook・supplementary material・教材のadaptationの説明に沿うものとして、最も適切なものを一つ選びなさい。',opts,[
'同用語集はコースブックを授業で継続的に使い、通常シラバスに沿う教材とし、副教材をそれに加えて使う教材と説明しています。分類を用いる際はこの役割の違いに着目し、特定の形態だけに限定しません。',
'同書のadaptの項目は、特定のクラスに合うように文章等を変更することを示し、長すぎたり難しすぎたりする文章の一部を省く例も挙げています。全練習を無条件に原順序で完遂するという肢とは異なります。',
'教材のadaptationは、学習者に合うように内容等を変更することです。クラスの違いを考慮せず一切変更しない、という定義は対応しません。個々の調整が必ず学習効果を上げると保証する説明ではありません。',
'副教材はコースブックに加えて使う教材であり、発音練習の教材が例示されています。コースブックそのものだけを指し、補う教材を含まないとする肢は分類を取り違えています。'],1,'TKT公式用語集印刷2・6・44頁/PDF3・7・45の定義と例を本文・画像照合。全コースブックの体系性や学習者分析が常に最優先という未取得の順位付けを断定せず、通常の特徴と調整の定義に範囲限定。副教材をあらゆる教具・全メディアへ無条件に拡張する説明を除き、追加して使う教材という機能を問う。',['正：通常のコースブックと追加教材の役割に対応','誤：教材調整の例を排し無条件の全内容完遂を原則とする','誤：adaptationの定義を無変更使用と取り違える','誤：追加教材を副教材から除きコースブック自体に限定する'])
k='Q_M_032';opts=q[k]['opts'].copy()
opts[0]='授業後に何がうまくいき、何がうまくいかなかったかを振り返り、活動に見積もった時間の見直しを検討することは、今後の授業改善を目指す省察の一例となる。'
review(k,'CambridgeのTKT公式用語集にある授業の省察とtimingの説明を踏まえ、実施後に時間配分を検討する例として、最も適切なものを一つ選びなさい。',opts,[
'同書は省察を、授業後にうまくいった点・いかなかった点を考えて今後の改善を判断することと説明します。活動や段階に要する時間の見積りを振り返るという肢は、その定義に沿う具体例です。時間を変えれば必ず成果が上がるという保証ではありません。',
'省察は実施した授業を考えて今後の改善を判断するものです。一度決めた配分は今後一切変更できないとすることは、その改善の検討を閉ざしてしまいます。',
'timingは授業計画の活動や段階に要する時間の見積りです。毎回無作為に配分を決めるというだけでは、実施結果を振り返って次の配分を検討する例にはなりません。',
'時間の見積りは授業計画に関係し、その実施結果を考えて今後の改善を判断することは省察の例となります。これを授業計画や自己点検に無関係と断定する肢は対応しません。'],1,'TKT公式用語集印刷38・48頁/PDF39・49のReflect on teaching/ReflectiveとTimingを本文・画像照合。時間見直しを省察の具体例として独立判定し、あらゆる配分変更で学習効果が必ず上がるという実証的保証にしない。固定禁止・無作為・無関係という誤答を定義との不一致で説明。',['正：実施後の振り返りから時間の見積りを改善検討する例','誤：今後の見直しを一切禁止する','誤：無作為配分だけでは実施後の省察を示さない','誤：授業計画の時間見積りと改善の省察を無関係と断定'])
assert len(extra)==14,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch123.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'tkt.pdf').read_bytes()
(b.OUT/'evidence/batch123_sources.json').write_text(json.dumps([dict(source_id='S183',url='https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-16',body_read_scope='printed2/6/38/44/48, PDF3/7/39/45/49 text+images: Adapt, Book, Reflect on teaching/Reflective, Supplementary material, Timing; terms only, not underlying experimental studies',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('2 questions/14 edits')
