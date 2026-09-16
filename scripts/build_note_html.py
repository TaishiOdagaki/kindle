#!/usr/bin/env python3
"""
articles/note/*.md を、note.com にそのままコピペしたときに
見出し・リストが自動で認識されるHTMLに変換する。

使い方:
    python3 scripts/build_note_html.py

note.com のエディタはプレーンテキストのMarkdown記号（#, -, 1. など）は
解釈しないが、ブラウザ上でコピーした「リッチテキスト（HTML）」を貼り付けると
見出しやリストの構造を引き継ぐ。この特性を利用し、生成したHTMLファイルを
ブラウザで開いて本文を選択・コピーし、note のエディタに貼り付けることで
見出し変換の手作業を省略できる。

対応する記法:
    # タイトル        -> <h1>（note投稿画面のタイトル欄にはこちらを別途使う）
    ## 見出し         -> <h2>（note上で見出し/小見出しとして認識されやすい）
    - 項目            -> <ul><li>
    1. 項目           -> <ol><li>
    空行区切りの段落   -> <p>
"""
import html
import re
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "articles" / "note"
OUT_DIR = Path(__file__).resolve().parent.parent / "articles" / "note_html"

STYLE = """
body { font-family: sans-serif; line-height: 1.8; max-width: 640px; margin: 2em auto; padding: 0 1em; }
.title-box { border: 2px dashed #c00; padding: 0.8em 1em; margin-bottom: 1.5em; background: #fff5f5; }
.title-box .label { font-size: 0.8em; color: #c00; margin: 0 0 0.3em; }
.title-box h1 { font-size: 1.3em; margin: 0; }
.copy-note { font-size: 0.85em; color: #666; margin-bottom: 2em; }
h2 { font-size: 1.3em; margin-top: 1.6em; }
p { margin: 1em 0; }
"""


def convert(md_text: str) -> str:
    lines = md_text.splitlines()
    out = []
    i = 0
    paragraph = []

    def flush_paragraph():
        if paragraph:
            text = " ".join(paragraph).strip()
            if text:
                out.append(f"<p>{html.escape(text)}</p>")
            paragraph.clear()

    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith("# "):
            flush_paragraph()
            out.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
            i += 1
            continue

        if line.startswith("## "):
            flush_paragraph()
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            i += 1
            continue

        if line.startswith("- "):
            flush_paragraph()
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{html.escape(lines[i][2:].strip())}</li>")
                i += 1
            out.append("</ul>")
            continue

        if re.match(r"^\d+\. ", line):
            flush_paragraph()
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                item = re.sub(r"^\d+\. ", "", lines[i]).strip()
                out.append(f"<li>{html.escape(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        if line.strip() == "":
            flush_paragraph()
            i += 1
            continue

        paragraph.append(line.strip())
        i += 1

    flush_paragraph()
    return "\n".join(out)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for md_path in sorted(SRC_DIR.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        title_match = re.search(r"^# (.+)$", raw, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else md_path.stem

        # 本文からタイトル行(# ...)を取り除いてから変換する。
        # note投稿画面のタイトル欄はエディタ本文と別なので、
        # 本文としてコピーする範囲にh1が混ざらないようにする。
        body_only_md = re.sub(r"^# .+\n?", "", raw, count=1, flags=re.MULTILINE)
        body_html = convert(body_only_md)

        page = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>{STYLE}</style>
</head>
<body>
<div class="title-box">
<p class="label">↓ note投稿画面の「タイトル」欄にコピーする（本文にはコピーしない）</p>
<h1>{html.escape(title)}</h1>
</div>
<p class="copy-note">↓ ここから下を選択してコピーし、note本文欄に貼り付けると見出しが引き継がれます</p>
<div id="note-body">
{body_html}
</div>
</body>
</html>
"""
        out_path = OUT_DIR / (md_path.stem + ".html")
        out_path.write_text(page, encoding="utf-8")
        print(f"wrote {out_path.relative_to(OUT_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
