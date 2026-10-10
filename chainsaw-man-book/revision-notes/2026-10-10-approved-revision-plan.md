# Chainsaw Man (English) — Approved Revision Plan / 改訂作業記録

**Created:** 2026-10-10 (JST)  
**Status:** EDITORIAL CHANGES APPROVED; THIS FILE DOCUMENTS THE PLAN. Source manuscript, diagrams and EPUB have **not** yet been modified as part of this record.  
**Project:** *Chainsaw Man: The Devil in the Details* — Jiro Naozane / Japanese Culture Press  
**ASIN:** B0HKDYK4CQ  
**Repository branch:** `claude/festive-clarke-cnoct4`  
**Source-of-truth:** `chainsaw-man-book/manuscript.md` (per `chainsaw-man-book/README.md`).

## Reference and provenance

The user supplied an English-language EPUB on 2026-10-10: `チェンソーマン英語版.epub`, **4,192,074 bytes**, SHA-256 `c2dc0cdf8d286899949aa87691f50a4721c6dd7801208ea3fa197732153f26e5`. This attachment is **not yet checked into this branch**. Inspection found 22 embedded images and an intact ZIP archive; four distinctive passages were confirmed to match `chainsaw-man-book/manuscript.md` (Intro date wording and three Chapter 13 phrases). This is **not** proof that the complete repository source and attached EPUB are identical; compare them before final rebuild.

Repository inspection on 2026-10-10 found an original English manuscript, an existing generated EPUB, and chart/cover/chapter-opener assets in `chainsaw-man-book/`. Preserve these originals. Do **not** hand-edit the binary EPUB: edit Markdown, regenerate under a **new filename**, and verify the resulting book and diagrams. Do not publish to KDP or resume/edit Amazon Ads without an explicit new instruction.

## Editorial agreement (2026-10-10)

The author **approved** the proposed limited factual corrections, spoiler-warning alignment, Chapter 13 linguistic corrections, and necessary edits in Chapters 2, 7, 10 and 12. Preserve the existing 14-chapter structure, independent critical perspective, and all existing illustrations. Larger reinterpretations or major reordering require separate approval.

### Priority A — Spoiler system (confirmed defects in repository Markdown)

- `manuscript.md` under `HOW TO READ THIS BOOK` says that **only two chapters near the end** are fully manga-only. Inconsistent with manga-only chapters 10, 11, 12 and other advance disclosures. Rewrite guidance accurately.
- `INTRODUCTION` and Chapters **1, 2 and 3** carry `[Anime-safe]` labels although text reveals later manga developments. Chapter 1 explicitly identifies Makima and describes her eventual fate. Chapters 2 and 3 discuss Part 2 and later characters. Treat the novel spoilers as primary-reader material, rather than deleting analysis to cater to anime-only readers.
- Chapter 7 reveals Makima's identity **before** its internal `[Manga-only, spoilers ahead from here]` warning. Change placement/labels so warnings precede sensitive information.
- Chapter 8's opening label claims Power/Himeno are anime-safe and Reze movie-safe, but later sections discuss Nayuta and Asa. Add a clear manga-only transition **before** those sections and mark the chapter mixed-spoiler, or conservatively label all as manga spoilers.
- Chapter 4's mixed warning, and Chapter 10–12's major manga spoilers should be retained/refined based on an explicit chapter-by-chapter pass; do not assume old classifications are correct.
- Two **rasterized** diagrams, `images/charts/whats_inside.png` and `images/charts/spoiler_map.png`, also reflect old classifications. They must be updated to agree with the prose. Preserve design/legibility; do not merely alter source Markdown and leave images contradictory.
- After changes, verify every one of 14 chapters against manga/anime scope and check the EPUB's front and back matter.

### Priority A — Chapter 13 Japanese-language accuracy (confirmed wording)

1. Current: `"built entirely out of native Japanese vocabulary"` for `銃の悪魔 (jū no akuma)`. **Incorrect:** `銃` and `悪魔` are Sino-Japanese; `の` is a Japanese particle. Suggested replacement:  
   > The Japanese name for the Gun Devil is 銃の悪魔 (*jū no akuma*). The nouns *jū* (gun) and *akuma* (devil) are Sino-Japanese, joined by the native Japanese particle *no*. This contrasts with the title *Chainsaw Man*, whose English-derived words are written in katakana.
2. Current: `"Denji calls almost nobody by an honorific"`. Qualify, with particular attention to **マキマさん / Makima-san**. Confirm exact dialogue in the original Japanese before turning this into a claim about broader honorific frequency. Proposed direction: contrast Denji's blunt default speech with his use of `-san` for Makima, without pretending one example proves a universal rule.
3. Current: `"a gruff, heavily accented ... 'old soldier' register"` for Kishibe. **Unsupported as written:** gruff/direct speaking is not evidence of strong regional accent. Remove the regional/accent claim unless demonstrated from Japanese panels. Prefer: `Kishibe's clipped, blunt manner of speaking helps establish his veteran authority.`
4. Current: `"the oldest, most universal fears get named in the language's oldest words"`. Too broad: vocabulary strata do not map neatly to the age/universality of fears. Reframe as the coexistence of Sino-Japanese words, native particles, and katakana loans. Do not claim a particular fictional naming choice proves Fujimoto's intent.
5. If expanding discussion of `悪魔` and Japanese religious vocabulary, distinguish documented linguistic history from interpretive associations. Do not invent original Japanese lines or scenes.
6. Reference to `"this book's companion volume on anime culture"` requires verification that a **specific actual volume** exists; otherwise remove or rephrase as a general reminder.

### Priority A/B — Other passages flagged for targeted verification

These are **editorial findings/candidates**, not a substitute for checking primary manga chapters or official publication records:

| Source | Current text / issue | Proposed handling |
|---|---|---|
| Introduction | `"chapter 232 posted a week later"` | Check official dates of chs. 231 and 232; previous audit suggests **two weeks**, not one. Fix only after source confirmation. |
| Ch. 2 | Pochita's apparent weakness compared with actual powers | Avoid equating his small/weakened appearance with a permanently weak devil. |
| Ch. 7 | `"the human vessel of the Control Devil"` | Makima is the Control Devil, not a human host; correct terminology and placement of spoiler warning. |
| Ch. 7 | `"Pochita offering himself to be eaten"` | Check events and distinguish a heart/contract from being eaten. Preserve broader critical argument only if supported. |
| Ch. 8 | Nayuta `"carrying an adult devil's fragmented memory"` | Treat continuity of identity, memories, and instincts as separate claims; verify before asserting. |
| Ch. 10 | `"Fami ... connected to the Famine Devil"` | Reflect completed-manga identity revelations; verify chapters and phrasing before revising interpretation. |
| Ch. 10 | Denji `"enrolled, under a fake identity"` | Clarify concealment of his Chainsaw Man identity versus attending school under a fake personal name. |
| Ch. 11 | `"the finale this book spent Chapter 10 unpacking"` | Internal chapter reference likely should be Chapter **12**; check references comprehensively. |
| Ch. 12 | Pochita, Denji, Nayuta/Asa and ending timeline | Check exact sequence; do not inadvertently imply that all relationships remain intact at the end. |
| Ch. 6 | Internal reference to `"the whiplash Chapter 7 spent time on"` | Check whether Chapter **9** is the intended reference; repo notes suggest an earlier fix may already have occurred. |
| Front matter | Author bio/affiliation claims | Ensure pen-name narrative cannot be mistaken for invented verifiable institutional credentials. |

**Important:** Prior audit included hypotheses about source material and external dates. They must not be represented as independently verified facts. Separate confirmed text defects from pending original-work fact checks in the eventual changelog.

## Secondary writing and product improvements (after factual fixes)

- Use `english-writing-lab` editorial principles: specificity, natural rhythm, concrete evidence, restrained claims, serious engagement with counterarguments. Do **not** homogenize the writer's voice or globally rewrite all chapters.
- Preserve 14 chapter-openers and existing chart/guide assets; optimize size only when actual KDP delivery cost warrants it.
- Inspect Kindle Previewer / sample opening; an engaging argument should appear early, with front matter not swallowing most of the preview.
- Draft a **separate** U.S. Amazon description using the approved central line `Chainsaw Man Is Over. But What Did It All Mean?`, truthful book contents, and KDP-supported HTML/character limits. Do not update Amazon listing automatically.
- Ads remain **paused**, and ad settings/budgets may not be modified without specific approval. Historical audit (user-supplied, 2026-09-01–10-10): 3,346 impressions, 14 clicks, USD 9.44 spend, 0 attributed orders. These are not validated keyword conversion results.

## Deliverables and verification protocol

- [x] Locate actual English book directory on its existing Claude branch.
- [x] Record the user's approved scope, preserving existing source and art.
- [ ] Compare attached 2026-10-10 EPUB comprehensively with branch `manuscript.md`; resolve divergences before editing.
- [ ] Verify every spoiler label and all chart classifications.
- [ ] Verify Chapter 13 claims against Japanese text and reliable dictionaries.
- [ ] Make targeted Markdown edits and write an itemized change log; preserve original as retrievable Git history.
- [ ] Regenerate corrected diagram assets while preserving their style.
- [ ] Build an EPUB with a **new filename**, not the existing published EPUB's filename.
- [ ] Run `epubcheck`, verify internal links/TOC, inspect chapter image/chart presentation, and use Kindle Previewer where available.
- [ ] Deliver proposed KDP product description and modest post-update sales-test plan **separately**.
- [ ] Get approval before any KDP publication, ad changes, or material narrative reinterpretation.

## Coordination with Claude Code

Claude Code should start from this branch and read `chainsaw-man-book/README.md`, this revision record, `manuscript.md` and the image assets. Do not overwrite uncommitted local changes, silently discard new work, or assume this branch's generated EPUB is the October 10 attachment. Do not modify the Japanese translation branch/folder while revising the English title.
