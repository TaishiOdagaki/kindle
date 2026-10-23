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

## 2026-10-23 continued editorial comparison
- Materialized 2027 first editorial DOCX, 2026 version with 32 shortened options, and 2026 fifth edited DOCX. Compared using python-docx: all have 7,329 body paragraphs, 500 numbered question headings and 10 tables. 2027 first edition vs 2026 fifth edition differs in only 11 paragraphs, mainly title/frontmatter/section headings; all table-cell text identical. This comparison does not establish equality against any *later* W6 academic master.
- Found a concrete 2027 TOC defect: duplicated text '基礎試験60問＋応用試験15問（計75問）基礎60問＋応用読解15問（計75問・聴解なし）'. Created second 2027 editorial draft with the line corrected to '基礎60問＋応用読解15問（計75問・聴解なし）'. File: 2027_パーフェクト問題集_第2次編集稿_要内容確認.docx, local working container; not yet committed in repository.
- The new Word is NOT publication-ready: full render and page-by-page visual QA have not completed; academic-master binary content has not been fully retrieved, so full scholarly alignment remains unverified. Keep release_ready=false.
- Next actions: verify Word render; materialize/compare academic master and W6 word; reconcile any later academic changes; review claims in 2027 frontmatter and regenerate EPub only after content freeze.

## 2026-10-23 structural regression on second 2027 editorial DOCX
- Inspected `/mnt/data/2027_パーフェクト問題集_第2次編集稿_要内容確認.docx`, SHA-256 `d169296d0d147b55afc378fabbed2f0556178431998148097ceeedd9e71c84d7`.
- Independent python-docx/OOXML check: exactly 500 question headings, 500 with four numbered options, 500 explanation headings, 10 tables, 2,059 internal hyperlink anchors, zero missing destinations. Word paragraph count 7,329.
- Initial simple parser flagged two questions Q_2_023 and Q_5_094 due to multi-paragraph dialogue/composition stem; corrected parser confirmed 500/500, not manuscript errors.
- Result does **not** establish correct scholarship, question-to-answer semantic accuracy, or final visual Kindle quality. Manuscript unchanged. Structural regression report produced locally at /mnt/data/2027_構造検査結果.json.
- Next: obtain full scholarly master, compare 500 ID full fields, render/visual-QA complete 2027 Word, and prepare final EPUB. Release remains blocked until content and publishing gates are met.

## 2026-10-23 paragraph-level alignment check
- Compared 2027 second editorial DOCX against 2026 fifth-edited DOCX with python-docx, 7,329 paragraphs each.
- Differences only at paragraph indices 0,1,2,5,7,9,29,30,3178,3730,6729 (title, explanatory frontmatter, TOC and closing exercise labels). All tables identical in OOXML and question/answer/explanation paragraphs unchanged.
- Thus 2027 current editorial draft inherits the 2026 fifth-edited question corpus; it is NOT yet proven identical to a later W6 academic master.
- Local independent comparison report: `/mnt/data/2027_第7次照合報告.md`.
- Still pending: obtain full W6 master data, match question-level content and reconcile subsequent revisions; final EPUB and Kindle QA. Publishing not approved.

## 2026-10-23: supplemental scholarly edits identified
- GitHub academic_master_500_20261022.json remains unreadable via connector (empty content for whole/ranged read); metadata blob SHA c4252ee33ba264fee3aeb4033ebc25b7261a4094.
- Successfully read `audit/v9/academic_master_supplemental_edits_20261022.json`: exactly 69 records. Field types: case_text, stem_continuation, glossary, table_cell. Includes CASE_O_01/03/05/07/10, CASE_MO_02/03, Q_3_029, Q_4_067, Q_5_008 and others. THESE ARE HISTORIC EDITS, not 69 confirmed omissions from the 2027 DOCX.
- Read `audit/v9/evidence/20261022_academic_master_integrity_gate.json`: academic baseline 500 questions, 2000 option explanations, zero structural errors; 32 length-cue issues in this pre-publication academic baseline. Later 2026 edited lineage reportedly addressed those 32, thus do not report 32 outstanding problems for the 2027 draft without live rerun.
- Crucial next task: check the 69 `after` edits against the 2027 second DOCX, distinguish present/absent/nontrivial contextual conflict, and avoid duplicate insertion. If academic master cannot be read, use these supplemental records and independently validated 2026 release as a partial controlled crosscheck; state coverage precisely. No automatic source-substance approval.

## 2026-10-23 supplemental edit spot verification
- Tested three source edits using exact string matching against 2027 second editorial DOCX (library file ID file_00000000da488211a71b772308dbf734). Case O01 revised initial scenario sentence found at parsed text line 6854; superseded old version not found as exact phrase.
- Case O03 revised heading 'ケース3　会社のウチとソトに応じた待遇表現の指導' found at line 7061; superseded heading not found.
- Case O03 revised explanation example '部長の田中は、このように申しておりました' found at line 18032.
- Therefore at least these examples of the 69 supplemental edits are already included. **Do not reapply them.** This is spot verification only, not a 69/69 comparison or independent factual endorsement.
- The full large academic_master_500_20261022.json could not be obtained through GitHub's text connector (empty content); the metadata QA is not an alternative to comparing manuscripts.
- Next: compare remaining supplemental changes at field/paragraph level and record presence by ID, then verify academic master and final EPUB. No manuscript changes. Publication not approved.

## 2026-10-23: all 69 supplemental edits reconciled against 2027 second editorial draft
- Loaded all 69 records in audit/v9/academic_master_supplemental_edits_20261022.json, and all 21,095 lines of parsed 2027 second-edition DOCX (22 paged text reads). Compared normalized whitespace for each nonempty `after` and empty-after deletion candidates.
- 28 edits: revised `after` text exists in current 2027 draft. 40 deletion records: old `before` passage absent. 1 interim change: CASE_O_07 record 49 `after` text absent, but record 50 uses record 49's after as its before, explicitly supersedes it, and record 50's after text exists in current text (included among 28). This is intentional sequential revision, NOT an omission.
- Thus 69/69 historical supplemental records are accounted for by presence/deletion/supersession at text level; no new edit warranted. This is not independent scholarly correctness verification; pure matching doesn't validate case/explanation consistency or final whole-master equality.
- Next: full academic master vs 2027 DOCX substantive comparison, 2027 claims, page rendering/EPUB QA. Do not replay earlier superseded versions. Publication still not approved.
