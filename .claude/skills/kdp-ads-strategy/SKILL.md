---
name: kdp-ads-strategy
description: Use when reviewing Amazon Ads (Sponsored Products/Brands) performance data for this project's Kindle books, deciding whether to adjust targeting or budget, or when the user shares an Ads Console screenshot or asks for marketing/advertising advice on these titles. Use as a diagnostic checklist for interpreting campaign metrics, and as a growing, dated log of what's actually worked for these specific books — not generic marketing advice.
---

# KDP / Amazon Ads Strategy for This Project's Books

This skill exists to accumulate real, book-specific advertising knowledge over time, the same way `verify-nonfiction-claims` grew out of this project's own factual mistakes rather than generic writing advice. It starts thin, on purpose. Every time a real campaign decision gets made here and its outcome becomes visible, add a dated entry to "What we've learned" below — that log is the actual point of this file, more than the checklist above it.

## Reading a performance snapshot without overreacting

- **Small-account KDP ad spend produces tiny sample sizes.** A few thousand yen of spend and single-digit purchase counts are not enough data to call a campaign "working" or "broken." Before changing strategy based on one week's numbers, check the cumulative window (30 days is usually the first meaningful one) and don't treat a single zero-sales week as a verdict — it's very likely noise at this scale.
- **Separate the CTR problem from the conversion problem.** Impressions → clicks tells you whether the ad is being shown to and noticed by a plausible audience. Clicks → purchases tells you whether the product page itself closes the sale once someone's there. A reasonable CTR (roughly 0.3%–1%+ is normal for Sponsored Products) with zero downstream purchases points at the listing (cover thumbnail, title, price, description) or at mismatched targeting — not at ad visibility. Don't "fix" the wrong half of the funnel.
- **The single highest-leverage, lowest-effort action available on any dashboard check-in**: open the "underperforming targets" / search-term report, sort by clicks descending with zero orders, and pause or negative-match the ones that are clearly off-target. Worth doing on essentially every review, regardless of anything else that's happening.
- **Cross-check active ad targeting against the KDP keyword list actually chosen for the book** (see each book's own `README.md` → "Suggested KDP Metadata" / KDP keyword section). If a campaign is running on Amazon's automatic targeting, pull the search-term report and confirm the queries actually driving clicks resemble the high-intent phrases the book was positioned around — not generic franchise-name traffic that was never going to convert into a critical-analysis purchase specifically.
- **Budget too small to learn from is a real, distinct failure mode from "the campaign doesn't work."** If total weekly clicks are in the single digits, the targeting algorithm doesn't have enough signal to optimize. Before concluding a keyword set or targeting strategy has failed, make sure the campaign actually got enough traffic (rough rule of thumb: tens of clicks, not single digits, per week) to judge it fairly.
- **A book's own README keyword list and its live ad targeting can drift apart** — the keyword list gets updated in this repo, but nothing pushes that update into an already-running Amazon Ads campaign automatically. Treat a mismatch between the two as a routine thing to check, not a one-time setup step.

## What we've learned (dated log — add to this, don't just read it)

- **2026-09-20 — first campaign snapshot reviewed.** ¥1,096 spent over ~30 days, 3 purchases, ¥1,365 sales, ROAS 1.25 (net positive, but on an n of 3 — not enough to trust yet). Most recent 7-day window: 706 impressions, 8 clicks, 0 conversions. CTR (~1.1%) was fine; the stall was purely at the conversion step. Sample size judged too small to draw a real conclusion either way. Recommended next steps: (1) open the "clicks but zero sales" target list and prune obviously off-target entries, (2) confirm auto-targeting search terms actually match the book's KDP keyword positioning, (3) let the campaign accumulate more clicks before revisiting rather than reacting to one flat week. No budget or bid changes were made at this checkpoint. Outcome of the pruning step: not yet known — update this entry (or add a new one) once it is.

## Open questions to resolve as more data comes in

- What ROAS threshold, specifically for this project's ~¥1,000-ish-priced companion books, actually represents "worth continuing" once KDP royalty rate and Amazon's ad fee are both netted out? Not yet calculated — needs an actual royalty-per-copy number plugged in.
- Does automatic or manual (keyword) targeting perform better for this specific genre (anime/manga critical-analysis nonfiction)? No comparison run yet.
- Whether running separate campaigns per book vs. one shared campaign changes anything meaningful for cross-promotion (the "Also by Jiro Naozane" convention in each book's KDP description exists partly to support this) — untested.
