#!/usr/bin/env python3
"""Import the viewing-check sheets (data/entry/*.csv) into the atlas.

  python3 build/import_entry.py --dry-run   # validate and show what would change
  python3 build/import_entry.py             # write to atlas/ and sync figures.csv

Conventions:
  - blank cell = not yet filled in;   '-' = checked, and there is none
  - lists are separated by ';' (or '；')
  - ok = ○ marks the row as checked against the work. Requires checked_by and all required fields.
"""
import re, sys, datetime, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import entry
ROOT = entry.ROOT
DRY = "--dry-run" in sys.argv
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
errors, warns, changes = [], [], []
SOURCE = "src-work-tv"

def clean_body(body, note, who, date, edition):
    body = re.sub(r"^.*\[\[CHECK.*\]\].*\n?", "", body, flags=re.M).strip()
    stamp = f"確認: {who}({date})" + (f"/ 視聴した版: {edition}" if edition else "")
    return (body + "\n\n" if body else "") + stamp + (f"\n確認メモ: {note}" if note else "")

def check_row_common(r, label):
    ok = (r.get("ok") or "").strip() in ("○", "o", "O", "yes", "1")
    if ok:
        if not (r.get("checked_by") or "").strip(): errors.append(f"{label}: ○ だが checked_by(確認者)が空")
        d = (r.get("checked_date") or "").strip()
        if not DATE.match(d): errors.append(f"{label}: ○ だが checked_date が YYYY-MM-DD 形式でない({d!r})")
    return ok

def import_episodes():
    for r in entry.read_csv(entry.ENTRY / "episodes.csv"):
        try: n = int(r["episode"])
        except Exception: errors.append(f"episodes.csv: episode が数字でない: {r.get('episode')!r}"); continue
        label = f"第{n}話"
        p = ROOT / "atlas" / "episodes" / f"ep-{n:02d}.md"
        if not p.exists(): errors.append(f"{label}: atlas に ep-{n:02d} がない"); continue
        meta, body = entry.read_entity(p)
        ok = check_row_common(r, label)
        d = (r.get("air_date_jp") or "").strip()
        if d and d != "-" and not DATE.match(d): errors.append(f"{label}: air_date_jp は YYYY-MM-DD 形式(例 1995-10-04)。入力値: {d!r}")
        for k in ("sorties", "focus", "reveals"):
            v = entry.split_list(r.get(k))
            if sum(len(x) for x in v) > 52: warns.append(f"{label}: {k} が長い(カードに収まらない可能性)。短くする")
            meta[k] = v
        meta["title_jp"] = (r.get("title_jp") or "").strip() or meta.get("title_jp", "")
        meta["title_en"] = (r.get("title_en") or "").strip()
        meta["air_date_jp"] = "" if d == "-" else d
        meta["version_note"] = (r.get("version_note") or "").strip()
        meta["viewed_edition"] = (r.get("viewed_edition") or "").strip()
        if ok:
            req = {"title_jp": meta["title_jp"], "air_date_jp": d, "viewed_edition": meta["viewed_edition"], "sorties": r.get("sorties"), "focus": r.get("focus"),
                   "reveals": r.get("reveals"), "version_note": r.get("version_note")}
            for k, v in req.items():
                if not (v or "").strip(): errors.append(f"{label}: ○ だが {k} が空欄(なければ「-」を入れる)")
            if not any(e.startswith(label + ":") for e in errors):
                meta.update({"status": "verified", "verified_by": r["checked_by"].strip(), "verified_date": r["checked_date"].strip(), "sources": [SOURCE]})
                body = clean_body(body, (r.get("note") or "").strip(), meta["verified_by"], meta["verified_date"], meta["viewed_edition"])
        else:
            if meta.get("status") == "verified": meta["status"] = "draft"; warns.append(f"{label}: ○ が外れたので draft に戻した")
            if (r.get("note") or "").strip(): body = body.rstrip() + f"\n確認メモ(未確定): {r['note'].strip()}"
        changes.append((p, meta, body, label))

def import_angels():
    for r in entry.read_csv(entry.ENTRY / "angels.csv"):
        try: n = int(r["number"])
        except Exception: errors.append(f"angels.csv: number が数字でない: {r.get('number')!r}"); continue
        label = f"第{n}使徒"
        hits = [p for p in (ROOT / "atlas" / "angels").glob("an-*.md") if entry.read_entity(p)[0]["number"] == n]
        if not hits: errors.append(f"{label}: atlas に該当なし"); continue
        p = hits[0]; meta, body = entry.read_entity(p)
        ok = check_row_common(r, label)
        ev = (r.get("episodes") or "").strip()
        if ev in ("", "-"): eps = []
        else:
            eps = []
            for x in entry.split_list(ev):
                if not x.isdigit() or not 1 <= int(x) <= 26: errors.append(f"{label}: episodes に不正な値 {x!r}(1〜26の数字を ; で区切る)")
                else: eps.append(int(x))
        meta["episodes"] = eps
        meta["name_jp"] = (r.get("name_jp") or meta["name_jp"]).strip(); meta["name_en"] = (r.get("name_en") or meta["name_en"]).strip()
        if ok:
            if ev == "": errors.append(f"{label}: ○ だが episodes が空欄(戦わない使徒は「-」)")
            if not any(e.startswith(label + ":") for e in errors):
                meta.update({"status": "verified", "verified_by": r["checked_by"].strip(), "verified_date": r["checked_date"].strip(), "sources": [SOURCE]})
                body = clean_body(body, (r.get("note") or "").strip(), meta["verified_by"], meta["verified_date"], "")
        else:
            if meta.get("status") == "verified": meta["status"] = "draft"; warns.append(f"{label}: ○ が外れたので draft に戻した")
            if (r.get("note") or "").strip(): body = body.rstrip() + f"\n確認メモ(未確定): {r['note'].strip()}"
        changes.append((p, meta, body, label))

def sync_figures():
    """f-ep-NN is verified when ep-NN and every Angel appearing in it are verified. f-angels-episodes: all fought Angels verified."""
    ents = {}
    for p in list((ROOT / "atlas" / "episodes").glob("*.md")) + list((ROOT / "atlas" / "angels").glob("*.md")):
        m, _ = entry.read_entity(p); ents[m["id"]] = m
    for p, m, _, _ in changes: ents[m["id"]] = m   # reflect pending changes
    angels = [m for m in ents.values() if m["type"] == "angel"]
    rows = entry.read_csv(ROOT / "figures.csv"); out = []
    for r in rows:
        if r["id"].startswith("f-ep-"):
            n = int(r["id"][5:]); e = ents.get(f"ep-{n:02d}")
            need = [a for a in angels if n in (a.get("episodes") or [])]
            r["verified"] = "yes" if e and e.get("status") == "verified" and all(a.get("status") == "verified" for a in need) else "no"
        elif r["id"] == "f-angels-episodes":
            fought = [a for a in angels if a.get("episodes")]
            r["verified"] = "yes" if fought and all(a.get("status") == "verified" for a in fought) else "no"
        out.append(r)
    return out

import_episodes(); import_angels()
for w in warns: print("警告:", w)
if errors:
    print("エラー(取り込みを中止):"); [print(" -", e) for e in errors]; sys.exit(1)
figrows = sync_figures()
ver = sum(1 for _, m, _, _ in changes if m.get("status") == "verified")
print(f"検証済み(○): {ver} / {len(changes)} 行。図の検証済み: {sum(1 for r in figrows if r['verified']=='yes')} / {len(figrows)}")
if DRY: print("(dry-run: 何も書き込んでいません)"); sys.exit(0)
for p, meta, body, _ in changes: entry.write_entity(p, meta, body)
entry.write_csv(ROOT / "figures.csv", list(figrows[0].keys()), figrows, bom=False)
print("atlas と figures.csv を更新しました。python3 build/validate.py && python3 build/figs.py を実行してください。")
