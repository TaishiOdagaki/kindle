# EPUB image optimization — 2026-10-10

**Status:** Delivered separately to the author as a new EPUB. Neither the existing KDP live book nor the existing binary `Chainsaw Man - The Devil in the Details.epub` in this branch was overwritten. The separate **cover file remains unchanged**.

## Exact input/output

- Source: the **October 10 revised EPUB** `chainsaw_man_revised.epub`, **4,164,779 bytes**, SHA-256 `2cde7f19da719be5e25f24513777de99984e115d0d0a79eaa3a9cf53e79f1c3d`.
- Output: `chainsaw_man_optimized_2026-10-10.epub`, **2,765,875 bytes**, SHA-256 `6499f25bde811b546212fee80c111efd3e49bac35301491fc520f28541f2c616`.
- Reduction: **1,398,904 bytes / 33.6%**.

## Reproducible procedure

A fresh editable script now lives at [../tools/optimize_epub_images.py](../tools/optimize_epub_images.py) (Python 3 + Pillow). It reproduces the same Pillow transformation settings used for the delivered EPUB:

- Recompress **15 JPEG chapter-opening images** at original pixel dimensions (1600 x 2560), quality 75, optimized Huffman, 4:2:0 sampling.
- Convert **7 PNG diagrams** to standard 256-color indexed PNG at their existing resolutions (2400 px wide); avoids WebP for conservative EPUB compatibility.
- Keep the input archive's entry names, XML/CSS/TOC, text, metadata, navigation, compression types and image positions. Never rewrite the separate KDP cover file.
- Preserve source by always supplying a **different output filename**.

Example after obtaining the completed, revised EPUB:

```bash
python -m pip install pillow
python tools/optimize_epub_images.py \
  "Chainsaw Man - The Devil in the Details - Revised 2026-10-10.epub" \
  "Chainsaw Man - The Devil in the Details - Optimized 2026-10-10.epub"
```

**Do not optimize the older binary committed under the old published filename and assume the result contains the Oct 10 content fixes.** The correct input is the Oct 10 *revised* EPUB.

## Checks completed

- ZIP CRC passes and first `mimetype` entry is uncompressed.
- 53 archive entries unchanged as a set. **31 non-image files are byte-for-byte identical** (no textual or metadata changes).
- All **22 images** preserved at exactly the same pixel dimensions.
- Parsed **29 XML/XHTML-related files**, checked **146 internal references** with zero broken links.
- All chart labels are still present. Sample visual crops checked manually; quantitative downscaled-image SSIM min **0.99605**, mean **0.99738** (640px width). These are only engineering checks, not device-display certification.
- Pandoc can open and extract the resulting book.

**Outstanding prepublication QA:** formal EPUBCheck; Kindle Previewer/device verification especially small diagram text; actual KDP-assessed delivery charge.

## Royalty calculation (indicative only)

The user stated an Amazon.com list price of **USD 2.99**, with **70% royalty**. KDP's published US delivery rate is **USD 0.15 per MB** for 70%-eligible orders ([official KDP pricing terms](https://kdp.amazon.com/en_US/help/topic/G200634500)).

If KDP assessed the above uploaded EPUB byte sizes as its delivery sizes, rough one-copy royalty would move from **~USD 1.66** to **~USD 1.80**, **~USD +0.15 per copy**. These are *not* verified KDP royalty values: conversion, rounding and the KDP-calculated file size can differ. Check the listing's actual delivery cost in KDP.

## Publication and coordination

No price, ad campaign, KDP page or published book changes were made. This GitHub branch contains the corrected Markdown manuscript and the optimization **script**, but **the optimized binary EPUB is not committed**. Make sure a future Claude Code run does not mistake the repository's old EPUB and charts for the finished October 10 edition.

## Author decision — 2026-10-10: hold publication

The author specifically decided **not** to upload this optimized October 10 EPUB to KDP now. Further manuscript revisions will be made first; the author will upload a consolidated **next revision** afterward. This optimized file is an **intermediate deliverable** and should not be mistaken for the release candidate. The next EPUB must incorporate the newest approved editorial changes, updated visual spoiler guides, and image optimization, followed by EPUBCheck and Kindle Previewer checks. Preserve the current cover and do not alter the live listing, USD 2.99 price, 70% royalty choice, or paused advertising without further user instruction.
