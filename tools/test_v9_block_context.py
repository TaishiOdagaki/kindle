"""Regression: block filtering must not alter the previously saved manuscript."""
import sys,subprocess,tempfile,runpy,zipfile
from pathlib import Path
import v9_apply_batch1 as b
BASE='dcb9598a8f5557ce372f674d5b07bfb54db393cd'
root=Path(__file__).resolve().parents[1]
old_doc=subprocess.check_output(['git','show',BASE+':'+str(b.DST.relative_to(root))],cwd=root)
old_changes=subprocess.check_output(['git','show',BASE+':audit/v9/changes.json'],cwd=root)
with tempfile.TemporaryDirectory(prefix='v9-block-regression-') as t:
 p=Path(t);b.OUT=p;b.DST=p/'rebuilt.docx'
 (p/'changes.json').write_bytes(old_changes)
 runpy.run_path(str(root/'tools/v9_rebuild.py'),run_name='__main__')
 import io
 assert zipfile.ZipFile(io.BytesIO(old_doc)).read('word/document.xml')==zipfile.ZipFile(b.DST).read('word/document.xml')
print('block-context regression: prior document.xml byte-identical')
