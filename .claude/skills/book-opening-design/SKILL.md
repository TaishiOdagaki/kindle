---
name: book-opening-design
description: Use when writing, rewriting, or reviewing the opening of a nonfiction Kindle book for this project (front matter, the first hook, Chapter 1's first paragraphs), or deciding which front-matter sections to keep or cut. Captures what was learned on Murakami Vol.1 (2026-10-02) about choosing the single most fun, readable, well-sourced episode as the hook, cutting everything that does not earn its place in the free Look Inside sample, and verifying every fact before it goes in.
---

# Designing a Book's Opening

The opening is the part a browsing reader sees for free (Amazon's Look Inside / sample, default about 10%, adjustable in KDP). On a 9,400-word book that is roughly 940 words. Every sentence before the real content spends that budget, so the opening has one job: make a stranger want to keep reading, and buy.

## Principles (each one was learned the hard way on Murakami Vol.1)

1. **Count the budget honestly.** List every section before Chapter 1 with its word count, footnotes included, and the running total. (The front matter was reported as ~350 words once; it was ~520 with footnotes.)
2. **Standing order for Vol.1-style books: unheaded hook, then a short About the Author, then Chapter 1.** No "How to Read This Book", no "The Question This Whole Book Is Trying To Answer", no "Let's get into it." All three were cut because they repeated what the hook and Chapter 1 already say, used generic template headings that read as AI, and pushed the real content further from the reader. (The anime books kept a "How to Read" only because they needed spoiler-tag definitions. Ask whether a section has a function like that before keeping it.)
3. **The hook is the one most fun, most visual, most readable episode in the book.** For Murakami Vol.1 it was the afternoon at Jingū Stadium: lying on the outfield grass with a cold beer, a Texan named Dave Hilton hitting a double, the thought "I'll try writing a novel," a two-thousand-yen Sailor pen bought that day, a Yakult fan saying a chemical reaction in the heart is no surprise. Why it works: a picture in the first sentence; ordinary, human-scale details; the humor comes from the facts, not from the narrator telling you it is funny; an international reader can picture baseball; a long sentence followed by short ones.
4. **End the hook by tying to the book's thesis in one flat, hedged sentence.** "By Murakami's own account, he built that sound himself, on purpose, before any translator touched a page." Do not end on a summary of the book ("This is the story of...") or an aphorism.
5. **Lead Chapter 1 with what people love, not what failed.** The first Chapter 1 opened with "Zero. That's how many times the prize went to him." That was both negative and logically odd (the Akutagawa Prize can go to a writer only once, so "how many times" is a meaningless count). It now opens on the fans: about 200 "Harukists" at a Tokyo shrine with party poppers on the night of the 2017 Nobel announcement, the bookstore display swapped for the winner's books, and the running joke that his Nobel miss is an autumn seasonal word. Then it turns to the jury.
6. **Every fact in a hook needs a source you have actually opened or been given.** Web-search summaries are leads, not sources. The first Nobel-night draft came from search summaries and was wrong in two details ("polite applause" and "more than thirty titles"); the BBC News Japan article of 2017-10-06 (text pasted by the user) showed that the crowd set off the party poppers for the winner anyway and that the display was "about thirty." Put the source in a footnote and in the Sources section. A book that promises "checked against primary sources" cannot carry an unverified anecdote.
7. **Do not state the unverified as fact.** Hedge with the person's own account ("by Murakami's own account", "Murakami has written").
8. **Translate quoted foreign-language passages.** Japanese jury remarks sat untranslated in footnotes; add an English rendering after each original.
9. **Scrub internal words from published text.** "The user's copy" had reached two footnotes; grep for it before every build.
10. **Process rules:** manuscript edits are free; do not rebuild or send an EPUB until the user explicitly asks; after a build, run epubcheck and grep the built EPUB for the strings you changed and the strings you removed.

## Procedure for an opening

1. Pick candidate episodes (3 to 5) from the book and its sources. Choose by: visual, funny or surprising, easy for the widest English-reading audience, and verifiable.
2. Draft the hook; run `humanize-writing-en` (no verb triads, no self-narrated significance, no em dashes, no "It's easy to assume X. It wasn't.").
3. Run `book-section-audit`: purpose, duplication, template smell, word count.
4. Confirm each fact against an opened source; add footnote and Sources entry.
5. Put the author's human detail (see `author-persona-tyler-atsumori`) in a short bio that ends on its best line.
6. Make the KDP description's first lines match the opening scene (`kdp-description-writing`).

## Dated log

- **2026-10-02, Murakami Vol.1 (published to KDP that day, enrolled in KDP Select; reader response not yet known).** Sequence: original hook was a 3-sentence Jingū scene ending in a summary; rewritten into the full humorous scene using the Tokyo Shimbun article of 2024-05-10; "Dave Hilton" confirmed as a Texan (user), added to tie to the jury's "too American" complaint; "How to Read" removed; "The Question" removed with its punchline moved into the hook; Ch.1 opening replaced (Nobel-night fans, BBC-sourced); humanize pass removed verb chains, "in a detail it is hard to resist," and the "That is what being loved looks like" aphorism. Outcome (does the new opening raise conversion): not yet known. Revisit after the Nobel announcement week.
- **2026-10-02, Murakami Vol.3.** The chosen hook (Hamaguchi and *Drive My Car*) was followed by a Chapter 1 on a different book, which dropped the energy exactly where the free sample ends (the sample is about 10%, roughly 830 words of 8,300). Fix: reorder so Chapter 1 continues the hook, and cut from that chapter anything the hook already said. When chapters are thematic rather than chronological, reordering costs only cross-reference updates.
