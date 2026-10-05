"""Shared helpers for the viewing-check data entry sheets (episodes.csv / angels.csv)."""
import csv, re, pathlib
import yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRY = ROOT / "data" / "entry"
SEP = re.compile(r"\s*[;；]\s*")
EP_COLS = ["episode", "title_jp", "title_en", "air_date_jp", "viewed_edition", "sorties", "focus", "reveals", "version_note",
           "ok", "checked_by", "checked_date", "note", "(参考)使徒の登録内容", "(参考)現在の状態"]
AN_COLS = ["number", "name_jp", "name_en", "episodes", "ok", "checked_by", "checked_date", "note", "(参考)現在の状態"]

def split_list(s):
    s = (s or "").strip()
    return [x for x in SEP.split(s) if x] if s else []

def read_entity(path):
    t = pathlib.Path(path).read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    return yaml.safe_load(m.group(1)), m.group(2)

def write_entity(path, meta, body):
    pathlib.Path(path).write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + body.strip() + "\n")

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def write_csv(path, cols, rows, bom=True):
    with open(path, "w", newline="", encoding="utf-8-sig" if bom else "utf-8") as f:   # BOM only for sheets meant to be opened in Excel
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
