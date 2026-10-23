#!/usr/bin/env python3
"""Classify manuscript/source differences without treating historical changes as errors."""
import collections,csv,hashlib,json,re,sys
from pathlib import Path
from audit_2027_epub import read_epub,norm,txt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'publishing/2027/round39';OUT.mkdir(exist_ok=True)
old=json.loads((ROOT/'publishing/2027/round37_baseline/corpus_500.json').read_text());B={q['id']:q for q in old}
master=json.loads((ROOT/'audit/v9/academic_master_500_20261022.json').read_text());M={q['id']:q for q in master['questions']}
supp=json.loads((ROOT/'audit/v9/academic_master_supplemental_edits_20261022.json').read_text())['edits']
_,roots,new,_,qa=read_epub(ROOT/'publishing/2027/round38/2027_round38_review.epub');N={q['id']:q for q in new}
body=norm(''.join(txt(r) for r in roots.values()))
supp_results=[]
for k,e in enumerate(supp):
 before=norm(e['before']);after=norm(e['after']);hit=after in body if after else before not in body
 superseded=[j+1 for j,f in enumerate(supp) if j>k and after and norm(f['before'])==after and f['id']==e['id']]
 state='after_present' if after and hit else 'before_absent' if not after and hit else 'superseded' if superseded else 'unresolved'
 supp_results.append(dict(record=k+1,id=e['id'],field=e['field'],state=state,superseded_by=superseded))
assert not any(e['state']=='unresolved' for e in supp_results)
shortdocs='\n'.join(p.read_text() for p in (ROOT/'publishing/2026_exam_last_minute_20261022').glob('round*'))
shortnorm=norm(shortdocs)
decisions=[]
for q in old:
 id=q['id'];m=M[id];fields={}
 for f in ['stem','options','answer','explanations']:
  if q[f]==m[f]:continue
  if f=='stem':
   if norm(q[f])==norm(m[f]):state='whitespace_only'
   elif id=='Q_4_083':state='retain_2027_schon_round33_revision_pending_primary_text_freeze'
   else:
    stripped=norm(m[f]);removed=[]
    for k,e in enumerate(supp):
     if e['id']==id and e['field'] in ['stem_continuation','case_text'] and not e['after']:
      needle=norm(e['before'])
      if needle in stripped:stripped=stripped.replace(needle,'');removed.append(k+1)
    state='retain_documented_supplemental_deletion' if stripped==norm(q[f]) else 'unresolved'
   fields[f]=dict(decision=state)
   if state=='retain_documented_supplemental_deletion':fields[f]['supplemental_records']=removed
  elif f=='options':
   if id=='Q_4_083':fields[f]=dict(decision='retain_2027_schon_round33_revision_pending_primary_text_freeze')
   else:
    diffs=[dict(option=k,academic=a,baseline=b,documented_text_present=norm(b) in shortnorm,restored_in_round38=N[id]['options'][k-1]==a) for k,(a,b) in enumerate(zip(m[f],q[f]),1) if a!=b]
    fields[f]=dict(decision='review_historical_shortening',details=diffs,scholarly_reendorsement=False)
  elif f=='explanations' and id=='Q_4_083':fields[f]=dict(decision='retain_2027_schon_round33_revision_pending_primary_text_freeze')
  else:fields[f]=dict(decision='unresolved')
 if fields:decisions.append(dict(id=id,fields=fields))
unresolved=[dict(id=d['id'],field=f) for d in decisions for f,v in d['fields'].items() if v['decision']=='unresolved']
print('Unresolved source differences:',unresolved)
assert not unresolved
(OUT/'baseline_difference_decisions_56.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
(OUT/'supplemental_69.json').write_text(json.dumps(supp_results,ensure_ascii=False,indent=2)+'\n')
def screen(qs):
 lengths=[];stems=collections.defaultdict(list);duplicate_options=[]
 for q in qs:
  lens=[len(norm(x)) for x in q['options']];key=q['answer']-1;other=max(v for k,v in enumerate(lens) if k!=key);gap=lens[key]-other
  lengths.append(dict(id=q['id'],correct=q['answer'],correct_characters=lens[key],longest_incorrect=other,gap=gap,correct_strictly_longest=gap>0))
  stems[norm(q['stem'])].append(q['id'])
  if len(set(norm(x) for x in q['options']))<4:duplicate_options.append(q['id'])
 return dict(total=len(qs),strictly_longest=sum(r['gap']>0 for r in lengths),gap_at_least_10=sum(r['gap']>=10 for r in lengths),gap_at_least_20=sum(r['gap']>=20 for r in lengths),exact_duplicate_stems=[ids for ids in stems.values() if len(ids)>1],duplicate_options=duplicate_options),lengths
bs,bl=screen(old);ns,nl=screen(new)
reviewed=set(e['id'] for e in json.loads((ROOT/'publishing/2027/round38/revisions_14.json').read_text())['edits'])
rows=[]
for seq,q in enumerate(new,1):
 id=q['id'];priority=next(r for r in nl if r['id']==id)
 rows.append(dict(sequence=seq,id=id,current_scholarly_status='new_source_check_round38' if id in reviewed and id not in ['Q_2_025','Q_3_011'] else 'qualification_restored_inherited_source' if id in reviewed else 'inherited_v9_review_not_newly_reaudited',prior_sources=';'.join(M[id]['academic_review']['sources']),current_round38_modified=id in reviewed,remaining_option_length_gap=priority['gap']))
with (OUT/'audit_queue_500.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
with (OUT/'option_length_500.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=nl[0]);w.writeheader();w.writerows(nl)
summary=dict(all_500_full_fields_compared=True,baseline_differing_questions=len(decisions),stem_difference_classification=dict(collections.Counter(v['decision'] for d in decisions for f,v in d['fields'].items() if f=='stem')),supplemental_records=dict(collections.Counter(e['state'] for e in supp_results)),before_all500=bs,after_all500=ns,newly_source_checked_questions=12,qualification_restorations=2,other_questions_not_newly_scholarly_reaudited=486,release_ready=False)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
