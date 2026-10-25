from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json, re, hashlib, csv, io, collections, argparse

parser=argparse.ArgumentParser(description='Verify fixed cp320 DOCX/EPUB content and build current 500-question ledger.')
parser.add_argument('--docx',type=Path,default=Path('v9_integration_working_cp320.docx'))
parser.add_argument('--epub',type=Path,default=Path('epub_cp320_run325/v9_integration_cp320_final_candidate.epub'))
parser.add_argument('--classifications',type=Path,default=Path('release_cp330/classifications_cp308.json'))
parser.add_argument('--output',type=Path,default=Path('release_cp330'))
args=parser.parse_args()
OUT=args.output; OUT.mkdir(parents=True,exist_ok=True)
DOCX=args.docx; EPUB=args.epub
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
norm = lambda s: re.sub(r'\s+', '', s)
expected_docx = 'd544cb33f760023b8030bb3ca36c6401b7297ef394156cfb944f046fd0bff1d3'
expected_epub = '358b7a80c18a992c07358123719ffd3679b12f1dbfb65964ededbe381a97db10'
assert sha(DOCX) == expected_docx
assert sha(EPUB) == expected_epub
classifications = json.loads(args.classifications.read_text())['classifications']
with ZipFile(DOCX) as z:
    assert z.testzip() is None
    xml = etree.fromstring(z.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs = xml.xpath('//w:body//w:p', namespaces=ns)
blocks = {}; active = None
for p in paragraphs:
    text = ''.join(p.xpath('.//w:t/text()', namespaces=ns))
    anchors = p.xpath('.//w:bookmarkStart/@w:name', namespaces=ns)
    target = [a for a in anchors if re.fullmatch(r'[QA]_(?:[1-5]|M|O|MO)_\d{3}', a)]
    if target:
        assert len(target) == 1 and target[0] not in blocks
        active = target[0]; blocks[active] = []
    if active:
        blocks[active].append(text)
        if '目次に戻る' in text:
            active = None
with ZipFile(EPUB) as z:
    assert z.testzip() is None
    opf = etree.fromstring(z.read('EPUB/content.opf'))
    ons = {'o':'http://www.idpf.org/2007/opf'}
    items = {e.get('id'):e.get('href') for e in opf.xpath('//o:item', namespaces=ons)}
    files = ['EPUB/'+items[e.get('idref')] for e in opf.xpath('//o:itemref',namespaces=ons)]
    epub_blocks = {}; all_epub_text = []
    for filename in files:
        root = etree.fromstring(z.read(filename)); active = None
        body = root.xpath('//*[local-name()="body"]')[0]
        all_epub_text.append(''.join(body.itertext()))
        for element in body.xpath('.//*[local-name()="p" or local-name()="h1" or local-name()="h2" or local-name()="h3" or local-name()="h4"]'):
            text = ''.join(element.itertext())
            anchors = element.xpath('.//@id') + ([element.get('id')] if element.get('id') else [])
            target = [a for a in anchors if re.fullmatch(r'[QA]_(?:[1-5]|M|O|MO)_\d{3}', a)]
            if target:
                assert len(set(target)) == 1 and target[0] not in epub_blocks
                active = target[0]; epub_blocks[active] = []
            if active:
                epub_blocks[active].append(text)
                if '目次に戻る' in text:
                    active = None
question_ids = sorted(k for k in blocks if k.startswith('Q_'))
assert len(question_ids) == 500
assert len(blocks) == 1000 and set(blocks) == set(epub_blocks)
assert set(question_ids) == set(classifications)
mismatches = [k for k in blocks if norm(''.join(blocks[k])) != norm(''.join(epub_blocks[k]))]
assert not mismatches, mismatches
flat_epub = norm(''.join(all_epub_text))
missing = [i for i,p in enumerate(paragraphs) if norm(''.join(p.xpath('.//w:t/text()',namespaces=ns))) not in flat_epub]
assert not missing, missing
rows=[]; sections=collections.Counter(); adoption=collections.Counter()
for qid in question_ids:
    aid='A_'+qid[2:]; q=blocks[qid]; a=blocks[aid]
    options=[p for p in q if re.match(r'^[1-4][.．]',p)]
    explanations=[p for p in a if re.match(r'^[1-4][（(][正誤][）)]',p)]
    answers=[int(m.group(1)) for p in a if (m:=re.fullmatch(r'正解[：:]\s*([1-4])',p))]
    assert len(options)==4 and [int(p[0]) for p in options]==[1,2,3,4],qid
    assert len(explanations)==4 and [int(p[0]) for p in explanations]==[1,2,3,4],qid
    assert len(answers)==1,qid
    tagged=[int(p[0]) for p in explanations if re.match(r'^[1-4]（正）',p)]
    assert tagged==answers,(qid,tagged,answers)
    c=classifications[qid]; status=c['classification']
    assert status in ['accept-github','accept-library','manual-rewrite','equivalent']
    if 'independent_answer' in c: assert c['independent_answer']==answers[0],qid
    assert not c.get('unresolved'),qid
    if qid=='Q_4_111':
        assert '704頁' in explanations[0] and '700頁' not in explanations[0]
    refs=c.get('source_ids',c.get('sources',[]))
    refs=[str(x) for x in refs] if isinstance(refs,list) else [str(refs)]
    sections[qid.split('_')[1]]+=1;adoption[status]+=1
    rows.append([qid,answers[0],status,4,4,';'.join(refs),hashlib.sha256(norm(''.join(q+a)).encode()).hexdigest(),qid,aid])
buf=io.StringIO(); writer=csv.writer(buf)
writer.writerow(['question_id','answer','adoption','options','explanations','source_ids','normalized_question_answer_sha256','question_bookmark','answer_bookmark'])
writer.writerows(rows)
(OUT/'v9_cp320_500_question_audit_ledger.csv').write_text('\ufeff'+buf.getvalue(),encoding='utf-8')
answer_map={row[0]:row[1] for row in rows}
tables=xml.xpath('//w:tbl',namespaces=ns)
table_keys=['1','2','3','4','5','O','M','M','MO']
table_answer_rows=0
for i,section in enumerate(table_keys):
    for row in tables[i].xpath('./w:tr',namespaces=ns)[1:]:
        cells=[''.join(c.xpath('.//w:t/text()',namespaces=ns)) for c in row.xpath('./w:tc',namespaces=ns)]
        number=int(re.search(r'\d+',cells[0]).group())
        if section=='O':
            case=int(re.search(r'ケース(\d+)',cells[0]).group(1))
            number=(case-1)*5+number
        if section=='MO': number-=60
        qid=f'Q_{section}_{number:03d}'
        assert answer_map[qid]==int(cells[1]),(qid,cells[1])
        table_answer_rows+=1
assert table_answer_rows==500
assert len(tables)==10
assert all(t.xpath('./w:tr[1]/w:trPr/w:tblHeader',namespaces=ns) for t in tables)
summary={
 'schema':'release-verification-cp330-v1','docx_sha256':sha(DOCX),'epub_sha256':sha(EPUB),
 'questions':len(question_ids),'answers':len(blocks)-len(question_ids),
 'four_options_verified':500,'four_explanations_verified':500,'single_correct_tag_matching_answer':500,
 'docx_epub_question_and_answer_blocks_equal':len(blocks),'block_text_mismatches':mismatches,
 'docx_paragraphs_checked':len(paragraphs),'docx_paragraphs_missing_in_epub':missing,
 'normalization':'Whitespace only; no punctuation, wording, numeral or answer normalization.',
 'section_counts':dict(sections),'adoption_counts':dict(adoption),
 'manual_rewrite_Q_4_111_704_page_applied':True,
 'answer_quick_reference_rows_matching_current_answers':table_answer_rows,
 'word_tables_with_header_row':10,
 'scope_limit':'Structural checks and conversion preservation; does not independently re-prove scholarly truth or Kindle rendering.',
 'kindle_previewer':'not_run','publication_decision':'hold'}
(OUT/'verification_cp330.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
