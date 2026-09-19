# Chainsaw Man: The Devil in the Details — Manuscript

Draft manuscript for a ~14,000-word Kindle companion book of critical analysis on *Chainsaw Man*, written under the pen name Jiro Naozane. Fourteen chapters plus front/back matter, built around three design choices agreed with the author before drafting:

1. **Meaning over mechanism** in spoiler-heavy chapters — the ending is discussed directly, but framed around why it works rather than as a plain plot recap, so it holds value for readers who already know how the series ends.
2. **A Spoiler Map** (see the back matter) tracking which chapters are safe for anime-only viewers (Season 1 + the *Reze Arc* movie) versus which require having read the completed manga.
3. **A specific authorial voice** — critical, not purely promotional, written as a Japanese fan who followed the series in near-real time, with untranslated fan terminology (glossed in the back-matter glossary) and blunt opinions where the text calls for them (see Chapter 11, on Part 2's divisive pacing).

## Files

- `manuscript.md` — full manuscript (~14,000 words, 14 chapters + front/back matter).

## Before Publishing

1. **Fact-check before printing.** Plot and production details (chapter numbers, character fates, adaptation credits, release dates) were verified against current sources as of September 2026, but *Chainsaw Man* coverage online is dense and sometimes contradictory — spot-check anything load-bearing before final publication, especially Part 2/Academy Saga specifics.
2. **Author bio.** A short "About the Author" note for Jiro Naozane is already in the front matter. It intentionally avoids naming any specific real institution (see this project's chat history for why) — keep any further additions to non-verifiable general background, not specific real organizations or credentials.
3. **Copyright posture.** No panels, extended dialogue, or character art are reproduced. Quotation is limited to a couple of short, already-widely-quoted phrases (e.g., Pochita's final line) used for critical discussion. The front-matter disclaimer names the relevant rights holders (Tatsuki Fujimoto, Shueisha, MAPPA) as unaffiliated. Keep it that way in any further edits — this is a single-work deep dive, which carries more derivative-work risk than a multi-topic culture book, so avoid adding extended scene-by-scene retellings.
4. **No images.** Unlike the companion anime-culture book in this repo, this manuscript doesn't use `[IMAGE: ...]` placeholders — there's no clean source of non-infringing images for a single-series critical companion, so it's designed as a text-only read.

## Converting for KDP

Same workflow as the other book in this repo:

```
pandoc manuscript.md -o manuscript.epub --metadata title="Chainsaw Man: The Devil in the Details" --metadata author="Jiro Naozane"
```

## Suggested KDP Metadata

- **Categories:** Nonfiction > Performing Arts > Comics & Graphic Novels, or Literary Criticism
- **Keywords to consider:** Chainsaw Man analysis, manga criticism, Tatsuki Fujimoto, shonen manga essay, anime companion book
- **Content note:** discusses character deaths and dark themes present in the source material; no explicit content of its own.
