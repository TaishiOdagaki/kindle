"""Shared helpers: chapter table, volume filtering, cross-reference resolution."""
import csv, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_rows():
    return list(csv.DictReader(open(ROOT / "chapters.csv", newline="")))

def vols_of(r):
    return r["volume"].split("|")

def in_volume(r, vol):
    return vol == "all" or vol in vols_of(r)

def chapter_numbers(rows, vol):
    """Number the 'cNN' chapters. vol='all' -> global (cNN -> NN); else sequence within the volume."""
    nums, n = {}, 0
    for r in rows:
        if not r["id"].startswith("c"):
            continue
        if vol == "all":
            nums[r["id"]] = int(r["id"][1:])
        elif vol in vols_of(r):
            n += 1; nums[r["id"]] = n
    return nums

def home_volume(rows, cid):
    r = next(x for x in rows if x["id"] == cid)
    return vols_of(r)[0]

def resolve_refs(text, rows, cur_vol):
    nums_cur = chapter_numbers(rows, cur_vol)
    cache = {}
    def num(cid):
        v = home_volume(rows, cid)
        if cur_vol == "all":
            return None, int(cid[1:])
        if v not in cache:
            cache[v] = chapter_numbers(rows, v)
        return v, cache[v][cid]
    def fmt(cid):
        v, n = num(cid)
        return f"第{n}章" if v in (None, cur_vol) else f"第{v}巻 第{n}章"
    def rng(m):
        a, b = m.group(1), m.group(2)
        va, na = num(a); vb, nb = num(b)
        if va == vb and va in (None, cur_vol):
            return f"第{na}〜{nb}章"
        if va == vb:
            return f"第{va}巻 第{na}〜{nb}章"
        return f"{fmt(a)}〜{fmt(b)}"
    text = re.sub(r"\{\{(c\d+)\.\.(c\d+)\}\}", rng, text)
    text = re.sub(r"\{\{(c\d+)\}\}", lambda m: fmt(m.group(1)), text)
    return text

def apply_volume_fences(text, vol):
    """<!--vol 1,2--> ... <!--/vol--> : keep only for the listed volumes."""
    def f(m):
        keep = vol == "all" or vol in [x.strip() for x in m.group(1).split(",")]
        return m.group(2) if keep else ""
    return re.sub(r"<!--vol ([\d,\s]+)-->(.*?)<!--/vol-->", f, text, flags=re.S)
