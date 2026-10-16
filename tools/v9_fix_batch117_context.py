"""One-time context repair; does not rerun or replace scholarly judgments."""
import json
from pathlib import Path
p=Path('audit/v9')
for name in ['changes.json','changes_batch117.json']:
 cs=json.loads((p/name).read_text())
 candidates=[c for c in cs if c['id']=='Q_4_086' and c.get('remove_paragraph')]
 assert len(candidates)==1 and 'previous_paragraph' not in candidates[0]
 stem=next(c['after'] for c in reversed(cs) if c['id']=='Q_4_086' and c['field']=='stem' and not c.get('remove_paragraph'))
 candidates[0]['previous_paragraph']=stem
 (p/name).write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n')
print('Obsolete math paragraph identified by its preceding new stem; no judgments changed')
