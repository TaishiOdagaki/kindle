"""Before committing batch89, remove an unsupported lexical aside from its draft."""
import json
from pathlib import Path
p=Path('audit/v9');c=json.loads((p/'changes.json').read_text());assert len(c)==1990
batch=c[-18:];assert batch==json.loads((p/'changes_batch89.json').read_text())
e=next(x for x in batch if x['id']=='Q_2_013' and x['field']=='explanations' and x['index']==2)
assert 'デスク' in e['after']
e['after']='表5は母語の語を目標言語の発音に寄せる行動を達成・補償の欄に挙げています。この肢は、知識の不足を補って伝達しようとする行動を回避・縮小に分類しているため対応しません。'
for name,obj in [('changes.json',c),('changes_batch89.json',batch)]: (p/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Removed unverified desk lexical aside before batch89 commit; edit count unchanged')
