"""One-time rubric/case6 audit against acquired institutional primary teaching texts."""
import json,html,gzip,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2532
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(o,n) in enumerate(zip(olds,news)):
   o=html.unescape(o)
   if o==n:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=sources,applied=True,before_version='第114バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='ケース6の全2段落、設問、全4肢を精読。評価観点・段階記述と、保護者への根拠説明という明示事実に照らして独立比較。',explanation_review='各肢の意味・解説を取得した根拠本文と照合。用語の機能とケースへの適用判断を区別し、基準表を用いるだけで妥当性・公平性・納得の因果効果が保証されるとはしない。',unresolved='',multiple_correct_risk='なし：明示された機能・説明方針に合うのは'+str(key)+'のみ',no_correct_risk='なし：独立正答'+str(key))
k='Q_O_026'
review(k,q[k]['stem'],q[k]['opts'],[
'言語学習のポートフォリオの例として、欧州評議会のELPには学習歴・経験を記録する部分や、作品などを選んで収めるドシエがあります。評価に使う資料を蓄積できますが、このケースの観点別・段階別の評価基準表を指す名称はルーブリックです。',
'CMUの教材は、ルーブリックを評価観点、その記述、到達段階を示す採点用の道具と説明しています。ケースの表はこの構成に合います。表があるだけで採点の妥当性や採点者間の一致が保証されるという意味ではありません。',
'国立国語研究所の解説は、コーパスを実際に使われた言葉のデータを集め、検索や言語研究に使えるようにしたデータベースと説明しています。ここで問う観点別・段階別の評価基準表そのものではありません。評価との関係を一律に否定して区別する必要はありません。',
'Cornell大学の教材は、シラバスが学ぶ内容・時期・方法や、課題・試験の日程、成績評価に関する方針を伝えると説明しています。評価の情報を含む場合もありますが、ケースの観点ごとの到達段階を記述した表を指す名称とは異なります。'],2,['S174','S176','S177','S178'],
'設問と4用語は維持し、各解説を一次本文へ照合。コーパスを評価と無関係とする全面否定、シラバスを項目一覧だけとする狭い説明を修正。ポートフォリオはELPを具体例としてルーブリックと区別し、両者の併用を否定しない。',
['誤：学習の記録・作品等の集積と基準表の名称を混同','正：評価観点・記述・到達段階という表の構成に一致','誤：言語データベースと基準表の名称を混同','誤：授業の方針・計画を伝える文書と基準表の名称を混同'])
k='Q_O_028';opts=q[k]['opts'].copy();opts[0]='用いた評価の観点・到達段階と、実際の発話のどの部分を根拠に採点したかを対応させて説明する'
review(k,'このケースでは、評価の観点と採点の根拠を具体的に説明する方針をとる。保護者の疑問に対するルーブリックの用い方として、この方針に合うものを一つ選びなさい。',opts,[
'Cornell大学の教材は、ルーブリックによって課題の評価対象や期待を明確にし、段階ごとに記述を設ける考え方を示しています。それを本ケースに適用し、実際の発話と基準を対応させて採点理由を説明する提案です。保護者の納得を必ず得られるという実証結果ではありません。',
'設問は観点と採点根拠を具体的に説明する方針を明示しています。ルーブリックが示す基準や段階と対応させず、根拠を不要として感覚だけで答える肢は、その方針に合いません。',
'ルーブリックは評価対象や期待を明確にする採点資料です。このケースでは基準を参照し、判断した根拠を説明するために使えます。説明とは無関係と一律に扱う肢は合いません。法令上の説明義務の有無を判断する問題ではありません。',
'基準表を示すことと、疑問に応じて採点理由を説明することは同じではありません。資料は段階の区別を明確にし、利用者の意見を基に見直す手順も挙げています。見せるだけで疑問が必ずなくなり説明も不要になるという肢は、この方針に合いません。'],1,['S175'],
'Cornell大学のルーブリック本文（定義・基準の明確化・段階記述・利用者からのフィードバックと改訂）を取得し、ケースへの独立した適用として判断条件を明示。納得を得やすくなるという未照合の対保護者効果を正答から除き、基準と実際の発話を対応させる説明に改訂。原著の保護者対象実験や法的義務の証明とはしない。',
['正：評価観点・段階と発話の根拠を対応させる','誤：明示された根拠説明の方針に反する','誤：基準を説明の資料とする機能を全面否定','誤：提示だけで疑問消滅・説明不要とする'])
assert len(extra)==10,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch115.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path('/workspace/scratch/01d7c3f9b818');meta=[]
for sid,name,url,scope in [
('S174','cmu_rubric','https://www.cmu.edu/teaching/assessment/assesslearning/rubrics.html','definition: criteria, descriptors, performance levels; not universal effect proof'),
('S175','cornell_rubric','https://teaching.cornell.edu/teaching-resources/assessing-student-learning/using-rubrics','definition, Why use, Considerations, Getting started; case6 parent explanation is editorial application, not parent experiment'),
('S176','coe_elp','https://www.coe.int/en/web/portfolio/introduction','definition and components; ELP is example, not all portfolios identical'),
('S176','coe_dossier','https://www.coe.int/en/web/portfolio/the-dossier','selected work/records, process/display dossiers; not grading rubric itself'),
('S177','ninjal_corpus','https://kotoba.ninjal.ac.jp/digest/03/d-03-02/','2018-04-18 interview: Ogiso answer to first corpus-definition question only'),
('S178','cornell_syllabus','https://teaching.cornell.edu/teaching-resources/preparing-teach/designing-your-course/write-course-syllabus','introduction and Functions of a Syllabus; not every syllabus or law')]:
 raw=(root/(name+'115.html')).read_bytes();assert len(raw)>10000
 meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),archive=None,archival_limit='full source HTML cached privately for inspection, not redistributed in repository',body_read_scope=scope,retrieved='2026-10-16',approval='source body acquired; no snippet-only approval; independent Japanese paraphrase, not full translation'))
(b.OUT/'evidence/batch115_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('2 questions/10 ordered changes;6 primary HTML acquisition hashes recorded')
