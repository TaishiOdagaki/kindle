#!/usr/bin/env python3
"""原稿/*.md から EPUB 3 を作る(標準ライブラリのみ)。
使い方: python3 tools/build_epub.py 出力.epub [--no-tables]
--no-tables: 表を「見出し: 値」の箇条書きに置き換える(画面の狭い端末で表が崩れる場合の予備版)。"""
import sys, re, os, zipfile, uuid, html, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '原稿')
TITLE = '登録日本語教員試験 完全ガイド'
SUBTITLE = '試験の全体像・本番の問題・資格の活かし方'
AUTHOR = '全国【登録日本語教員試験】研究グループ'
LANG = 'ja'
# (部の見出し, [ファイル...]) 部のないものは None
STRUCTURE = [
    (None, ['00_はじめに.md']),
    ('第1部　資格と試験を知る', ['01_登録日本語教員とは何か.md', '02_資格を取るまでの道筋.md', '03_試験の全体像.md', '04_出題範囲を読み解く.md']),
    ('第2部　本番の問題を知る', ['05_基礎試験の問題を解いてみる.md', '06_応用試験の問題を解いてみる.md']),
    ('第3部　合格する勉強法', ['07_学習計画のつくり方.md', '08_分野別の攻略法.md']),
    ('第4部　資格を取った後', ['09_資格の活かし方.md', '10_現場で働く人の声.md']),
    (None, ['あとがき.md']),
    ('付録', ['付録A_試験日程と手続きのチェックリスト.md', '付録B_頻出用語集.md', '付録C_出題範囲対応表.md', '付録D_参考資料と公式サイト.md', '付録E_問題集の案内.md']),
]
CSS = """
html { font-size: 100%; }
body { line-height: 1.8; margin: 0; padding: 0 0.2em; }
h1 { font-size: 1.5em; line-height: 1.4; margin: 1.5em 0 1em; page-break-before: always; }
h2 { font-size: 1.2em; line-height: 1.4; margin: 1.8em 0 0.6em; }
p { margin: 0 0 0.9em; text-align: justify; }
blockquote { margin: 1em 0.5em; padding: 0.2em 0.8em; border-left: 3px solid #999; font-size: 0.95em; }
blockquote p { margin: 0.4em 0; }
ul, ol { margin: 0.6em 0 1em; padding-left: 1.6em; }
li { margin: 0.2em 0; }
ul.check { list-style: none; padding-left: 0.2em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.85em; line-height: 1.5; }
th, td { border: 1px solid #999; padding: 0.3em 0.4em; vertical-align: top; overflow-wrap: break-word; }
.nw { white-space: nowrap; }
th { background: #eee; }
hr { border: 0; border-top: 1px solid #bbb; margin: 2em 0; }
.part { text-align: center; margin-top: 30%; }
.part h1 { page-break-before: auto; font-size: 1.6em; }
.title { text-align: center; margin-top: 25%; }
.title h1 { page-break-before: auto; font-size: 1.9em; }
.title .sub { font-size: 1.05em; margin-top: 1.5em; }
.title .by { margin-top: 3em; font-size: 1.05em; }
.colophon { margin-top: 30%; font-size: 0.9em; }
"""

def esc(s): return html.escape(s, quote=False)

def inline(s):
    s = re.sub(r'\\([*_`\\#\[\]])', lambda m: '\x00%d\x00' % ord(m.group(1)), s)
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(https?://[^\s<）)」]+)', r'<a href="\1">\1</a>', s)
    s = re.sub(r'\x00(\d+)\x00', lambda m: chr(int(m.group(1))), s)
    return s

def plain(s):
    s = re.sub(r'\\([*_`\\#\[\]])', r'\1', s)
    return re.sub(r'\*\*(.+?)\*\*', r'\1', s)

def split_row(line):
    cells = line.strip().strip('|').split('|')
    return [c.strip() for c in cells]

def render_table(rows, no_tables):
    head, body = rows[0], rows[2:]
    if no_tables:
        out = ['<ul>']
        for r in body:
            r = r + [''] * (len(head) - len(r))
            first = inline(r[0]) if r[0] else ''
            parts = []
            for h, v in zip(head[1:], r[1:]):
                if v: parts.append('%s: %s' % (esc(h), inline(v)) if h else inline(v))
            lead = '<strong>%s</strong>' % first if first else ''
            out.append('<li>%s%s</li>' % (lead, ('　' + ' ／ '.join(parts)) if parts else ''))
        out.append('</ul>')
        return '\n'.join(out)
    short0 = all(len(plain(r[0])) <= 7 for r in body if r) and len(plain(head[0])) <= 7
    def cell(tag, k, c):
        return '<%s%s>%s</%s>' % (tag, ' class="nw"' if (k == 0 and short0) else '', inline(c), tag)
    out = ['<table>', '<thead><tr>' + ''.join(cell('th', k, c) for k, c in enumerate(head)) + '</tr></thead>', '<tbody>']
    for r in body:
        r = r + [''] * (len(head) - len(r))
        out.append('<tr>' + ''.join(cell('td', k, c) for k, c in enumerate(r[:len(head)])) + '</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)

def md_to_xhtml(text, no_tables, headings):
    lines = text.split('\n'); out = []; i = 0
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        m = re.match(r'^(#{1,3})\s+(.*)$', l)
        if m:
            n = len(m.group(1)); t = m.group(2).strip()
            hid = 'h%d' % (len(headings) + 1)
            headings.append((n, plain(t), hid))
            out.append('<h%d id="%s">%s</h%d>' % (n, hid, inline(t), n)); i += 1; continue
        if re.match(r'^-{3,}\s*$', l): out.append('<hr/>'); i += 1; continue
        if l.lstrip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                rows.append(split_row(lines[i])); i += 1
            out.append(render_table(rows, no_tables)); continue
        if l.startswith('>'):
            ps = []
            while i < len(lines) and lines[i].startswith('>'):
                ps.append(lines[i].lstrip('>').strip()); i += 1
            out.append('<blockquote>' + ''.join('<p>%s</p>' % inline(p) for p in ps if p) + '</blockquote>'); continue
        if re.match(r'^- ', l):
            items = []
            while i < len(lines) and re.match(r'^- ', lines[i]):
                items.append(lines[i][2:]); i += 1
            check = all(re.match(r'^\[[ x]\] ', it) for it in items)
            if check:
                out.append('<ul class="check">' + ''.join('<li>☐ %s</li>' % inline(re.sub(r'^\[[ x]\] ', '', it)) for it in items) + '</ul>')
            else:
                out.append('<ul>' + ''.join('<li>%s</li>' % inline(it) for it in items) + '</ul>')
            continue
        if re.match(r'^\d+\.\s', l):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                items.append(re.sub(r'^\d+\.\s', '', lines[i])); i += 1
            out.append('<ol>' + ''.join('<li>%s</li>' % inline(it) for it in items) + '</ol>'); continue
        para = [l.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3}\s|- |\d+\.\s|>|\||-{3,}\s*$)', lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append('<p>%s</p>' % inline(''.join(para)))
    return '\n'.join(out)

def page(title, body, cls=None):
    b = '<div class="%s">\n%s\n</div>' % (cls, body) if cls else body
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="%s" xml:lang="%s">\n'
            '<head><meta charset="UTF-8"/><title>%s</title><link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            '<body>\n%s\n</body>\n</html>\n') % (LANG, LANG, esc(title), b)

def build(out_path, no_tables=False):
    pages = []   # (filename, id, title, xhtml, toc_level, headings)
    toc = []     # (level, title, href)
    def add(fn, title, xhtml, level, headings=None):
        pages.append((fn, 'p%d' % len(pages), title, xhtml))
        toc.append((level, title, fn))
        for n, t, hid in (headings or []):
            if n == 2: toc.append((level + 1, t, '%s#%s' % (fn, hid)))
    # 扉
    add('title.xhtml', '扉', page(TITLE, '<h1>%s</h1><p class="sub">%s</p><p class="by">%s</p>' % (esc(TITLE), esc(SUBTITLE), esc(AUTHOR)), 'title'), 1)
    toc[:] = []  # 扉は目次に載せない
    toc.append((1, '目次', 'nav.xhtml'))
    n = 0
    for part, files in STRUCTURE:
        plevel = 1
        if part:
            n += 1
            add('part%02d.xhtml' % n, part, page(part, '<h1>%s</h1>' % esc(part), 'part'), 1)
            plevel = 2
        for f in files:
            text = open(os.path.join(ROOT, f), encoding='utf8').read()
            heads = []
            body = md_to_xhtml(text, no_tables, heads)
            title = next((t for lv, t, _ in heads if lv == 1), f)
            n += 1
            add('c%02d.xhtml' % n, title, page(title, body), plevel, heads)
    year = datetime.date.today().year
    colo = ('<h1>奥付</h1><p>%s</p><p>著者　%s</p><p>本書の制度・日程・金額は、文部科学省の公表資料(令和8年度日本語教員試験実施要項、登録日本語教員の登録申請の手引き令和8年6月公開版ほか)にもとづく。制度は変わるため、出願や申請の前に最新の案内を確認すること。</p><p>本書のサンプル問題は、実際の試験問題ではない。</p>' % (esc(TITLE), esc(AUTHOR)))
    add('colophon.xhtml', '奥付', page('奥付', colo, 'colophon'), 1)

    uid = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'toroku-nihongo-kyoin-guide'))
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    manifest = ['<item id="css" href="style.css" media-type="text/css"/>', '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>', '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
    spine = []
    for fn, pid, _, _ in pages:
        manifest.append('<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (pid, fn))
        spine.append('<itemref idref="%s"/>' % pid)
    # nav.xhtml を扉の次に置く
    spine.insert(1, '<itemref idref="nav"/>')
    opf = ('<?xml version="1.0" encoding="UTF-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="ja">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n<dc:identifier id="bookid">%s</dc:identifier>\n<dc:title>%s</dc:title>\n<dc:creator>%s</dc:creator>\n<dc:language>ja</dc:language>\n'
           '<meta property="dcterms:modified">%s</meta>\n</metadata>\n<manifest>\n%s\n</manifest>\n<spine toc="ncx">\n%s\n</spine>\n</package>\n') % (uid, esc(TITLE), esc(AUTHOR), now, '\n'.join(manifest), '\n'.join(spine))
    # nav(入れ子)
    def nested(items):
        out = []; cur = 0
        for lv, t, href in items:
            if lv > cur:
                out.append('<ol>')
            else:
                out.append('</li>')
                for _ in range(cur - lv): out.append('</ol></li>')
            out.append('<li><a href="%s">%s</a>' % (href, esc(t)))
            cur = lv
        out.append('</li>')
        for _ in range(cur - 1): out.append('</ol></li>')
        out.append('</ol>')
        return '\n'.join(out)
    navbody = '<nav epub:type="toc" id="toc"><h1>目次</h1>\n%s\n</nav>' % nested([x for x in toc if x[2] != 'nav.xhtml'])
    nav = page('目次', navbody)
    ncx_pts = []
    for k, (lv, t, href) in enumerate([x for x in toc if x[2] != 'nav.xhtml'], 1):
        ncx_pts.append('<navPoint id="n%d" playOrder="%d"><navLabel><text>%s</text></navLabel><content src="%s"/></navPoint>' % (k, k, esc(t), href))
    ncx = ('<?xml version="1.0" encoding="UTF-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="%s"/></head>'
           '<docTitle><text>%s</text></docTitle><navMap>\n%s\n</navMap></ncx>\n') % (uid, esc(TITLE), '\n'.join(ncx_pts))
    container = '<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>\n'
    with zipfile.ZipFile(out_path, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/content.opf', opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/nav.xhtml', nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/toc.ncx', ncx, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/style.css', CSS, compress_type=zipfile.ZIP_DEFLATED)
        for fn, _, _, xh in pages:
            z.writestr('OEBPS/' + fn, xh, compress_type=zipfile.ZIP_DEFLATED)
    return len(pages)

if __name__ == '__main__':
    out = sys.argv[1]; nt = '--no-tables' in sys.argv
    print('pages', build(out, nt), '->', out)
