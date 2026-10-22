---
name: evidence-based-editorial-workflow
description: Use for multi-step research, manuscript revision, quality audits, publication preparation, or interrupted agent work. Require traceable evidence, a single source of truth, and human publication approval.
---

# Evidence-Based Editorial Workflow v1.0 (2026-10-22)

## Trigger
Apply whenever working on article research, Japanese/English writing experiments, Kindle/EPUB book revisions, quality audits, repository-backed editorial pipelines, or resuming an interrupted task. This is a process skill, not a substitute for each project's editorial or research standards.

## Responsibility split
- **Chat**: agree scope, quality standards, expert/editorial judgments, release decision.
- **Work / execution tools**: batch file operations, validation scripts, evidence collection, transformations, reports.
- **GitHub**: canonical work products, audit ledger, decisions, checkpoints and resumable state.
- Do not assume Work intrinsically supplies better factual judgments than Chat. Both require independent evidence checks.

## Before editing
1. Read local AGENTS.md and project-specific guidelines; local safety, copyright and editorial constraints take precedence.
2. Identify exactly ONE canonical source and version/ref/commit. Never silently merge different manuscripts or treat matching answer keys as matching question text.
3. Record scope, inventory, baseline, immutable publication snapshots, expected deliverables and explicit **done criteria**.
4. Check git status/branch and protect unrelated or uncommitted changes. Avoid edits to published snapshots; branch for new editions.

## Four independent review gates
- **Structure**: identifiers, ordering, completeness, links, answer/explanation alignment, schema, duplicates.
- **Substance**: claim accuracy, sources, evidence quality, answer uniqueness where relevant, uncertainty, fact-vs-interpretation.
- **Editorial quality**: audience, originality, clarity, interest, rhythm, genre fit, coverage and redundancy.
- **Publication**: file format, render, metadata, hyperlinks, contents, accessibility and destination requirements.
Never report an overall PASS merely because mechanical checks or successful export passed.

## Evidence ledger
Record per unit/artifact: stable ID, canonical source version, gate, status (NOT_STARTED / IN_PROGRESS / PASS / FAIL / NEEDS_HUMAN / BLOCKED), finding, evidence URL/document locator and access date, proposed fix, applied commit, recheck evidence, reviewer and timestamp. Do not invent completed reviews or metrics. Clearly distinguish automated checks, AI appraisal and verified human approval.

## Fix / recheck discipline
1. Inventory findings without silently rewriting canonical text.
2. Triage and plan a bounded change set.
3. Apply edits to tracked files and link each to findings.
4. Rerun affected tests **and** full regression checks where possible.
5. Compare canonical versions and report unresolved risks. A changed passage invalidates its prior review until rechecked.

## Checkpoints and continuity
After each bounded batch (e.g., 20–25 questions or a defined set of articles), save the ledger, source ref, completed IDs, failed IDs, next action and artifacts in GitHub. On resume, read these files first; avoid redoing passed, unchanged units. When execution cannot continue, record blockers and remaining work; do not imply background work is running.

## Release gate
Provide concise summary of each review gate, evidence coverage, open blockers, version/ref and rendered output checks. Mark 'ready for human review' only if defined release conditions have been met. **Never publish, push public articles, alter prices/ads or declare final approval without the user's explicit authorization.**

## Project-specific application
- **Japanese Writing Lab**: preserve discovery/read/analysis distinctions, attribution and rights; test new techniques in actual drafts. No fabricated engagement statistics.
- **English Writing Lab**: preserve genre-specific judgments, independent verification and the candidate→tested→adopted lifecycle; cross-language transfer remains a hypothesis.
- **English criticism / Kindle**: distinguish facts about the work and verifiable publication details from cultural interpretation; check spoilers, edition-specific source facts, rights, chapter links, EPUB validity, reader-facing rendering and KDP metadata.
- **500-question exam books**: track per-question stem/options/key/explanation and independent subject-matter review; number alignment is not proof of knowledge accuracy.

## Completion report
State: canonical ref, checked scope by gate, PASS/FAIL/NEEDS_HUMAN counts, fixes and regression outcome, unresolved issues, saved checkpoint path, publication approval status. Never call a partially checked manuscript 'fully audited'.
