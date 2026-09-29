# Murakami criticism trilogy — citation tracking

Working log of physical-book citations gathered for the three Murakami
criticism manuscripts (`murakami-book/`, `murakami-book-vol2/`,
`murakami-book-vol3/`). Update this file whenever a citation is
requested, fulfilled, or corrected — don't rely on chat history alone.
This file is the only thing that survives between sessions; a prior
session's library-borrowing plan (below) was never written here and
almost got lost as a result — don't repeat that mistake.

## Pre-publish audit, Vol.1 + Vol.2 (2026-09-29)

**Plan confirmed by user: Vol.1 and Vol.2 publish together; Vol.3 waits
until after the Nobel Prize result is announced.** Did a publish-readiness
pass on both volumes, per the `verify-nonfiction-claims` discipline.

### Vol.1

- **Footnotes**: all 14 sequential, no orphans — clean.
- **Chapter title/content match**: spot-checked all 9 chapter titles
  against their bodies (the way Ch.3's "Light" mismatch was caught
  earlier). All 9 hold up, including Ch.6 ("Two Worlds, One Skull,"
  which literally quotes "one skull" in its own text). No further
  Ch.3-style bugs found in Vol.1.
- **Front matter / back matter structure**: matches the documented
  convention exactly — hook, About the Author, How to Read This Book,
  the Question, chapters, Glossary, A Note on What Comes Next,
  Sources, disclaimer as the very last lines. Clean.
- **Opening-hook fact-check** (highest-visibility text in the book —
  first thing a Look Inside browser sees): the Jingū Stadium/Dave
  Hilton anecdote (April 1978, a batter hitting a double, the thought
  "I could write a novel") checked against multiple sources (Lit Hub's
  own translation of Murakami's *Novelist as a Vocation* essay on
  this, PRX/WBEZ, murakami.club) — accurate as written.
- **Found and fixed a real numeric error**: Ch.8's *Norwegian Wood*
  sales footnote [^11] had the domestic/international split backward.
  Manuscript said "ten million copies worldwide, including roughly
  four million in Japan alone." The actual widely-reported figure
  (multiple sources, consistent with Wikipedia's sourcing, tied to the
  2010 English-language/film release) is the reverse: **over ten
  million in Japan alone**, plus roughly 2.6 million more across 33
  other languages internationally. Fixed both the inline text (line
  ~198) and the footnote. This isn't just a correction — the right
  number actually makes Ch.9's "inescapable at home" argument land
  harder than the wrong one did, since the wrong version implied more
  copies sold abroad than domestically.
- **Previously flagged, now resolved:** Ch.9's "next volume picks up"
  line was flagged as a risk when Vol.1 might publish alone. Now that
  Vol.1 and Vol.2 are confirmed to launch together, this is accurate
  and needs no change.
- **Not blocking, not done**: the English-translation edition of
  *Novelist as a Vocation* (only the Japanese text is quoted in Ch.2)
  — open per the master library list above, optional enrichment, not
  a publish blocker.

### Vol.2

- **Footnotes**: all 18 sequential, no orphans — clean.
- **Chapter title/content match**: spot-checked all 8 chapter titles.
  **Found and fixed a real mismatch**: Ch.3 was titled "Two
  Earthquakes," but the chapter actually covers one earthquake (the
  Great Hanshin earthquake) and one terrorist attack (the Aum
  Shinrikyo sarin gas attack) — only one of the two events is
  literally an earthquake. Same category of bug as Vol.1 Ch.3's
  "Light" mismatch. Retitled to "Two Catastrophes, Ten Weeks Apart,"
  reusing the chapter's own opening subsection heading (which also had
  to be retitled to avoid exact duplication — now "A Country He'd
  Started Watching from a Distance"). Updated the Sources section
  entry to match. Confirmed no other reference to the old title
  anywhere in the trilogy. Other 7 chapter titles all hold up.
- **Front matter / back matter structure**: matches the documented
  convention. Clean.
- **Numeric fact-check**: *1Q84*'s launch figures (680,000 combined
  initial print run, ~100,000 advance sales in Tokyo/Kansai over the
  two days before the nationwide May 29, 2009 release) verified
  against multiple sources (The Millions' "1Q84 Revealed," contemporary
  Japanese press coverage) — accurate as written, no fix needed.
- **Judgment call, resolved, 2026-09-29:** the "A Note on What Comes
  Next" back-matter section described Vol.3 as covering "his
  decades-long status as literature's most reliable Nobel Prize
  non-winner" — accurate today, but risky to leave sitting in an
  already-published Vol.2 for an indeterminate stretch while Vol.3
  waits on the actual Nobel result. User asked for the softened
  version; changed to "his decades-long status as one of literature's
  most closely watched Nobel Prize contenders," which stays accurate
  regardless of how the Nobel result eventually lands.

### Outside this repo, not yet started for this trilogy

Unlike the sibling anime-book project, which has these as separate
assets: EPUB build + epubcheck validation, KDP book description,
category/keyword selection. **Cover art: finalized, 2026-09-29.** Got
flagged in a separate `pro-ui-director` design review (2026-09-29) for
a register mismatch (reads as self-help/lifestyle rather than literary
criticism), AI-slop stock-photo imagery unrelated to Murakami's actual
themes, a possible trademark issue (Vol.2's cover originally featured
headphones closely resembling Apple AirPods Max), and inconsistent
styling across the three covers. User's final call: keep the overall
look as-is (register/stock-photo concerns acknowledged, not acted on —
their creative decision to make), but fixed the one non-aesthetic
issue — Vol.2's headphones were redesigned to no longer resemble
AirPods Max, resolving the trademark risk. All three covers (Vol.1
blue-sky, Vol.2 train-platform, Vol.3 night-sky silhouette) are
confirmed final. Not yet added to this repo as files. EPUB build, book
description, and category/keyword selection remain fully unstarted for
all three volumes — next up before Vol.1 + Vol.2 are fully
publish-ready.

## Prose polish pass (2026-09-28) — not a citation task, logged for continuity

Vol.1 and Vol.2 got a readability/craft pass using the `humanize-writing-en`
skill from the anime-criticism sibling project, plus a read-through of
that project's three companion books (Chainsaw Man, Attack on Titan,
Demon Slayer) for concrete technique. Vol.3 is deliberately excluded —
the user will add a Nobel Prize result section once it's announced, so
Vol.3 gets its own polish pass then, not now. Applied, in order:
1. Front matter: replaced the "isn't X, isn't Y" opener pattern with
   concrete hooks (Vol.1's Jingū Stadium/Dave Hilton anecdote, verified
   by web search); varied the three volumes' "How to Read"/"Question"
   sections so they don't read as structural clones of each other.
2. Added a direct "who this is for" line to each volume's opening,
   modeled on Chainsaw Man's "A Note Before You Begin."
3. Added the anime series' recurring "Let's get into it." transition
   and an invitation to disagree with the book's own answer — adapted
   to this series' third-person voice (no first-person "I" introduced,
   unlike the anime books' persona-driven voice).
4. Chapter-level pass across all 17 chapters in Vol.1 and Vol.2: varied
   opening sentences (numbers, fragments — every chapter previously
   opened "Subject + verb + exposition"), shortened several closing
   sentences that were long dependent-clause "bows," and split the
   densest paragraphs (250–350 words) at natural pivot points for
   Kindle readability.
5. Bonus find while close-reading Vol.1: Chapter 3 was titled "What
   'Light' Meant as an Insult" but the word "light" never actually
   appeared in the chapter — retitled to "The Line the Jury Was
   Actually Defending," which matches the chapter's real content (the
   junbungaku/taishū bungaku split). Worth spot-checking Vol.3's
   chapter titles against their bodies the same way at some point.

**Front-matter convention, all three volumes — updated twice, current
shape below:**

1st pass: moved the rights disclaimer to the very back of each book
(after "About the Author").

2nd pass (superseding "About the Author"'s placement from the 1st
pass): user asked for an even shorter, more immediate hook right at
the very top — before any explanatory material — and for "About the
Author" to move from the back to the front, positioned before "How to
Read This Book." Current final shape, all three volumes:

```
Title / subtitle / imprint
---
[2-3 sentence hook, no heading — immediate, concrete, no scaffolding]
---
## About the Author
[existing bio, unchanged]
---
## How to Read This Book
[existing "who this is for" note + trimmed framing paragraph,
 with the material now covered by the top hook removed so it's not
 repeated twice]
---
## THE QUESTION...
---
Chapter 1...
...
[back matter: Glossary, A Note on What Comes Next, Sources, then the
 rights disclaimer as the very last lines — About the Author no
 longer appears in the back matter, only at the front]
```

Each volume's top hook reuses material already established elsewhere
in that book (Vol.1: the Jingū Stadium/Dave Hilton anecdote, trimmed
down further since the fuller version still lives in "How to Read
This Book"; Vol.2: the Wind-Up Bird Chronicle phone/spaghetti opening
+ Nomonhan; Vol.3: the Nanjing passage + the seventy-four-year-old
return to the walled town) rather than introducing new claims — no
new fact-checking needed for these hooks.

This is now a bigger deviation from the sibling anime-book series'
own convention (which keeps About the Author at the very back, past
even the Sources section) — that's a deliberate choice for this
series specifically, not a mistake to "fix" back toward the anime
books' pattern. Vol.3's chapter-2-specific sensitivity note (on
discussing the Nanjing Massacre) is a different, content-specific
warning and stays where it is, directly before that chapter — it was
never part of this front-matter reshuffling.

## Master library list (prioritized, from a prior session)

The user got this list from a different Claude Code session/thread. It
doesn't survive in chat memory across sessions, only in this file from
now on. Status annotations added 2026-09-28.

**① Top priority — foundational for the whole series**
1. *Novelist as a Vocation* [職業としての小説家] (Shinchō bunko) — the
   original-Japanese account of writing in English and translating back.
   English translation (trans. Philip Gabriel & Ted Goossen) also
   wanted if available. **STATUS: Japanese text confirmed (Ch.2,
   「小説家になった頃」) and quoted in Vol.1 footnote 2. English
   translation edition not yet obtained — open if the user finds a
   copy, but not blocking.**
2. Jury remarks (選評) for the 81st and 82nd Akutagawa Prizes (1979,
   1980). **STATUS: done — and this one mattered far more than its
   "low priority" label suggested.** User found the full remarks on
   prizesworld.com (sourced to *Akutagawa-shō Zenshū* vol. 12, 1983).
   Checking them uncovered a real error, not just a missing citation:
   Vol.1 Ch.3 had Kenzaburō Ōe reviewing *Hear the Wind Sing* and
   calling it a "dead end" — he's recorded with **zero lines** on that
   candidate in the actual 81st-round remarks. His only documented
   comment on either Akutagawa round is on *Pinball, 1973* (82nd
   round), and it's a qualified compliment ("that can only be called
   clear talent"), not a dismissal. Ch.3's claim that Saiichi Maruya
   named "Vonnegut and Brautigan" was also unsupported by his actual
   remarks. Fixed across three chapters:
   - **Vol.1 Ch.1**: replaced an unverified "外国翻訳小説の読み過ぎ"
     characterization with Mitsuo Nakamura's actual, verified 82nd-round
     comment.
   - **Vol.1 Ch.3** ("What 'Light' Meant as an Insult"): replaced the
     false Ōe/Maruya-Vonnegut-Brautigan paragraph with the four jurors
     who actually commented on *Hear the Wind Sing* (Maruya, Takii,
     Yoshiyuki, Endō), quoted directly, and an explicit note that Ōe
     didn't comment on this round at all.
   - **Vol.1 Ch.4**: retitled from "The Critics Who Changed Their Minds
     — In Both Directions" to "What the Critical Record Actually Shows,"
     since the Ōe "dismissal to respect" arc doesn't hold up — rewrote
     as a myth-correction (Ōe was never the hostile early critic the
     popular story claims) sitting alongside Kawamoto's real, still-
     documented reversal.
   This is exactly the kind of error the verify-nonfiction-claims skill
   exists to catch — confidently written, specific, and wrong. Audit
   the rest of the trilogy's named-critic claims the same way if
   sourcing for them ever turns up.

**② For expanding close readings**
3. *The Wind-Up Bird Chronicle* Part 1 — (a) the opening
   spaghetti-boiling scene, (b) the start of Mamiya's Nomonhan
   monologue. **STATUS: done — (a) Ch.1, p.7, opening line "The phone
   rang while I was boiling spaghetti in the kitchen" quoted directly
   in Vol.2 Ch.2 with footnote 6; (b) Ch.12 opening, p.245, cited.**
4. *1Q84* BOOK 1 — opening scene, taxi with Janáček's *Sinfonietta*
   playing. **STATUS: done.** User photographed Shinchōsha's own
   online preview (試し読み) rather than a physical copy — same 2009
   edition either way. Now quoted directly in Vol.2 Ch.5 (a new
   subsection, since the chapter previously only covered the release
   as a sales phenomenon, not the opening's craft), cited to BOOK 1,
   Chapter 1, p. 11.
5. *Killing Commendatore* [騎士団長殺し] — the scene where Menshiki
   talks on the phone about Amada Tomohiko's brother Tsuguhiko, and
   the Nanjing death-toll line ("some say 400,000, others say
   100,000"). **STATUS: done.** User provided the exact Japanese text
   directly (typed, not photographed) from Part 2 [第2部
   遷ろうメタファー編] (Shinchōsha, 2017). Now quoted directly in Vol.3
   with a footnote and Sources entry. In the process, softened one
   overclaim: the manuscript had said the passage "asks, in effect,
   what real difference that gap actually makes" — the quoted text
   only confirmed as far as "the killing is an undeniable fact
   regardless of the exact count," so the stronger rhetorical-question
   framing was walked back to what's actually verified.
   **Follow-up, done:** note.com is blocked by this session's network
   egress, so WebFetch couldn't reach the Sasaki Atsushi essay the
   user linked — the user pasted its full text directly instead. Its
   thesis (the novel's "portrait of nothing" structure, and its final
   chapter's timeline reveal placing the story in 2007-08, ending on
   the day of the March 2011 disaster) is now incorporated into Vol.3
   Ch.2 as three new subsections, cross-referenced to Vol.2 Ch.3's
   *after the quake* material, with Sasaki's own hedges on the Vienna/
   Amada-brothers backstory preserved rather than flattened into fact.

**③ For translation side-by-side comparisons — need BOTH the Japanese
original and the English translation**
6. *Norwegian Wood* — Japanese opening already in hand; needed the
   English translation (Jay Rubin) to compare. **STATUS: done** — Jay
   Rubin, Vintage International, 2010, cited in Vol.1 Ch.7.
7. *Hard-Boiled Wonderland and the End of the World* — Japanese
   passages (the elevator scene, the golden beast scene) already in
   hand; needed the English translation (Alfred Birnbaum) to compare.
   **STATUS: done.** Both quotes now use Birnbaum's actual wording,
   cited to Vintage International, 2003 (year confirmed by the user):
   Ch.1 "Elevator, Silence, Overweight" (p. 3, "The elevator continued
   its impossibly slow ascent...") and Ch.2 "Golden Beasts" ("With the
   approach of autumn, a layer of long golden fur grows over their
   bodies..." — opening page number not visible/confirmed, noted as
   such in the footnote rather than guessed). Also caught and fixed:
   the manuscript's own English gloss of the chapter title (肥満) had
   said "Obesity" — Birnbaum's actual published title is "Overweight."

*Hear the Wind Sing*'s English translation (Birnbaum) only exists in
the bilingual Kodansha English Library edition, unlikely to be at a
foreign public library — deprioritize translation comparisons for that
title in favor of #6/#7.

## Done

- **Vol.1, Ch.7 (*Norwegian Wood*)** — opening-page "melody" quote
  replaced with Jay Rubin's actual translation (*Norwegian Wood*,
  trans. Jay Rubin, New York: Vintage International, 2010), cited from
  the user's own copy. Also corrected the claim that "yare yare" first
  appears in this novel — it's documented as first appearing in
  *Pinball, 1973* (1980) and established by *A Wild Sheep Chase*
  (1982).
- **Vol.2, Ch.2 (*The Wind-Up Bird Chronicle*)** — the "absence of any
  real guiding principle" claim is now anchored to Mamiya's own words,
  cited to the user's physical copy: *The Wind-Up Bird Chronicle*,
  Part 1 [ねじまき鳥クロニクル 第1部 泥棒かささぎ編] (Tokyo:
  Shinchōsha, 1994), Chapter 13 "Lieutenant Mamiya's Long Story, Part 2"
  (間宮中尉の長い話２), p. 263.
- **Vol.2, Ch.2** — Chapter 12, "Lieutenant Mamiya's Long Story, Part 1"
  (間宮中尉の長い話・1), opening page 245, confirmed and photographed:
  Mamiya's own account starts with his posting to the Kwantung Army
  General Staff's military-geography section in Manchuria in early
  1937. Added to Sources.
- **Vol.1, Ch.2 (*Novelist as a Vocation*)** — footnote [^2] and its
  Sources entry now cite the exact chapter (第二章「小説家になった頃」)
  and quote his own description of the process directly: typing in
  English, then sitting back down with manuscript paper and a fountain
  pen to "translate" (his scare quotes) that chapter into Japanese —
  "not a rigid literal translation... something closer to a free
  'transplantation'" (「移植」に近いもの). No page number was visible in
  the photos, so the citation is chapter-level only.
- **Vol.2, Ch.2** — Kano Creta's introduction: confirmed as **Chapter 8**,
  「加納クレタの長い話、苦痛についての考察」(user-photographed, pp.
  159–181) — her birth date, decision to end her life at 20, family
  background, and (pp. 179–181) becoming numb to physical pain and
  pleasure after that attempt, then being coerced by two yakuza who
  filmed and blackmailed her into sex work for their organization. This
  confirms the manuscript's "psychic prostitute" description is
  grounded in the text, not overstated. Added to the Sources list; kept
  the main text's phrasing brief given how graphic the source pages
  are. This chapter guess happened to match an earlier one of mine, but
  that's coincidence, not license to trust title-based guessing again.

## Open / candidates

- **Vol.2, Ch.2** — the dry-well scene (Toru Okada sitting at the
  bottom of a dry well). User has confirmed it is **not** Chapter 4.
  Chapter number still unknown — do not guess again; ask directly.
- **Vol.2/3, *The Wind-Up Bird Chronicle* Parts 2–3** — the user only
  owns Part 1 (第一巻) of the novel. Chapter 2 of Vol.2's manuscript only
  makes claims about the novel as a whole that are already confirmable
  within Part 1 (Mamiya's account, the well, Kano Creta), so nothing
  currently blocks on this. If a future claim turns out to depend on
  Part 2 or 3 specifically, don't ask the user to source it from Part 1
  — flag it as unverified/needs Parts 2–3 and wait until they have those
  volumes (they'll follow up once they do).
- See the master library list above for what's still open: *Novelist
  as a Vocation* (English ed.), Akutagawa jury remarks, the Wind-Up
  Bird spaghetti-cooking opening, *1Q84*'s taxi opening, *Killing
  Commendatore*'s Menshiki/Nanjing scene, and *Hard-Boiled Wonderland*'s
  English translation.

## Zero-quote chapters — close-reading expansion (2026-09-28)

User's own observation: several chapters discuss a single major novel
at full chapter length but currently quote nothing from it at all —
plot summary and interpretation only, no textual grounding. Nothing
here is wrong (nothing quoted, nothing to misquote), but it's thin for
serious criticism. Audited all three manuscripts for this; the real
list (excluding chapters that are legitimately not about one novel —
Nobel odds, Murakami Studies institutions, the Drive My Car adaptation,
verdict/synthesis chapters). **All five items below are now done as of
2026-09-29** — this was the whole list; no further zero-quote chapters
remain open in any of the three volumes.

1. **Vol.1, Ch.5, *A Wild Sheep Chase* [羊をめぐる冒険]** — **STATUS:
   done.** User photographed p. 230, the actual final scene: the J's
   Bar conversation (splitting the reward money, making J a partner)
   and the closing beach passage ("二時間泣いた... 生まれてはじめてだった"
   / "the first time in my life I'd cried that much," ending on "小さな
   波の音"/the sound of waves). Added as a new subsection with both
   quotes and a footnote, cited to Volume 2 [下巻], Kōdansha Bunko,
   1985 (user confirmed the edition after the fact).
2. **Vol.2, Ch.1, *Dance Dance Dance* [ダンス・ダンス・ダンス]** —
   **STATUS: done.** User typed out the Sheep Man's full "dance for as
   long as the music plays" speech directly (Kōdansha Bunko, 1991).
   Added as a new subsection with two direct quotes (the "don't think
   about meaning" passage and the closing line), replacing what had
   been only a paraphrase.
3. **Vol.2, Ch.4, *Kafka on the Shore* [海辺のカフカ]** — **STATUS:
   done.** User typed out the sandstorm monologue directly (Shinchōsha
   Bunko, 2002). Added as a new subsection ("A Storm That Turns Out to
   Be Yourself") before the reception-history material, tying the
   "fate as a storm that's actually you" passage to the chapter's own
   point about the novel staying mysterious even to devoted domestic
   readers.
4. **Vol.3, Ch.3, *The City and Its Uncertain Walls* [街とその不確かな
   壁]** — **STATUS: done.** User photographed pp. 18–20: the golden
   beasts' autumn transformation (directly echoing *Hard-Boiled
   Wonderland*'s "Golden Beasts" chapter, quoted in Vol.1 Ch.6 — same
   image, 38 years apart), the Gatekeeper's daily razor/horn ritual,
   and the previously-undocumented spring mating-week violence. Added
   as a new subsection ("What Carried Over, and What Got Built Out")
   comparing this version directly to the *Hard-Boiled Wonderland*
   material Vol.1 already quoted.
5. **Vol.3, Ch.1, *Colorless Tsukuru Tazaki*** — **STATUS: done,
   2026-09-29.** User got the book a day early and ended up
   photographing both candidate passages, not just one. Added two new
   subsections to Chapter 1:
   - **"A Blankness That, For Once, Doesn't Hurt"** (p. 121) — the
     university-pool scene with Haida, quoted directly: Tsukuru
     watching Haida's kick stir bubbles through the water, and the
     "light paralysis of consciousness" it brings him. Tied to the
     novel's recurring 空っぽ/"empty" self-description — the one place
     that blankness reads as restful rather than a wound.
   - **"Twelve Rings, and a Light Going Out"** (pp. 366–369) — the
     phone ringing twelve times while Tsukuru hesitates to answer
     Sara's call, and the novel's actual final paragraph (Tsukuru
     falling asleep without knowing her answer, ending on "the sound
     of wind moving through a stand of white birch trees"). Ties into
     the chapter's "recovery, not resolution" argument.
   New footnotes [^2] (pool scene) and [^3] (ending), in that order to
   match where they appear in the text — all later footnotes in the
   volume renumbered twice in the process (originally 2–11; briefly
   3–12 after the first addition; now 4–13 after the second). Verified
   sequential, no orphans, each round. **Caveat logged in footnote
   [^3] itself:** the ending's English wording is a working
   translation, not Philip Gabriel's published one — a websearch
   surfaced what claims to be his wording for the closing line, but it
   added imagery ("sucked into the depths of the night") not present
   in the photographed Japanese, so it wasn't trusted and a plainer
   literal gloss was used instead. Worth a side-by-side check against
   the actual Gabriel translation if an English copy turns up later,
   same as Vol.1/Vol.2 did for other novels. Edition/printing of the
   user's physical copy also not yet confirmed (page numbers 121 and
   366–369 suggest the single-volume Bunshun Bunko paperback, but
   that's an inference, not confirmed) — update the Sources citation
   once known.

(All five done — see status notes above.)

## Follow-up audit: other named-critic claims (2026-09-28)

Prompted by the Ōe finding, checked two other named-critic claims that
had the same vague-citation pattern ("appears across his published
criticism," "is documented in contemporary reporting" with no actual
article named). Both held up as substantively accurate, unlike Ōe, but
both got upgraded to real, specific citations since a vague footnote
is itself a risk even when the underlying claim turns out true:

- **Vol.2, Katō Norihiro's "detachment" pushback** — confirmed via web
  search. His argument runs through *Murakami Haruki no Sekai*
  (Kōdansha) and *Murakami Haruki wa, Muzukashii* (Iwanami Shoten,
  2015). Footnote and Sources entry now name both books instead of
  gesturing at "his published criticism" generally.
- **Vol.3, Hyakuta/Sakurai/Sankei criticism of the Nanjing passage** —
  confirmed and enriched via web search. Real, specific detail found
  that wasn't in the manuscript before: Hyakuta's actual complaint was
  that Murakami was currying favor with China (and Nobel momentum) by
  including the passage; Sakurai quoted the passage's actual content
  back at his followers rather than objecting in the abstract; *Lite-Ra*
  published a rebuttal arguing the novel as a whole argues against
  historical revisionism. Footnote and Sources now cite the actual
  *Lite-Ra* and People's Daily Online articles instead of a vague
  gesture at "contemporary reporting."

No more Akutagawa 選評 exist to check — Murakami was only ever
nominated twice (81st and 82nd), both already covered in Vol.1. If
further named-critic claims turn up elsewhere in the trilogy with this
same "vague citation, no real title/quote" pattern, check those too —
it's a reasonable general audit heuristic now, not just a one-off.

## Notes

- Don't trust a chapter-title match from a web search as confirmation
  of content — the Ch.4 mistake happened because a title mentioning
  "Nomonhan" was assumed to be where the Nomonhan narration starts.
  Always confirm against the user's physical copy or an explicit
  chapter-content description before citing.
- 南京虫 (nankinmushi) = bedbug/louse, unrelated to 南京 (Nanjing) the
  city — a false-cognate risk specific to this trilogy since Vol.3
  covers the actual Nanjing Massacre. Doesn't affect anything cited so
  far, but worth remembering when reading further Wind-Up Bird Chronicle
  material.
