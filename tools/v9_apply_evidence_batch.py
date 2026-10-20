"""Apply an explicitly reviewed batch; never infer approval from machine checks."""
import argparse,json,html
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
ap=argparse.ArgumentParser();ap.add_argument('data');args=ap.parse_args()
data=json.loads(Path(args.data).read_text());batch=data['batch'];cs=json.loads((b.OUT/'changes.json').read_text());d=json.loads((b.OUT/'decisions.json').read_text())
assert len(cs)==data['expected_prior_edits']
_,q,a=qa.audit(str(b.DST));blocks,_=qa.blocks(qa.load(str(b.DST))[0]);extra=[]
for r in data['reviews']:
 k=r['id'];ak='A_'+k[2:];key=r['answer'];assert d[k]['status']=='要追加確認' and int(a[ak]['ans'])==key
 assert len(r['options'])==len(r['explanations'])==len(r['verdicts'])==4 and r['sources'] and r['reason']
 stems=[html.unescape(x['t']) for x in blocks[k][1:-1] if not x['ind']]
 assert all(stems)
 for i,old in enumerate(stems):
  new=r['stem'] if i==0 else ''
  if old!=new:extra.append(dict(id=k,field='stem',index=None,before=old,after=new,reason=r['reason'],sources=r['sources'],applied=True,before_version=f'第{batch-1}バッチ後',block_context=k,**({'remove_paragraph':True} if i else {})))
 for field,oldvalues,values in [('options',q[k]['opts'],r['options']),('explanations',a[ak]['txt'],r['explanations'])]:
  for i,(old,new) in enumerate(zip(oldvalues,values)):
   old=html.unescape(old)
   if old==new:continue
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else {'stem_context':r['stem']}
   extra.append(dict(id=k,field=field,index=i,before=old,after=new,reason=r['reason'],sources=r['sources'],applied=True,before_version=f'第{batch-1}バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=r['sources'],reason=r['reason'],option_verdicts=r['verdicts'],candidate_answers=[],stem_review=r['stem_review'],explanation_review=r['explanation_review'],unresolved='',multiple_correct_risk=f'なし：設問条件に合うのは{key}のみ',no_correct_risk=f'なし：{key}は取得本文と設問条件に整合')
assert extra
for name,obj in [('changes.json',cs+extra),(f'changes_batch{batch}.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(f"Explicitly reviewed {len(data['reviews'])} questions; {len(extra)} edits")
