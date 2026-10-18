"""Find changed strings and render every matching page."""
import json,re,subprocess
from pathlib import Path
from pypdf import PdfReader
from PIL import Image
p=Path('audit/v9');r=Path(__file__).resolve().parents[2]/'qa155'
norm=lambda s:re.sub(r'\s+','',s)
reader=PdfReader(r/'qa.pdf',strict=True);texts=[norm(pg.extract_text()) for pg in reader.pages]
cs=json.loads((p/'changes_batch155.json').read_text())
matches={str(i):[n+1 for n,t in enumerate(texts) if norm(c['after']) in t] for i,c in enumerate(cs)}
for i,c in enumerate(cs):
 if not matches[str(i)]:
  pairs=[(n+1,n+2) for n in range(len(texts)-1) if norm(c['after']) in texts[n]+texts[n+1]]
  matches[str(i)]=sorted({n for pair in pairs for n in pair})
assert len(matches)==9 and all(matches.values()),matches
(r/'matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2)+'\n')
pages=sorted({n for ns in matches.values() for n in ns})
for n in pages:
 out=r/f'review-{n:03}.png'
 subprocess.run(['pdftocairo','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1800','-png',str(r/'qa.pdf'),str(out.with_suffix(''))],check=True)
 with Image.open(out) as im:im.load()
print(len(reader.pages),pages)
