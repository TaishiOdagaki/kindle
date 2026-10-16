"""One-time AR review against the program authors' own account, not cited originals."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2463
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_4_077';assert d[k]['status']=='要追加確認' and a['A_4_077']['ans']=='4'
stem='BurnsとKhalifa（2017）第1章が報告するアクション・リサーチの実施方法として、説明に合うものを一つ選びなさい。'
opts=q[k]['opts'].copy()
opts[3]='教師が実践上の課題を探究し、採用された四段階モデルでは計画・実践・観察・内省を関連付け、得られた知見を次の取組に生かす。'
exps=[
'4頁は日常の実践現場での課題と介入、その結果の系統的な検討を扱います。理論との結び付きも目指しますが、万能の理論を作るために実験室で行うという肢の説明には対応しません。',
'5頁では、一人の教師、教師の共同研究、研究者や支援者との協働という形態を認めています。外部研究者の参加自体が誤りなのではなく、教師の探究を一方的な評価に置き換える点が、この章の説明に合いません。',
'5頁は四段階を相互に関連する反復的な過程とし、7頁も参加者が研究計画を練り直すことを記述しています。計画の変更を禁止し、最初の手順の完遂を義務とする説明は一致しません。',
'4〜5頁の実践の探究と、著者らのプログラムで採用した計画・実践・観察・内省のモデルに対応します。内省で観察結果を検討し、次の取組へつなぎます。四段階をあらゆる研究に共通する唯一の固定手順としたり、改善の成功を保証したりする説明ではありません。']
reason='S169 Burns・Khalifa2017の実施者自身による第1章公開本文4〜7頁へ照合。外部専門家の排除という誤読を防ぎ、四段階を当該プログラム採用モデルと明示。原初のKemmis・McTaggart1988や引用された各原著の取得とは区別する。'
extra=[]
for field,old,new in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_4_077']['txt'],exps)]:
 for i,(o,n) in enumerate(zip(old,new)):
  o=html.unescape(o)
  if o==n:continue
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S169'],applied=True,before_version='第109バッチ反映後',block_context='A_4_077' if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(e)
assert len(extra)==6
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S169'],reason=reason,option_verdicts=['誤：日常の実践課題の探究を万能理論の実験室研究へ置換','誤：外部研究者との協働は許容されるが一方的評価を主目的とする説明は異なる','誤：反復と計画の練り直しを否定','正：著者らの採用モデルの相互関連性と次の取組への利用'],stem_review='報告した著者・章を明示し、全4肢を4〜7頁に照合。未変更の誤答3肢も独立に否定根拠を確認。',explanation_review='全4解説を4〜5頁と7頁へ照合。実施者自身の報告するモデルと運営に限定し、全教育現場への一般効果や引用先原初モデルの全文承認は行わない。',unresolved='',multiple_correct_risk='なし：指定章に対応するのは4のみ',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',c+extra),('changes_batch110.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/01d7c3f9b818/burns110.pdf').read_bytes()
(b.OUT/'evidence/batch110_source.json').write_text(json.dumps(dict(id='S169',authors='Anne Burns and Hanan Khalifa',year=2017,title='Engaging action research to explore use of assessment for improving language ability',book='Second Language Assessment and Action Research',url='https://assets.cambridge.org/97811084/36700/excerpt/9781108436700_excerpt.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),obtained='Publisher excerpt, printed1-10, all10 pages text read',image_review_printed_pages=[4,5],question_support_pages=[4,5,7],limits='Only printed1-10 obtained, not full chapter1. Own program account only, not original Kemmis/McTaggart1988, Burns2010, other cited sources or chapter-level empirical effects. Individual research cycle differs from program management cycle in Figure1.'),ensure_ascii=False,indent=2)+'\n')
print('1 full question/6 edits; key4 unchanged')
