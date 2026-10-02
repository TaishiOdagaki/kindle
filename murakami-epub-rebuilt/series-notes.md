# Murakami trilogy — series-wide notes (pen name: Tyler Atsumori, imprint: Japanese Culture Press)

Reusable decisions for Vol.1, Vol.2, Vol.3. Update this file when a decision is made; chat history does not survive between sessions.

## Author persona (user-provided, 2026-10-02)

Established background (already in each volume's "About the Author"): born and raised in Kyoto to an American mother and a
Japanese father; studied modern and contemporary Japanese literature at a university in the Kansai region; research focus is how
Japanese novelists are read and argued about at home versus how they are received in translation.

**Signature detail (the "real person" specific to use in every volume's bio), as given by the user, in Japanese:**

> 彼は毎朝のジョギング中に村上春樹の作品をオーディブルで繰り返し聴き続けることで、彼の日本語のリズムやシグネチャーを日々学んでいる。
> ときにジョギングよりもリスニングに集中してしまい、新調した自慢のアシックスのジョギングシューズを水たまりに浸してしまうこともある。

Meaning: every morning, during his run, he listens to Murakami's works on Audible over and over, learning Murakami's Japanese
rhythm and "signature" day by day. Sometimes he concentrates on the listening more than the running and has dunked his
brand-new, much-loved Asics running shoes in a puddle.

Why it works (from `kdp-conversion-design`: a specific, slightly odd, behavioral detail reads as a real person; a generic
"passionate about Japanese literature" line reads as AI-written). It also rhymes with the Vol.1 opening, since Murakami's own
running essay is the source of the Jingū Stadium scene.

Rules for reuse:
- Keep this one running joke consistent across volumes; do not invent new anecdotes about the author without the user supplying them.
- Keep the author's pronoun as the user wrote it ("he").
- Keep it to ~2 sentences inside the bio; the bio stays short (front matter eats the free Look Inside sample).

### Proposed bio wording (English), NOT yet applied to any manuscript — awaiting user's go-ahead

Vol.1:
> Tyler Atsumori was born and raised in Kyoto to an American mother and a Japanese father, and studied modern and contemporary Japanese literature at a university in the Kansai region. Every morning he goes for a run with Murakami's novels playing in his ears, in Japanese, on audiobook, listening again and again for the rhythm of the sentences. Sometimes he listens harder than he runs, and has put a brand-new, much-loved pair of Asics straight into a puddle. His research draws on Japanese-language sources most English-language criticism never reaches: literary-magazine criticism, prize-jury commentary, and Murakami's own essays.

Vol.2 / Vol.3: same two running-and-puddle sentences; keep the closing sentence about sources specific to that volume
(Vol.2: historical scholarship on the events Murakami's fiction engages with; Vol.3: recent criticism and the debate over the Nanjing passage).

## Other series decisions

- Front matter order (Vol.1, as of 2026-10-02): unheaded hook (Jingū Stadium scene, from *Tokyo Shimbun* 2024-05-10) -> About the Author (with the running/Asics detail) -> chapters. ("The Question" section also removed 2026-10-02: duplicated the hook's last paragraph, stalled the flow, ~130 words of sample. Its one strong line, "He built that sound himself, on purpose, years before any translator touched a page," now closes the hook.) "How to Read This Book" was removed: its three points (audience, premise, "not a ranked list") were duplicated by the hook, the Question, and Ch.1, and it cost ~140 words of the free sample. Consider the same cut for Vol.2/Vol.3.
- Vol.1 Ch.1 now opens with the 2017 Nobel-night anecdote (about 200 "Harukists" with party poppers at a Tokyo shrine, Ishiguro wins, Kinokuniya swaps its 30+ title Murakami display), then pivots to the two Akutagawa nominations. **Source verified 2026-10-02** from the BBC News Japan article of 2017-10-06, whose text the user pasted (about 200 "Harukists" at Hatonomori Hachiman Shrine, Sendagaya; party poppers set off for Ishiguro after the initial surprise and silence, per Mainichi; Kinokuniya Shinjuku swapped its ~30-title Murakami display, per Asahi; the "autumn seasonal word" tweet). Earlier search-summary details that the article does not support were corrected ("polite applause" -> they popped the poppers anyway; "more than thirty" -> "about thirty"). Footnote text should be checked against the article's exact headline and URL when convenient. The Kinokuniya event page the user also supplied (2024 public viewing, store.kinokuniya.co.jp/event/1726982266) does not mention the 2017 episode. Chapter 1's title is still "The Prize He Never Won" (sub-heading changed to "Party Poppers at the Ready").
- Standing process rule: do not rebuild or send an EPUB until the user explicitly asks.
- No living creator's name in the KDP keyword field; other works' titles in the keyword field are an experiment on Vol.1 only (see `vol1-kdp-metadata.md`).
- The Akutagawa Prize is awarded to a writer at most once, so avoid "how many times it went to X" framing (fixed in the Vol.1 description; Vol.1 Ch.1 opening still to fix).

## Skills holding the lessons (2026-10-02)

`book-opening-design`, `kdp-description-writing`, `kdp-listing-setup`, `author-persona-tyler-atsumori` (persona facts now live there too), `book-section-audit`, `humanize-writing-en`, all under `.claude/skills/`.

## Status

Vol.1 (*Murakami, Untranslated*) submitted and published to KDP on 2026-10-02, enrolled in KDP Select, $5.99. Vol.2 could not be saved that day (weekly new-title limit; resets Sunday 00:00 UTC = Sunday 9:00 JST) and is still to do: description (same structure as Vol.1, see `vol2-kdp-description.html`, needs the same human-voice and bold pass), categories, keywords (use `kafka on the shore`, `dance dance dance`, `the wind-up bird chronicle`, `1q84`), price, EPUB.

## Vol.2 status (2026-10-02, evening)

Manuscript opening reworked, description and metadata plan written (`vol2-manuscript.md`, `vol2-kdp-description.html`, `vol2-kdp-metadata.md`). Stopped before the EPUB build, per the standing rule. Blocking items: verify the Kafka email story and its figures; cover file; price decision; weekly new-title limit resets Sunday 00:00 UTC.

## Vol.2 humanize pass and bio (2026-10-02, later)

Whole-book tic pass done on `vol2-manuscript.md` (em dashes 27 to 12, tic words 15 to 0, negations 19 to 11, no facts changed). Vol.2 bio now tells the twenty-years-of-jogging story (see `author-persona-tyler-atsumori`). Still blocked before the EPUB: verify the Kafka email story, cover file, price, new-title limit (resets Sunday 00:00 UTC). Vol.1 is published and has not had the whole-book pass.

## Vol.1 humanize pass (2026-10-02, evening)

Whole-book pass applied to `vol1-manuscript.md` (em dashes 35 to 11, tic words 30 to 0, "worth ..." 17 to 0). Also corrected three content problems found while editing (Nakamura paraphrase, Ch.9 vs Ch.4 Oe contradiction, "disowned"). The published Vol.1 EPUB does NOT yet include these; a rebuild (only when the user asks) and a KDP "Edit eBook Content" re-upload are needed.

## Status (2026-10-02, later)

Vol.1: on sale, new EPUB re-uploaded, $5.99, KDP Select. Vol.2: EPUB built (`Murakami, Everywhere.epub`), cover chosen (`vol2-cover.jpg`), description ready; to submit on or after Sunday 2026-10-04 9:00 JST (weekly new-title limit resets). Vol.2 price still to confirm ($5.99 vs $4.99).

## Pricing and ads (2026-10-02, later)

Price rule for the whole Murakami series: $5.99 per volume. Ads for Vol.1: undecided; the break-even math (CPC divided by a $4.19 royalty means about 18% of clicks must buy at a $0.75 CPC), this account's record on bare-name exact-match keywords (impressions, under 5% top-of-search share, zero conversions on the anime books) and the zero-review state all argue against paid ads for now. Ideas on the table instead: link Vol.1 and Vol.2 as a KDP series, and watch organic placement for the first 72 hours and through Nobel week.

## Vol.3 status snapshot (2026-10-02, later)

`vol3-manuscript.md` copied from the loving-volta branch for work (7,900 words; 8 chapters; old-style front matter with "How to Read" and "The Question"; 30 em dashes, 23 tic words, 31 negations, 4 "worth ..."; one "the user's copy" leak; Ch.4 is titled and written as if the Nobel never comes). To do: front-matter redo, new hook, third persona story (ask the user), whole-book humanize pass, Nobel-dependent text prepared in two versions, description, keywords, categories, cover file, price $5.99, EPUB.

## KDP series name (2026-10-02, later)

Series title decided by the user: **Murakami in Three Acts** (Vol.1 *Murakami, Untranslated*; Vol.2 *Murakami, Everywhere*; Vol.3 *Murakami, Unfinished*). Set the series in KDP when submitting Vol.2 (after Sunday 2026-10-04 9:00 JST) and attach Vol.1 to it. The text already uses the "act" language (Vol.1 Ch.9 speaks of the end of Act One).

## Vol.3 bio (2026-10-02, later)

Vol.3 bio now uses the Kyoto-summer-jog and mantra story (see `author-persona-tyler-atsumori`); applied to `vol3-manuscript.md`. The rest of Vol.3's front matter is still the old form.

## Vol.3 hook decision in progress (2026-10-02, later)

User chose the *Drive My Car* hook for Vol.3 but not framed as "little of the original, big success"; the framing should come from director Hamaguchi's own view of the adaptation, per a Brutus article (https://brutus.jp/post-71697/). brutus.jp is blocked from this environment and a search did not surface it, so the hook cannot be written until the user pastes the relevant passages. Search leads (not the Brutus article; unverified): a producer reported Hamaguchi wanting to "dig his own well" and reach the same underground water vein Murakami found; Hamaguchi also reportedly used the methods of Murakami's long novels as a reference (moviewalker.jp articles 1047487 and 1008992; an Osaka University comparative study of the story and the film). Chapter 5 facts already in the manuscript (fn 12): Oscar for Best International Feature at the 94th Academy Awards (2022), Best Picture nomination (first for a Japanese production), Cannes 2021 Best Screenplay.

## Vol.3 Ch.5 rewrite (2026-10-02, later)

Chapter 5 rewritten from the BRUTUS interview with Hamaguchi (brutus.jp/post-71697, 2022-02-25, text pasted by the user): new title "Three Stories and a Red Car"; the old claim that the Uncle Vanya material "barely exists in the source" and that the film worked loosely was wrong per Hamaguchi (the Vanya/Sonya correspondences are in the story; Takatsuki's speech is nearly verbatim) and was replaced. User confirmed the mother-dies-in-a-car-accident (story) versus landslide (film) detail. Glossary entry and Sources updated. Still to do in Vol.3: the hook (the Hamaguchi opening drafted in chat, not yet in the manuscript), front-matter cuts, whole-book humanize pass, "the user's copy" leak in fn 10, and the two-version Nobel text.

## Vol.3 front matter done (2026-10-02, later)

Vol.3 now opens on the Hamaguchi/*Drive My Car* hook (BRUTUS interview, footnote [^brutus-hook]); "How to Read This Book" and "The Question" removed; five "the user's copy" leaks fixed (footnotes and sources). Still to do: whole-book humanize pass (Vol.3 had 30 em dashes, 23 tic words, 31 negations), the two-version Nobel text (Ch.4 is titled and written as if he never wins), description, keywords, categories, cover file, EPUB. Check that the hook's numbers and Hamaguchi paraphrases match the interview wording.

## Vol.3 Nobel branches prepared (2026-10-02, later)

`murakami-epub-rebuilt/vol3-nobel-branches/` holds `ch4-no-win.md`, `ch4-win.md`, `swap-checklist.md`, and `apply_ch4.py` (replaces Chapter 4 in `vol3-manuscript.md`; refuses to run while any `[[FILL: ...]]` marker remains). The manuscript still carries the old Chapter 4 until the result is known (expected Thursday 2026-10-08 about 20:00 JST; confirm the date). The shared sections (annual ritual, sealed records, betting odds) were rewritten past-tense so they hold on both branches.

## Vol.3 humanize pass done outside Ch.4 (2026-10-02, later)

Chapters 1-3, 5-8 cleaned (em dashes 0 outside glossary/sources, tic words and "worth ..." gone). Chapter 4 is replaced on the Nobel branch (new text then needs its own pass). Remaining for Vol.3: Ch.4 swap on 2026-10-08, Ch.7/Ch.8/back-matter Nobel wording, description, keywords, categories, cover file, EPUB (only when asked).
