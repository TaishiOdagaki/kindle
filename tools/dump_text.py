#!/usr/bin/env python3
"""通読用に、章ごとの問題・選択肢・解説と、前付け・巻末のテキストを書き出す。
使い方: python3 tools/dump_text.py 本.docx 出力ディレクトリ
出力: dump_<章>.txt (章は 1〜5 / O / M / MO)、front.txt (問題以外の見出しと本文)"""
import os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(__file__))
import quiz_audit as qa

def main(src, outdir):
    os.makedirs(outdir, exist_ok=True)
    _, Q, A = qa.audit(src); g = {}
    for k in Q: g.setdefault(k.split('_')[1], []).append(k)
    for ch, ks in g.items():
        with open(os.path.join(outdir, f'dump_{ch}.txt'), 'w') as f:
            for k in ks:
                q, a = Q[k], A['A_' + k[2:]]
                f.write(f"## {k} 正解={a['ans']}\n{q['stem']}\n")
                for n, o in enumerate(q['opts'], 1): f.write(f" {n}. {o}\n")
                f.write('解説: ' + str(a['txt']) + '\n')
    s = zipfile.ZipFile(src).read('word/document.xml').decode()
    paras = re.findall(r'<w:p[ >].*?</w:p>', s, flags=re.S)
    out = [''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p)) for p in paras]
    with open(os.path.join(outdir, 'front.txt'), 'w') as f:
        for i, t in enumerate(out):
            if t.strip(): f.write(f'{i} {t}\n')
    print({c: len(v) for c, v in g.items()}, '段落', len(out))

if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
