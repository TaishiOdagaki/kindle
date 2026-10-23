"""Read-only final manuscript, full-book, links and corpus validation."""
import json,hashlib,re,posixpath,zipfile
from pathlib import Path
from lxml import etree as E
from apply_2027_round38 import docx_records,equivalent
from audit_2027_epub import read_epub
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/round40';wp=O/'2027_review_manuscript.docx';ep=wp.with_suffix('.epub')
d,W,_=docx_records(wp);z,roots,Q,_,qa=read_epub(ep);WM={q['id']:q for q in W};assert len(W)==500 and all(equivalent(q,WM[q['id']]) for q in Q)
base=json.loads((R/'publishing/2027/round37_baseline/corpus_500.json').read_text());BM={q['id']:q for q in base};changes=[q['id'] for q in Q if not equivalent(q,BM[q['id']])];assert len(changes)==20
assert all(q['answer']==BM[q['id']]['answer'] for q in Q)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','h':'http://www.w3.org/1999/xhtml','o':'http://www.idpf.org/2007/opf'}
x=E.fromstring(zipfile.ZipFile(wp).read('word/document.xml'));anchors=x.xpath('//w:bookmarkStart/@w:name',namespaces=ns);links=x.xpath('//w:hyperlink/@w:anchor',namespaces=ns);assert len(links)==2059 and set(links)<=set(anchors)
opf=E.fromstring(z.read('EPUB/content.opf'));manifest={e.get('id'):posixpath.normpath('EPUB/'+e.get('href')) for e in opf.findall('o:manifest/o:item',ns)};spine=[manifest[e.get('idref')] for e in opf.findall('o:spine/o:itemref',ns)];body=''.join(''.join(roots[n].find('h:body',ns).itertext()) for n in spine);norm=lambda s:re.sub(r'\s+','',s);word=''.join(x.xpath('//w:body//w:t/text()',namespaces=ns));assert norm(word)==norm(body)
sections=[]
for n,r in roots.items():
 for e in r.xpath('//*[@id]',namespaces=ns):
  if e.get('id').startswith('nav-section-'):
   parent=e
   while parent.getparent() is not None and E.QName(parent.getparent()).localname!='body':parent=parent.getparent()
   b=r.find('h:body',ns);previous=''.join(b.itertext()).split(''.join(e.itertext()),1)[0]
   sections.append(dict(id=e.get('id'),document=n,text=''.join(e.itertext()),is_first_text=not previous.strip()))
assert len(sections)==40 and len({s['document'] for s in sections})==40 and all(s['is_first_text'] for s in sections)
assert not qa['broken_hrefs'] and not qa['duplicate_ids'] and not qa['replacement_characters']
report=dict(questions=500,word_epub_full_question_matches=500,changed_question_ids=changes,changed_questions=20,keys_changed=0,paragraphs=len(d.paragraphs),tables=len(d.tables),word_internal_links=len(links),word_broken_links=0,whole_book_equal_normalized=True,whole_book_normalized_characters=len(norm(word)),epub=qa,section_boundaries=sections,docx_sha256=hashlib.sha256(wp.read_bytes()).hexdigest(),epub_sha256=hashlib.sha256(ep.read_bytes()).hexdigest(),fresh_independent_primary_audit_all500=False,publication_approved=False)
(O/'final_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['section_boundaries']},ensure_ascii=False))
