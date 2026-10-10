#!/usr/bin/env python3
"""Correct spoiler-category icons in both Chainsaw Man English charts.

Requires Pillow: python -m pip install pillow
Run from the book folder:
    python tools/refresh_spoiler_charts_2026_10_10.py --in-place

The source chart images are preserved in Git history. By default this script
writes _preview PNGs only; --in-place is needed to change the actual image assets.
It expects the chart geometry used in the 2026-09-28 edition.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageChops

CHARTS = {
    "whats_inside.png": {
        "size": (2400, 3195), "first_center": 510, "step": 162,
        "x0": 2145, "x1": 2300, "half": 56
    },
    "spoiler_map.png": {
        "size": (2400, 3630), "first_center": 538, "step": 198,
        "x0": 2140, "x1": 2310, "half": 67
    },
}
# Rows: 0=Introduction, 1..14=chapter numbers.
# Chapter 4 and Chapter 8 remain mixed; other statuses remain unchanged.
CHANGE_ROWS = (0, 1, 2, 3, 7)
SOURCE_FULL_SPOILER_ROW = 10

def update_image(file_path: Path, conf: dict, in_place: bool):
    with Image.open(file_path) as image:
        im = image.convert("RGB")
    if im.size != conf["size"]:
        raise ValueError(f"{file_path} has dimensions {im.size}, expected {conf['size']}; refusing to draw")
    src = im.copy()
    x0, x1, half = conf["x0"], conf["x1"], conf["half"]
    y0, step = conf["first_center"], conf["step"]
    donor = src.crop((x0, y0 + SOURCE_FULL_SPOILER_ROW * step - half,
                      x1, y0 + SOURCE_FULL_SPOILER_ROW * step + half))
    for row in CHANGE_ROWS:
        im.paste(donor, (x0, y0 + row * step - half))
    changed = ImageChops.difference(src, im).getbbox()
    if changed is None:
        raise ValueError(f"{file_path}: no pixels changed; refusing silently to mark complete")
    destination = file_path if in_place else file_path.with_name(file_path.stem + "_preview.png")
    im.save(destination, "PNG", optimize=True)
    print(f"Wrote {destination} | modified pixels bbox = {changed}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-place", action="store_true", help="Update original chart paths (the Git commit preserves previous versions)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "images" / "charts"
    for name, conf in CHARTS.items():
        update_image(root / name, conf, args.in_place)

if __name__ == "__main__":
    main()
