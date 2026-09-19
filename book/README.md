# The Japan They Never Told You — Manuscript

This folder contains the draft manuscript for a nonfiction Kindle title aimed at overseas anime/manga fans: cultural commentary, Japanese folklore, yakuza history, and industry trivia, written to explain the cultural context behind anime without reproducing any copyrighted characters, artwork, or story content.

## Files

- `manuscript.md` — full manuscript (~11,000 words, 11 chapters + front/back matter). Written in Markdown so it's easy to convert to EPUB/KDP formats.

## Before You Publish: Required Steps

1. **Insert your own photos.** Every `[IMAGE: ...]` bracket in the manuscript marks a suggested spot and a content idea for a photo. Replace each bracket with an actual image (Markdown syntax: `![caption](path/to/image.jpg)`), using only photos you took yourself or have clear rights to use. Do **not** use screenshots or fan art of *One Piece*, *Demon Slayer*, or any other copyrighted series — the manuscript deliberately avoids this, and adding it later would undermine that.
2. **Fact-check the numbers.** A handful of specific figures (yakuza membership counts, animator wage statistics, specific years for laws/ordinances) are included for context and should be verified against current primary sources (National Police Agency white papers, MHLW labor statistics, news reporting) before final publication — some may have shifted since this draft was written.
3. **Add your author bio and photo** in the "About This Book" section at the end.
4. **Legal review recommended.** Because this book discusses real organized crime, sex-industry regulation, and named copyrighted franchises (in a commentary-only capacity), a quick pass by someone familiar with KDP content guidelines and basic fair-use/trademark principles is worth doing before publishing, especially if you expand the manuscript further.

## Converting for KDP

Kindle Direct Publishing accepts EPUB or a properly formatted Word/HTML file. A common workflow:

```
pandoc manuscript.md -o manuscript.epub --metadata title="The Japan They Never Told You" --metadata author="Your Name"
```

(Requires [Pandoc](https://pandoc.org/) installed locally.) After inserting images and confirming the `![]()` paths, re-run the conversion — Pandoc will embed the images into the EPUB automatically.

## Suggested KDP Metadata

- **Publisher / imprint:** Japanese Culture Press (this repo's label for the series — see the repo root README)
- **Categories:** Nonfiction > Asia Travel, or Nonfiction > Popular Culture / Japanese Studies
- **Keywords to consider:** anime culture, Japan travel, yakuza history, otaku, Japanese folklore, manga industry
- **Content note:** the manuscript includes historical organized-crime content and brief, non-explicit adult-industry discussion (Chapter 8) — review KDP's content guidelines for the appropriate age/content rating before submission.
