#!/usr/bin/env python3
"""Apply a Nobel branch to ../manuscript.md.
Usage (from murakami-jp/nobel-branches): python3 apply_nobel.py win|no
Replaces: (1) the Chapter 18 result placeholder, (2) the finale placeholder, (3) the last timeline line,
and appends the two footnotes. Refuses to run while any [[FILL: ...]] marker is left in the branch file,
or when a placeholder in the manuscript is missing (already applied)."""
import re, sys
b = sys.argv[1] if len(sys.argv) > 1 else ""
if b not in ("win", "no"):
    sys.exit("usage: apply_nobel.py win|no")
src = "win.md" if b == "win" else "no-win.md"
txt = open(src, encoding="utf-8").read()
left = re.findall(r"\[\[FILL:[^\]]*\]\]", txt)
if left:
    sys.exit("Fill these first (%d left):\n- " % len(left) + "\n- ".join(left))
parts = {}
for key in ("CH18", "FINALE", "TIMELINE", "NOTES"):
    m = re.search(r"<!-- %s -->\n(.*?)(?=<!-- [A-Z0-9]+ -->|\Z)" % key, txt, re.S)
    if not m:
        sys.exit("section missing: " + key)
    parts[key] = m.group(1).strip("\n")
p = "../manuscript.md"
s = open(p, encoding="utf-8").read()
def sub(pattern, repl):
    global s
    m = re.search(pattern, s)
    if not m:
        sys.exit("placeholder not found: " + pattern)
    s = s[:m.start()] + repl + s[m.end():]
sub(r"【この章の後半\(結果を受けた部分\)[^】]*】\n\n", "")
sub(r"【ノーベル賞の結果を受けた節:[^】]*】", parts["CH18"])
sub(r"【終章の最後の数段落は[^】]*】\n\n", "")
sub(r"【終章の結び:[^】]*】", parts["FINALE"])
sub(r"- \*\*二〇二六年\*\*[^\n]*\n", parts["TIMELINE"] + "\n")
s = s.rstrip("\n") + "\n\n" + parts["NOTES"] + "\n"
open(p, "w", encoding="utf-8").write(s)
used = set(re.findall(r"\[\^([^\]]+)\](?!:)", s)); defd = set(re.findall(r"^\[\^([^\]]+)\]:", s, flags=re.M))
print("applied", src, "| footnotes consistent:", used == defd, "| unresolved placeholders:", len(re.findall(r"【[^】]*(発表後|結果を受け)[^】]*】", s)))
