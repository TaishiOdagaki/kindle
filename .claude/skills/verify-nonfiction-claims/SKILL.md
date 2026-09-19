---
name: verify-nonfiction-claims
description: Use when writing or editing nonfiction/critical-commentary content about real works, people, or events (book chapters, KDP descriptions, author bios) — anywhere a specific factual claim, quote, date, or attribution could be wrong. Use as a while-writing discipline and, always, as a pre-publish audit pass before finalizing a manuscript.
---

# Verifying Claims in Nonfiction Writing

This skill exists because it was needed. The *Chainsaw Man* companion book shipped with, and only caught after explicit user questioning, several confident, fluently-written factual errors: a quote spliced together from two separate lines and misattributed to the wrong chapter, an entire chapter's thesis built on a wrong claim about which magazine serialized the manga, a citation to "interviews" that didn't exist, and a etymology claim that was backwards. None of these read as uncertain. All of them read as fact. That's the actual danger: **confidence is not correctness, and the claims most worth double-checking are the ones that feel too obviously right to bother checking.**

Sourced from Anthropic's own hallucination-reduction guidance, several published Claude Code fact-checking skills, and this project's own incident history.

## While writing

- **Separate two voices explicitly, in the prose itself.** A documented fact ("Part 1 ran in Weekly Shonen Jump from 2018 to 2020") and a critical reading ("I think this scene is the most honest thing the series does") must not sound the same. When making an interpretive claim, say so — "I read this as," "this plays as," "my take is" — rather than borrowing the flat declarative voice that implies a checkable fact.
- **Never write "has said in interviews," "reportedly," "documented," or "according to" unless you have actually retrieved that source this session.** If you can't point to where a claim came from, it doesn't get citation-flavored language. Either search for it now, or rewrite it as your own reading.
- **Never merge separate quotes into one continuous quotation.** If a real quote is built from two fragments of a scene, either quote each fragment separately, use an accurate ellipsis, or paraphrase instead of using quotation marks. A quotation mark is a promise that this exact string of words appears in the source, in that order.
- **Don't infer facts from narrative plausibility.** "This would make a good story if X were true" is not evidence that X is true. The Jump+ error happened exactly this way: violent, blunt content "sounded like" it belonged on a permissive digital platform, so that was asserted without checking. Treat a fact that conveniently supports the point you're making as the one that most needs a search, not the one you can skip.
- **It's fine to not know.** A sentence can say a detail is disputed, unconfirmed, or simply left out. An unverified specific is worse in the manuscript than no detail at all.

## Before publishing — audit pass

Do this as a distinct, final pass, separate from writing. Treat it as skeptical of the draft, not confirmatory of it.

1. **Extract every checkable claim into a list.** Direct quotes, chapter/episode/scene attributions, dates, release venues, character events causally described ("X killed Y by doing Z"), any claim citing an interview or "documented" source, etymology/translation claims, statistics.
2. **Classify each one**: verified (you found a source this session), unverified (haven't checked), or interpretation (should be rewritten in first-person critical voice, not fact voice, if it isn't already).
3. **Search to verify every unverified item.** Don't rely on training-knowledge recall for anything specific — names, dates, exact wording, who-did-what. Recall is exactly what produced the errors this skill exists to catch. For anything time-sensitive (is a series finished? still running? release date?), search fresh rather than trusting what was true as of training cutoff — status like that can and does change.
4. **Grep the manuscript for risk phrases** before calling it done: "has said," "in interviews," "reportedly," "documented," "according to," "studies show," "it's known that." Every hit needs a real source behind it or a rewrite into first-person reading.
5. **Fix and re-verify downstream.** A correction rarely stays contained — check the introduction, other chapters, the glossary, and any marketing copy (book description, back-cover text) for the same claim repeated elsewhere. The Jump+ error alone required fixing five separate spots across two files once found.
6. **Rebuild and re-check the final artifact** (EPUB, PDF, whatever ships) after any correction — don't consider a fix done until it's in the file that actually gets published.

## The four-step verification workflow, when checking a specific claim

1. Identify exactly what's being asserted (not the general vibe of the sentence — the specific, falsifiable piece: a name, a date, a venue, a quote, a causal attribution).
2. Search for it specifically, not for the surrounding topic. A search for "Chainsaw Man Jump+" would have caught the error immediately; a general familiarity with the series didn't.
3. Check that the source actually supports the specific claim, not just the general subject. A result confirming Fujimoto loves film doesn't confirm the specific claim that he called a specific arc a "siege thriller."
4. If confirmed, keep it and know why. If contradicted, fix it and check for the same error elsewhere. If neither confirmed nor contradicted, don't keep it stated as fact — hedge it, cut it, or reframe it as a reading.
