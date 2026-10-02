---
name: book-section-audit
description: Use before presenting or finalizing any reader-facing copy for this project's books (front matter, hooks, chapter openings, KDP descriptions, author bios), and whenever the user asks to review, scrutinize, or 精査 a draft. A self-review checklist so redundant, boring, or stale sections get caught by the reviewer, not only after the user asks "is this needed? is it interesting?"
---

# Book Section Audit (self-review before presenting)

Related skills: `book-opening-design` (how to choose and build a book's opening), `kdp-description-writing`, `kdp-listing-setup` (keywords, categories, price, Select), `author-persona-tyler-atsumori`, `humanize-writing-en`. This skill is the checklist; those hold the design guidance and worked examples.

Why this exists: on 2026-10-02 the user had to ask, section by section, "is this needed? is it interesting?" ("How to Read This Book", then "The Question") and both turned out to be cuttable. Other problems only surfaced on a later close read: Chapter 1 opened with the same "how many times did the prize go to him" framing the user had already rejected in the description; the published text said "the user's copy"; the description said "Volume Two is available now" after Vol.2 failed to save. Run this audit *before* showing a draft, and report its verdicts unprompted.

## Procedure

1. **Map the reader's path.** List every section in the order a browsing reader meets it, with a word count (footnotes included, since they sit inside the free Look Inside sample) and the running total before the first real chapter content. State this budget in the first line of the review.
2. **Per section, answer each question (then report only the verdict and the reason):**
   - *What new thing does the reader get here?* If nothing they haven't already got, cut or merge.
   - *Is it vivid, specific, and fun, or generic?* Test: could this paragraph be pasted into a different book unchanged? If yes, it's generic.
   - *Would a browsing reader keep reading or skim?* Boilerplate headings ("THE QUESTION THIS WHOLE BOOK IS TRYING TO ANSWER", "How to Read This Book") and filler transitions ("Let's get into it.") are skim points and read as AI-written.
   - *Is it duplicated elsewhere?* grep the hook, bio, intro sections, Chapter 1, and the KDP description for the same facts, phrases, and setup; keep the best occurrence.
   - *Template smell:* "isn't X, it's Y" constructions, scene-setting sentences before a list, a closing sentence that restates the hook.
3. **Human-voice pass.** Run the `humanize-writing-en` checklist on the text being reviewed (in this repo it was copied onto this branch from `festive-clarke-cnoct4`): rule-of-three verb/adjective chains, "It's easy to assume X. It wasn't.", "not X, it's Y" and "merely" contrasts, self-narrated significance ("in a detail it is hard to resist"), unhedged insider claims, closing bows, em dashes (the Murakami Vol.1 manuscript had 3.7 per 1,000 words), and the "actually/genuinely/really/truly" tic (32 hits in Vol.1). Also check the persona's specific, odd, human details are present and that the section *ends* on the best one.
4. **Consistency across surfaces.** Manuscript vs. KDP description vs. keywords vs. metadata notes. Check for stale claims ("available now", "coming soon", counts, prices, volume numbers) and for framing the user has already rejected anywhere else in the book.
5. **Leak and fact check.** grep the published text for internal words ("user", "session", "TODO", tool names). Any new factual claim goes through `verify-nonfiction-claims`; anything taken from a search summary rather than an opened source is flagged as unverified in the book's notes.
6. **Report verdicts first, unprompted:** keep / cut / merge / rewrite per section with a one-line reason, and a proposed replacement for anything rewritten. Don't make the user ask "is this needed?".
7. **Process rules still apply:** no EPUB build until the user asks; log decisions in `murakami-epub-rebuilt/series-notes.md` (or the book's own notes), not just in chat.

## Dated log

- **2026-10-02 — origin.** Cut from Murakami Vol.1: "How to Read This Book" (three points all duplicated elsewhere, ~140 words of sample) and "The Question" (duplicated the hook's last paragraph, stalled the flow, generic heading, 60-word question sentence). Kept its one strong line ("He built that sound himself, on purpose, years before any translator touched a page") by moving it to the hook. Also caught on close read: Ch.1 "Zero." opening, "the user's copy" leak, stale "Volume Two is available now". Miscounting lesson: the front matter was reported as ~350 words but was ~520 with footnotes.
- **2026-10-02 — human-voice pass added after the user asked "does the opening read as AI? is it human enough?"** Found in text written during this same session: a four-verb chain and a three-verb chain in the hook, "in a detail it is hard to resist" (self-narrated significance), an unhedged "He built that sound himself, on purpose", a CV-style triad plus "never reaches" absolute closing the bio, and in Ch.1 "That is what being loved looks like" + "It is easy to assume ... It wasn't." The humanize checklist should have been run before showing those drafts.
- **2026-10-02, Murakami Vol.3 audit.** Per-chapter word counts showed one chapter at 24% of the book with a 53-word average sentence and 290-word paragraphs, so it was cut about 25% and split with its strongest scene first. The hook (Drive My Car) and the Chapter 1 that followed (Tsukuru Tazaki, a dry background opener) did not connect, so the Drive My Car chapter became Chapter 1; cross-references ("Chapter N", glossary "See Chapter N", the Sources headings) were renumbered with a mapping script that skips "Volume Two, Chapter 3"-style references to other volumes. A hook and its own chapter repeated the same facts (only real things happen, the budget, the borrowed well); the chapter's copy was cut. Two closing chapters recapped the same theme and are to be merged. Checks used: section word counts and the share of the free sample, repeated key phrases, hook-versus-chapter overlap, longest paragraphs, leaks.
