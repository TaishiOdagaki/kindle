---
name: kdp-description-writing
description: Use when writing or revising the KDP book description (the Amazon "About this book" copy) for any of this project's books. Captures the structure, formatting, and wording rules worked out for Murakami Vol.1 on 2026-10-02: lead with the book's best opening scene so the first lines sell, plain-language bullets for a broad audience, five bolds at most, no unverifiable claims, HTML limits.
---

# Writing the KDP Description

The description is the second thing a shopper reads after the cover and title. Only the first few lines show before "Read more", so they must carry the sale on their own.

## Structure that worked (Murakami Vol.1)

1. **Bold opening sentence = the book's best scene, one sentence.** "In April 1978, a jazz-bar owner lay down on the grass at a Tokyo baseball game, watched a Texan hit a double, and decided to write a novel." It must match the book's own opening, so Look Inside delivers what the page promised.
2. **One or two flat sentences of tension, with the thesis in bold.** "Japan's most serious literary judges later said, in print, that the result sounded foreign. **They weren't wrong, and that was the point.**"
3. **One paragraph of promise:** the most surprising fact (written in English first, then translated back), the biggest number (ten million copies), the human texture (fans with party poppers, the critics who were unimpressed).
4. **"This book is for you if" with 3 to 4 plain bullets** spanning the audience: devoted fans, never-read-him newcomers, people following the news hook (Nobel Prize every October), readers curious about translation.
5. **"What's inside": 5 to 6 bullets in plain language,** no insider jargon (not "junbungaku," not "split narration" without explaining it).
6. **A short "built from primary sources" line** that names the kinds of sources, without absolutes.
7. **A "Look Inside" call to action** that names what the reader will see ("start at the baseball game").
8. **Author bio** in the persona's human voice (see `author-persona-tyler-atsumori`).
9. **Series line** (check it is true today: "coming soon" vs "available now").
10. **Short disclaimer** (not affiliated, independent criticism).

## Formatting and limits

- KDP accepts the text editor or basic HTML. Tags used: `<p>`, `<b>`, `<i>`, `<h4>`, `<ul>`, `<li>`. KDP's usable headings are h4 to h6 (confirm in KDP help if in doubt).
- The 4,000-character limit counts tags. Budget for them. Vol.1 ended at 3,172 characters with tags; longer is not better, the first three lines matter most.
- **Bold at most five spots:** the opening sentence, the thesis line, the most surprising fact, the biggest number, the Look Inside CTA. Do not bold one phrase per bullet; that reads as a slide deck.
- Zero em dashes.

## Wording rules

- No absolute claims ("every claim checked against a primary source," "never reaches"). While preparing Vol.1, real factual errors were found and fixed, so an absolute promise is false; name the kinds of sources instead.
- No "It isn't X, it's Y," no triads of adjectives, no self-narrated significance (run `humanize-writing-en`).
- Do not describe the book as something it is not (it is not a "where to start" guide, so do not say "beginners").
- The AI-assistance disclosure belongs in KDP's submission form. The user decided on 2026-10-02 to keep it out of the public description. Confirm the exact requirement in KDP help.

## Process

1. Write the book's opening first; derive the description from it.
2. Run `book-section-audit` on the description (jargon, absolutes, stale claims, length with tags).
3. Show it to the user rendered, with the bolds visible, plus the file path. Save to the book's folder as an `.html` file.
4. After publishing, open the live page logged out and check the first three lines and the formatting.

## Dated log

- **2026-10-02.** Vol.1's first description opened on "the Akutagawa Prize never went to Murakami": negative, obscure to non-Japanese readers, and the "how many times" framing was illogical for a one-time prize. Rewritten per the structure above. Outcome (conversion): not yet known.
