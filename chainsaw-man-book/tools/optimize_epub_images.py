#!/usr/bin/env python3
"""Recompress image payloads in an EPUB while keeping content and cover unchanged.

Usage from chainsaw-man-book/:
  python tools/optimize_epub_images.py input.epub output-optimized.epub

Requires Pillow. All image pixel dimensions are preserved.
"""
import argparse
from io import BytesIO
from pathlib import Path
import zipfile
from PIL import Image

JPEG_QUALITY = 75
PNG_PALETTE_COLORS = 256


def compress_image(name: str, data: bytes) -> bytes:
    low = name.lower()
    if not low.endswith(('.jpg', '.jpeg', '.png')):
        return data
    image = Image.open(BytesIO(data)).convert("RGB")
    stream = BytesIO()
    if low.endswith(('.jpg', '.jpeg')):
        image.save(stream, format="JPEG", quality=JPEG_QUALITY,
                   subsampling=2, optimize=True)
    else:
        indexed = image.quantize(colors=PNG_PALETTE_COLORS,
                                 method=Image.Quantize.MEDIANCUT,
                                 dither=Image.Dither.NONE)
        indexed.save(stream, format="PNG", optimize=True)
    encoded = stream.getvalue()
    return encoded if len(encoded) < len(data) else data


def optimize_epub(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output paths must differ; keep original EPUB")
    with zipfile.ZipFile(source, "r") as incoming:
        if incoming.testzip() is not None:
            raise RuntimeError("Input EPUB failed ZIP CRC test")
        entries = incoming.infolist()
        if (not entries or entries[0].filename != "mimetype"
                or incoming.read("mimetype") != b"application/epub+zip"):
            raise RuntimeError("Invalid EPUB mimetype entry")
        image_count, replaced_count = 0, 0
        with zipfile.ZipFile(destination, "w") as outgoing:
            for info in entries:
                original = incoming.read(info.filename)
                if info.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_count += 1
                    replacement = compress_image(info.filename, original)
                    if replacement != original:
                        replaced_count += 1
                else:
                    replacement = original
                outgoing.writestr(info, replacement)
    with zipfile.ZipFile(destination) as check:
        if check.testzip() is not None:
            raise RuntimeError("Output EPUB failed ZIP CRC test")
        if check.infolist()[0].compress_type != zipfile.ZIP_STORED:
            raise RuntimeError("Output EPUB must retain uncompressed mimetype")
    print("Original:", source.stat().st_size, "bytes")
    print("Optimized:", destination.stat().st_size, "bytes")
    print("Images:", image_count, "recompressed:", replaced_count)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_epub", type=Path)
    parser.add_argument("output_epub", type=Path)
    arguments = parser.parse_args()
    optimize_epub(arguments.input_epub, arguments.output_epub)


if __name__ == "__main__":
    main()
