# Review-Generation Outreach — Japanese Culture Press Series

Companion doc to `.claude/skills/kdp-ads-strategy/SKILL.md`. That skill tracks ad campaign performance; this doc tracks the non-ad side of getting reviews: in-book asks (done, see below) and public fan-community outreach (drafted here, not yet posted).

## Why this exists

All four books in this series (Chainsaw Man, Demon Slayer, Attack on Titan, Ramen Jiro) currently have 0 reviews. Zero reviews caps ad conversion rate regardless of spend — a cold visitor with no social proof has little reason to buy from an unknown pen name. The same problem was already solved once for this account's other product line (登録日本語教員試験問題集, see `nihongo-kyoin-ads-strategy` skill): public callouts to people already interested in the topic, not personal asks to friends/family, and never incentivized/traded reviews (KDP ToS violation risk).

## What's done

- **In-book review asks added** (2026-09-24): each book now has two asks — a short "A QUICK FAVOR" section right after the final content chapter (before the Spoiler Map / Glossary back matter, so it's seen even by readers who don't read every back-matter page) and a one-line reminder at the very end of the Afterword. All four EPUBs regenerated via the documented pandoc command and validated clean with epubcheck (0 errors/warnings each).
- **⚠️ Chainsaw Man is already live on KDP.** Regenerating the EPUB in this repo does not update the published listing — the updated `.epub` file needs to be manually re-uploaded via KDP's "Edit Paperback/eBook Content" flow for the review ask to actually reach readers. Demon Slayer, Attack on Titan, and Ramen Jiro are pre-publication, so their updated EPUBs are already what will ship.

## What's drafted, not yet posted: public fan-community callouts

Same principle as the exam-book strategy — post where people already interested in the specific fandom will see it, framed as "I wrote this, here's something for you," not "please review my book." Before posting any of these:

- **Check each subreddit's self-promotion rules first.** Most manga/anime subs (r/ChainsawMan, r/AttackOnTitan, r/KimetsuNoYaiba) either restrict self-promo to a weekly megathread, require mod pre-approval, or enforce a 9:1 non-promotional-to-promotional post ratio for the account posting. Posting a bare "I wrote a book, buy it" thread outside those rules risks an instant removal or a ban, which burns the account for future use. Read the sidebar/rules wiki of each sub immediately before posting, not from memory of past visits.
- **Stagger posts, don't drop all four at once.** Posting to four different fandom subs on the same day from a new/low-karma account reads as a coordinated spam run even if each individual post follows that sub's rules. One book, one sub, then wait a few days before the next.
- **Disclose authorship up front.** "I wrote a critical companion book about X" is honest framing and far better received than pretending to be a neutral fan; undisclosed self-promotion gets removed faster and damages the account long-term.
- **Never trade or incentivize reviews** — offering a free copy in exchange for a review, or joining review-swap groups, violates Amazon's content guidelines and risks the whole KDP account, not just one book.

### Chainsaw Man (target: r/ChainsawMan)

**Post title:** "I wrote a full critical companion book on Chainsaw Man's ending, from a Japanese fan's perspective — here's the thesis"

**Body:**
> I've been following this series since Part 1 and finally sat down and wrote a full-length critical companion — not a recap, but an argument about why the ending works even though it upset a lot of readers (myself included, at first). Covers the fear-as-currency worldbuilding, Makima's "care and control are the same gesture" character logic, why Part 2's pacing split the fandom, and the ending itself in detail.
>
> It's on Kindle under the pen name Jiro Naozane if anyone wants to check it out: *Chainsaw Man: The Devil in the Details*. Happy to talk through any of the actual arguments here too if people want to push back on them — that's kind of the point of writing it.

### Demon Slayer (target: r/KimetsuNoYaiba)

**Post title:** "Wrote a companion book on why Infinity Castle broke box office records twice — sharing the core argument here"

**Body:**
> Put together a full critical companion covering why *Demon Slayer* specifically was the franchise to break records at this scale twice (Mugen Train, then Infinity Castle), the Taisho-era setting choices that make the Corps' secrecy make sense historically, and what the wait for Parts 2/3 means for the trilogy. Written from Japan, under the pen name Jiro Naozane, out now on Kindle: *Demon Slayer: Total Concentration*.
>
> Genuinely curious what people here think about the "why did this specific franchise cross over" question — happy to get into specifics in the comments.

### Attack on Titan (target: r/AttackOnTitan)

**Post title:** "Wrote a full book on whether the ending earned its own thesis — the nationalism debate, the studio switch, all of it"

**Body:**
> Spent a long time on a critical companion book working through the ending debate properly — not just "good or bad" but whether the story's own central argument about freedom actually holds up by its final page. Also covers the nationalism controversy as precisely as I could state it (with the actual peer-reviewed academic source), the Wit-to-MAPPA studio switch, and the China ban. Pen name Jiro Naozane, out on Kindle: *Attack on Titan: The Price of Freedom*.
>
> This fandom argues about the ending better than almost any other I've seen, so I'd rather get pushback here than not — happy to defend any specific claim in the comments.

### Ramen Jiro (target: r/ramen or r/JapanTravel)

**Post title:** "Wrote a deep-dive book on Ramen Jiro — the lineage system, the intimidation-as-business-model argument, the trademark fights"

**Body:**
> If you've ever been curious (or scared off) by Ramen Jiro specifically — not just Jiro-style ramen generally — I wrote a full book on it: the founder's approach, the chokkei/Jiro-kei lineage taxonomy, why the ritual and intimidation are load-bearing for the business model rather than incidental, and the actual trademark disputes around the name. Pen name Jiro Naozane (a coincidence I address directly in the afterword — no relation to the shop). On Kindle: *Ramen Jiro: The Cult of Tokyo's Most Intimidating Bowl*.

## Open items

- Actually posting these (staggered, one sub at a time, rules-checked immediately before each post) — not done yet.
- Re-upload the updated Chainsaw Man EPUB to the live KDP listing so the in-book review ask reaches current/future readers.
- Track review counts per book after each post goes up; log outcomes here or in `kdp-ads-strategy` the same way the exam-book campaign's outcomes are logged.
