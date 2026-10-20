"""Update only batch202 evidence after fixing inherited bold formatting."""
import json,hashlib,subprocess,tempfile
from pathlib import Path
from docx import Document
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa202b');doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
c=json.loads((p/'changes_batch202.json').read_text())[0];assert c['glossary_head']=='モダリティ'
d=Document(doc);ps=[x for x in d.paragraphs if x.text==c['after']];assert len(ps)==1
rs=[x for x in ps[0].runs if x.text];assert len(rs)==2 and rs[0].text=='モダリティ' and rs[0].bold is True and rs[1].bold is False
assert rs[0].text+rs[1].text==c['after']
with tempfile.TemporaryDirectory(prefix='v9-202-final-') as t:
 f=Path(t)/'before.docx';f.write_bytes(subprocess.check_output(['git','show','bc373c1326a7efdac27e49df3999ae64972800fb:'+str(doc)]));_,q0,a0=qa.audit(str(f))
_,q,a=qa.audit(str(doc));assert q==q0 and a==a0 and len(q)==len(a)==500
matches=json.loads((r/'matches202.json').read_text());assert len(matches)==1 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
f=p/'evidence/batch202_review.json';e=json.loads(f.read_text());e.update(docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),render_pages=len(PdfReader(r/'qa.pdf').pages),visually_reviewed_pages=pages,page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},render_revision='qa202b 最終の変更箇所描画',glossary_style_checked={'head_bold':True,'explanation_bold':False},style_fix='初回qa202で説明まで太字になったためglossary_head属性を変更記録へ追加。v9_rebuildはこの属性のある改訂だけ見出しと本文のランを分ける。再描画後に画像確認。',regression='readiness8・replacement4・block-contextの過去document.xml一致を検査済み。全500問本文の前稿同一を追加比較。')
f.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
note='\n第202バッチ描画追補：初回描画で追加説明全体への太字継承を発見し、glossary_head属性による局所書式指定を再構成処理へ追加。見出し語だけを太字、説明を通常字としてqa202bを再描画し、最新の影響頁を直接画像確認。evidence/batch202_review.jsonの原稿・PDF・ページハッシュは再描画後のもの。初回画像を最終確認に流用していない。全問の本文・正答・判定は変更なし。\n'
for n in ['interim_report.md','visual_qa.md']:
 f=p/n;assert '第202バッチ描画追補' not in f.read_text();f.write_text(f.read_text()+note)
print(e['docx_sha256'],e['render_pages'],pages)
