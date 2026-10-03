# Chainsaw Man: The Devil in the Details — Manuscript

Draft manuscript for a ~14,000-word Kindle companion book of critical analysis on *Chainsaw Man*, written under the pen name Jiro Naozane. Fourteen chapters plus front/back matter, built around three design choices agreed with the author before drafting:

1. **Meaning over mechanism** in spoiler-heavy chapters — the ending is discussed directly, but framed around why it works rather than as a plain plot recap, so it holds value for readers who already know how the series ends.
2. **A Spoiler Map** (see the back matter) tracking which chapters are safe for anime-only viewers (Season 1 + the *Reze Arc* movie) versus which require having read the completed manga.
3. **A specific authorial voice** — critical, not purely promotional, written as a Japanese fan who followed the series in near-real time, with untranslated fan terminology (glossed in the back-matter glossary) and blunt opinions where the text calls for them (see Chapter 11, on Part 2's divisive pacing).

## Status (2026-10-03)

**Re-uploaded as a 2nd edition, live on KDP** — the 2026-09-28 interior redesign (chapter-opener images, original charts, front-matter "WHAT'S INSIDE" roadmap; see "Before Publishing" point 4 below) is now the live listing, per the user's confirmation. This is this project's one deliberate, concentrated bet right now: the user has chosen to focus marketing/ad effort on this title alone going forward, rather than spreading it across the series — *Demon Slayer* and *Attack on Titan* are intentionally being left as-is (paused ad campaigns, pre-redesign listing content, no further investment for now). Don't treat those two books' stale state as an oversight if it comes up again; it's a deliberate resource-allocation choice. See `kdp-ads-strategy`'s dated log for the reasoning that led here (the 2nd edition exists specifically to test whether the reviews/trust-driven conversion problem improves once a better-looking listing is actually live, which hadn't been tested as of the 09-28 entries).

## Files

- `manuscript.md` — full manuscript (~14,000 words, 14 chapters + front/back matter). Source of truth — edit this, then regenerate the EPUB.
- `cover/cover.jpg` — chosen cover (AI-generated chainsaw product shot + typography), author's own design, selected over three typographic concepts also explored in this project's chat history. 1250×2000px (1.6:1), matches KDP's recommended cover ratio; above KDP's 1000px minimum on the short side.
- `Chainsaw Man - The Devil in the Details.epub` — built interior file, ready to upload to KDP as the manuscript. Validated with `epubcheck` (0 errors, 0 warnings). This is a generated artifact — regenerate it any time `manuscript.md` changes (command below); don't hand-edit the `.epub` directly.
- `kdp-book-description.txt` — the KDP product page description (~3,860 characters including markup, under KDP's 4,000-character hard limit which counts HTML tags too), for the "Book Description" field, not the manuscript itself. Structured with `<h4>` section headings and `<ul>/<li>` bullet lists for scannability, plus `<b>`/`<i>` emphasis — all KDP-supported tags. Note: KDP's description field doesn't render HTML live while editing (you'll see the raw tags in the box) — it renders once saved, on the KDP preview or the live product page.

## Before Publishing

1. **Fact-check before printing.** Plot and production details (chapter numbers, character fates, adaptation credits, release dates) were verified against current sources as of September 2026, but *Chainsaw Man* coverage online is dense and sometimes contradictory — spot-check anything load-bearing before final publication, especially Part 2/Academy Saga specifics.
2. **Author bio.** A short "About the Author" note for Jiro Naozane is already in the front matter. It intentionally avoids naming any specific real institution (see this project's chat history for why) — keep any further additions to non-verifiable general background, not specific real organizations or credentials.
3. **Copyright posture.** No panels, extended dialogue, or character art are reproduced. Quotation is limited to a couple of short, already-widely-quoted phrases (e.g., Pochita's final line) used for critical discussion. The front-matter disclaimer names the relevant rights holders (Tatsuki Fujimoto, Shueisha, MAPPA) as unaffiliated. Keep it that way in any further edits — this is a single-work deep dive, which carries more derivative-work risk than a multi-topic culture book, so avoid adding extended scene-by-scene retellings.
4. **Interior images added 2026-09-28.** `images/chapter-openers/` holds one opener per Intro/chapter (title text baked directly into a grayscale crop of the cover's own chainsaw photo, generated with Pillow — see `images/chapter-openers/` source script history). `images/charts/` holds 7 original data visualizations (spoiler map, glossary, publication timeline, and three chapters' own arguments turned into diagrams). None reproduce copyrighted artwork — the opener photos are the same real-world product photograph used on the cover, not manga/anime art. Text is baked into every image rather than CSS-overlaid, since Kindle's reflowable format doesn't reliably support precisely positioned text-over-image layering across devices.
5. **Cover is AI-generated — disclose it on KDP.** `cover/cover.jpg` was AI-generated. Amazon KDP's content-origin disclosure requirement covers AI-generated images the same as AI-generated text, regardless of how much the image was subsequently art-directed or edited — tick the appropriate box in the publishing form's content declaration when you upload it. This is separate from, and doesn't resolve, the manuscript-text disclosure already noted for the sibling book in this repo. **The chapter-opener images in `images/chapter-openers/` are grayscale crops of this same AI-generated cover photo**, so the same KDP disclosure covers them too — no separate declaration needed, but don't treat them as a "real photograph" source if this ever comes up.

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
- **Categories:** ✅ **Resolved 2026-09-28.** KDP initially rejected "Criticism & Literary Studies > Subjects & Themes > Comics & Graphic Novels" on 2026-09-20 (email: "categories including Comics, but content is not manga or a graphic novel"), but the user disputed rather than switching categories, and after a few rounds of correction emails KDP settled on keeping all three original categories — confirmed live on the published listing on 2026-09-28: `Kindle本 › 小説・文芸 › 評論・文学研究 › 主題・テーマ › コミック・グラフィックノベル`, `Kindle本 › エンターテイメント › ポップカルチャー › ポップカルチャー一般`, `Kindle本 › エンターテイメント › 映画 › ジャンル › アニメ化`. No change needed — this is the final, stable combination.
- **KDP's 7-keyword field (each ≤50 characters):**
  1. manga finale ending explained
  2. Denji Makima Power Aki Reze
  3. manga creator biography essays
  4. Part 2 fandom reception debate
  5. shonen manga nonfiction essay
  6. devil hunters Public Safety arc
  7. anime manga pop culture criticism

  Chosen to avoid repeating words already in the title/subtitle ("Chainsaw Man," "Devil in the Details," "Critical Companion," "Japanese Researcher," "Fans Worldwide") — see the `attack-on-titan-book/README.md` for the reasoning behind this approach. Covers: the "ending explained" search intent directly, a character-name cluster, format/genre, the Part 2 reception controversy as its own searchable topic, in-universe setting terms, and the general nonfiction/pop-culture-criticism category. Replaces an earlier, unstructured keyword list — if this campaign's live Amazon Ads targeting still reflects the old list, check it against this one (see the `kdp-ads-strategy` skill). ⚠️ Keyword #3 was originally "Tatsuki Fujimoto biography interviews" — changed to avoid the real creator's name after KDP rejected Demon Slayer's keyword list on 2026-09-20 for including the real original creator's name and a separate trademarked movie title. Never put a real living creator's name in this field, even in a biography/interview framing.

  **⚠️ 2026-09-28 — found the live KDP listing's keyword field doesn't actually match this list.** The account's current live values were: `manga finale ending explained`, `pop fandom Japan`, `Japanese anime manga pop otaku`, `devil hunters Public Safety arc`, `Denji Makima Power Aki Reze`, `shonen manga nonfiction essay`, `animation creator biography essays`. None of these violate the creator-name/trademarked-title rule, but three of them (`pop fandom Japan`, `Japanese anime manga pop otaku`, `animation creator biography essays`) are generic filler that don't target a specific search intent the way the documented list above does — and "animation creator" is also the wrong medium word for a manga-criticism book. **Re-confirmed the list above (all 7, unchanged) as the one to actually paste into the live field** — it's already compliant with the 2026-09-20 lesson and more search-intent-targeted than what's currently live. Not yet re-applied to the live listing as of this note; do that via KDP's "Edit eBook Content" → keywords field the next time the listing is touched.
- **Content note:** discusses character deaths and dark themes present in the source material; no explicit content of its own.
