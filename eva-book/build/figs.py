#!/usr/bin/env python3
"""Generate book figures (own-made diagrams only) from atlas data.

Rules (see FIGURES.md): grayscale-safe, large text, no images/logos/typefaces from the work.
Each figure is registered in figures.csv; `verified != yes` -> DRAFT watermark and release is blocked.
Usage: python3 build/figs.py [--lang=ja|en|both]
"""
import csv, sys, pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib_fontja
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "img"
INK, MID, LIGHT, PALE = "#111111", "#6b6b6b", "#c8c8c8", "#efefef"
W = 8.0  # inches; dpi 200 -> 1600 px wide

def setup():
    matplotlib_fontja.japanize()
    plt.rcParams.update({"font.size": 13, "axes.unicode_minus": False, "figure.dpi": 200,
                         "axes.edgecolor": INK, "text.color": INK, "axes.labelcolor": INK})

def box(ax, x, y, w, h, text, fc=PALE, ec=INK, lw=1.4, fs=13, bold=False, ls="-", ha="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.35)

def arrow(ax, p, q, text=None, ls="-", lw=1.6, fs=11.5, off=(0, 0.08), style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16, lw=lw, ls=ls, color=INK, shrinkA=0, shrinkB=0))
    if text:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], text, ha="center", va="bottom", fontsize=fs, color=MID)

def canvas(ymax):
    """Canvas whose x range is 0..10 and y range is 0..ymax, with equal unit scale."""
    fig = plt.figure(figsize=(W, W * ymax / 10)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, ymax); return fig, ax

# ---------------------------------------------------------------- figures
def f_angels_episodes(lang, E):
    angels = sorted([e for e in E.values() if e["type"] == "angel" and e.get("episodes")], key=lambda e: e["number"])
    fig, ax = plt.subplots(figsize=(W, 0.42 * len(angels) + 1.3))
    for i, a in enumerate(angels):
        y = len(angels) - 1 - i
        for ep in a["episodes"]:
            ax.barh(y, 0.84, left=ep - 0.42, height=0.62, color=INK, edgecolor=INK)
    ax.set_yticks(range(len(angels)))
    ax.set_yticklabels([("第%d使徒 %s" % (a["number"], a["name_jp"])) if lang == "ja" else ("#%d %s" % (a["number"], a["name_en"])) for a in reversed(angels)], fontsize=12)
    ax.set_xticks(range(1, 27, 1)); ax.set_xticklabels([str(i) if i % 5 == 0 or i == 1 else "" for i in range(1, 27)])
    ax.set_xlim(0.4, 26.6); ax.set_ylim(-0.7, len(angels) - 0.3)
    ax.set_xlabel("話数" if lang == "ja" else "Episode"); ax.grid(axis="x", color=LIGHT, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); return fig

def f_eva_system(lang, E):
    t = (lambda ja, en: ja if lang == "ja" else en)
    fig, ax = canvas(5.0)
    box(ax, 0.1, 2.7, 2.2, 1.5, t("パイロット\n(チルドレン)", "Pilot\n(Child)"))
    box(ax, 3.2, 2.45, 3.6, 2.0, t("エントリープラグ\n内部はLCLで満たされる", "Entry plug\nfilled with LCL"), fc="white", fs=12.5)
    box(ax, 7.7, 2.7, 2.2, 1.5, t("エヴァ", "Evangelion"), fc=LIGHT)
    arrow(ax, (2.3, 3.45), (3.2, 3.45)); arrow(ax, (6.8, 3.45), (7.7, 3.45), t("神経接続", "neural link"), off=(0, 0.12))
    ax.text(5.0, 4.7, t("シンクロ率: 同調の度合いを示す指標", "Sync ratio: how well pilot and Eva are matched"), ha="center", fontsize=12, color=MID)
    srcs = [(0.1, t("アンビリカルケーブル\n(外部電源)", "Umbilical cable\n(external power)"), "-"), (3.45, t("内部電源\n(活動限界 約5分)", "Internal battery\n(about 5 min)"), "-"), (6.8, t("S²機関\n(一部の機体・使徒)", "S² organ\n(some units / Angels)"), "--")]
    for (x, label, ls), tx in zip(srcs, (8.0, 8.8, 9.6)):
        box(ax, x, 0.15, 3.1, 1.1, label, fs=12, ls=ls)
        arrow(ax, (x + 1.55, 1.25), (tx, 2.7), lw=1.3, ls=ls)
    return fig

def f_nerv_org(lang, E):
    t = (lambda ja, en: ja if lang == "ja" else en)
    fig, ax = canvas(5.6)
    box(ax, 3.4, 4.4, 3.2, 0.8, t("国連", "United Nations"), fc="white")
    box(ax, 0.1, 3.0, 3.2, 0.9, t("ゼーレ\n(人類補完委員会)", "SEELE\n(Human Instrumentality Cttee.)"), fc=LIGHT, bold=True, fs=12)
    box(ax, 3.8, 3.0, 2.4, 0.9, t("ネルフ", "NERV"), bold=True)
    arrow(ax, (3.3, 3.45), (3.8, 3.45), t("指示", "directs"), ls="--", off=(0, 0.05), fs=10.5)
    arrow(ax, (5.0, 4.4), (5.0, 3.9), style="-")
    box(ax, 6.5, 3.0, 3.3, 0.9, t("総司令 碇ゲンドウ\n副司令 冬月コウゾウ", "Commander: Gendo Ikari\nVice: Kozo Fuyutsuki"), fs=12)
    box(ax, 0.6, 1.2, 2.7, 1.1, t("作戦部\n葛城ミサト\n日向マコト", "Operations\nMisato Katsuragi\nMakoto Hyuga"), fs=11.5)
    box(ax, 3.65, 1.2, 2.7, 1.1, t("技術部\n赤木リツコ\n伊吹マヤ", "Technology\nRitsuko Akagi\nMaya Ibuki"), fs=11.5)
    box(ax, 6.7, 1.2, 2.7, 1.1, t("チルドレン\n(エヴァのパイロット)", "Children\n(Eva pilots)"), fs=11.5)
    for x in (1.95, 5.0, 8.05): arrow(ax, (x, 2.3), (5.0, 3.0), style="-", lw=1.1)
    ax.text(5.0, 0.45, t("※組織図は概念的な整理。肩書・関係は作品との照合が必要", "Conceptual chart. Titles and relations need verification against the work."), ha="center", fontsize=11, color=MID)
    return fig

def f_two_plans(lang, E):
    t = (lambda ja, en: ja if lang == "ja" else en)
    fig, ax = canvas(5.1)
    ax.text(0.1, 4.55, t("ゼーレのシナリオ", "SEELE's scenario"), fontsize=13, fontweight="bold")
    ax.text(0.1, 1.85, t("ゲンドウの計画", "Gendo's plan"), fontsize=13, fontweight="bold")
    xs = [0.1, 2.75, 5.4]
    for i, s in enumerate([t("死海文書\n(シナリオ)", "Dead Sea\nScrolls"), t("量産機・槍", "Mass-prod. Evas\n+ Lance"), t("サード\nインパクト", "Third\nImpact")]):
        box(ax, xs[i], 3.25, 2.1, 1.0, s, fc=LIGHT if i == 2 else PALE, fs=12, bold=(i == 2))
    box(ax, 7.8, 3.2, 2.0, 1.0, t("人類補完", "Instrumentality"), fs=12)
    for i in range(3): arrow(ax, (xs[i] + 2.1, 3.7), (xs[i + 1] if i < 2 else 7.8, 3.7))
    for i, s in enumerate([t("アダム\n(右手)", "Adam\n(his hand)"), t("リリス・綾波レイ", "Lilith / Rei")]):
        box(ax, [0.1, 2.75][i], 0.7, 2.1, 1.0, s, fs=12)
    box(ax, 7.8, 0.7, 2.0, 1.0, t("ユイとの\n再会", "Reunion\nwith Yui"), fs=12, bold=True)
    arrow(ax, (2.2, 1.2), (2.75, 1.2)); arrow(ax, (4.85, 1.2), (7.8, 1.2), ls="--")
    arrow(ax, (6.45, 3.25), (6.45, 1.25), ls=":", lw=1.2); ax.text(6.55, 2.2, t("同じ出来事を\n利用する(?)", "Same event\nused? (?)"), fontsize=10.5, color=MID)
    ax.text(5.0, 0.12, t("※概念図(筆者の整理)。細部は作品との照合が必要", "Conceptual sketch (author's reading). Details need verification."), ha="center", fontsize=11, color=MID)
    return fig

def f_reveal_order(lang, E):
    items = [("使徒・エヴァ・ネルフの基本", "Angels, Evas, NERV basics", 1, 1), ("ATフィールド", "AT Field", 4, 6), ("ダミー・エヴァの出自の一部", "Dummy system / Eva origins (part)", 17, 19),
             ("ユイとエヴァの関係", "Yui and the Eva", 20, 21), ("加持・ゼーレ", "Kaji / SEELE deepen", 20, 26), ("綾波レイの出自", "Rei's origin", 23, 23),
             ("使徒と人類(リリン)", "Angels and humans (Lilin)", 24, 24), ("補完計画の核心", "Core of Instrumentality", 25, 26)]
    fig, ax = plt.subplots(figsize=(W, 0.5 * len(items) + 1.3))
    for i, (ja, en, a, b) in enumerate(items):
        y = len(items) - 1 - i
        ax.barh(y, b - a + 0.84, left=a - 0.42, height=0.55, color=INK if a == b else MID)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([(i[0] if lang == "ja" else i[1]) for i in reversed(items)], fontsize=12)
    ax.set_xticks(range(1, 27)); ax.set_xticklabels([str(i) if i % 5 == 0 or i == 1 else "" for i in range(1, 27)]); ax.set_xlim(0.4, 26.6)
    ax.set_xlabel("話数(概観)" if lang == "ja" else "Episode (overview)"); ax.grid(axis="x", color=LIGHT, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); return fig

def f_evidence_levels(lang, E):
    t = (lambda ja, en: ja if lang == "ja" else en)
    fig, ax = canvas(2.9)
    rows = [("●", t("描写", "Shown"), t("作中の映像・台詞で確定している", "Established on screen, by image or dialogue")),
            ("■", t("発言", "Stated"), t("制作者の発言・公式資料で確定している", "Established by a creator's statement or official document")),
            ("▲", t("解釈", "Interpreted"), t("筆者・批評家の読み(異説は併記する)", "A reading by the author or critics (rival views are listed)"))]
    for i, (m, a, b) in enumerate(rows):
        y = 2.3 - i * 0.85
        ax.text(0.4, y, m, fontsize=22, va="center"); ax.text(1.3, y, a, fontsize=15, fontweight="bold", va="center"); ax.text(3.3, y, b, fontsize=12.5, va="center")
    return fig

FIGS = {"f-angels-episodes": f_angels_episodes, "f-eva-system": f_eva_system, "f-nerv-org": f_nerv_org,
        "f-two-plans": f_two_plans, "f-reveal-order": f_reveal_order, "f-evidence-levels": f_evidence_levels}

def load_registry():
    return {r["id"]: r for r in csv.DictReader(open(ROOT / "figures.csv", newline=""))}

def render(lang, only=None):
    setup(); OUT.mkdir(parents=True, exist_ok=True)
    E, errs = validate.load(); reg = load_registry(); n = 0
    for fid, fn in FIGS.items():
        if only and fid not in only: continue
        fig = fn(lang, E)
        if reg.get(fid, {}).get("verified") != "yes":
            fig.text(0.995, 0.995, "DRAFT・未確認" if lang == "ja" else "DRAFT – unverified", ha="right", va="top", fontsize=10, color=MID, alpha=0.9)
        fig.savefig(OUT / f"{fid}.{lang}.png", dpi=200, facecolor="white"); plt.close(fig); n += 1
    return n

if __name__ == "__main__":
    langs = ["ja", "en"] if "--lang=both" in sys.argv else ["en" if "--lang=en" in sys.argv else "ja"]
    for l in langs: print(l, render(l), "figures")
