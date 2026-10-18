"""Constrain the queued deletion to the old standalone case paragraph."""
import json
from pathlib import Path
p=Path('audit/v9');cs=json.loads((p/'changes.json').read_text());extra=json.loads((p/'changes_batch167.json').read_text())
assert len(cs)==3363 and cs[-10:]==extra and extra[1]['remove_paragraph'] and not extra[1].get('previous_paragraph')
extra[1]['previous_paragraph']=extra[0]['after'];cs[-10:]=extra
for n,obj in [('changes.json',cs),('changes_batch167.json',extra)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
