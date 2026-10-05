#!/usr/bin/env python3
"""Export the current atlas state to data/entry/episodes.csv and angels.csv (for viewing-check entry)."""
import sys, glob, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import entry
ROOT = entry.ROOT
angels = {}
for p in sorted((ROOT / "atlas" / "angels").glob("an-*.md")):
    m, _ = entry.read_entity(p); angels[m["id"]] = m
ep_rows = []
for p in sorted((ROOT / "atlas" / "episodes").glob("ep-*.md")):
    m, _ = entry.read_entity(p); n = m["number"]
    ang = [a for a in angels.values() if n in (a.get("episodes") or [])]
    ep_rows.append({"episode": n, "title_jp": m.get("title_jp", ""), "title_en": m.get("title_en", ""), "air_date_jp": m.get("air_date_jp", ""),
                    "viewed_edition": m.get("viewed_edition", ""), "sorties": ";".join(m.get("sorties") or []), "focus": ";".join(m.get("focus") or []),
                    "reveals": ";".join(m.get("reveals") or []), "version_note": m.get("version_note", ""),
                    "ok": "○" if m.get("status") == "verified" else "", "checked_by": m.get("verified_by", ""), "checked_date": m.get("verified_date", ""), "note": "",
                    "(参考)使徒の登録内容": "、".join("第%d使徒 %s" % (a["number"], a["name_jp"]) for a in sorted(ang, key=lambda a: a["number"])) or "(なし)",
                    "(参考)現在の状態": m.get("status", "")})
an_rows = []
for a in sorted(angels.values(), key=lambda a: a["number"]):
    an_rows.append({"number": a["number"], "name_jp": a["name_jp"], "name_en": a["name_en"], "episodes": ";".join(map(str, a.get("episodes") or [])) or "-",
                    "ok": "○" if a.get("status") == "verified" else "", "checked_by": a.get("verified_by", ""), "checked_date": a.get("verified_date", ""), "note": "",
                    "(参考)現在の状態": a.get("status", "")})
entry.ENTRY.mkdir(parents=True, exist_ok=True)
entry.write_csv(entry.ENTRY / "episodes.csv", entry.EP_COLS, ep_rows)
entry.write_csv(entry.ENTRY / "angels.csv", entry.AN_COLS, an_rows)
print(f"exported {len(ep_rows)} episodes, {len(an_rows)} angels -> data/entry/")
