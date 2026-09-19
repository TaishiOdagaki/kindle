# Demon Slayer: Total Concentration — Manuscript

Draft manuscript for a ~14,000-word Kindle companion book of critical analysis on *Demon Slayer: Kimetsu no Yaiba*, written under the pen name Jiro Naozane. Fourteen chapters plus front/back matter, built around a page-turning strategy agreed with the author before drafting:

1. **A central mystery question**, posed in the intro ("why did this specific film break every record") and answered piecemeal across chapters, paid off directly in Chapter 13.
2. **Dramatic irony used deliberately** — the manga has been finished and public since 2020, but most of the movie-trilogy audience doesn't know the ending yet. The book names that gap in Chapter 1 and uses it honestly rather than dangling it cruelly.
3. **A three-tier spoiler system** (see the Spoiler Map in the back matter): `[Manga-known]`, `[Anime/Movie-current]`, and `[Beyond Part 1]` — reflecting a finished manga next to a movie trilogy that's only one-third adapted.
4. **Hook-style chapter titles and chapter-ending forward hooks**, with deliberately varied chapter length — short, punchy chapters (1, 6) alongside longer deep-dives (7, 14) rather than uniform pacing.

## Files

- `manuscript.md` — full manuscript (~14,000 words, 14 chapters + front/back matter). Source of truth — edit this, then regenerate the EPUB.
- `Demon Slayer - Total Concentration.epub` — built interior file, ready to upload to KDP as the manuscript. Validated with `epubcheck` (0 errors, 0 warnings). This is a generated artifact — regenerate it any time `manuscript.md` changes (command below); don't hand-edit the `.epub` directly.
- `kdp-book-description.txt` — the KDP product page description (under KDP's 4,000-character hard limit, which counts HTML tags too), for the "Book Description" field, not the manuscript itself. Structured with `<h4>` section headings and `<ul>/<li>` bullet lists for scannability, plus `<b>`/`<i>` emphasis — all KDP-supported tags. Note: KDP's description field doesn't render HTML live while editing (you'll see the raw tags in the box) — it renders once saved, on the KDP preview or the live product page.
- No cover file yet — see "Before Publishing" below.

## Before Publishing

1. **Cover art not yet chosen.** Unlike the *Chainsaw Man* book in this repo, no cover exists yet for this title. Follow the same process: either the author supplies an AI-generated cover image directly, or concepts get explored via this project's design tooling first. Whichever path, disclose AI origin on KDP per point 4 below.
2. **Run the `verify-nonfiction-claims` audit pass again before final publish**, even though most claims in this manuscript were searched and verified at the point they were written (director, composers, voice cast, box office figures by market, Japan Academy Prize/Oscar submission history, manga sales figures, Taisho-era history including the Haitōrei Edict, oni folklore, Kagura/Amaterasu mythology, tamahagane swordsmithing, Weekly Shonen Jump's survey system, anime industry revenue figures, TV season air dates, and the stage play/Kimetsu Academy spin-offs were all confirmed via search during drafting, current as of September 2026). Time-sensitive claims — release dates for Parts 2 and 3, box office totals still climbing, any pending awards — should be re-checked immediately before publication since they can shift between drafting and upload.
3. **Author bio.** The same "About the Author" note used in the *Chainsaw Man* book is reused verbatim here for consistency across the series. It intentionally avoids naming any specific real institution — keep any further additions to non-verifiable general background, not specific real organizations or credentials.
4. **Copyright posture.** No panels, extended dialogue, or character art are reproduced. The front-matter disclaimer names the relevant rights holders (Koyoharu Gotouge, Shueisha, Aniplex, ufotable, Crunchyroll) as unaffiliated. This is a single-franchise deep dive, so avoid adding extended scene-by-scene retellings in any further edits.
5. **No interior images.** Text-only manuscript, same as the *Chainsaw Man* book. The cover, once chosen, is the exception.
6. **AI-generated text disclosure.** Tick KDP's content-origin declaration for AI-generated manuscript text, and separately for the cover image once one is chosen and if it's AI-generated — see the repo-root README's standing conventions.

## Converting for KDP

Regenerate the EPUB after any manuscript edit:

```
pandoc manuscript.md \
  -o "Demon Slayer - Total Concentration.epub" \
  --metadata title="Demon Slayer: Total Concentration" \
  --metadata author="Jiro Naozane" \
  --metadata publisher="Japanese Culture Press" \
  --metadata lang=en-US \
  --toc --toc-depth=2 \
  --split-level=2
```

Then validate before uploading (catches malformed markup pandoc would otherwise pass through silently):

```
java -jar /usr/share/java/epubcheck.jar "Demon Slayer - Total Concentration.epub"
```

## Ready to Upload — KDP Submission Checklist

1. **Manuscript file:** `Demon Slayer - Total Concentration.epub` — upload as the interior content file.
2. **Cover file:** not yet created — see "Before Publishing" above. Upload separately in KDP's dedicated Cover step once ready; don't also embed it as a page inside the EPUB.
3. **AI content disclosure:** tick this for the manuscript text in KDP's content-origin declaration, and for the cover image too once it exists, if AI-generated.
4. **Publisher field:** Japanese Culture Press.
5. **Author field:** Jiro Naozane.
6. Everything else below this checklist (categories, keywords, pricing, territories) is a normal KDP account/business decision, not something this repo tracks.

## Suggested KDP Metadata

- **Publisher / imprint:** Japanese Culture Press (this repo's label for the series — see the repo root README)
- **Categories:** Nonfiction > Performing Arts > Comics & Graphic Novels, or Literary Criticism
- **Keywords to consider:** Demon Slayer analysis, Kimetsu no Yaiba, manga criticism, Koyoharu Gotouge, anime companion book, Infinity Castle
- **Content note:** discusses character deaths and dark themes present in the source material; no explicit content of its own.
