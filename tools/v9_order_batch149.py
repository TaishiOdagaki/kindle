"""One-time ordering repair before publication; do not reapply batch149."""
import json, subprocess
from pathlib import Path
p=Path('audit/v9')
prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/changes.json']))
cs=json.loads((p/'changes.json').read_text())
batch=json.loads((p/'changes_batch149.json').read_text())
assert len(prior)==3012 and cs==prior+batch and len(batch)==22
ordered=[]
for k in ['Q_O_032','Q_4_103']:
    rows=[c for c in batch if c['id']==k]
    ordered.extend([c for c in rows if c['field']=='stem'])
    ordered.extend([c for c in rows if c.get('remove_paragraph')])
    ordered.extend([c for c in rows if c['field']!='stem' and not c.get('remove_paragraph')])
assert len(ordered)==22
for name, data in [('changes.json',prior+ordered),('changes_batch149.json',ordered)]:
    (p/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Ordered old continuation removal before option context validation; original 3012 edits preserved.')
