"""Record additional header/answer-key page inspected before remote save."""
import json,hashlib
from pathlib import Path
from PIL import Image
p=Path('audit/v9');f=p/'evidence/batch89_review.json';e=json.loads(f.read_text());assert e['visually_reviewed_pages']==[28,62,226,260]
img=Path('/workspace/scratch/77d0d0a1a222/batch89b-qa/review-259.png');Image.open(img).verify()
e['visually_reviewed_pages']=[28,62,226,259,260];e['page_sha256']['259']=hashlib.sha256(img.read_bytes()).hexdigest();e['pagination_followup']='Q_4_021 heading and key3 end page259; all four explanations on260. No clipping, but final keep-with-next tuning needed.'
f.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;f.write_text(f.read_text()+'\n第89バッチ追加QA：259頁も直接目視。問21の見出し・正解3だけが259頁末、全4解説は260頁に分かれるため最終改頁調整候補。対象5頁を確認したが全399頁の最終目視は未了。\n')
print('Added page259 header/key visual check and pagination follow-up')
