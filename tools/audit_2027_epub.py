#!/usr/bin/env python3
"""Extract by stable bookmarks and compare complete question fields, never by rank."""
import argparse, collections, csv, hashlib, json, posixpath, re, zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from lxml import etree as ET

NS={'h':'http://www.w3.org/1999/xhtml','o':'http://www.idpf.org/2007/opf'}
ID=re.compile(r'[QA]_(?:[1-5]|O|M|MO)_\d{3}')
def txt(e): return ''.join(e.itertext()).strip()
def norm(s): return re.sub(r'\s+','',s)
def read_epub(path):
    z=zipfile.ZipFile(path); assert z.testzip() is None
    opf=ET.fromstring(z.read('EPUB/content.opf'))
    manifest={e.get('id'):posixpath.normpath('EPUB/'+e.get('href')) for e in opf.findall('o:manifest/o:item',NS)}
    spine=[manifest[e.get('idref')] for e in opf.findall('o:spine/o:itemref',NS)]
    roots={n:ET.fromstring(z.read(n)) for n in z.namelist() if n.endswith('.xhtml')}
    ps=[]; loc={}; anchor_docs={}; duplicates=[]; links=0; broken=[]
    for n,r in roots.items():
        ids=r.xpath('//@id'); duplicates.extend((n,x) for x,c in collections.Counter(ids).items() if c>1)
        anchor_docs[n]=set(ids)
    for n,r in roots.items():
        for href in r.xpath('//@href'):
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            links+=1; target=posixpath.normpath(posixpath.join(posixpath.dirname(n),unquote(u.path))) if u.path else n
            if target not in z.namelist() or (u.fragment and unquote(u.fragment) not in anchor_docs.get(target,set())):broken.append([n,href])
    for n in spine:
        r=roots.get(n)
        if r is None:continue
        for p in r.findall('.//h:body//h:p',NS):
            for i in p.xpath('.//@id'):
                if ID.fullmatch(i):
                    assert i not in loc,i
                    loc[i]=len(ps)
            ps.append((n,p))
    records=[]; nodes={}
    qids=[i for i in loc if i.startswith('Q_')]
    for qid in qids:
        start=loc[qid]; stem=[]; opts=[]; onodes=[]; snodes=[]
        for n,p in ps[start+1:]:
            if any(ID.fullmatch(i) for i in p.xpath('.//@id')):break
            t=txt(p); m=re.match(r'^([1-4])[.．]\s*(.*)',t,re.S)
            if m and len(opts)<4:
                assert int(m[1])==len(opts)+1,qid
                opts.append(m[2]); onodes.append(p)
            elif not opts:
                stem.append(t);snodes.append(p)
            if len(opts)==4:break
        astart=loc['A_'+qid[2:]]; ap=[p for _,p in ps[astart+1:astart+6]]
        am=re.fullmatch(r'正解[：:]\s*([1-4])',txt(ap[0])); assert am,qid
        answer=int(am[1]);ex=[]
        for k,p in enumerate(ap[1:],1):
            m=re.fullmatch(r'([1-4])（(正|誤)）\s*(.*)',txt(p),re.S)
            assert m and int(m[1])==k and (m[2]=='正')==(k==answer),qid
            ex.append(m[3])
        assert len(opts)==len(ex)==4 and stem,qid
        records.append(dict(id=qid,stem='\n'.join(stem),options=opts,answer=answer,explanations=ex))
        nodes[qid]=dict(stem=snodes,options=onodes,explanations=ap[1:])
    assert len(records)==len(set(qids))==500
    assert len(loc)==1000
    qa=dict(questions=500,options=2000,explanations=2000,bookmarks=1000,spine_documents=len(spine),xhtml_documents=len(roots),internal_hrefs=links,broken_hrefs=broken,duplicate_ids=duplicates,replacement_characters=sum(z.read(n).decode('utf8').count('\ufffd') for n in roots),zip_crc_ok=True)
    return z,roots,records,nodes,qa

def main():
    ap=argparse.ArgumentParser();ap.add_argument('epub',type=Path);ap.add_argument('--academic',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    z,roots,qs,nodes,qa=read_epub(a.epub)
    master=json.loads(a.academic.read_text())['questions']; M={q['id']:q for q in master};assert {q['id'] for q in qs}==set(M)
    a.output.mkdir(parents=True,exist_ok=True)
    fields=['stem','options','answer','explanations']; rows=[];details=[]
    for seq,q in enumerate(qs,1):
        m=M[q['id']];flags={f:q[f]==m[f] for f in fields}
        normalized={f:([norm(s) for s in q[f]]==[norm(s) for s in m[f]] if isinstance(q[f],list) else norm(str(q[f]))==norm(str(m[f]))) for f in fields}
        row=dict(sequence=seq,id=q['id'],**{f+'_equal':flags[f] for f in fields},**{f+'_normalized_equal':normalized[f] for f in fields});rows.append(row)
        if not all(flags.values()): details.append(dict(id=q['id'],fields={f:dict(epub=q[f],academic=m[f]) for f in fields if not flags[f]}))
    qa.update(sha256=hashlib.sha256(a.epub.read_bytes()).hexdigest(),academic_sha256=hashlib.sha256(a.academic.read_bytes()).hexdigest(),exact_matches={f:sum(r[f+'_equal'] for r in rows) for f in fields},normalized_matches={f:sum(r[f+'_normalized_equal'] for r in rows) for f in fields},fully_identical=sum(all(r[f+'_equal'] for f in fields) for r in rows),full_field_comparison_completed=True,scholarly_correctness_certified=False,release_ready=False)
    for name,data in [('corpus_500.json',qs),('comparison_details.json',details),('qa.json',qa)]: (a.output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    with (a.output/'comparison_500.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    print(json.dumps(qa,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
