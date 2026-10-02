#!/usr/bin/env python3
"""Replace Chapter 4 of vol3-manuscript.md with a chosen Nobel branch file.
Usage (from the murakami-epub-rebuilt folder): python3 vol3-nobel-branches/apply_ch4.py no|yes
Refuses to run while any [[FILL: ...]] marker is left in the branch file."""
import re, sys
branch = sys.argv[1] if len(sys.argv) > 1 else ""
if branch not in ("no", "yes"):
    sys.exit("usage: apply_ch4.py no|yes")
src = "vol3-nobel-branches/ch4-%s.md" % ("win" if branch == "yes" else "no-win")
new = open(src, encoding="utf-8").read()
left = re.findall(r"\[\[FILL:[^\]]*\]\]", new)
if left:
    sys.exit("Fill these first (%d left): %s" % (len(left), "; ".join(left)))
p = "vol3-manuscript.md"
s = open(p, encoding="utf-8").read()
a = s.index("## CHAPTER 4")
b = s.index("## CHAPTER 5")
s = s[:a] + new.rstrip("\n") + "\n\n" + s[b:]
open(p, "w", encoding="utf-8").write(s)
used = set(re.findall(r"\[\^([^\]]+)\](?!:)", s)); defd = set(re.findall(r"^\[\^([^\]]+)\]:", s, flags=re.M))
print("Chapter 4 replaced with", src, "| footnotes consistent:", used == defd)
