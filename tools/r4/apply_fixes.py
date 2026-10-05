#!/usr/bin/env python3
"""事実確認で見つかった誤りの本文修正。fixes*.py の FIX=[(メモ, 旧, 新), ...] を順に適用する。
旧は document.xml 上で必ずちょうど1回(4つ目の要素で回数を指定可)現れること(重複や不一致は停止)。
使い方: python3 tools/r4/apply_fixes.py 入力.docx 出力.docx"""
import sys, os, glob, zipfile, importlib.util
from xml.sax.saxutils import escape
def load():
    F = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'fixes*.py'))):
        sp = importlib.util.spec_from_file_location('f', f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); F += m.FIX
    return F
def run(src, dst):
    z = zipfile.ZipFile(src); s = z.read('word/document.xml').decode('utf8'); bad = 0
    for fx in load():
        memo, old, new = fx[:3]; want = fx[3] if len(fx) > 3 else 1
        o, n = escape(old), escape(new); c = s.count(o)
        if c != want: print('NG', memo, f'出現{c}回(想定{want})', old[:30]); bad += 1; continue
        s = s.replace(o, n)
    if bad: sys.exit(f'{bad}件が適用できませんでした')
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in z.infolist():
            d = z.read(it.filename)
            if it.filename == 'word/document.xml': d = s.encode('utf8')
            zo.writestr(it, d, compress_type=zipfile.ZIP_DEFLATED)
    print('適用', len(load()), '件')
if __name__ == '__main__': run(sys.argv[1], sys.argv[2])
