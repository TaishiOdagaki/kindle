"""One-time removal of an unverified short-term retention advantage."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2797
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_O_053';assert d[k]['status']=='修正必要' and a['A_O_053']['ans']=='3'
stem='ケース11でA教師が中心とした練習の特徴として、ケース本文から直接確認できるものを一つ選べ。'
opts=[
'学習者が新しい相手に理由を尋ね返し、依頼の条件について自由に交渉する練習である。',
'学習者自身が依頼の場面と学習目標を自由に選び、活動の進め方を決める練習である。',
'教師の提示語に応じて文の一部を入れ替え、同じ文型を口頭で繰り返す練習である。',
'学習者は内容を黙読するだけで、文型への注意や発話の練習を行わない活動である。']
exps=[
'A教師の中心とした活動は、提示語に応じた文の置換と対話文の暗唱です。新しい相手との自由な条件交渉を行う練習は、ケースのA教師の説明には示されていません。',
'A教師は対象文型を定め、提示語を与えて練習を進めています。学習者が場面・目標・進め方を自由に決めるという活動は、ケース本文から確認できません。',
'公式TKT用語集は、置換ドリルを教師の提示した文と別の語句に基づき、同じ構造で語句を入れ替える練習と説明します。ケースの提示語による置換に対応します。反復の機会があることと、短期間で定着する効果が実証されていることは別です。',
'ケースには文の置換、対話文の暗唱、誤用時の言い直しが示されています。黙読だけで文型への注意や発話の練習をしないという説明とは一致しません。']
reason='ケース11本文とCambridge公式TKT GlossaryのDrill（印刷14/PDF15）を本文・画像照合。提示語による同じ構造の置換とguided repetitionという活動の特徴を確認。元の短期間の正確な定着、他教授法より自発能力を育成、即時訂正と不安、学習スタイル対応という未取得実証の比較/因果を承認せず、ケースから直接確認できる練習機会に限定して再構成。方法の特徴と学習効果の実証を区別する。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_O_053']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  old=html.unescape(old)
  if old==new:continue
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S183'],applied=True,before_version='第128バッチ反映後',block_context='A_O_053' if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==2 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=3,fixes_applied=True,sources=['S183'],reason=reason,option_verdicts=['誤：自由な条件交渉はA教師の説明にない','誤：場面・目標・進め方の自由選択は説明にない','正：提示語による文の置換に一致','誤：置換・暗唱・言い直しの明示と矛盾'],stem_review='設問と4肢をケース11のA教師の本文と公式用語集Drillへ独立照合。本文にない効果・活動を推定しない。',explanation_review='全4解説をケースとDrillの本文・画像照合。短期定着、教授法間の効果比較、不安への因果、学習スタイルへの一般化は撤回し未承認。',unresolved='',multiple_correct_risk='なし：独立正答3のみ適切',no_correct_risk='なし：独立正答3')
for name,obj in [('changes.json',cs+extra),('changes_batch129.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'tkt-glossary.pdf').read_bytes()
(b.OUT/'evidence/batch129_sources.json').write_text(json.dumps([dict(source_id='S183',url='https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-17',body_read_scope='Printed14/PDF15 Drill entry full text+image; guided repetition/substitution matching case11, no comparative retention/anxiety/style causal approval',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('1 question/9 edits')
