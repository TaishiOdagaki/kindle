#!/usr/bin/env python3
"""問題集docx(本書の書式)の自動検査。標準ライブラリのみ。

使い方: python3 tools/quiz_audit.py 本.docx [--json out.json]

検査項目(コード):
 S1 選択肢が1〜4の4つでない / S2 設問文に問いの文末がない / S3 選択肢に設問文が混入
 S4 正解行・正誤タグの形式不正 / S5 正解が早見表と不一致 / S6 リンク宛先なし・不一致
 D1 選択肢が1つずれて解説と対応(混入の典型) / D2 解説の並びが入れ替わっている疑い
 P1 (正)の解説が否定で終わり他に肯定がある(正誤タグ取り違えの疑い)
 A1 (正)の選択肢に断定語(一切・絶対…)があり、(誤)に無い選択肢が他にある
 T1 ゼロ幅文字・制御文字 / T2 「X（X）」の重複 / T3 同字・同句の連続 / T4 既知の誤植辞書
 T5 全角カッコ内の不自然な空白 / N1 目次の問数と実数の不一致 / N2 同一選択肢の重複
"""
import re, sys, zipfile, itertools, json, collections

QMARK = re.compile(r'選びなさい|選べ|選択しなさい|どれか|ですか[。？]?$|答えなさい|はどれ')
ABS = re.compile(r'一切|絶対|完全に|常に|すべて|全く|必ず|のみ|決して|無条件|唯一')
NEG_END = re.compile(r'(ではありません|ではない|適切でない|不適切|誤り|異なる|できない|存在しない|逆です|ありません|当たらない|関係しない|無関係|とは言えない|言い切れない|つながらない)[。）]?$')
VARIANTS = [('情意フィルター', '情緒的フィルター'), ('ディスプレイ・クエスチョン', 'ディスプレー・クエスチョン'),
            ('リファレンシャル', 'レファレンシャル'), ('JF日本語教育標準', 'JF日本語教育スタンダード'),
            ('明示的訂正', '明示的修正'), ('明確化要求', '明瞭化要求'), ('ポートフォリオ', 'ポートフォリヨ'),
            ('コミュニケーション・ストラテジー', 'コミュニケーションストラテジー'), ('ストラテジー', 'ストラテジィ'),
            ('モダリティ', 'ムード'), ('ダイグロシア', 'ディグロッシア'), ('アクション・リサーチ', 'アクションリサーチ'),
            ('ウェイト・タイム', 'ウエイト・タイム'), ('ティーチャートーク', 'ティーチャー・トーク'), ('ハネムーン期', '蜜月期')]
TYPO_DICT = ['複号','答答','正義文','事体','敬度','文筆','articulatig','非宣誓','類形辞','リアリア','言い刺す',
             'レコールド','減角','渡世的','完壁','誤習正','一矢的','固格化','就達先','毎変動','習達度','面授',
             '現体描写','対態的','文文脈','補合','固有銘柄','直前的','省録','親意','語声','基声','限界地質','アクティブ・コントロール']

def load(path):
    z = zipfile.ZipFile(path); s = z.read('word/document.xml').decode('utf8')
    paras = []
    for p in re.findall(r'<w:p>.*?</w:p>|<w:p [^>]*>.*?</w:p>', s, flags=re.S):
        paras.append(dict(
            t=''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', p, flags=re.S)),
            bm=re.findall(r'bookmarkStart w:name="([^"]+)"', p),
            link=re.findall(r'w:anchor="([^"]+)"', p),
            ind='<w:ind w:left="360"' in p))
    rows = []
    for r in re.findall(r'<w:tr>.*?</w:tr>', s, flags=re.S):
        cells = [''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', c, flags=re.S)) for c in re.findall(r'<w:tc>.*?</w:tc>', r, flags=re.S)]
        rows.append(cells)
    return paras, rows

def blocks(paras):
    qs, as_, cur = {}, {}, None
    for p in paras:
        for b in p['bm']:
            if b[:2] in ('Q_', 'A_'):
                cur = b; (qs if b[0] == 'Q' else as_)[b] = []
        if cur: (qs if cur[0] == 'Q' else as_)[cur].append(p)
        if cur and any(l[:2] in ('A_', 'Q_') for l in p['link']): cur = None
    return qs, as_

def gram(s):
    s = re.sub(r'[\s、。「」『』（）()・，,.：:？?！!／/]', '', s)
    return {s[i:i+2] for i in range(len(s)-1)}
def sim(a, b):
    A, B = gram(a), gram(b)
    return len(A & B) / (len(A)**.5 * len(B)**.5) if A and B else 0

def audit(path):
    paras, rows = load(path)
    issues = []
    def add(code, ident, msg): issues.append((code, ident, msg))
    qs, as_ = blocks(paras)
    bms = {b for p in paras for b in p['bm']}
    for p in paras:
        for l in p['link']:
            if l not in bms: add('S6', l, 'リンク宛先の見出しがない')
    Q, A = {}, {}
    for k, v in qs.items():
        body = v[1:-1]
        stems = [x['t'] for x in body if not x['ind']]; opts = [x['t'] for x in body if x['ind']]
        nums = [re.match(r'(\d)\. ', o).group(1) if re.match(r'(\d)\. ', o) else '?' for o in opts]
        if nums != list('1234'): add('S1', k, f'選択肢番号 {nums}')
        stem = ' '.join(stems)
        if not QMARK.search(stem): add('S2', k, '設問文に問いの文末がない: …' + stem[-30:])
        o = [re.sub(r'^\d\. ', '', x) for x in opts]
        Q[k] = dict(stem=stem, opts=o)
        for i, x in enumerate(o):
            if QMARK.search(x) and re.search(r'(最も|として|はどれ)', x): add('S3', k, f'選択肢{i+1}に設問文が混入: {x[:30]}')
        if len(set(o)) != len(o): add('N2', k, '同一の選択肢がある')
    for k, v in as_.items():
        lines = [x['t'] for x in v[1:-1]]
        m = re.match(r'正解：(\d)$', lines[0]) if lines else None
        tags = [re.match(r'(\d)（([正誤])）', l) for l in lines[1:]]
        if not m or len(tags) != 4 or any(t is None for t in tags) or [t.group(1) for t in tags] != list('1234'):
            add('S4', k, '正解行/解説行の形式不正'); continue
        sei = [t.group(1) for t in tags if t.group(2) == '正']
        if len(sei) != 1 or sei[0] != m.group(1): add('S4', k, f'正誤タグ {sei} と正解 {m.group(1)} が不一致')
        A[k] = dict(ans=m.group(1), txt=[re.sub(r'^\d（[正誤]）\s*', '', l) for l in lines[1:]])
    for k in Q:
        if 'A_' + k[2:] not in A: add('S6', k, '対応する解説がない')
    # 早見表
    tab = [r for r in rows if len(r) == 2 and re.fullmatch(r'[1-4]', r[1])]
    ex = {'Q_O_': 'O', 'Q_M_': 'M'}
    expl = [a['ans'] for k, a in A.items()]          # 文書順=早見表順
    if tab:
        if len(tab) != len(expl): add('S5', '早見表', f'行数{len(tab)}と解説数{len(expl)}が違う')
        else:
            for (r, a_) in zip(tab, A.items()):
                if r[1] != a_[1]['ans']: add('S5', a_[0], f'早見表({r[0]})={r[1]} 解説={a_[1]["ans"]}')
    # D1/D2/P1/A1
    perms = list(itertools.permutations(range(4)))
    for k, q in Q.items():
        a = A.get('A_' + k[2:])
        if not a or len(q['opts']) != 4: continue
        M = [[sim(q['opts'][i], a['txt'][j]) for j in range(4)] for i in range(4)]
        ident = sum(M[i][i] for i in range(4)); sh = sum(M[i+1][i] for i in range(3))
        if sh >= ident: add('D1', k, f'選択肢が1つずれて解説に対応(恒等{ident:.2f}/ずれ{sh:.2f})')
        best = max(perms, key=lambda p: sum(M[i][p[i]] for i in range(4)))
        if best != (0,1,2,3) and sum(M[i][best[i]] for i in range(4)) - ident > .25:
            add('D2', k, f'解説の並びが入れ替わっている疑い {tuple(x+1 for x in best)}')
        ans = int(a['ans']) - 1
        neg = [bool(NEG_END.search(t.split('。')[-2] if t.endswith('。') and '。' in t[:-1] else t)) for t in a['txt']]
        if neg[ans] and any(not neg[i] for i in range(4) if i != ans):
            add('P1', k, f'(正){ans+1}の解説が否定で終わる/肯定の(誤)がある: {[i+1 for i in range(4) if i!=ans and not neg[i]]}')
        ab = [bool(ABS.search(o)) for o in q['opts']]
        if ab[ans] and sum(ab) <= 1 or (ab[ans] and not all(ab[i] for i in range(4) if i != ans) and sum(ab) == 1):
            pass
        if ab[ans] and sum(1 for i in range(4) if i != ans and not ab[i]) >= 2:
            add('A1', k, f'正解選択肢{ans+1}に断定語、他に断定語なし2つ以上')
    # T*
    for p in paras:
        t = p['t']
        if re.search('[​‌‍﻿­\x00-\x08\x0b\x0c\x0e-\x1f]', t): add('T1', t[:20], '不可視文字')
        if re.search(r'([^\s（(「『]{3,12})（\1）', t): add('T2', t[:20], '「X（X）」の重複')
        m = re.search(r'(.{2,6})\1{1,}', t)
        if m and not re.fullmatch(r'[0-9A-Za-z\s]+', m.group(1)) and m.group(1) not in ('ーー', 'ははは', 'ババ') and not re.search(r'そうそう|いろいろ|ますます|だんだん|ざあざあ|それぞれ|人々|時々|様々|少しずつ|ごとごと', t):
            if re.search(r'(の|を|に|は|が|で|と|も){2,}', m.group(0)) or re.search(r'(.)\1\1', m.group(0)):
                add('T3', t[:20], f'同字連続の疑い: {m.group(0)}')
        for w in TYPO_DICT:
            if w == '面授':
                if re.search(r'(?<!対)面授(?!業)', t): add('T4', t[:20], f'既知の誤植: {w}')
            elif w in t: add('T4', t[:20], f'既知の誤植: {w}')
        t5 = t.replace('（ ）', '').replace('（　）', '')
        if re.search(r'（ [^）]*|[^（]* ）', t5): add('T5', t[:20], 'カッコ内の不自然な空白')
    # N1 目次の問数
    toc = {}
    for p in paras:
        m = re.match(r'^第(\d)章.*（(\d+)問）$', p['t'])
        if m: toc[m.group(1)] = int(m.group(2))
    for c, n in toc.items():
        act = len([k for k in Q if k.startswith(f'Q_{c}_')])
        if act != n: add('N1', f'第{c}章', f'目次の問数{n}と実数{act}が違う')
    # X1: 解説中の「選択肢N」参照(番号の並べ替え後に壊れやすい)
    for k, a in A.items():
        for j, t in enumerate(a['txt']):
            for m in re.finditer(r'選択肢([1-4１-４])', t): add('X1', k, f'解説{j+1}が「選択肢{m.group(1)}」を参照')
    for k, q in Q.items():
        for o in q['opts']:
            if re.search(r'上記|すべて正しい|いずれも正しい|選択肢[1-4]', o): add('X1', k, '選択肢が他の選択肢を参照: ' + o[:30])
    # V1: 表記ゆれ
    text = '\n'.join(p['t'] for p in paras)
    for grp in VARIANTS:
        cnt = {w: len(re.findall(w, text)) for w in grp}
        if sum(1 for v in cnt.values() if v) >= 2: add('V1', '表記ゆれ', str(cnt))
    return issues, Q, A

def stats(Q, A):
    out = {}
    ans = collections.Counter(a['ans'] for a in A.values()); n = sum(ans.values())
    out['正解位置の分布'] = {k: f'{v} ({v/n:.0%})' for k, v in sorted(ans.items())}
    by = collections.defaultdict(collections.Counter)
    for k, a in A.items(): by[re.match(r'A_([^_]+)_', k).group(1)][a['ans']] += 1
    out['章別'] = {c: dict(sorted(v.items())) for c, v in by.items()}
    longest = sum(1 for k, q in Q.items() if 'A_'+k[2:] in A and len(q['opts']) == 4 and
                  max(range(4), key=lambda i: len(q['opts'][i])) == int(A['A_'+k[2:]]['ans'])-1)
    out['正解が最長の選択肢'] = f'{longest}/{len(Q)} ({longest/len(Q):.0%}) 無作為なら25%'
    return out

if __name__ == '__main__':
    path = sys.argv[1]
    issues, Q, A = audit(path)
    c = collections.Counter(i[0] for i in issues)
    print(f'問題 {len(Q)} / 解説 {len(A)} / 指摘 {len(issues)}', dict(c))
    for code, ident, msg in issues: print(code, ident, msg)
    print('--- 統計'); [print(k, v) for k, v in stats(Q, A).items()]
    if '--json' in sys.argv:
        json.dump(issues, open(sys.argv[sys.argv.index('--json')+1], 'w'), ensure_ascii=False, indent=1)
