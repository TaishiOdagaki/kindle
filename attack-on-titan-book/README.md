# Attack on Titan: The Price of Freedom — Manuscript

Finished manuscript for a ~23,700-word Kindle companion book of critical analysis on *Attack on Titan* (*Shingeki no Kyojin*), written under the pen name Jiro Naozane. Sixteen chapters plus front/back matter, built around a page-turning strategy agreed with the author before drafting:

1. **A central question**, posed in the intro ("did a horror-to-war-epic transformation earn its politically divisive ending?") and argued to a direct, first-person verdict in Chapter 15, rather than hedged into a survey of everyone else's opinions.
2. **Three intertwined axes**, unlike the single-question structure of the prior two books in this series: the story's genre transformation from horror to war epic, the real-world nationalism controversy surrounding its author, and the gap between the ending's authorial intent and its fandom reception.
3. **A dedicated Japanese-domestic-reception chapter** (Chapter 6), plus a chapter distinguishing the nationalism controversy from the ending controversy — two arguments that split along completely different fault lines (one domestic-vs-overseas, one that doesn't break along national lines at all).
4. **A three-tier spoiler system** (see the Spoiler Map in the back matter), reflecting a manga that's been finished since 2021 next to an anime that only finished in 2023.

## Files

- `manuscript.md` — full manuscript (~23,700 words, 16 chapters + front/back matter). Source of truth — edit this, then regenerate the EPUB.
- `cover/cover.jpg` — chosen cover (AI-generated breached-wall photographic scene + typography), author's own design. 1250×2000px (1.6:1), matches the *Chainsaw Man* and *Demon Slayer* books' cover dimensions and reuses the same series typography (bold condensed display face for the title, rounded geometric sans for subtitle/author/imprint) for series consistency.
- `Attack on Titan - The Price of Freedom.epub` — built interior file, ready to upload to KDP as the manuscript. Validated with `epubcheck` (0 errors, 0 warnings). This is a generated artifact — regenerate it any time `manuscript.md` changes (command below); don't hand-edit the `.epub` directly.
- `kdp-book-description.txt` — the KDP product page description (under KDP's 4,000-character hard limit, which counts HTML tags too), for the "Book Description" field, not the manuscript itself. Structured with `<h4>` section headings and `<ul>/<li>` bullet lists for scannability, plus `<b>`/`<i>` emphasis — all KDP-supported tags. Note: KDP's description field doesn't render HTML live while editing (you'll see the raw tags in the box) — it renders once saved, on the KDP preview or the live product page.

## Before Publishing

1. **Run the `verify-nonfiction-claims` audit pass again immediately before upload**, even though a full dedicated audit pass was already run on this manuscript. That pass found and fixed two real errors that had gone unnoticed while writing: a fabricated Rotten Tomatoes figure (the manuscript had claimed a "96 percent critical score" for the anime that didn't match actual RT data — corrected to the real season-by-season figures) and a wrong volume count (the manuscript said the manga ran "35 volumes" in two places; it actually concluded at Volume 34). Both are fixed in the current manuscript, but the lesson stands: re-verify time-sensitive claims (China's ban status, any pending sequels/adaptations, box office totals) immediately before upload, since they can shift between drafting and publication.
2. **Author bio.** The same "About the Author" note used in the *Chainsaw Man* and *Demon Slayer* books is reused verbatim here for series consistency. It intentionally avoids naming any specific real institution.
3. **Copyright posture.** No panels, extended dialogue, or character art are reproduced. The front-matter disclaimer names the relevant rights holders (Hajime Isayama, Kodansha, Wit Studio, MAPPA, Crunchyroll) as unaffiliated.
4. **No interior images.** Text-only manuscript, same as the prior two books. The cover is the exception.
5. **Cover is AI-generated — disclose it on KDP.** `cover/cover.jpg` was AI-generated. Amazon KDP's content-origin disclosure requirement covers AI-generated images the same as AI-generated text, regardless of how much the image was subsequently art-directed or edited — tick the appropriate box in the publishing form's content declaration when you upload it.
6. **AI-generated text disclosure.** Tick KDP's content-origin declaration for AI-generated manuscript text too — see the repo-root README's standing conventions.
7. **Sensitive content note specific to this book.** This manuscript discusses real, named living political figures (a U.S. Congressman's 2021 censure over a video using this franchise's imagery) and a real exiled political artist (Hong Kong's Kacey Wong). Both passages are sourced to multiple mainstream outlets and written carefully — see the manuscript's Chapter 7 and Chapter 8 — but are worth a final read-through given how reputationally sensitive this category of claim is.

## Converting for KDP

Regenerate the EPUB after any manuscript edit:

```
pandoc manuscript.md \
  -o "Attack on Titan - The Price of Freedom.epub" \
  --metadata title="Attack on Titan: The Price of Freedom" \
  --metadata author="Jiro Naozane" \
  --metadata publisher="Japanese Culture Press" \
  --metadata lang=en-US \
  --toc --toc-depth=2 \
  --split-level=2
```

Then validate before uploading (catches malformed markup pandoc would otherwise pass through silently):

```
java -jar /usr/share/java/epubcheck.jar "Attack on Titan - The Price of Freedom.epub"
```

## Ready to Upload — KDP Submission Checklist

1. **Manuscript file:** `Attack on Titan - The Price of Freedom.epub` — upload as the interior content file.
2. **Cover file:** `cover/cover.jpg` — upload separately in KDP's dedicated Cover step. Don't also embed it as a page inside the EPUB.
3. **AI content disclosure:** tick this for *both* the manuscript text and the cover image in KDP's content-origin declaration.
4. **Publisher field:** Japanese Culture Press.
5. **Author field:** Jiro Naozane.
6. Everything else below this checklist (categories, keywords, pricing, territories) is a normal KDP account/business decision, not something this repo tracks.

## Suggested KDP Metadata

- **Publisher / imprint:** Japanese Culture Press (this repo's label for the series — see the repo root README)
- **Categories:** ⚠️ Do not use the "Criticism & Literary Studies > Subjects & Themes > Comics & Graphic Novels" category — KDP rejected it for both *Chainsaw Man* and *Demon Slayer* on 2026-09-20 (email: "categories including Comics, but content is not manga or a graphic novel"). This book is prose criticism *about* a manga/anime, not a comic itself, so any category path with "Comics" or "Graphic Novels" in the breadcrumb is apparently unsafe, even a criticism-of-comics subcategory. Use a verified, non-Comics literary-criticism category instead (not yet identified — pending the live KDP category picker). The other two categories those books used (Pop Culture General; Movies > Genre > Anime) were not flagged and are likely still safe.
- **KDP's 7-keyword field (each ≤50 characters):**
  1. Shingeki no Kyojin explained
  2. AOT ending controversy analysis
  3. Eren Yeager Mikasa Levi Armin
  4. anime manga essay collection
  5. Hajime Isayama biography interviews
  6. Titans Eldia Marley lore guide
  7. otaku anime pop culture nonfiction

  Chosen deliberately to avoid repeating words already in the title/subtitle ("Attack on Titan," "Price of Freedom," "Critical Companion," "Japanese Researcher," "Fans Worldwide") — KDP's own guidance is that repeating those doesn't add search surface. These instead cover: the original Japanese title, the "AOT" fan abbreviation plus the ending controversy directly, character names, format/genre, the author's name, in-universe lore terms, and the general nonfiction/pop-culture-criticism category.
- **Content note:** discusses genocide, war, and real historical atrocity as depicted in the source material, plus real-world political controversy tied to the work's reception; no explicit content of its own.
