# Murakami Vol.1 (*Murakami, Untranslated*) — KDP metadata decisions

Logged 2026-10-02, the day Vol.1 + Vol.2 were submitted to KDP (primary marketplace: Amazon.com).

## Categories (3 of 3)

1. Kindle > Literature & Fiction > History & Criticism > Regional & Cultural > Asian > Japanese
2. Kindle > Literature & Fiction > History & Criticism > General
3. Kindle > Literature & Fiction > History & Criticism > Movements & Periods > Postmodernism

Reasoning: all three are accurate for the subject, so no misleading-category rejection risk. #3 chosen because it is the only plausible
fit among the Movements & Periods options and is much smaller than a "General" bucket. Caveat: Vol.1's text never uses the word
"postmodern" (Vol.2 once); Murakami is commonly discussed under that label, so it is defensible but not something the book argues.
The "Subjects & Themes" branch was rejected: its options are literary themes (mystery, myth, horror, SF...), none fit.
Categories can be changed after publication (up to ~72h to take effect).

## Keywords (7 slots, <=50 chars each)

Rules applied (from `kdp-ads-strategy`): no living creator's name ("Murakami" is already in the title, which Amazon indexes
automatically); real search words; distinct words per slot (KDP keywords are not exact match, repeating words wastes space).

| # | Keyword |
|---|---|
| 1 | japanese novels literature novelist author |
| 2 | nobel prize literature award |
| 3 | norwegian wood wild sheep chase |
| 4 | hear the wind sing pinball 1973 |
| 5 | hard-boiled wonderland end of the world |
| 6 | criticism analysis essays translation meaning |
| 7 | contemporary modern postwar fiction explained |

### Experiment: other works' titles in slots 3-5 (user's decision, 2026-10-02)

Known risk: this account has had a KDP keyword field rejected for another work's title ("Infinity Castle") and for a living
creator's name. Murakami novel titles may trigger the same rule. User chose to test it anyway; plenty of time before the Nobel
announcement (~10/8) to fix. Only titles discussed in Vol.1 are used (Vol.2/3 titles such as Kafka on the Shore / 1Q84 deliberately
excluded). Titles are kept in their own slots so a rejection only requires swapping slots 3-5.

**Fallback for slots 3-5 if KDP objects:**
3. translation translated english original text
4. contemporary modern postwar fiction 1980s
5. explained understand debut early career

Also watch: "nobel prize" in slot 2 could be flagged as a trademark; fallback `literature prize japanese author`.

### Check after publication (~72h)

Search Amazon.com for "murakami nobel prize", "murakami criticism", "murakami translation", "murakami wild sheep chase" and see whether the
book appears. Note that title searches mostly come from people wanting the novels themselves, so conversion may be low.

## Price (decided 2026-10-02)

User set **$5.99** (Amazon.com, 70% royalty tier, which covers $2.99–$9.99). Royalty ≈ 70% × ($5.99 − delivery fee; a ~44 KB file costs
well under $0.01) ≈ **$4.19 per sale**. For reference the anime companion books are $2.99 (≈$2.01/sale) and had 0 paid orders in
the 9/4–10/2 window. Vol.1 manuscript is ~9,000 words, a short read, so $5.99 is on the high side; price is changeable any time
(takes effect within ~72h). Revisit if no sales by the end of Nobel week (~10/8–10/15).
Ads break-even for reference: required click-to-purchase rate = CPC ÷ royalty ≈ $0.75 ÷ $4.19 ≈ 18% (still not a profitable ad target).

## Keyword slots 6-7: final decision (2026-10-02)

The user's own draft had `kafka on the shore dance dance dance` (6) and `the wind-Up bird chronicle` (7). Those works are not discussed in
Vol.1 (0 mentions; they are in Vol.2), so they risk a KDP relevance rejection and mislead shoppers. User agreed to use the proposed
replacements instead, so the final Vol.1 list is:

1. japanese novels literature novelist author
2. nobel prize literature award
3. norwegian wood wild sheep chase
4. hear the wind sing pinball 1973
5. hard-boiled wonderland end of the world
6. criticism analysis essays translation meaning
7. contemporary modern postwar fiction explained

Save `kafka on the shore`, `dance dance dance`, `the wind-up bird chronicle`, `1q84` for Vol.2's keyword field (all four are discussed there).
Slots 3-5 remain the experiment (other works' titles); fallbacks are listed above.

## Source check for the Nobel-night anecdote (Vol.1 Ch.1), 2026-10-02

The user supplied https://store.kinokuniya.co.jp/event/1726982266/ as the source. That domain is blocked from this environment, so its contents
were not read. A web search suggests Kinokuniya's Shinjuku store runs Murakami "Nobel support fairs" and midnight release events, which is
consistent with the bookshop-display part, but nothing opened here confirms the shrine / ~200 fans / party poppers / Ishiguro-win sequence.
Open item: user to check the page (or the original 2017 press report) and report what it says; then correct the footnote [^fans] and
Sources entry in `vol1-manuscript.md` if needed.
