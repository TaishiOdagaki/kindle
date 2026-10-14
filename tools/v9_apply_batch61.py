"""Apply source-checked recast revision; cumulative before-text assertions retained."""
import json, html
import quiz_audit as qa
import v9_apply_batch1 as b
p=json.loads((b.OUT/'evidence/batch61_Q_M_034_pending_revision.json').read_text())
c=json.loads((b.OUT/'changes.json').read_text())
assert len(c)==1252
_,q,a=qa.audit(str(b.DST))
extra=[]
for field,old,new in [('stem',[q[p['id']]['stem']],[p['proposed_stem']]),('options',q[p['id']]['opts'],p['proposed_options']),('explanations',a['A_M_034']['txt'],p['proposed_explanations'])]:
 for i,(before,after) in enumerate(zip(old,new)):
  if html.unescape(before)!=after:
   entry=dict(id=p['id'],field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=p['finding'],sources=['S37'],applied=True,before_version='第60バッチ反映後の累積作業稿')
   if field=='options':entry['stem_context']=p['proposed_stem']
   if field=='explanations':entry['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
   extra.append(entry)
(b.OUT/'changes.json').write_text(json.dumps(c+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes_batch61.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
d=json.loads((b.OUT/'decisions.json').read_text())
d[p['id']].update(status='確認済み',fixes_applied=True,independent_answer=4,sources=['S37'],option_verdicts=p['independent_option_verdicts'],reason=p['finding'],stem_review='LysterとRanta1997の分類を明示。教師の再定式化と暗示性を条件化し4肢を独立判定。',explanation_review='原著46–49頁の明示的訂正・リキャスト・明確化要求・誘導を4解説に照合。教育効果の優劣は主張しない。',unresolved='',multiple_correct_risk='なし：原著の分類と明示した条件に合うのは4のみ',no_correct_risk='なし：独立正答4')
(b.OUT/'decisions.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
