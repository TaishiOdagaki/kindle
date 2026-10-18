"""Find each replacement in a fresh PDF and emit affected pages for manual QA."""
import json,re,sys,subprocess
from pathlib import Path
from pypdf import PdfReader
batch=int(sys.argv[1]);r=Path(sys.argv[2]);cs=json.loads(Path(f'audit/v9/changes_batch{batch}.json').read_text())
norm=lambda s:re.sub(r'\s+','',s).replace('～','〜')
reader=PdfReader(r/'qa.pdf',strict=True);texts=[norm(p.extract_text()) for p in reader.pages];matches={}
for i,c in enumerate(cs):
 if c.get('remove_paragraph'):
  matches[str(i)]=[]
  continue
 ns=[n+1 for n,t in enumerate(texts) if norm(c['after']) in t]
 if not ns:ns=sorted({v for n in range(len(texts)-1) if norm(c['after']) in texts[n]+texts[n+1] for v in [n+1,n+2]})
 matches[str(i)]=ns
assert all(matches[str(i)] for i,c in enumerate(cs) if not c.get('remove_paragraph')),matches
(r/f'matches{batch}.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2)+'\n')
pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 subprocess.run(['pdftocairo','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1800','-png',str(r/'qa.pdf'),str(r/f'review-{n:03}')],check=True)
print(len(reader.pages),pages)
