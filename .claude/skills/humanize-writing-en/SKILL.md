---
name: humanize-writing-en
description: Use when writing or revising English-language prose meant to read as natural human writing — Kindle books, essays, articles, marketing copy — especially when the user says things like "make this sound less like AI," "humanize this," "remove AI-isms," or before finalizing any long-form English manuscript. Use as a pre-write style guide and a post-write checklist.
---

# Writing English Prose That Doesn't Read as AI-Generated

LLM output has a recognizable statistical fingerprint: low "burstiness" (sentence length and rhythm barely vary), low "perplexity" (word choices are the most predictable ones available), a narrow "house vocabulary" that recurs regardless of topic, and a small set of favorite rhetorical structures reused constantly. None of these individually proves a text is AI-written — they appear in mediocre human writing too — but stacked together, density is the signal. This skill is a concrete checklist for keeping that density low.

Sources this is based on: Wikipedia's "Signs of AI Writing" essay (the most systematic public catalogue of these patterns), multiple 2025–2026 analyses of ChatGPT's most-overused vocabulary (including a PubMed-abstract frequency study), standard "burstiness/perplexity" AI-detection literature, and (items 9-11, and the em-dash note in item 3) real, confirmed field evidence from this project's own `reddit-comment-voice` skill — a live Reddit account under this project got directly, repeatedly flagged as AI, including one reader explicitly naming em dashes as the tell. Those items generalize beyond Reddit and belong here as much as there.

## Vocabulary to strike on sight

These words are individually fine, but they cluster in AI output far more than in human prose. If more than one or two appear per 1,000 words, cut or replace them:

delve, tapestry, boast/boasts, realm, landscape (metaphorical, e.g. "the landscape of..."), navigate (metaphorical), leverage (as a verb), foster, underscore(s), showcase/showcasing, pivotal, crucial, vital, intricate, multifaceted, comprehensive, robust, vibrant, meticulous, testament (to), embark, elevate, unlock, unleash, game-changer, cutting-edge, seamless, holistic, dynamic (as filler), ever-evolving, in today's [world/landscape], utilize (just say "use").

Also flag the intensifier tic: genuinely, truly, certainly, really, actually stacked as reflexive hedge-softeners rather than doing real work. If you can delete the word and the sentence loses nothing, delete it.

## Phrases to strike on sight

- "It's important to note that..." / "It's worth noting that..." / "It's worth remembering that..."
- "No discussion of X would be complete without..."
- "Certainly! Here is/are..."
- "Based on the information provided..."
- "Navigating the complexities of..." / "Navigating the landscape of..."
- "Delving into the intricacies of..."
- "In conclusion," / "In summary," / "Overall," as a paragraph-opener
- "This isn't just about X — it's about Y" and its cousin "It's not X, it's Y" (see below — this is a structural pattern, not just a phrase, and it's the single most diagnostic AI tell)

## Structural patterns to break up

These matter more than individual words, because you can pass a word-list check and still read as obviously AI-written if the sentence architecture is uniform.

**1. The "It's not X, it's Y" negative parallelism.** ("This isn't a bug. It's a feature." / "It's not just a book, it's a lens.") LLMs reach for this constantly because it sounds punchy in isolation. Used once per essay, fine. Used three times, it reads as a tic. Search your own draft for "not just" and "it's not" — if you find more than one or two per chapter, cut most of them and just state the claim directly.

**2. The rule of three.** Three examples, three adjectives, three clauses in a list — "clear, concise, and compelling." AI defaults to triads because they're the most statistically common list length in training data. Deliberately break some lists to two items and some to four or five. Real thinking doesn't arrive in neat groups of three.

**3. Em dash overuse.** AI output uses em dashes far more than typical human prose, often in places a human would use a comma, a colon, parentheses, or just a period. Go through your draft and convert at least half your em dashes to something else — or to a full stop. **Confirmed, not just theoretical**: a real reader on Reddit, replying to an AI-accusation this project's own account faced, stated outright "em dashes are associated with LLMs, sadly" — people are now actively watching for this specific punctuation mark as a tell, not treating it as a vague stylistic preference. Treat zero em dashes as the safe default in any writing meant to pass as casually human-written; reserve them for contexts (formal essays, book-length prose with an established, confident narrator voice) where a slightly more literary register is already expected.

**4. Tailing participial clauses.** Sentences that end with a present-participle clause bolted on for false weight: "...ultimately reshaping how we think about the topic entirely." "...creating a ripple effect across the industry." These add a vague sense of importance without adding information. Cut them; end the sentence on the actual claim instead.

**5. Editorializing and puffery.** AI struggles to just state a fact — it wants to tell you why the fact matters, every time. "This represents a significant shift." "This is a testament to X's enduring appeal." If you're narrating the significance of your own sentence, delete the narration and trust the reader.

**6. Section-closing significance statements.** Every chapter or section ending with a tidy one-sentence summary of what it all means ("Ultimately, this shows that..."). Human essays are allowed to just stop. End on a concrete image, an open question, or a flat statement — not a bow.

**7. Symmetrical, evenly-paced structure.** If every section is the same length, every paragraph is 3–5 sentences, and every sentence is 15–25 words, that regularity itself is a tell (low burstiness). Deliberately vary: let one paragraph run long and digressive, then follow it with a two-word sentence. Fragment occasionally. Start a sentence with "And" or "But" sometimes.

**8. Excessive boldface / "key takeaway" formatting.** Bolding one phrase per bullet like a slide deck. Fine in a listicle, deadly in narrative prose. Use bold sparingly, if at all, in book-length nonfiction.

**9. The "acknowledge, then add a complicating nuance" dialectical move, overused.** Validate what someone said or what a prior point established, then introduce a wrinkle, synthesis, or "but actually" refinement — once or twice in a piece, this is just good argumentation. Repeated as the default move for nearly every paragraph or every reply in a sequence, it becomes a recognizable fingerprint distinct from the "It's not X, it's Y" pattern above: this one is a move across whole paragraphs or turns, not a single sentence. Real human argument is blunter and more one-sided more often — flat agreement, flat disagreement, a joke with no follow-up synthesis. Deliberately let some reactions just land without complicating them further.

**10. Confident assertion of specialized or insider claims you haven't actually verified.** Stating a claim about expert/cultural/technical knowledge as settled fact ("this is deliberate," "this means X") rather than as a hedged personal observation is a double risk: if the claim turns out wrong, the confident framing makes the correction land as overreach rather than an honest slip, and confident-assertion-without-real-expertise is itself a trait readers associate with AI output. This compounds — being caught overclaiming primes suspicion of everything else in the same piece. Default to "I noticed X, might be coincidental" over "X means Y" whenever the underlying claim hasn't been independently verified.

**11. Vocabulary pitched above the established voice's plausible expertise.** A narrator or persona established as a casual enthusiast, not a specialist, reaching for precise technical/academic terminology (e.g., field-specific jargon) is a tell on its own, independent of sentence rhythm or word-frequency lists — it's a mismatch between the voice's claimed knowledge level and its actual vocabulary. Keep technical precision consistent with what the established voice would plausibly know and say unprompted.

## Techniques that actively help

- **Load in irrelevant-but-real specificity.** Not "one afternoon" but "on a Tuesday, around 4pm, with the AC broken." Concrete, slightly off-topic detail is the single hardest thing for AI output to fake convincingly, and the easiest thing for a human writer to add in a pass.
- **Leave something unresolved.** Don't answer every question you raise. A stray thought that doesn't get tied off reads as more human than a perfectly closed loop.
- **Let opinion wobble.** Real writers hedge, contradict themselves slightly, or change their mind mid-paragraph. A perfectly consistent argumentative through-line from start to finish is itself a mild tell.
- **Use contractions and a few sentence fragments.** Not in every sentence — but their total absence reads as stiff.
- **Read it aloud.** The rhythm problems (uniform pacing, tailing clauses, over-hedged sentences) surface immediately out loud even when they're invisible on a silent read.
- **Vary your paragraph openers.** If you scan the first word of every paragraph and see a wall of "This," "Additionally," "Furthermore," "In," rewrite half of them.

## Post-write checklist

Run this against a finished draft before calling it done:

- [ ] Search for "not just," "it's not," "isn't just" — cut most hits
- [ ] Search for "important to note," "worth noting," "no discussion... complete" — cut all hits
- [ ] Count em dashes per 1,000 words; if it feels high, halve it
- [ ] Scan for triads (X, Y, and Z lists / three-part sentences); break up at least half
- [ ] Check paragraph and sentence-length variation — does anything run short and blunt, or does everything sit in the same 15–25 word band?
- [ ] Check every section/chapter ending — does it close with a tidy "in summary" bow? Cut the bow.
- [ ] Check the vocabulary list above — flag and replace clustered hits
- [ ] Read one full chapter aloud; fix whatever trips your tongue
- [ ] Confirm at least one piece of oddly specific, slightly irrelevant concrete detail appears per section
- [ ] Scan for "acknowledge, then complicate" as the default move across paragraphs/replies — let at least some reactions land flat, without a follow-up synthesis
- [ ] Any confident claim about specialized/insider/cultural knowledge that hasn't actually been verified? Hedge it ("I noticed X") rather than assert it ("X means Y")
- [ ] Does any vocabulary sit above what the established voice would plausibly know and say unprompted?

## A caveat worth keeping in mind

None of this is about disguising authorship for platforms that require disclosure — style edits don't change whether content legally/contractually counts as "AI-generated" for a given publisher's policy (e.g., Amazon KDP requires internal disclosure of AI-generated text regardless of how heavily it was subsequently edited). This skill is about craft — making prose read as alive and specific rather than statistically average — not about evading a disclosure obligation.
