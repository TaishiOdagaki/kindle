---
name: kdp-listing-setup
description: Use when filling in a KDP title's keywords, categories, price, or enrollment settings for any of this project's books, or when KDP blocks or rejects a listing field. Captures the rules and decisions from the Murakami Vol.1 submission on 2026-10-02: how to build the 7 keyword slots, how to choose 3 accurate categories, price and royalty math, KDP Select, the weekly new-title limit, and the AI-content declaration.
---

# KDP Listing Setup

## Keywords (7 slots, up to 50 characters each)

- KDP keywords are **not exact match**. Amazon splits them into words and combines them with the title, subtitle, and categories. So:
  - Do not repeat words across slots, and do not repeat words already in the title (the title already contributes "Murakami").
  - Pack each slot with distinct, real search words.
- **Never put a living creator's name in the field** (this account has had that rejected). For a book about a living author, the title carries the name.
- **Other works' titles are a risk, not a rule-free zone** (this account has had "Infinity Castle" rejected). The Murakami Vol.1 field is an experiment: slots 3 to 5 hold titles of works the book actually discusses (`norwegian wood wild sheep chase`, `hear the wind sing pinball 1973`, `hard-boiled wonderland end of the world`), kept in their own slots so a rejection only means swapping those three. Fallbacks are in `murakami-epub-rebuilt/vol1-kdp-metadata.md`. Only use titles the book discusses (Vol.2's titles were moved out of Vol.1's list). Outcome: not yet known.
- Never use words that misrepresent the book (not "beginners" for a book that is not a guide).
- KDP listing keywords and Amazon Ads keywords are different tools; never reuse one list for the other (see `kdp-ads-strategy`).
- After about 72 hours, search Amazon for combinations of the title word plus each keyword ("murakami nobel prize", "murakami criticism") and see whether the book appears; swap slots that do not work. The Amazon search box's autocomplete shows what people actually type.
- Final Vol.1 list: `japanese novels literature novelist author` / `nobel prize literature award` / the three title slots / `criticism analysis essays translation meaning` / `contemporary modern postwar fiction explained`.

## Categories (up to 3)

- Choose by accuracy first. A category that misleads (for example "Comics" for prose criticism, or the Fiction-in-foreign-languages branch for a nonfiction book) invites rejection.
- The KDP dialog is shown in the account's language but is the Amazon.com (US) tree; the links show the node.
- Murakami Vol.1: Literature & Fiction > History & Criticism > Regional & Cultural > Asian > Japanese; > History & Criticism > General; > Movements & Periods > Postmodernism. "Subjects & Themes" had no fitting option (themes such as mystery, myth, horror). Postmodernism is defensible for Murakami but Vol.1's text does not use the word; it was chosen as the only plausible Movements option and is smaller than "General."
- Smaller, accurate categories rank higher. To judge crowding, open the category link and look at the overall sales rank around the 20th book. Categories can be changed after publishing (up to about 72 hours to take effect).

## Price and royalty

- The 70% royalty tier covers $2.99 to $9.99; royalty is about 70% of the price minus a small delivery fee (negligible for small text files).
- Required click-to-purchase rate for ads = CPC ÷ royalty per sale. For a $5.99 book (royalty about $4.19) at a $0.75 CPC it is about 18%, which is still not a profitable ad target. Low-priced books almost never pay back ads; see `kdp-ads-strategy`.
- Murakami Vol.1: $5.99 (a short book, about 9,400 words, so on the high side with zero reviews). Revisit if there are no sales by the end of the Nobel announcement week; price changes take effect in about 72 hours.

## KDP Select

- Murakami Vol.1 was enrolled. Reason: KENP (read-through payments) was about a third of the account's royalties in the 9/4 to 10/2 data. Cost: 90 days of exclusivity (no other ebook stores).

## Blocks and gotchas

- **Weekly new-title limit:** KDP shows "the weekly title-creation limit for this format has been reached; the limit resets Sunday 00:00 UTC" (Sunday 9:00 JST). Our inference (unconfirmed): editing an existing draft should not count against the limit; creating a new title does. On 2026-10-02 Vol.2 could not even be saved as a new title. Plan multi-volume launches around it.
- **AI-content declaration** is made in the submission form, not in the description. Answer it accurately.
- **Cover** is uploaded in the Cover step, never inside the EPUB.
- Upload the EPUB that was built from the latest manuscript (check that recent edits are in the built file).
- After publishing, view the live page in a genuinely logged-out window to see what shoppers see.

## Dated log

- **2026-10-02, Murakami Vol.1 published.** Vol.2 could not even be saved because of the weekly limit and was deferred. Description edits are in `kdp-description-writing`; hook and manuscript decisions are in `book-opening-design`.
