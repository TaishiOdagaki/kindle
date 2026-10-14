"""Render an isolated Japanese-font QA copy; never alter the working DOCX.

Use the documents skill marker before authoring, then run with the primary
runtime Python. Supply an already acquired Noto Sans JP variable font and a
writable copy of the bundled LibreOffice. Inspect the resulting PNGs manually.
"""
import argparse,importlib.util,sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from docx import Document
from docx.oxml.ns import qn

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True)
 ap.add_argument('--output',type=Path,required=True);ap.add_argument('--font',type=Path,required=True)
 ap.add_argument('--soffice',type=Path,required=True)
 ap.add_argument('--renderer',type=Path,default=Path('/root/.codex/skills/builtins/documents/render_docx.py'))
 args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 assert args.input.is_file() and args.font.is_file() and args.soffice.is_file()
 # Never allow stale page images to be mistaken for this render.
 assert not list(args.output.glob('page-*.png')),'Use a fresh QA output directory'
 font=instantiateVariableFont(TTFont(args.font),{'wght':400},inplace=True)
 for n in font['name'].names:
  if n.nameID in (1,4,6,16):
   n.string=('NotoSansJPStatic' if n.nameID==6 else 'Noto Sans JP Static').encode(n.getEncoding())
 fontdir=args.soffice.resolve().parent.parent/'share/fonts/truetype'
 fontdir.mkdir(parents=True,exist_ok=True);font.save(fontdir/'NotoSansJPStatic.ttf')
 doc=Document(args.input)
 for s in doc.styles:
  if s.type in (1,2):
   s.font.name='Noto Sans JP Static'
   s._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Noto Sans JP Static')
 for p in doc.paragraphs:
  for r in p.runs:
   r.font.name='Noto Sans JP Static'
   r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Noto Sans JP Static')
 qa=args.output/'qa.docx';assert qa.resolve()!=args.input.resolve();doc.save(qa)
 spec=importlib.util.spec_from_file_location('documents_renderer',args.renderer)
 renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
 renderer._resolve_soffice=lambda:str(args.soffice.resolve())
 sys.argv=['render_docx.py',str(qa),'--output_dir',str(args.output),'--dpi','100','--emit_pdf']
 renderer.main()

if __name__=='__main__':main()
