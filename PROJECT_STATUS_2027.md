# 2027 edition checkpoint

Updated: 2026-10-23

Canonical audit starting point: audit/v9-merge-matrix-2026-10-22.
Audit decisions: audit/v9/decisions.json; 500 entries marked confirmed. These are not equivalent to 500 resolved integration choices.

Next: identify merge decision ledger and canonical manuscript, reconcile pending differences against 2027 first editorial draft, then perform regression checks. Do not redo unchanged passed reviews. Preserve the published 2026 edition.

Release: NOT APPROVED. Do not publish without user approval.

## 2026-10-23 resume verification
- Verified three branches: audit/v9-2026-10-12, audit/v9-integration-2026-10-21, audit/v9-merge-matrix-2026-10-22.
- Confirmed audit/v9/decisions.json has 500 entries with status 確認済み in all three branches. The 2026-10-22 blob is 48355492ed19384148cf286b2b8d13fdec9c3d72; earlier branches use 2fb43017ad5a0a5b11be00fce1fb734442937e29. These statuses do not prove all merge decisions or the latest manuscript.
- Library report 2026_500問_統合稿_品質検査報告.md says an integrated Word adopted all 500 stems, 2000 options and 2000 individual explanations from academic GitHub audit source, with separate editorial additions. Another library artifact, 2027年度向け 第1次編集稿.docx, is a derivative and has not been demonstrated to incorporate subsequent W6 changes.
- Historic library comparison: answer positions matched 500/500 while complete stem matches were 31/500, all-option matches 33/500, all-explanation matches 7/500, and fully identical questions 7/500. Do not interpret answer-key equality as manuscript equality.
- Next action: locate actual merge-matrix decision ledger and canonical manuscript by exact path and revision, confirm whether W6 has a newer checkpoint; compare hashes/IDs to 2027 first editorial draft before any rewrite. No question text changed in this session.
- Release status: BLOCKED pending canonical file verification, substantive unresolved issues and publication gate. User approval required.

## 2026-10-23 continuation: resolved W6 file locations and editorial collision
- Identified W6 resume ledger: audit/v9/CONTINUE_20261022.md.
- Identified merge-screening matrix: audit/v9/evidence/20261022_cross_track_merge_500.csv, with review explanation at audit/v9/evidence/20261022_cross_track_merge_matrix_review.md. Screening categories 449 content_differs, 42 no_stem_change_history, 8 substring, 1 match. These are stem-excerpt comparisons, **not** 500 decisions about fully verified manuscript equivalence.
- Identified academic data candidate: audit/v9/academic_master_500_20261022.json, blob SHA c4252ee33ba264fee3aeb4033ebc25b7261a4094. Not yet validated/read end-to-end: GitHub connector returned empty/truncated content for this large file. Do not claim it is a final master.
- Identified published-2026 candidate revision metadata: publishing/2026_exam_last_minute_20261022/round2_20_revisions.json, round3_7_revisions_20261022.json, and continuation report recording cumulative 32 revisions in a separate artifact.
- W6 had an *alternative* editorial proposal at publishing/revised_edition_20261022/new_edition_editorial_spec.md with title 正解と誤答の理由がわかる500問. That is NOT the user-selected 2027 title. Current authorized 2027 working title is 登録日本語教員試験 パーフェクト問題集; do not silently inherit the alternative new title or rewrite the book as a different project.
- W6 archive mentions a separate GitHub 395-page Word and 2026 integrated 373-page Word. They are different binaries; the latter is reflected in 2026 published edition's lineage. Do not combine visual-QA counts or falsely claim remaining 109 pages of former are the current 2027 draft's pages.
- Next: obtain complete academic master file plus last confirmed Word binary, compare the 500 ID fields against 2027 first edited Word and 2026 published release. Determine exact intended master, then check substance for unresolved changes and run regression. Preserve 2026 book, no KDP publish.
