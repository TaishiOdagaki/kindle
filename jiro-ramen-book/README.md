# Ramen Jiro: The Cult of Tokyo's Most Intimidating Bowl — Manuscript

Manuscript for a ~8,400-word Kindle nonfiction book about Ramen Jiro (ラーメン二郎) and the wider Jiro-kei (二郎系) ramen subculture, written under the pen name Jiro Naozane. This is the fourth book in the Japanese Culture Press series and the first outside anime/manga criticism — a departure into food culture, built around the same page-turning strategy as the prior three books:

1. **A central question**, posed up front ("is Ramen Jiro's intimidation a real barrier, or the whole point, dressed up as one?") and argued to a direct verdict in Chapter 11, rather than left open.
2. **Eleven chapters** covering the founding accident, the founder's decades of media silence, the physical anatomy of the bowl, the ordering ritual, the lineage taxonomy (chokkei/Jiro-kei/inspaia-kei), Jirolian fan culture, the health controversy, the (nonexistent) official overseas expansion versus independently-founded Jiro-style shops abroad, the business economics behind the ritual, and a real 2021 Japan Patent Office trademark dispute most casual fans have never heard of.
3. **A glossary and afterword**, the latter fulfilling a promise made in the "About the Author" note to address the coincidence between this pen name and the book's subject directly.

## Files

- `manuscript.md` — full manuscript (~8,400 words, 11 chapters + front/back matter). Source of truth — edit this, then regenerate the EPUB.
- `cover/` — empty; no cover has been chosen yet. See "Before Publishing" below.

## Before Publishing

1. **Cover art needed.** Unlike the prior three books, no cover exists yet for this title. This needs either a design brief handed to the author for their own cover work (matching the series' established look) or an AI-generated cover discussed and approved before use — either way, this is the one outstanding blocker before this book is upload-ready.
2. **Run the `verify-nonfiction-claims` audit pass again immediately before upload**, even though a full pass already ran during drafting. That pass caught and fixed two real errors: a fabricated reason for the shop's 1972 relocation (the manuscript originally invented a "Tachiaigawa river-channel redevelopment" story; the real cause was Meguro Ward sewer-line construction), and a mixed-up birthplace for founder Takumi Yamada (the manuscript originally said "Tsukishima," an adjacent but different neighborhood from his actual birthplace, Tsukuda). Both are fixed in the current manuscript. Re-verify anything time-sensitive before upload regardless — this book explicitly flags branch counts (currently ~40-45, still growing) and the founder's age/health status as things that can shift between drafting and publication; see the front-matter disclaimer and Chapter 10.
3. **Author bio.** The same "About the Author" framing used in the prior three books is adapted here for "Japanese pop culture — anime, manga, and now food culture," with a parenthetical flagging the Jiro Naozane / Ramen Jiro name coincidence and pointing to the Afterword, where it's addressed directly and honestly as coincidence, not branding.
4. **Copyright posture.** No recipes, proprietary techniques, or trademarked signage are reproduced. The front-matter disclaimer names Ramen Jiro, founder Takumi Yamada, and all independently-run branches and Jiro-style restaurants discussed as unaffiliated with this book.
5. **No interior images.** Text-only manuscript, same as the prior three books.
6. **AI-generated text disclosure.** Tick KDP's content-origin declaration for AI-generated manuscript text — see the repo-root README's standing conventions. Once a cover exists, disclose that too if it's AI-generated.
7. **Sensitive content note specific to this book.** This manuscript discusses a real, named, living private individual (founder Takumi Yamada) in some biographical depth, including his age and a documentary framed around his own mortality (its title translates to roughly "testament"/"last words"). It also names a real practicing attorney (Masashi Kaneko) and describes a real, specific 2021 Japan Patent Office trademark ruling. All of these passages are sourced to multiple outlets and written carefully — see Chapters 2 and 10 — but are worth a final read-through given how reputation-sensitive claims about named living people and real legal proceedings are.

## Converting for KDP

Regenerate the EPUB after any manuscript edit:

```
pandoc manuscript.md \
  -o "Ramen Jiro - The Cult of Tokyo's Most Intimidating Bowl.epub" \
  --metadata title="Ramen Jiro: The Cult of Tokyo's Most Intimidating Bowl" \
  --metadata author="Jiro Naozane" \
  --metadata publisher="Japanese Culture Press" \
  --metadata lang=en-US \
  --toc --toc-depth=2 \
  --split-level=2
```

Then validate before uploading:

```
java -jar /usr/share/java/epubcheck.jar "Ramen Jiro - The Cult of Tokyo's Most Intimidating Bowl.epub"
```

## Ready to Upload — KDP Submission Checklist

1. **Manuscript file:** the built EPUB — upload as the interior content file. Not yet built; see "Converting for KDP" above.
2. **Cover file:** not yet chosen — see "Before Publishing" above. Blocks upload until resolved.
3. **AI content disclosure:** tick this for the manuscript text, and for the cover image too once one exists and if it's AI-generated.
4. **Publisher field:** Japanese Culture Press.
5. **Author field:** Jiro Naozane.
6. Everything else below this checklist (categories, keywords, pricing, territories) is a normal KDP account/business decision, not something this repo tracks.

## Suggested KDP Metadata

- **Publisher / imprint:** Japanese Culture Press (this repo's label for the series — see the repo root README).
- **Categories:** this book isn't about comics/manga, so the Comics-category trap that hit the first three books doesn't apply here. Reasonable candidates, pending the live KDP category picker: Cooking, Food & Wine > Regional & International > Asian > Japanese; Travel > Asia > Japan; Nonfiction > Social Science > Customs & Traditions / Popular Culture. Not yet verified against the live picker — check before finalizing, the way the other three books' categories had to be corrected after initial rejection.
- **KDP's 7-keyword field (each ≤50 characters):**
  1. Ramen Jiro explained
  2. Jiro style ramen culture guide
  3. ramen founder biography essays
  4. how to order ramen Jiro
  5. Japanese food subculture nonfiction
  6. ramen otaku pop culture book
  7. Tokyo food culture essays

  Keyword #3 deliberately avoids naming Takumi Yamada directly, following this series' established rule against putting a real living person's name in the KDP keyword field — same logic as avoiding "Hajime Isayama" or "Koyoharu Gotouge" in the manga books' keyword lists. "Ramen Jiro" itself is used freely, the same way the manga books use their own subject's title, since it's the book's actual subject rather than an unrelated trademark.

  **⚠️ This list is for the KDP listing-keyword field specifically — see `kdp-ads-strategy`'s dated log before reusing any of it for Amazon Ads manual keyword targeting.** The two fields work differently; an ad keyword only serves impressions when it matches something a shopper actually types.
- **Content note:** discusses a real living person's age and a documentary built around his own mortality, real trademark litigation, and food-related health risks (obesity, diabetes risk) in a nonfiction, sourced context; no explicit content of its own.
