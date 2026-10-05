#!/usr/bin/env python3
"""Typographic cover prototypes (own design: no images, logos, or typefaces from the work).
Output: build/img/cover.v<vol>.<lang>.png (1600x2560). Usage: python3 build/cover.py [--lang=ja|en|both]"""
import sys, pathlib, random
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib_fontja
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import design
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "img"

def motif(ax, vol, th):
    rnd = random.Random(7)
    tint = th["tint"]
    if vol == "1":      # ripples: a starting point radiating outward (1995 as origin)
        for i, r in enumerate([1.2, 2.2, 3.4, 4.8, 6.4, 8.2]):
            ax.add_patch(Circle((7.2, 3.2), r, fill=False, ec=tint, lw=2.0, alpha=0.5 - i * 0.05))
    elif vol == "2":    # two overlapping rings: two endings / a restart
        ax.add_patch(Circle((4.6, 3.6), 3.6, fill=False, ec=tint, lw=3.0, alpha=0.55))
        ax.add_patch(Circle((7.0, 3.6), 3.6, fill=False, ec=tint, lw=3.0, alpha=0.55))
        ax.add_patch(Circle((5.8, 3.6), 1.0, fc=tint, ec="none", alpha=0.25))
    else:               # constellation: interpretations linked
        pts = [(rnd.uniform(1, 9), rnd.uniform(0.8, 6.2)) for _ in range(14)]
        for i, p in enumerate(pts):
            for q in pts[i + 1:i + 3]:
                ax.plot([p[0], q[0]], [p[1], q[1]], color=tint, lw=1.6, alpha=0.45)
        for p in pts: ax.add_patch(Circle(p, 0.16, fc=tint, ec="none", alpha=0.7))

def render(lang):
    matplotlib_fontja.japanize()
    for vol in "123":
        th = design.theme(vol); ja = lang == "ja"
        fig = plt.figure(figsize=(8, 12.8), dpi=200, facecolor=th["accent"])
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 16); ax.axis("off"); ax.set_facecolor(th["accent"])
        sub = ax.inset_axes([0, 0, 1, 0.55], transform=ax.transData) if False else None
        mot = fig.add_axes([0, 0, 1, 0.45]); mot.set_xlim(0, 10); mot.set_ylim(0, 7.2); mot.axis("off"); mot.patch.set_alpha(0)
        motif(mot, vol, th)
        on = th["on_accent"]
        ax.text(0.8, 15.0, "Japanese Culture Press", color=on, fontsize=15, alpha=0.85)
        ax.text(0.8, 12.6, "エヴァンゲリオン\n決定版" if ja else "EVANGELION\nThe Complete\nCritical Guide", color=on, fontsize=44 if ja else 40, va="top", linespacing=1.25)
        ax.text(0.8, 8.9, f"第{vol}巻" if ja else f"VOL. {vol}", color=on, fontsize=34, va="top")
        ax.text(0.8, 7.8, th["title_ja"] if ja else th["title_en"], color=on, fontsize=19, va="top", alpha=0.95)
        ax.text(9.2, 0.5, "(仮表紙)" if ja else "WORKING COVER", color=on, fontsize=11, ha="right", alpha=0.7)
        fig.savefig(OUT / f"cover.v{vol}.{lang}.png", dpi=200, facecolor=th["accent"]); plt.close(fig)

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for l in (["ja", "en"] if "--lang=both" in sys.argv else ["en" if "--lang=en" in sys.argv else "ja"]): render(l)
    print("covers ok")
