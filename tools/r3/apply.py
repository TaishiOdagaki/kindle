#!/usr/bin/env python3
"""第3ラウンド: tools/r3/batch*.py の辞書(B)を順に適用し、正解が最長でなくなったか検証する。
使い方: python3 tools/r3/apply.py 入力.docx 出力.docx"""
import sys, re, glob, importlib.util, zipfile, os
from xml.sax.saxutils import escape
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import quiz_audit as qa

def load():
    E = {}; R = set()
    for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'batch*.py'))):
        spec = importlib.util.spec_from_file_location('b', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, v in m.B.items(): E.setdefault(k, {}).update(v)
        for k in getattr(m, 'REVERT', []): R.add(k)
    for k in R: E.pop(k, None)
    return E

def run(src, dst):
    E = load(); z = zipfile.ZipFile(src); s = z.read('word/document.xml').decode('utf8'); n = 0
    for qid, opts in E.items():
        i = s.index(f'w:name="{qid}"'); j = s.index('w:anchor="A_', i); blk = s[i:j]
        for num, new in opts.items():
            m = re.search(r'(<w:t xml:space="preserve">' + str(num) + r'\. )([^<]*)(</w:t>)', blk); assert m, (qid, num)
            blk = blk[:m.start()] + m.group(1) + escape(new) + m.group(3) + blk[m.end():]; n += 1
        s = s[:i] + blk + s[j:]
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in z.infolist():
            d = z.read(it.filename)
            if it.filename == 'word/document.xml': d = s.encode('utf8')
            zo.writestr(it, d, compress_type=zipfile.ZIP_DEFLATED)
    issues, Q, A = qa.audit(dst); bad = []
    for qid in E:
        ai = int(A['A_' + qid[2:]]['ans']) - 1; L = [len(o) for o in Q[qid]['opts']]
        if L[ai] >= max(L[j] for j in range(4) if j != ai): bad.append((qid, L[ai], max(L[j] for j in range(4) if j != ai)))
    print('書き換え', n, '/ 正解がまだ最長:', bad)
    still = [k for k in Q if (lambda ai, L: L[ai] >= max(L[j] for j in range(4) if j != ai))(int(A['A_'+k[2:]]['ans'])-1, [len(o) for o in Q[k]['opts']])]
    print('全体で正解が最長(同長含む):', len(still), '/', len(Q))
if __name__ == '__main__': run(sys.argv[1], sys.argv[2])
