---
name: book-section-audit
description: Use before presenting or finalizing any reader-facing copy for this project's books (front matter, hooks, chapter openings, KDP descriptions, author bios), and whenever the user asks to review, scrutinize, or 精査 a draft. A self-review checklist so redundant, boring, or stale sections get caught by the reviewer, not only after the user asks "is this needed? is it interesting?"
---

# Book Section Audit (self-review before presenting)

Why this exists: on 2026-10-02 the user had to ask, section by section, "is this needed? is it interesting?" ("How to Read This Book", then "The Question") and both turned out to be cuttable. Other problems only surfaced on a later close read: Chapter 1 opened with the same "how many times did the prize go to him" framing the user had already rejected in the description; the published text said "the user's copy"; the description said "Volume Two is available now" after Vol.2 failed to save. Run this audit *before* showing a draft, and report its verdicts unprompted.

## Procedure

1. **Map the reader's path.** List every section in the order a browsing reader meets it, with a word count (footnotes included, since they sit inside the free Look Inside sample) and the running total before the first real chapter content. State this budget in the first line of the review.
2. **Per section, answer each question (then report only the verdict and the reason):**
   - *What new thing does the reader get here?* If nothing they haven't already got, cut or merge.
   - *Is it vivid, specific, and fun, or generic?* Test: could this paragraph be pasted into a different book unchanged? If yes, it's generic.
   - *Would a browsing reader keep reading or skim?* Boilerplate headings ("THE QUESTION THIS WHOLE BOOK IS TRYING TO ANSWER", "How to Read This Book") and filler transitions ("Let's get into it.") are skim points and read as AI-written.
   - *Is it duplicated elsewhere?* grep the hook, bio, intro sections, Chapter 1, and the KDP description for the same facts, phrases, and setup; keep the best occurrence.
   - *Template smell:* "isn't X, it's Y" constructions, scene-setting sentences before a list, a closing sentence that restates the hook.
3. **Consistency across surfaces.** Manuscript vs. KDP description vs. keywords vs. metadata notes. Check for stale claims ("available now", "coming soon", counts, prices, volume numbers) and for framing the user has already rejected anywhere else in the book.
4. **Leak and fact check.** grep the published text for internal words ("user", "session", "TODO", tool names). Any new factual claim goes through `verify-nonfiction-claims`; anything taken from a search summary rather than an opened source is flagged as unverified in the book's notes.
5. **Report verdicts first, unprompted:** keep / cut / merge / rewrite per section with a one-line reason, and a proposed replacement for anything rewritten. Don't make the user ask "is this needed?".
6. **Process rules still apply:** no EPUB build until the user asks; log decisions in `murakami-epub-rebuilt/series-notes.md` (or the book's own notes), not just in chat.

## Dated log

- **2026-10-02 — origin.** Cut from Murakami Vol.1: "How to Read This Book" (three points all duplicated elsewhere, ~140 words of sample) and "The Question" (duplicated the hook's last paragraph, stalled the flow, generic heading, 60-word question sentence). Kept its one strong line ("He built that sound himself, on purpose, years before any translator touched a page") by moving it to the hook. Also caught on close read: Ch.1 "Zero." opening, "the user's copy" leak, stale "Volume Two is available now". Miscounting lesson: the front matter was reported as ~350 words but was ~520 with footnotes.
