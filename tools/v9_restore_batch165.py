"""Recover uploaded ordered edits and decision records without replaying old reviews."""
import json,hashlib
from pathlib import Path
p=Path('audit/v9');root=Path(__file__).resolve().parents[2]
old=json.loads((p/'changes.json').read_text());assert len(old)==3290
extra=json.loads((p/'evidence/batch165_recovered_edits.json').read_text());assert len(extra)==27
dec=json.loads((p/'decisions.json').read_text());recovered=json.loads((p/'evidence/batch165_recovered_decisions.json').read_text())
assert set(recovered)=={'Q_1_034','Q_1_035','Q_1_008'}
for k,v in recovered.items():
 assert dec[k]['status']=='要追加確認' and v['status']=='確認済み'
 dec[k].update(v)
for n,obj in [('changes.json',old+extra),('changes_batch165.json',extra),('decisions.json',dec)]:
 (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
assert hashlib.sha1(b'blob '+str((p/'changes.json').stat().st_size).encode()+b'\0'+(p/'changes.json').read_bytes()).hexdigest()=='cce17b0044ebbf3ae972af6cb6e5276f63367ef4'
print('Recovered exact 3317-edit blob and three decision records; no old review replay.')
