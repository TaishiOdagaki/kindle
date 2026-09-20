# Chainsaw Man: The Devil in the Details — Manuscript

Draft manuscript for a ~14,000-word Kindle companion book of critical analysis on *Chainsaw Man*, written under the pen name Jiro Naozane. Fourteen chapters plus front/back matter, built around three design choices agreed with the author before drafting:

1. **Meaning over mechanism** in spoiler-heavy chapters — the ending is discussed directly, but framed around why it works rather than as a plain plot recap, so it holds value for readers who already know how the series ends.
2. **A Spoiler Map** (see the back matter) tracking which chapters are safe for anime-only viewers (Season 1 + the *Reze Arc* movie) versus which require having read the completed manga.
3. **A specific authorial voice** — critical, not purely promotional, written as a Japanese fan who followed the series in near-real time, with untranslated fan terminology (glossed in the back-matter glossary) and blunt opinions where the text calls for them (see Chapter 11, on Part 2's divisive pacing).

## Files

- `manuscript.md` — full manuscript (~14,000 words, 14 chapters + front/back matter). Source of truth — edit this, then regenerate the EPUB.
- `cover/cover.jpg` — chosen cover (AI-generated chainsaw product shot + typography), author's own design, selected over three typographic concepts also explored in this project's chat history. 1250×2000px (1.6:1), matches KDP's recommended cover ratio; above KDP's 1000px minimum on the short side.
- `Chainsaw Man - The Devil in the Details.epub` — built interior file, ready to upload to KDP as the manuscript. Validated with `epubcheck` (0 errors, 0 warnings). This is a generated artifact — regenerate it any time `manuscript.md` changes (command below); don't hand-edit the `.epub` directly.
- `kdp-book-description.txt` — the KDP product page description (~3,860 characters including markup, under KDP's 4,000-character hard limit which counts HTML tags too), for the "Book Description" field, not the manuscript itself. Structured with `<h4>` section headings and `<ul>/<li>` bullet lists for scannability, plus `<b>`/`<i>` emphasis — all KDP-supported tags. Note: KDP's description field doesn't render HTML live while editing (you'll see the raw tags in the box) — it renders once saved, on the KDP preview or the live product page.

## Before Publishing

1. **Fact-check before printing.** Plot and production details (chapter numbers, character fates, adaptation credits, release dates) were verified against current sources as of September 2026, but *Chainsaw Man* coverage online is dense and sometimes contradictory — spot-check anything load-bearing before final publication, especially Part 2/Academy Saga specifics.
2. **Author bio.** A short "About the Author" note for Jiro Naozane is already in the front matter. It intentionally avoids naming any specific real institution (see this project's chat history for why) — keep any further additions to non-verifiable general background, not specific real organizations or credentials.
3. **Copyright posture.** No panels, extended dialogue, or character art are reproduced. Quotation is limited to a couple of short, already-widely-quoted phrases (e.g., Pochita's final line) used for critical discussion. The front-matter disclaimer names the relevant rights holders (Tatsuki Fujimoto, Shueisha, MAPPA) as unaffiliated. Keep it that way in any further edits — this is a single-work deep dive, which carries more derivative-work risk than a multi-topic culture book, so avoid adding extended scene-by-scene retellings.
4. **No interior images.** Unlike the companion anime-culture book in this repo, the manuscript itself doesn't use `[IMAGE: ...]` placeholders — there's no clean source of non-infringing images for a single-series critical companion, so it's designed as a text-only read. The cover is the exception (see below).
5. **Cover is AI-generated — disclose it on KDP.** `cover/cover.jpg` was AI-generated. Amazon KDP's content-origin disclosure requirement covers AI-generated images the same as AI-generated text, regardless of how much the image was subsequently art-directed or edited — tick the appropriate box in the publishing form's content declaration when you upload it. This is separate from, and doesn't resolve, the manuscript-text disclosure already noted for the sibling book in this repo.

## Converting for KDP

Regenerate the EPUB after any manuscript edit:

```
pandoc manuscript.md \
  -o "Chainsaw Man - The Devil in the Details.epub" \
  --metadata title="Chainsaw Man: The Devil in the Details" \
  --metadata author="Jiro Naozane" \
  --metadata publisher="Japanese Culture Press" \
  --metadata lang=en-US \
  --toc --toc-depth=2 \
  --split-level=2
```

Then validate before uploading (catches malformed markup pandoc would otherwise pass through silently):

```
java -jar /usr/share/java/epubcheck.jar "Chainsaw Man - The Devil in the Details.epub"
```

## Ready to Upload — KDP Submission Checklist

1. **Manuscript file:** `Chainsaw Man - The Devil in the Details.epub` — upload as the interior content file.
2. **Cover file:** `cover/cover.jpg` — upload separately in KDP's dedicated Cover step. Don't also embed it as a page inside the EPUB; KDP renders the uploaded cover on its own, and a duplicated cover page is a common self-publishing mistake this avoids.
3. **AI content disclosure:** tick this for *both* the manuscript text and the cover image in KDP's content-origin declaration — see point 5 below.
4. **Publisher field:** Japanese Culture Press.
5. **Author field:** Jiro Naozane.
6. Everything else below this checklist (categories, keywords, pricing, territories) is a normal KDP account/business decision, not something this repo tracks.

## Suggested KDP Metadata

- **Publisher / imprint:** Japanese Culture Press (this repo's label for the series — see the repo root README)
- **Categories:** ⚠️ KDP rejected the "Criticism & Literary Studies > Subjects & Themes > Comics & Graphic Novels" category on 2026-09-20 (email: "categories including Comics, but content is not manga or a graphic novel") — this book is prose criticism *about* a manga, not a comic itself, and any category path with "Comics" or "Graphic Novels" in the breadcrumb is apparently not safe for that reason, even a criticism-of-comics subcategory. Needs a verified, non-Comics literary-criticism category as a replacement — check this against Demon Slayer's and Attack on Titan's READMEs, which had the identical problem. The other two categories (Pop Culture General; Movies > Genre > Anime) were not flagged.
- **KDP's 7-keyword field (each ≤50 characters):**
  1. manga finale ending explained
  2. Denji Makima Power Aki Reze
  3. Tatsuki Fujimoto biography interviews
  4. Part 2 fandom reception debate
  5. shonen manga nonfiction essay
  6. devil hunters Public Safety arc
  7. anime manga pop culture criticism

  Chosen to avoid repeating words already in the title/subtitle ("Chainsaw Man," "Devil in the Details," "Critical Companion," "Japanese Researcher," "Fans Worldwide") — see the `attack-on-titan-book/README.md` for the reasoning behind this approach. Covers: the "ending explained" search intent directly, a character-name cluster, the author's name, the Part 2 reception controversy as its own searchable topic, format/genre, in-universe setting terms, and the general nonfiction/pop-culture-criticism category. Replaces an earlier, unstructured keyword list — if this campaign's live Amazon Ads targeting still reflects the old list, check it against this one (see the `kdp-ads-strategy` skill).
- **Content note:** discusses character deaths and dark themes present in the source material; no explicit content of its own.
