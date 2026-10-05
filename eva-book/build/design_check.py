#!/usr/bin/env python3
"""Check the design tokens: WCAG contrast and grayscale luminance (so the volumes stay readable on e-ink)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import design

def lum(h):
    def f(c):
        c /= 255; return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

ok = True
print(f'{"vol":4} {"name":6} {"on/accent":>10} {"ink/tint":>9} {"accent L":>9} {"tint L":>7}  gray(accent)')
for v in "123":
    t = design.theme(v)
    r1, r2 = ratio(t["on_accent"], t["accent"]), ratio(t["ink"], t["tint"])
    g = round(lum(t["accent"]) ** (1 / 2.2) * 255)
    print(f'{v:4} {t["name_ja"]:6} {r1:10.2f} {r2:9.2f} {lum(t["accent"]):9.3f} {lum(t["tint"]):7.3f}  #{g:02x}{g:02x}{g:02x}')
    if r1 < 4.5 or r2 < 4.5: ok = False
Ls = sorted(lum(design.theme(v)["accent"]) for v in "123")
steps_ok = all(b - a >= 0.03 for a, b in zip(Ls, Ls[1:]))
print("grayscale luminance steps >= 0.03:", "OK" if steps_ok else "FAIL (volumes collapse to one gray on e-ink)")
ok = ok and steps_ok
print("OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
