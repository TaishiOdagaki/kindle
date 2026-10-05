#!/usr/bin/env python3
"""Generate book figures (own-made diagrams only) from atlas data, themed per volume.

Rules (see FIGURES.md / design/DESIGN.md): grayscale-safe, large text, no images/logos/typefaces from the work.
Each figure is registered in figures.csv; `verified != yes` -> DRAFT watermark and release is blocked.
Output: build/img/<id>.v<vol>.<lang>.png
Usage: python3 build/figs.py [--lang=ja|en|both] [--only=ID,ID]
"""
import csv, sys, pathlib, functools
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib_fontja
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate, design

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "img"
W = 8.0  # inches; dpi 200 -> 1600 px wide
TH = design.theme(1)  # set per render

def setup():
    matplotlib_fontja.japanize()
    plt.rcParams.update({"font.size": 13, "axes.unicode_minus": False, "figure.dpi": 200})

def c(name): return TH[name]
def acc2(): return design.mix(TH["accent_dark"], "#ffffff", 0.45)  # secondary tone of the accent (for marks on white)

def box(ax, x, y, w, h, text, fc=None, ec=None, lw=1.4, fs=13, ls="-", color=None):
    fc = fc or c("pale"); ec = ec or c("ink")
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color or c("ink"), linespacing=1.35)

def arrow(ax, p, q, text=None, ls="-", lw=1.6, fs=11.5, off=(0, 0.08), style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16, lw=lw, ls=ls, color=c("ink"), shrinkA=0, shrinkB=0))
    if text:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], text, ha="center", va="bottom", fontsize=fs, color=c("mid"))

def canvas(ymax):
    fig = plt.figure(figsize=(W, W * ymax / 10)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, ymax); return fig, ax

def T(lang): return (lambda ja, en: ja if lang == "ja" else en)

# ---------------------------------------------------------------- charts and diagrams
def f_angels_episodes(lang, E):
    angels = sorted([e for e in E.values() if e["type"] == "angel" and e.get("episodes")], key=lambda e: e["number"])
    fig, ax = plt.subplots(figsize=(W, 0.42 * len(angels) + 1.3))
    for i, a in enumerate(angels):
        y = len(angels) - 1 - i
        for ep in a["episodes"]:
            ax.barh(y, 0.84, left=ep - 0.42, height=0.62, color=c("accent_dark"))
    ax.set_yticks(range(len(angels)))
    ax.set_yticklabels([("第%d使徒 %s" % (a["number"], a["name_jp"])) if lang == "ja" else ("#%d %s" % (a["number"], a["name_en"])) for a in reversed(angels)], fontsize=12)
    ax.set_xticks(range(1, 27)); ax.set_xticklabels([str(i) if i % 5 == 0 or i == 1 else "" for i in range(1, 27)])
    ax.set_xlim(0.4, 26.6); ax.set_ylim(-0.7, len(angels) - 0.3)
    ax.set_xlabel("話数" if lang == "ja" else "Episode"); ax.grid(axis="x", color=c("light"), lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); return fig

def f_eva_system(lang, E):
    t = T(lang); fig, ax = canvas(5.0)
    box(ax, 0.1, 2.7, 2.2, 1.5, t("パイロット\n(チルドレン)", "Pilot\n(Child)"))
    box(ax, 3.2, 2.45, 3.6, 2.0, t("エントリープラグ\n内部はLCLで満たされる", "Entry plug\nfilled with LCL"), fc=c("paper"), fs=12.5)
    box(ax, 7.7, 2.7, 2.2, 1.5, t("エヴァ", "Evangelion"), fc=c("accent"), color=c("on_accent"))
    arrow(ax, (2.3, 3.45), (3.2, 3.45)); arrow(ax, (6.8, 3.45), (7.7, 3.45), t("神経接続", "neural link"), off=(0, 0.12))
    ax.text(5.0, 4.7, t("シンクロ率: 同調の度合いを示す指標", "Sync ratio: how well pilot and Eva are matched"), ha="center", fontsize=12, color=c("mid"))
    srcs = [(0.1, t("アンビリカルケーブル\n(外部電源)", "Umbilical cable\n(external power)"), "-"), (3.45, t("内部電源\n(活動限界 約5分)", "Internal battery\n(about 5 min)"), "-"), (6.8, t("S²機関\n(一部の機体・使徒)", "S² organ\n(some units / Angels)"), "--")]
    for (x, label, ls), tx in zip(srcs, (8.0, 8.8, 9.6)):
        box(ax, x, 0.15, 3.1, 1.1, label, fs=12, ls=ls, fc=c("tint"))
        arrow(ax, (x + 1.55, 1.25), (tx, 2.7), lw=1.3, ls=ls)
    return fig

def f_nerv_org(lang, E):
    t = T(lang); fig, ax = canvas(5.6)
    box(ax, 3.4, 4.4, 3.2, 0.8, t("国連", "United Nations"), fc=c("paper"))
    box(ax, 0.1, 3.0, 3.2, 0.9, t("ゼーレ\n(人類補完委員会)", "SEELE\n(Human Instrumentality Cttee.)"), fc=c("accent"), color=c("on_accent"), fs=12)
    box(ax, 3.8, 3.0, 2.4, 0.9, t("ネルフ", "NERV"), fc=c("tint"))
    arrow(ax, (3.3, 3.45), (3.8, 3.45), t("指示", "directs"), ls="--", off=(0, 0.05), fs=10.5)
    arrow(ax, (5.0, 4.4), (5.0, 3.9), style="-")
    box(ax, 6.5, 3.0, 3.3, 0.9, t("総司令 碇ゲンドウ\n副司令 冬月コウゾウ", "Commander: Gendo Ikari\nVice: Kozo Fuyutsuki"), fs=12)
    box(ax, 0.6, 1.2, 2.7, 1.1, t("作戦部\n葛城ミサト\n日向マコト", "Operations\nMisato Katsuragi\nMakoto Hyuga"), fs=11.5)
    box(ax, 3.65, 1.2, 2.7, 1.1, t("技術部\n赤木リツコ\n伊吹マヤ", "Technology\nRitsuko Akagi\nMaya Ibuki"), fs=11.5)
    box(ax, 6.7, 1.2, 2.7, 1.1, t("チルドレン\n(エヴァのパイロット)", "Children\n(Eva pilots)"), fs=11.5)
    for x in (1.95, 5.0, 8.05): arrow(ax, (x, 2.3), (5.0, 3.0), style="-", lw=1.1)
    ax.text(5.0, 0.45, t("※組織図は概念的な整理。肩書・関係は作品との照合が必要", "Conceptual chart. Titles and relations need verification against the work."), ha="center", fontsize=11, color=c("mid"))
    return fig

def f_two_plans(lang, E):
    t = T(lang); fig, ax = canvas(5.1)
    ax.text(0.1, 4.55, t("ゼーレのシナリオ", "SEELE's scenario"), fontsize=13)
    ax.text(0.1, 1.85, t("ゲンドウの計画", "Gendo's plan"), fontsize=13)
    xs = [0.1, 2.75, 5.4]
    for i, s in enumerate([t("死海文書\n(シナリオ)", "Dead Sea\nScrolls"), t("量産機・槍", "Mass-prod. Evas\n+ Lance"), t("サード\nインパクト", "Third\nImpact")]):
        box(ax, xs[i], 3.25, 2.1, 1.0, s, fc=c("accent") if i == 2 else c("tint"), color=c("on_accent") if i == 2 else None, fs=12)
    box(ax, 7.8, 3.2, 2.0, 1.0, t("人類補完", "Instrumentality"), fs=12)
    for i in range(3): arrow(ax, (xs[i] + 2.1, 3.7), (xs[i + 1] if i < 2 else 7.8, 3.7))
    for i, s in enumerate([t("アダム\n(右手)", "Adam\n(his hand)"), t("リリス・綾波レイ", "Lilith / Rei")]):
        box(ax, [0.1, 2.75][i], 0.7, 2.1, 1.0, s, fs=12, fc=c("tint"))
    box(ax, 7.8, 0.7, 2.0, 1.0, t("ユイとの\n再会", "Reunion\nwith Yui"), fs=12, fc=c("accent"), color=c("on_accent"))
    arrow(ax, (2.2, 1.2), (2.75, 1.2)); arrow(ax, (4.85, 1.2), (7.8, 1.2), ls="--")
    arrow(ax, (6.45, 3.25), (6.45, 1.25), ls=":", lw=1.2); ax.text(6.55, 2.2, t("同じ出来事を\n利用する(?)", "Same event\nused? (?)"), fontsize=10.5, color=c("mid"))
    ax.text(5.0, 0.12, t("※概念図(筆者の整理)。細部は作品との照合が必要", "Conceptual sketch (author's reading). Details need verification."), ha="center", fontsize=11, color=c("mid"))
    return fig

def f_reveal_order(lang, E):
    items = [("使徒・エヴァ・ネルフの基本", "Angels, Evas, NERV basics", 1, 1), ("ATフィールド", "AT Field", 4, 6), ("ダミー・エヴァの出自の一部", "Dummy system / Eva origins (part)", 17, 19),
             ("ユイとエヴァの関係", "Yui and the Eva", 20, 21), ("加持・ゼーレ", "Kaji / SEELE deepen", 20, 26), ("綾波レイの出自", "Rei's origin", 23, 23),
             ("使徒と人類(リリン)", "Angels and humans (Lilin)", 24, 24), ("補完計画の核心", "Core of Instrumentality", 25, 26)]
    fig, ax = plt.subplots(figsize=(W, 0.5 * len(items) + 1.3))
    for i, (ja, en, a, b) in enumerate(items):
        y = len(items) - 1 - i
        ax.barh(y, b - a + 0.84, left=a - 0.42, height=0.55, color=c("accent_dark") if a == b else acc2())
    ax.set_yticks(range(len(items))); ax.set_yticklabels([(i[0] if lang == "ja" else i[1]) for i in reversed(items)], fontsize=12)
    ax.set_xticks(range(1, 27)); ax.set_xticklabels([str(i) if i % 5 == 0 or i == 1 else "" for i in range(1, 27)]); ax.set_xlim(0.4, 26.6)
    ax.set_xlabel("話数(概観)" if lang == "ja" else "Episode (overview)"); ax.grid(axis="x", color=c("light"), lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); return fig

def f_evidence_levels(lang, E):
    t = T(lang); fig, ax = canvas(2.9)
    rows = [("●", t("描写", "Shown"), t("作中の映像・台詞で確定している", "Established on screen, by image or dialogue")),
            ("■", t("発言", "Stated"), t("制作者の発言・公式資料で確定している", "Established by a creator's statement or official document")),
            ("▲", t("解釈", "Interpreted"), t("筆者・批評家の読み(異説は併記する)", "A reading by the author or critics (rival views are listed)"))]
    for i, (m, a, b) in enumerate(rows):
        y = 2.3 - i * 0.85
        ax.text(0.4, y, m, fontsize=22, va="center", color=c("accent_dark")); ax.text(1.3, y, a, fontsize=15, va="center"); ax.text(3.3, y, b, fontsize=12.5, va="center")
    return fig

def f_mother_eva(lang, E):
    t = T(lang); fig, ax = canvas(5.2)
    rows = [(t("ユイ", "Yui"), t("初号機", "Unit-01"), t("シンジ", "Shinji"), "-"),
            (t("キョウコ", "Kyoko"), t("弐号機", "Unit-02"), t("アスカ", "Asuka"), "-"),
            (t("ナオコ", "Naoko"), "MAGI", t("リツコ", "Ritsuko"), "--")]
    heads = [t("母", "Mother"), t("宿る先", "Where she dwells"), t("子", "Child")]
    for x, h in zip((0.5, 4.1, 7.7), heads): ax.text(x + 0.9, 4.45, h, ha="center", fontsize=12, color=c("mid"))
    for i, (m, k, ch, ls) in enumerate(rows):
        y = 3.5 - i * 1.55
        box(ax, 0.5, y, 1.8, 0.95, m, fc=c("tint"), ls="--" if i == 2 else "-")
        box(ax, 4.1, y, 1.8, 0.95, k, fc=c("accent"), color=c("on_accent"))
        box(ax, 7.7, y, 1.8, 0.95, ch, fc=c("paper"))
        arrow(ax, (2.3, y + 0.47), (4.1, y + 0.47), t("魂が宿る" if i < 2 else "人格を移植", "soul dwells" if i < 2 else "personality copied"), ls=ls, fs=10.5, off=(0, 0.06))
        arrow(ax, (5.9, y + 0.47), (7.7, y + 0.47), t("搭乗" if i < 2 else "同僚として扱う", "pilots" if i < 2 else "works with"), ls="-", fs=10.5, off=(0, 0.06))
    ax.text(5.0, 0.12, t("※概念図(筆者の整理)。各対応は作品との照合が必要", "Conceptual sketch (author's reading). Each pairing needs verification."), ha="center", fontsize=11, color=c("mid"))
    return fig

def _graph(ax, N, edges, t):
    for a, b, lab, ls in edges:
        (_, x1, y1, _), (_, x2, y2, _) = N[a], N[b]
        ax.plot([x1, x2], [y1, y2], color=c("ink"), lw=1.3, ls=ls, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, lab, ha="center", va="center", fontsize=10.5, color=c("mid"), zorder=3, bbox=dict(fc="white", ec="none", pad=1.5))
    for k, (name, x, y, kind) in N.items():
        box(ax, x - 0.8, y - 0.34, 1.6, 0.68, name, fc=c("accent") if kind == "hub" else c("tint") if kind == "absent" else c("paper"),
            color=c("on_accent") if kind == "hub" else None, ls="--" if kind == "absent" else "-", fs=12.5)
        ax.patches[-1].set_zorder(2); ax.texts[-1].set_zorder(4)

def f_relations_family(lang, E):
    t = T(lang); fig, ax = canvas(6.2)
    N = {"yui": (t("ユイ", "Yui"), 1.3, 5.0, "absent"), "gendo": (t("ゲンドウ", "Gendo"), 4.4, 5.0, "plain"), "keel": (t("キール", "Keel"), 7.9, 5.0, "plain"),
         "shinji": (t("シンジ", "Shinji"), 1.3, 2.0, "hub"), "rei": (t("レイ", "Rei"), 4.4, 2.0, "plain"), "fuyu": (t("冬月", "Fuyutsuki"), 7.9, 2.0, "plain")}
    edges = [("yui", "gendo", t("夫婦", "spouses"), "-"), ("gendo", "keel", t("同盟(?)", "allies(?)"), "--"), ("yui", "shinji", t("親子", "mother-son"), "--"), ("gendo", "shinji", t("親子", "father-son"), "-"),
             ("gendo", "rei", t("後見(?)", "guardian(?)"), "--"), ("gendo", "fuyu", t("補佐", "deputy"), "-"), ("shinji", "rei", t("同僚", "fellow pilot"), "-")]
    _graph(ax, N, edges, t)
    ax.text(5.0, 0.55, t("※点線の枠=作中に姿を見せない人物 / 点線=解釈を含む関係。線の意味は概念的な整理で、作品との照合が必要", "Dashed box: not seen on screen. Dashed line: interpretive. Conceptual; needs verification."), ha="center", fontsize=10.5, color=c("mid"))
    return fig

def f_relations_daily(lang, E):
    t = T(lang); fig, ax = canvas(6.2)
    N = {"shinji": (t("シンジ", "Shinji"), 5.0, 3.6, "hub"), "rei": (t("レイ", "Rei"), 1.6, 3.6, "plain"), "asuka": (t("アスカ", "Asuka"), 8.4, 3.6, "plain"), "kaworu": (t("カヲル", "Kaworu"), 8.4, 5.4, "plain"),
         "ritsuko": (t("リツコ", "Ritsuko"), 1.6, 1.2, "plain"), "misato": (t("ミサト", "Misato"), 5.0, 1.2, "plain"), "kaji": (t("加持", "Kaji"), 8.4, 1.2, "plain")}
    edges = [("shinji", "misato", t("同居", "lives with"), "-"), ("misato", "asuka", t("同居", "lives with"), "-"), ("shinji", "asuka", t("同僚", "fellow pilot"), "-"), ("shinji", "rei", t("同僚", "fellow pilot"), "-"),
             ("shinji", "kaworu", t("友情", "friendship"), "-"), ("misato", "kaji", t("元恋人", "ex-partner"), "-"), ("misato", "ritsuko", t("旧友", "old friend"), "-")]
    _graph(ax, N, edges, t)
    ax.text(5.0, 0.3, t("※線の意味は概念的な整理で、関係の性格は作品との照合が必要", "Conceptual reading; relationship types need verification."), ha="center", fontsize=10.5, color=c("mid"))
    return fig

# ---------------------------------------------------------------- episode card
def ep_card(lang, E, n):
    t = T(lang); e = E[f"ep-{n:02d}"]
    angels = sorted([a for a in E.values() if a["type"] == "angel" and n in (a.get("episodes") or [])], key=lambda a: a["number"])
    dash = "—"
    def show(items, ids=False):
        out = []
        for x in items or []:
            if x == "-": continue
            out.append(E[x].get("name_jp" if lang == "ja" else "name_en", x) if ids and x in E else x)
        return "、".join(out)
    def val(items, ids=False):
        if items == ["-"]: return "なし" if lang == "ja" else "none"
        return show(items, ids) or dash
    fig, ax = canvas(3.9)
    ax.add_patch(Rectangle((0, 0), 2.1, 3.9, fc=c("accent"), ec="none"))
    ax.text(1.05, 3.1, t("第", "EP."), ha="center", va="center", fontsize=15, color=c("on_accent"))
    ax.text(1.05, 2.15, str(n), ha="center", va="center", fontsize=58, color=c("on_accent"))
    if lang == "ja": ax.text(1.05, 1.2, "話", ha="center", va="center", fontsize=15, color=c("on_accent"))
    ax.text(1.05, 0.5, e.get("air_date_jp") or "", ha="center", va="center", fontsize=10.5, color=c("on_accent"))
    title = (e.get("title_jp") or "") if lang == "ja" else (e.get("title_en") or e.get("title_jp") or "")
    ax.text(2.5, 3.45, title, fontsize=19, va="center")
    sub = (e.get("title_en") or "") if lang == "ja" else ""
    if sub: ax.text(2.5, 3.1, sub, fontsize=11, va="center", color=c("mid"))
    ax.plot([2.5, 9.8], [2.85, 2.85], color=c("light"), lw=1)
    vn = e.get("version_note") or ""
    rows = [(t("使徒", "Angel"), ("、".join(("第%d使徒 %s" % (a["number"], a["name_jp"])) if lang == "ja" else ("#%d %s" % (a["number"], a["name_en"])) for a in angels) or dash)),
            (t("出撃", "Sortie"), val(e.get("sorties"))),
            (t("中心人物", "Focus"), val(e.get("focus"), ids=True)),
            (t("明かされる設定", "New in this ep."), val(e.get("reveals"))),
            (t("版による差", "Version notes"), ("なし" if vn == "-" and lang == "ja" else "none" if vn == "-" else vn or dash))]
    def wrap(text, width=26, maxlines=2):
        lines = [text[i:i + width] for i in range(0, len(text), width)] or [""]
        if len(lines) > maxlines: lines = lines[:maxlines]; lines[-1] = lines[-1][:-1] + "…"
        return lines
    y = 2.45
    for lab, v in rows:
        lines = wrap(v)
        ax.text(2.5, y, lab, fontsize=11, color=c("mid"), va="center")
        ax.text(4.6, y, "\n".join(lines), fontsize=13 if len(lines) == 1 else 11, va="center", linespacing=1.15)
        ax.plot([2.5, 9.8], [y - 0.3, y - 0.3], color=c("pale"), lw=0.8); y -= 0.52
    ax.text(9.8, 0.12, f"ep-{n:02d} · {e.get('status','')}", ha="right", fontsize=9, color=c("mid"))
    return fig

# ---------------------------------------------------------------- registry
FIGS = {"f-angels-episodes": f_angels_episodes, "f-eva-system": f_eva_system, "f-nerv-org": f_nerv_org,
        "f-two-plans": f_two_plans, "f-reveal-order": f_reveal_order, "f-evidence-levels": f_evidence_levels,
        "f-mother-eva": f_mother_eva, "f-relations-family": f_relations_family, "f-relations-daily": f_relations_daily}
for _n in range(1, 27):
    FIGS[f"f-ep-{_n:02d}"] = functools.partial(lambda lang, E, n=_n: ep_card(lang, E, n))

def load_registry():
    return {r["id"]: r for r in csv.DictReader(open(ROOT / "figures.csv", newline="", encoding="utf-8-sig"))}

def render(lang, vols=("1", "2", "3"), only=None):
    global TH
    setup(); OUT.mkdir(parents=True, exist_ok=True)
    E, errs = validate.load(); reg = load_registry(); n = 0
    for v in vols:
        TH = design.theme(v)
        for fid, fn in FIGS.items():
            if only and fid not in only: continue
            fig = fn(lang, E)
            if reg.get(fid, {}).get("verified") != "yes":
                fig.text(0.995, 0.995, "DRAFT・未確認" if lang == "ja" else "DRAFT – unverified", ha="right", va="top", fontsize=10, color=c("mid"))
            fig.savefig(OUT / f"{fid}.v{v}.{lang}.png", dpi=200, facecolor="white"); plt.close(fig); n += 1
    return n

if __name__ == "__main__":
    langs = ["ja", "en"] if "--lang=both" in sys.argv else ["en" if "--lang=en" in sys.argv else "ja"]
    only = next((a.split("=")[1].split(",") for a in sys.argv if a.startswith("--only=")), None)
    for l in langs: print(l, render(l, only=only), "images")
