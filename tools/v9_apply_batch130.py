"""One-time source-bounded post-task form-focus audit."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2806
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_O_054';assert d[k]['status']=='修正必要' and a['A_O_054']['ans']=='1'
stem='ケース11のB教師が行うタスク後の確認・整理を、Jane Willisの記事の提案を参考に計画する場合、適切な方針を一つ選べ。'
opts=[
'タスクで言語を使った経験を踏まえ、教材の文法項目などを用いて形式に焦点を当てる学習を組み込む。',
'タスクを先に行った授業では、その後も文法形式に焦点を当てる学習は一切行えないとする。',
'新しい文法をすべて先に教え終えることを必須条件とし、その順序を変えることを認めない。',
'言語の学習は教師の説明だけで成立するとし、学習者が自分で言語を使う経験を除く。']
exps=[
'記事はタスクの経験の後に教材の文法部分を使う形式学習を提案します。ケースの事後整理を計画する際の参考にできます。',
'記事にはタスク・サイクル後の形式学習が明示されています。文法を一切扱えないとする肢は逆です。',
'記事は教材の順序を変え、文法部分をタスクの後で扱う案を述べます。必ず文法を先に終えるという規則ではありません。',
'記事は学習者が自ら言語を使い経験して学ぶことを重視しています。その経験を除くという方針とは異なります。']
reason='Jane Willis本人署名のBritish Council公開記事本文を再取得し、Use the book but change the order、Task Cycle、Focus on Form、Conclusionを精読。ケース11のB教師の事後整理を計画する際の適用案として照合。元の正答肢の定着に時間がかかるという普遍的比較や、フィードバックの質が効果を大きく左右するという未取得の因果効果を承認せず、原著者のタスク後の形式学習の提案に限定。1996年書籍全体・全TBL手法・全員の上達効果を承認しない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_O_054']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  old=html.unescape(old)
  if old==new:continue
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S145'],applied=True,before_version='第129バッチ反映後',block_context='A_O_054' if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S145'],reason=reason,option_verdicts=['正：タスク後に教材の文法部分を使う提案に対応','誤：タスク後の形式学習を否定','誤：文法先行を固定し順序変更の提案を否定','誤：学習者自身の言語使用と経験を排除'],stem_review='ケース11の事後整理という設定と、本人記事の提案を参照する条件を明示し全4肢を独立照合。ケースがWillisの全サイクルを実施したとは推定しない。',explanation_review='全4解説を本人記事の該当本文へ照合。未取得の時間比較やフィードバックの因果効果は撤回。',unresolved='',multiple_correct_risk='なし：独立正答1のみ適切',no_correct_risk='なし：独立正答1')
for name,obj in [('changes.json',cs+extra),('changes_batch130.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'willis.html').read_bytes();assert b'Focus on Form' in raw and b'Jane Willis' in raw
(b.OUT/'evidence/batch130_sources.json').write_text(json.dumps([dict(source_id='S145',url='https://www.teachingenglish.org.uk/comment/1307',canonical_url='https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/priming-tasks-and-target-tasks-language-focus-and',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-17',body_read_scope='Complete signed article body read; use order change, task cycle, focus on form and conclusion only. Not comments, whole 1996 book, or comparative empirical effect approval.',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('1 question/9 edits')
