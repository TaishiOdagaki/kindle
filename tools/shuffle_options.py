#!/usr/bin/env python3
"""正解位置の偏りを直す: 各問の選択肢を並べ替え、解説・正解・早見表を合わせて更新する。
使い方: python3 tools/shuffle_options.py 入力.docx 出力.docx [--seed 7]
前提: 本書の書式(問題=選択肢段落4つ、解説=2ラン×4段落、早見表=2セル行)。
並べ替えない問: 解説が「選択肢N」を参照する/選択肢が数字の昇順など順序に意味がある。
"""
import re, sys, random, zipfile, collections

def main(src, dst, seed=7):
    z = zipfile.ZipFile(src); s = z.read('word/document.xml').decode('utf8')
    PAR = re.compile(r'<w:p>.*?</w:p>|<w:p [^>]*>.*?</w:p>', re.S)
    txt = lambda p: ''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', p, flags=re.S))
    # --- 段落ごとの位置を取る
    pars = [(m.start(), m.end(), m.group(0)) for m in PAR.finditer(s)]
    # ブロック検出
    def bm(p): return re.findall(r'bookmarkStart w:name="([^"]+)"', p)
    Qb, Ab, cur = {}, {}, None
    for idx, (a, b, p) in enumerate(pars):
        for n in bm(p):
            if n[:2] in ('Q_', 'A_'): cur = n; (Qb if n[0] == 'Q' else Ab)[n] = []
        if cur: (Qb if cur[0] == 'Q' else Ab)[cur].append(idx)
        if cur and re.search(r'w:anchor="[QA]_', p): cur = None
    Aorder = list(Ab)                      # 早見表の行順
    def opt_idx(k):
        return [i for i in Qb[k] if '<w:ind w:left="360"' in pars[i][2]]
    def exp_idx(k):
        return Ab[k][2:-1]                 # 見出し・正解行・戻るリンクを除く4段落
    eligible, skip = [], []
    for k in Qb:
        ak = 'A_' + k[2:]
        oi, ei = opt_idx(k), exp_idx(ak)
        otxt = [re.sub(r'^\d\. ', '', txt(pars[i][2])) for i in oi]
        etxt = [txt(pars[i][2]) for i in ei]
        ok = len(oi) == 4 and len(ei) == 4
        if ok and any(re.search(r'選択肢[1-4１-４]|上記|いずれも', t) for t in etxt + otxt): ok = False
        if ok:
            nums = [re.findall(r'\d+', t) for t in otxt]
            if all(nums) and [int(n[0]) for n in nums] == sorted(int(n[0]) for n in nums): ok = False
        (eligible if ok else skip).append(k)
    rng = random.Random(seed)
    n = len(eligible); targets = [i % 4 for i in range(n)]; rng.shuffle(targets)
    newkey = {}
    edits = {}                             # 段落index -> 新XML
    for k, tpos in zip(eligible, targets):
        ak = 'A_' + k[2:]; oi, ei = opt_idx(k), exp_idx(ak)
        tags = [txt(pars[i][2])[:4] for i in ei]
        old = [j for j, t in enumerate(tags) if '正' in t][0]
        others = [j for j in range(4) if j != old]; rng.shuffle(others)
        perm = [None] * 4; perm[tpos] = old                  # 新位置i <- 旧位置perm[i]
        it = iter(others)
        for i in range(4):
            if perm[i] is None: perm[i] = next(it)
        for i in range(4):
            o = pars[oi[perm[i]]][2]
            edits[oi[i]] = re.sub(r'(<w:t[^>]*>)\d\. ', lambda m: m.group(1) + f'{i+1}. ', o, count=1)
            e = pars[ei[perm[i]]][2]
            edits[ei[i]] = re.sub(r'(<w:t[^>]*>)\d（', lambda m: m.group(1) + f'{i+1}（', e, count=1)
        key_i = Ab[ak][1]
        edits[key_i] = re.sub(r'正解：\d', f'正解：{tpos+1}', pars[key_i][2], count=1)
        newkey[ak] = str(tpos + 1)
    # 段落を置換
    out, last = [], 0
    for idx, (a, b, p) in enumerate(pars):
        if idx in edits: out.append(s[last:a]); out.append(edits[idx]); last = b
    out.append(s[last:]); s2 = ''.join(out)
    # 早見表: 2セル行で2セル目が1〜4のものを文書順に対応づける
    rows = list(re.finditer(r'<w:tr>.*?</w:tr>', s2, flags=re.S))
    tab = [m for m in rows if len(re.findall(r'<w:tc>', m.group(0))) == 2 and re.fullmatch(r'[1-4]', ''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.findall(r'<w:tc>.*?</w:tc>', m.group(0), flags=re.S)[1])))]
    assert len(tab) == len(Aorder), (len(tab), len(Aorder))
    res, last = [], 0
    for m, ak in zip(tab, Aorder):
        row = m.group(0)
        if ak in newkey:
            j = row.rfind('</w:t>'); i = row.rfind('>', 0, j)
            row = row[:i+1] + newkey[ak] + row[j:]
        res.append(s2[last:m.start()]); res.append(row); last = m.end()
    res.append(s2[last:]); s3 = ''.join(res)
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in z.infolist():
            d = z.read(it.filename)
            if it.filename == 'word/document.xml': d = s3.encode('utf8')
            zo.writestr(it, d, compress_type=zipfile.ZIP_DEFLATED)
    print(f'並べ替え {len(eligible)}問 / 対象外 {len(skip)}問: {skip}')

if __name__ == '__main__':
    a = sys.argv; seed = int(a[a.index('--seed')+1]) if '--seed' in a else 7
    main(a[1], a[2], seed)
