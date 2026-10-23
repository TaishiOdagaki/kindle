"""Remove duplicated generated title matter, preserve all manuscript body text."""
import hashlib,json,posixpath,re,zipfile
from pathlib import Path
from lxml import etree as E
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/round40';p=O/'2027_review_manuscript.epub'
z=zipfile.ZipFile(p);data={n:z.read(n) for n in z.namelist()};ns={'o':'http://www.idpf.org/2007/opf','h':'http://www.w3.org/1999/xhtml'};opf=E.fromstring(data['EPUB/content.opf'])
for e in opf.xpath('//*[@id="title_page_xhtml"]|//*[@idref="title_page_xhtml"]'):e.getparent().remove(e)
del data['EPUB/text/title_page.xhtml']
n='EPUB/text/part001_s01.xhtml';r=E.fromstring(data[n]);hs=r.findall('.//h:body//h:h1',ns);assert len(hs)==1;hs[0].getparent().remove(hs[0]);body=r.find('h:body',ns);body.set('{http://www.idpf.org/2007/ops}type','frontmatter');section=body[0];section.set('{http://www.idpf.org/2007/ops}type','titlepage');first=section.find('h:p',ns);first.set('class','book-title');data[n]=E.tostring(r,encoding='utf-8',xml_declaration=True)
n='EPUB/nav.xhtml';r=E.fromstring(data[n]);hits=r.xpath('//*[@href="text/title_page.xhtml"]');assert len(hits)==1;hits[0].set('href','text/part001_s01.xhtml#登録日本語教員試験-パーフェクト問題集');hits[0].text='扉';data[n]=E.tostring(r,encoding='utf-8',xml_declaration=True)
data['EPUB/content.opf']=E.tostring(opf,encoding='utf-8',xml_declaration=True)
css='EPUB/styles/stylesheet1.css';data[css]+=b'\n.book-title {font-size:2em;line-height:1.25;margin-bottom:1em;}\n'
# Full linear body equality, including cases, tables, glossary and navigation text in the manuscript.
w=E.fromstring(zipfile.ZipFile(O/'2027_review_manuscript.docx').read('word/document.xml'));a=''.join(w.xpath('//w:body//w:t/text()',namespaces={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}));norm=lambda s:re.sub(r'\s+','',s)
manifest={e.get('id'):posixpath.normpath('EPUB/'+e.get('href')) for e in opf.findall('o:manifest/o:item',ns)};b=''
for e in opf.findall('o:spine/o:itemref',ns):
 r=E.fromstring(data[manifest[e.get('idref')]]);b+=''.join(r.find('h:body',ns).itertext())
assert norm(a)==norm(b),(len(norm(a)),len(norm(b)))
tmp=p.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w') as out:
 for info in z.infolist():
  if info.filename in data:out.writestr(info,data[info.filename])
tmp.replace(p)
report=dict(removed_generated_title_documents=1,removed_duplicate_generated_heading=1,manuscript_title_retained=True,word_epub_full_body_equal_after_whitespace_normalization=True,normalized_characters=len(norm(a)),scope='Entire linear book including all case premises, tables and appendices; OPF/nav/head metadata excluded',epub_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(O/'whole_book_equivalence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
