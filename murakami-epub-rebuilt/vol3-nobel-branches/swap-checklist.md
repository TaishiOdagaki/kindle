# Vol.3 Nobel swap: what to change on each branch (prepared 2026-10-02)

Announcement: expected Thursday 2026-10-08 (about 20:00 JST); confirm the date on nobelprize.org. Do not publish Vol.3 before the result.

## How to apply

1. Pick `ch4-no-win.md` or `ch4-win.md`.
2. Fill every `[[FILL: ...]]` from sources you have actually opened (the Academy's announcement, major press). The script refuses to run while any marker remains.
3. Run `python3 vol3-nobel-branches/apply_ch4.py no` or `... yes` from the `murakami-epub-rebuilt` folder. It replaces Chapter 4 in `vol3-manuscript.md`.
4. Do the other edits below.
5. Humanize pass on the new text (`humanize-writing-en`), then the description, keywords, EPUB (only when asked).

## Other places that depend on the result

| Place | If no win | If win |
|---|---|---|
| Book subtitle: "The Late Novels, the Nobel Bet, and Still Being Read as an Outsider" | keep | change to "...the Nobel Prize..." |
| Chapter 7 opening (the "two-decade fable" around his supposed nearness to the prize) | keep, adjust tense if needed | rewrite: the fable ended in 2026 |
| Chapter 8 verdict and "A Note on This Series" | check for "has not won" wording | rewrite the Nobel sentences |
| Sources list, "Chapter 4:" heading and entries | rename heading to match the new title; add the Academy announcement and press sources | same, plus the winner's citation |
| Glossary ("The 50-year rule") | keep | keep |
| Footnote [^11] ("only nominations through 1975 have been released") | check the year against nobelprize.org | same |
| KDP description, bullets about the Nobel | write neutrally for the no-win branch | lead with the win if the hook allows |
| Keywords (slot 2 `nobel prize literature award`) | keep | keep |
| Vol.2 back matter ("one of literature's most closely watched Nobel Prize contenders") | still true | still true as history, but consider an update on re-upload |

Hook check: the front-matter hook (Hamaguchi) is result-neutral. Its last line, "whether there is anything left for a writer this large to risk," works either way.
