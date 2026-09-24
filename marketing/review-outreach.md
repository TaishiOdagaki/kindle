# Review-Generation Outreach — Japanese Culture Press Series

Companion doc to `.claude/skills/kdp-ads-strategy/SKILL.md`. That skill tracks ad campaign performance; this doc tracks the non-ad side of getting reviews: in-book asks (done, see below) and public fan-community outreach (drafted here, not yet posted).

## Why this exists

All four books in this series (Chainsaw Man, Demon Slayer, Attack on Titan, Ramen Jiro) currently have 0 reviews. Zero reviews caps ad conversion rate regardless of spend — a cold visitor with no social proof has little reason to buy from an unknown pen name. The same problem was already solved once for this account's other product line (登録日本語教員試験問題集, see `nihongo-kyoin-ads-strategy` skill): public callouts to people already interested in the topic, not personal asks to friends/family, and never incentivized/traded reviews (KDP ToS violation risk).

## What's done

- **In-book review asks added** (2026-09-24): each book now has two asks — a short "A QUICK FAVOR" section right after the final content chapter (before the Spoiler Map / Glossary back matter, so it's seen even by readers who don't read every back-matter page) and a one-line reminder at the very end of the Afterword. All four EPUBs regenerated via the documented pandoc command and validated clean with epubcheck (0 errors/warnings each).
- **⚠️ Chainsaw Man, Demon Slayer, and Attack on Titan are all already live on KDP** (corrected 2026-09-24 — this repo's top-level README previously and incorrectly listed the latter two as "Ready for KDP upload"; all three are published). Regenerating the EPUB in this repo does not update an already-published listing — each of these three needs its updated `.epub` file manually re-uploaded via KDP's "Edit eBook Content" flow for the review ask to actually reach readers. Only Ramen Jiro is genuinely pre-publication (cover art still not finalized), so its updated EPUB is already what will ship once it's uploaded for the first time.

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

## Reddit basics for a first-time user (this project)

The user has never used Reddit before this series. Notes from walking through it, 2026-09-24.

- **There is no "Japanese Reddit" vs. "English Reddit," and nothing is auto-translated.** Reddit is one global site made of topic-based communities (subreddits, r/whatever); each one's language is just whatever its own members happen to write in, not a platform-level setting. Language-specific subreddits for Japanese speakers do exist, but they're small relative to English-language ones — Reddit never really took off domestically in Japan the way 5ch, X, and LINE did. Since these books are English-language companions written for a worldwide fandom, the only correct targets are the English-language fandom subs (r/ChainsawMan, r/AttackOnTitan, r/KimetsuNoYaiba, r/manga, r/anime) — a Japanese-language subreddit wouldn't reach the actual target readers even if one were posted to, and posting in Japanese on an English-language sub just looks out of place.
- **Account setup is trivial** (reddit.com → Sign Up, any handle, no real name needed) — the part that actually matters is everything after that.
- **Do not post a self-promo link the same day the account is created.** A brand-new, zero-karma account posting a "here's my book" link reads as spam to both Reddit's automated filters and every subreddit's moderators, and gets removed or shadowbanned (posts become invisible to everyone but the poster, often without any notice) far more often than not. Spend 1–2 weeks first genuinely participating in the target subs — commenting on other people's posts, upvoting — before attempting any promotional post. This is the single highest-risk-of-failure step to skip.
- **Read each target subreddit's own self-promotion rule before posting**, via its "Rules" / "About Community" panel or a `/wiki/rules` URL. Common patterns: self-promo confined to a specific recurring megathread rather than a standalone post, a 9:1 non-promotional-to-promotional ratio requirement, or a requirement to ask a moderator first via modmail. If the rule is unclear, message the mods directly before posting rather than guessing.
- **Stagger posts across subs and days** — see the caveat above; this still applies once the account is "warmed up," not just on day one.
- **Posting mechanics**: open the target subreddit → "Create Post" → choose the "Text" post type (reads less like an ad than a bare link post) → title + body (adapt the drafts below rather than pasting verbatim — a post that reads like copy-paste stands out) → set a flair if the sub requires one (e.g. "Discussion," "Fan Content") → after posting, reply to any comments, which itself builds the account's genuine history for next time.
- **Recommended sequence**: this week, create the account and spend time genuinely participating in 3–4 target subs; next, check one sub's rules and post about one book; wait a few days; move to the next sub/book. Log actual outcomes (comment engagement, whether any reviews followed) back into this file or into `kdp-ads-strategy`.

## Open items

- Create the Reddit account and spend 1–2 weeks building genuine karma/history in the target subs before any promotional post (see above) — not done yet.
- Actually posting these (staggered, one sub at a time, rules-checked immediately before each post) — not done yet.
- Re-upload the updated EPUBs for Chainsaw Man, Demon Slayer, and Attack on Titan to their live KDP listings so the in-book review ask reaches current/future readers (all three are published, not just Chainsaw Man — see the corrected note above). Ramen Jiro's updated EPUB just needs its first upload once the cover is ready.
- Track review counts per book after each post goes up; log outcomes here or in `kdp-ads-strategy` the same way the exam-book campaign's outcomes are logged.
