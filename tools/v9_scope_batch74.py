"""Scope the new changes without rerunning the one-time audit decisions."""
import json
from pathlib import Path
p=Path('audit/v9');c=json.loads((p/'changes.json').read_text());batch=json.loads((p/'changes_batch74.json').read_text())
assert len(c)==1506 and c[-35:]==batch
for e in batch:
 e['block_context']=('A_'+e['id'][2:]) if e['field']=='explanations' else e['id']
c[-35:]=batch
for name,obj in [('changes.json',c),('changes_batch74.json',batch)]: (p/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
