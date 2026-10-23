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

## 2026-10-23: 2027 edition title/section editorial fix
- Checked 2027 second editorial Word for wording that implies full simulated exam. Five instances of `本番予想模擬試験〈短縮演習〉` occur in subtitle, contents, problem section and explanation heading despite frontmatter correctly explaining only 75 shorter exercises (60 basic, 15 applied reading, no listening).
- Created 2027 third editorial Word in current session, replacing only these five instances with `実戦演習〈短縮版・75問〉`; source manuscript other 7,324 paragraphs unchanged. New SHA-256 `88e2c620374af6acd6fe6a78341351f7c1cd212a4ec38a3fbe71181ab5b81389`.
- New working file: `2027_パーフェクト問題集_第3次編集稿_出版前確認.docx` (conversation attachment, NOT tracked in GitHub). Do not call it typeset/approved; no full visual render QA conducted yet.
- Identified dated 2026 source claims at paragraph indices 70,98,106,113,120,155,285,292,3189,3785,3802,3975 etc. Preserve the cited dates until new official-source audit; do not silently rewrite historical question conditions as 2027 facts.
- Academic-master full-field comparison, visual QA and EPUB publication QA still open. User KDP publication approval not given.

## 2026-10-23 visual-render continuity / PDF mechanical QA
- Current third 2027 editorial DOCX converted to A4 PDF: 373 pages, PDF stored in working session as `2027_render_check/2027_パーフェクト問題集_第3次編集稿_出版前確認.pdf` (not committed).
- Examined text blocks on all PDF pages with PyMuPDF: 373/373 contain text; zero blocks outside page bounds. No empty pages. Short-text pages 171–182 are answer-key tables, not missing text, as confirmed by PDF extraction.
- Existing DOCX a11y audit JSON reports high=0, medium=0, low=0; that doesn't certify factual or visual quality.
- 146 page images exist from interrupted full rendering; full 373-page image-by-image visual review NOT completed. Do not claim final pass.
- Academic master all-field comparison remains blocked by full source binary read. EPUBCheck/Kindle Previewer not done; release_ready=false.

## 2026-10-23 EPUB candidate built from 2027 third DOCX
- Source DOCX: 2027_パーフェクト問題集_第3次編集稿_出版前確認.docx.
- Generated via pandoc: 2027_パーフェクト問題集_出版前検証候補.epub (current conversation artifact, not committed).
- EPUB ZIP CRC inspection (`testzip`) passed. Parsed EPUB3 XHTML/nav: 2061 internal links, 0 unresolved destinations/anchor IDs.
- Text scan shows revised `実戦演習〈短縮版・75問〉` appears 5 times, former `本番予想模擬試験` 0 times in main XHTML.
- Pandoc emitted missing Japanese translation warning; EPUBCheck official tool not run, Kindle Previewer not run, all-page visual EPUB QA not run. Candidate is NOT final/publishing-approved.
- Preserve previously confirmed 373-page DOCX mechanical QA and academic master block. Next: epubcheck and reader rendering, content equivalence, official 2027 policy updates. release_ready=false.

## 2026-10-23 live academic answer-key comparison (all 500)
- Extracted exactly 500 `正解：[1-4]` labels from 2027 third editorial DOCX (`2027_パーフェクト問題集_第3次編集稿_出版前確認.docx`) using python-docx.
- Read complete GitHub `audit/v9/decisions.json` (500 records). The raw JSON insertion order is not the book order; an unsorted comparison gave 302 *spurious* mismatches. Therefore mapped by canonical category and numeric question ID: Q_1 41, Q_2 36, Q_3 41, Q_4 127, Q_5 105, Q_O 75, Q_M 60, Q_MO 15, totaling 500.
- After canonical question-ID ordering: 500/500 answer numbers equal independent_answer, **0 mismatches**. This is a new direct check of the 2027 third DOCX against the W6 decisions, not reliance on old 2026 reports.
- Important limitation: matching answer numbers cannot establish that stem text, answer option text or explanations match. Full scholarly master still not completely available via connector; these gates remain open. No manuscript modifications in this comparison; release_ready=false.

## 2026-10-23 single-owner transition and EPUB Japanese encoding correction
- User explicitly stopped W6. This chat is the sole active coordination point for 2027 'パーフェクト問題集'; W6 records read-only. Do not revive W6 or apply parallel edits. Keep 2026 published edition immutable. Treat latest 2027 third DOCX as editorial candidate, not fully scholarly verified master.
- Audited the prior generated EPUB `2027_パーフェクト問題集_出版前検証候補.epub` and discovered severe UTF-8 encoding corruption (U+FFFD replacement glyphs) affecting title, author, title page, and body. Prior link-integrity PASS did not catch it. **Prior EPUB is INVALID and must not be published.**
- Root cause in this local execution: pandoc EPUB export under POSIX locale. Re-exported source DOCX with LANG=C.UTF-8 LC_ALL=C.UTF-8; supplied explicit Japanese title, author, lang metadata.
- New file `2027_パーフェクト問題集_EPUB修正版_未承認.epub` in conversation working container. SHA256 `4211ef572e970bdd59ae043ae21ce65379d6b66ee20f99a109913f872b1b1cc2`. EPUB ZIP passed CRC test; three XHTML files; 2064 local hyperlink destinations checked, zero missing; U+FFFD count 0; Japanese text present. OPF dc:title and dc:creator verified correct.
- This is an important technical fix but EPUBCheck official validation, Kindle Previewer, full scholarly content equivalence and 2027 rules audit still outstanding. Release remains NOT APPROVED.

## 2026-10-23 16th EPUB inspection and navigation repair
- Compared current 2027 third editorial Word (7321 nonempty paragraphs) to current UTF-8-corrected EPUB main XHTML (7322 rendered blocks): all 7321 Word paragraphs longer than 15 non-whitespace characters were found within the normalized EPUB text; no absent paragraphs detected. This is text-presence QA, not exact styled/page equivalence.
- EPUB main text has zero U+FFFD replacement glyphs; ZIP CRC valid; main XHTML 2059 local fragment links, zero broken targets.
- Discovered critical navigation usability defect: epub nav.xhtml table of contents linked to just one entry. Generated improved EPUB `2027_パーフェクト問題集_目次改良版_未承認.epub` by adding anchors to 40 main section and chapter headings. Rebuilt both EPUB3 nav.xhtml and EPUB2 toc.ncx for 40 entries. All 40 navigation targets exist. ZIP CRC valid. Output SHA256 `50c8fe812ba6c328f10cd2f9dc1666b19280c6b366ac20e1436cbcb949ab4b8e`.
- `2027_第15次EPUB本文照合報告.json` and `2027_第16次目次改善報告.json` generated in current working container. New EPUB is not in GitHub, is a candidate; it supersedes previous candidate for further testing.
- Official EPUBCheck and Kindle Previewer not available/run; academic full text comparison and full ebook visual inspection remain outstanding. No new scholarly edits. Release ready FALSE, no KDP publish.

## 2026-10-23 direct EPUB package inspection and remaining-work estimate
- Reopened `2027_パーフェクト問題集_目次改良版_未承認.epub` from current container. ZIP CRC pass, mimetype `application/epub+zip` stored without compression, OPF `dc:title` Japanese correct, `dc:creator` Japanese correct, `dc:language=ja-JP`. XHTML title and main chapter, navigation XHTML, OPF and NCX are XML well-formed. The CSS file was not parsed as XML (not expected).
- Estimated remaining active labor if academic canonical source obtainable and no significant factual issues: ~3-8 hours across full-field comparison (1-3), substantive diffs (1-3), official EPUB/Kindle validation (1-2). This is a contingent planning estimate, not guaranteed completion time or background work.
- Remaining hard blocker: full 500-question scholarly canonical JSON binary unavailable through GitHub connector; EPUBCheck and Kindle Previewer not run, full page visual QA unfinished. No substantive fixes applied. User approves no publication yet.

## 2026-10-23: EPUB structural inspection round 18
- Current EPUB candidate SHA256 50c8fe812ba6c328f10cd2f9dc1666b19280c6b366ac20e1436cbcb949ab4b8e.
- Reparsed 3 XHTML docs and OPF. No duplicate XHTML id values. No cover-image manifest item and no image elements. EPUB has one large main content XHTML (1,165,535 bytes uncompressed; 582,695 decoded Python characters), which is not by itself evidence of invalid EPUB, but device rendering requires inspection.
- The older claim 'official EPUBCheck passed' must not be made; epubcheck executable absent from local environment. Kindle Previewer not run.
- Academic master full text still not retrievable through connector; no all-fields scholarly equality guarantee.
- QA report locally created: /mnt/data/2027_第18次EPUB検査報告.json. No manuscript edits; release_ready=false. W6 remains stopped and read-only.

## 2026-10-23: Round 19 EPUB main XHTML split
- Input: `2027_パーフェクト問題集_目次改良版_未承認.epub` (large main XHTML 1,165,535 bytes).
- Created `2027_パーフェクト問題集_分割検証版_未承認.epub`, SHA-256 `12ff0056561963eeaf8dc337f4e5bd5a3463210af96791f1466b350513f5064d` (current conversation artifact; NOT checked into GitHub).
- Split main document into 15 EPUB XHTML files, max 107,256 uncompressed bytes. Rewrote internal fragment hrefs to correct new file, updated OPF manifest/spine, and EPUB nav.xhtml/NCX targets. Tested normalized full body text for byte-equivalent text after whitespace normalization; passed. Checked 2,099 local fragment references: 0 broken, ZIP CRC passed, TOC entries 41 link elements (includes an extra navigation link compared with previous 40 section entries).
- This is structural transformation of the *existing* 2027 edition manuscript, not a scholarly edit. Official EPUBCheck and Kindle Previewer not run; do not represent as final. Canonical large W6 academic master remains unreadable; release_ready=false.

## 2026-10-23 round 20 EPUB manifest/spine/nav audit
- Directly checked split EPUB `2027_パーフェクト問題集_分割検証版_未承認.epub`, SHA256 12ff0056561963eeaf8dc337f4e5bd5a3463210af96791f1466b350513f5064d.
- Parsed package OPF / all 17 XHTML documents, validated 19 manifest items, 16 spine entries, 41 nav links, unique identifiers and EPUB3 modified date; 2117 relative href references resolved, 0 missing resources or fragment anchors, duplicate XHTML IDs 0, ZIP CRC pass, language ja-JP, U+FFFD 0.
- Warning: no embedded cover image. Reader/KDP cover workflow must be checked separately. Official epubcheck not installed or run; Kindle Previewer not run.
- Machine-readable output `/mnt/data/2027_第20次EPUBパッケージ監査.json` locally generated (not pushed to GitHub). Scholarly 500-field master comparison still outstanding; no new content edits, release_ready=false.

## 2026-10-23 round 21: canonical full-text comparison preparation
- W6 remains stopped/read-only. Attempted independent retrieval of `audit/v9/academic_master_500_20261022.json` via GitHub connector and container raw URL; GitHub connector provides metadata but no payload, and container has no outbound network. Thus full-field academic equality still **unverified**; do not infer it from answer-key agreement.
- Extracted current 2027 third DOCX (SHA256 88e2c620374af6acd6fe6a78341351f7c1cd212a4ec38a3fbe71181ab5b81389) into 500 per-question rows with whitespace-normalized SHA256 of stem, four options, explanation and combined text. Results: 500 question headings; 500 explanation headings; 500 rows with four options; 500 rows each containing one answer label. An initial naive selector accidentally included numbering from section headings; restricted to first four numbered options per question and revalidated.
- Local CSV `/mnt/data/2027_500問_全文照合用指紋.csv` SHA256 `04265bc32de980833f7e7702345c198b4dd0606a4b5b7c42af40abe07ea2ff2c` (140804 bytes), plus `/mnt/data/2027_本文指紋作成報告.json`. They are files in this conversation, not GitHub-tracked source. These hashes are **comparison aids**; per-field segmentation for multi-paragraph cases must be validated before substantive diff judgments.
- No scholarly wording changes. Next: compare against W6 master once acquired; prioritize official 2027 policy checks and Kindle display, rather than recycling completed EPUB structural tests. Release NOT approved.

## 2026-10-23: Direct W6 audit-ledger completeness review
- Read the complete `audit/v9/decisions.json` from frozen W6 branch as an independent source (500 entries).
- Checked for all 500: `status=確認済み`, `content_reviewed=true`, `independent_answer` in 1..4, exactly four `option_verdicts`, one or more `sources`, and empty `unresolved`. Exceptions = 0. Found 281 distinct source IDs among entries (not verification that each source remains accessible/current).
- This confirms ledger metadata is complete, and combined with preceding separate check of current 2027 Word answer labels confirms answer positions are consistent. It does not establish equality of the complete stems, all four choices and four explanations with the academic master.
- GitHub connector's large academic master `audit/v9/academic_master_500_20261022.json` still returned empty bytes (even ranged/base64 calls). Do not infer equivalence; no manuscript text modified. Next focus full-field source acquisition and official EPUBCheck/Previewer; avoid repeating finished mechanical checks.
- W6 remains stopped/read-only; user approval for publication not given.

## 2026-10-23: 2027 time-sensitive item inventory and official date check
- Academic master `audit/v9/academic_master_500_20261022.json` remains inaccessible via GitHub fetch (empty content) and git network via local container cannot resolve github.com. This is a verified retrieval blocker, not an academic mismatch.
- Scanned the actual 2027 third DOCX for date/year-sensitive paragraphs: **17 matching paragraphs** across frontmatter, questions, answer choices and explanations. Stored actionable audit list in conversation artifact `/mnt/data/2027_年度依存記述_監査対象17件.csv`, supporting summary `/mnt/data/2027_年度依存記述_監査要約.json` (not tracked in repository).
- Spot-verified question 10 answer about 育成就労制度 effective date: Japanese Immigration Services Agency official law overview https://www.moj.go.jp/isa/03_00163.html states enactment, excluding partial provisions, 2027-04-01, consistent with present 2027 manuscript answer. This does not approve other dated statements or guarantee regulations won't change before 2027 exam.
- This session changed no scholarly manuscript content. Next audit remaining dated items from primary sources, obtain W6 final academic master, and official EPUBCheck/Kindle Previewer validation. Keep W6 read-only and publication unapproved.

## 2026-10-23 2027 edition dated-claims audit, official sources
- Read previously created `2027_年度依存記述_監査対象17件.csv` containing 17 date-sensitive paragraphs. Official-source checks below address grouped claims, not 17 independently validated paragraphs.
- Frontmatter para 9: MEXT 2026 exam official implementation guidelines confirm basic 100, applied reading 60, applied listening 50 questions; https://www.mext.go.jp/content/20260206-mxt_nihongo02-000036014_1.pdf . Manuscript describes them explicitly as 2026 reference figures and says 2027 official details require recheck. PASS as historically stated; do not represent as official 2027 format.
- EJU question/explanation paragraphs 292, 3785 and 3975: 2026 JASSO official guide https://www.jasso.go.jp/ryugaku/eju/about/eju_guide/2026.html confirms Japanese comprises writing, reading, listening/listening-reading, scored 0–400 plus 0–50 writing, and other available subjects science, Japan and the World/general subjects and mathematics chosen according to university requirements. Source supports gist; exact phrasing of each option remains to be fully verified. PARTIAL PASS.
- Immigration growing employment scheme question 10 paras 113/117 and explanation 3802: Immigration Services Agency states law effective 2027-04-01 except partial provisions: https://www.moj.go.jp/isa/03_00163.html . Date PASS as of 2026-10-23; the manuscript's future-tense phrasing is suitable while effective date is in the future. The complete Q&A's policy-purpose wording needs exact source matching. PARTIAL PASS.
- Remaining unverified source-freshness subjects: Specified Skilled Worker support/period, residence status/employment, individual exam formats, Highly Skilled Professional visa application, Engineer/Specialist in Humanities/International Services experience requirements, JLPT FAQ, EPA Japanese program. Do not change time-indexed question wording without source review.
- No DOCX/EPUB text edits in this batch. W6 read-only; academic master full fields and official EPUBCheck/Kindle Previewer still incomplete. release_ready=false.

## 2026-10-23: Round 25 primary-source check of remaining time-sensitive subjects
- Confirmed current Immigration Services Agency source on Specified Skilled Worker residence periods (https://www.moj.go.jp/isa/10_00233): SSW1 normally total <=5 years with listed exceptions, SSW2 no aggregate maximum. Question 11 / section 1 para 120 must not be paraphrased as an absolute 5-year cap.
- Confirmed official ISA SSW1 support-plan and 10 compulsory supports: https://www.moj.go.jp/isa/policies/ssw/supportssw.html ; relevant to question 4 para 70.
- Confirmed MOFA highly skilled professional visa source dated 2026-01-22: https://www.mofa.go.jp/mofaj/toko/visa/chouki/visa16.html ; relevant to question 13 para 134. Check actual answer choices against visa application procedures, not HSP2 or permanent residence rules.
- Confirmed ISA official Engineer/Specialist in Humanities/International Services supporting documents: generally 3 years relevant experience for foreign-culture based work, exception for university graduates engaged in translation/interpretation/language instruction: https://www.moj.go.jp/isa/applications/status/gijinkoku ; relevant to question 16 para 155.
- Confirmed Japan Foundation EPA predeparture Japanese training official program: Indonesian and Filipino nurse/care-worker candidates, about 6 months initial-intermediate instruction: https://www.jpf.go.jp/j/project/japanese/education/training/epa/index.html ; relevant to ch5 question 2 para 3189.
- Official 2026 JLPT implementation guide also located: https://info.jees-jlpt.jp/wp-content/uploads/2026/02/ddb072fcbc37f22844858b481e730d91.pdf (no comprehensive comparison of Q34 choices yet).
- These are source-topic-level checks, NOT substantive acceptance of every option/explanation. No manuscript wording changed. Continue remaining choices/full canonical academic master and official Kindle QA. W6 remains stopped/read-only, release_ready=false.

## 2026-10-23 Round 26: selected question, options, explanation audit
- Directly inspected 2027 third DOCX question and answer/explanation paragraphs for Ch1 Q4 (support), Q11 (SSW residency), Q13 (HSP visa), Q16 (Engineer/Specialist in Humanities/International Services) and Ch5 Q2 (EPA). Five named questions, 20 options, their answer keys and explanatory rationale.
- Ch1 Q11: correct 1, explicit '原則5年以内' for SSW1 and no aggregate maximum for SSW2; false option 4 asserts no exceptions. Official ISA https://www.moj.go.jp/isa/10_00233 confirms principal rule and exceptions.
- Ch1 Q13: correct 3, HSP visa 5 years with COE required; incorrect choices about family COE, uniform nationality documents and rejection of electronic COE match MOFA https://www.mofa.go.jp/mofaj/toko/visa/chouki/visa16.html.
- Ch1 Q16: correct 2, 3-year related work experience with university graduate translation/interpretation/language-teaching exception, corroborated in ISA https://www.moj.go.jp/isa/applications/status/gijinkoku .
- Ch5 Q2: correct 1, EPA Indonesian/Filipino nurse/careworker candidates ~6 months initial/intermediate Japanese, JPF https://www.jpf.go.jp/j/project/japanese/education/training/epa/about.html .
- Ch1 Q4: correct 3, SSW1 living orientation and Japanese school guidance; based on previously consulted ISA SSW support list, source https://www.moj.go.jp/isa/policies/ssw/supportssw.html .
- Verdict: all five keys and principal distinguishing option conditions consistent with cited sources. No manuscript edits. This is a focused five-question review, not a re-certification of 500 questions.
- Next: other dated Q8/Q9/Q34/Q35 and associated explanations, plus large master full-field comparison and official EPUBCheck/Kindle display validation. W6 remains stopped/read-only. release_ready=false.

## 2026-10-23: Round 27 primary-source review of Ch1 questions 8,9,34,35
- Examined actual 2027 third DOCX at paragraph indices 97/105/284/291 and matched explanation headings at 3783/3790/3965/3972. Answer keys Q8=1, Q9=3, Q34=4, Q35=2.
- Compared all 16 choice texts and four explanatory blocks to current official primary sources: BJT official score level https://www.kanken.or.jp/bjt/about/level_sample.html ; JLPT FAQ https://www.jlpt.jp/e/faq/ ; JASSO EJU Japanese scope and scores https://www.jasso.go.jp/ryugaku/eju/examinee/procedure/subject.html ; JASSO EJU equating https://www.jasso.go.jp/en/ryugaku/eju/about/score/index.html ; writing scoring https://www.jasso.go.jp/ryugaku/eju/about/score/writing.html ; ISA residence/work questions https://www.moj.go.jp/isa/applications/guide/kanri_qa.html.
- Primary conclusions: BJT is scored 0-800/J5-J1+ not pass/fail; student permission and holiday 8h rule not unrestricted for dependent status; JLPT uses IRT scaled scores; EJU writing is independently rubric-scored, other Japanese test components are score-equated. No observed answer-key correction needed.
- Scope caveat: full independent source substantiation of ACTFL OPI and JLPT expiration wording not finished in this batch. Treat as PARTIAL primary-source verification, not definitive 4-question approval; no text changed.
- W6 read-only, current 2027 DOCX/EPUB academic master full field comparison and EPUBCheck/Kindle Previewer remain uncompleted. release_ready=false.

## 2026-10-23 Round 28: ACTFL OPI and JLPT certificate primary-source closure
- ACTFL official OPI page https://www.actfl.org/assessments/postsecondary-assessments/opi confirms it is a proficiency-based interview assessing spontaneous, unrehearsed spoken language, not simply a fixed-choice grammar test. ACTFL official OPI Familiarization Guide https://www.actfl.org/uploads/files/general/OPI_Familiarization_Guide_2024_FINAL.pdf further confirms one-on-one interactive standardized procedure and role of certified raters. This addresses the outstanding ACTFL OPI method reference associated with Ch1 Q8.
- JLPT official FAQ https://www.jlpt.jp/e/faq/ confirms certificate never expires, including legacy results; hiring institutions and schools may independently impose recency limits when accepting results. This addresses validity caveat associated with Ch1 Q34 and any explanatory text about recognition.
- Important: This batch verified cited reference propositions, not every word of current 2027 manuscript option/explanation text; do not claim a full independent audit of all four options from this step alone. No DOCX or EPUB edits made. W6 stopped/read-only. Full academic master all-field comparison and official EPUBCheck/Kindle Previewer remain open. release_ready=false.

## 2026-10-23 round 29: editorial near-duplicate screening
- Performed new text-similarity screening on current 2027 third DOCX's **425 standard-form question stems** (Heading 3 `問題N` before answer section), using RapidFuzz ratio >=87.00 as flag only. Exact duplicate stems: 0; candidate highly similar pairs: 10. These 10 are not confirmed defects and are not evidence that distinct learning objectives duplicate.
- Examples: Oxford's six strategies stems for cognitive, metacognitive and memory strategies; Schoen reflective-practice prompts are lexically close but may test different aspects. No auto-edits.
- Case-form applied 75 questions use distinct formatting and were NOT included in this check. Never describe this as 500-question duplicate audit.
- Detailed report in current conversation artifact `/mnt/data/2027_第29次_設問重複検査.json` (local only). W6 academic master unchanged/unretrieved via GitHub connector; full-field comparison still open. EPUBCheck/Kindle Previewer still open, release_ready=false.

## 2026-10-23 Round 30: editorial classification of 10 near-duplicate pairs
- Read actual 2027 third DOCX question text and 4 choices for the 12 involved global standard question numbers: 54,100,101,103,105,119,139,201,246,251,321,327.
- Of 10 fuzzy-text candidate pairs from Round 29: 9 pairs test distinct concepts (Oxford cognitive/metacognitive/memory; Celce-Murcia strategy types; Saussure sign vs value; Austin illocution vs locution); keep. One pair (global standard question #119, #201; Schön reflective practice) overlaps substantively in correct idea of reexamining tacit practical knowledge. Editorial rewrite of one as practical classroom scenario is worth considering, but not a proven duplicate/error and requires subsequent academic re-audit.
- No questions deleted, rewritten or answer keys changed. Decision artifact `/mnt/data/2027_第30次_類似設問10組_内容判定.json` generated for current conversation (not committed to repo). The analysis covers question stems and four choices, not independent first-source confirmation of every explanation.
- Academic full master comparison/official EPUBCheck/Kindle Previewer remain open. W6 stopped and read-only; release_ready=false.

## 2026-10-23 Round 31: Schön duplicate resolved into concrete editorial direction
- Inspected actual third-edition 2027 DOCX paragraphs 930 (Ch3 Q1), 951 (Ch3 Q4), 1513 (Ch3 Q83): Q1 and Q83 both test general reflective-practice conception and have same correct option position 4; Q4 ALREADY supplies concrete classroom reflection-in-action application, so earlier suggestion to convert another item to in-action classroom scenario would itself repeat Q4.
- Suggested differentiated learning objectives: keep Q1 as general reflective practice, keep Q4 as reflection-in-action scenario, repurpose Q83 to reflection-on-action (post-class evidence-based review and planned lesson improvement). Independently checked conceptual distinction against Open University https://www.open.edu/openlearn/education-development/learning-teach-becoming-reflective-practitioner/content-section-2.1 and Kennesaw State https://campus.kennesaw.edu/faculty-staff/cetl/teaching-resources/teaching-essentials/what-reflection.php .
- Editorial proposal only: NO automatic DOCX/EPUB rewrite, because changing question stem, four options and four explanation verdicts would require reaudit, including stable Q-ID and link preservation. 500-question total unchanged. W6 read-only; release_ready=false.

## 2026-10-23 Round 32: Chapter 3 question 83 four-option rewrite PROPOSAL (unapplied)
- Read current 2027 third edition Word, Ch3 Q83 (paras 1512-1518) and answer/explanations (paras 5137-5143). Existing Q83 duplicates Ch3 Q1's general reflective-practice learning goal; existing Ch3 Q4 already tests reflection-in-action in classroom setting.
- Authored self-contained **candidate** question testing Schön's reflection-on-action: post-lesson investigation of unequal pair-activity speaking opportunities, analysis of teaching decisions and planning improvements. All four options and four explanations written, answer position 4 unchanged. Distractors distinguish during-action adjustment, no reflective review, and descriptive average-only reporting. Candidate file in conversation: `/mnt/data/2027_第32次_Schon問題83改稿案_未反映.md`.
- Internal consistency reviewed (4 options, only #4 fits stated post-lesson reflective scenario), but independent scholarly reference verification and full DOCX/EPUB regression still required before insertion. Do NOT assert this is already integrated in the book.
- Original DOCX and EPUB unchanged; W6 stopped/read-only; release_ready=false.

## 2026-10-23 Round 33: Applied Schön Q83 rewrite in unapproved fourth DOCX
- Source `2027_パーフェクト問題集_第3次編集稿_出版前確認.docx`. Created separate `/mnt/data/2027_パーフェクト問題集_第4次編集稿_Schon改稿_未承認.docx`, SHA256 `f601ae1b473852ca6094458af1861ec88ad377909fb19e9dd56a0ad9ba7ad653` (conversation artifact, not GitHub binary commit).
- Replaced nine paragraph texts: indices 1513..1517 (Ch3 Q83 stem, four options) and 5139..5142 (four option explanations). Answer position remains #4, original third draft preserved.
- Compared input vs output: exactly nine modified paragraphs among 7,329; 1,061 bookmark names and all 2,059 internal anchor links unchanged, no extra textual differences. Converted output DOCX to PDF using headless LibreOffice; 373 pages, same as prior draft; visually inspected affected PDF pages 72 and 258, both display correctly and unobstructed. Local evidence `/mnt/data/2027_第33次_Schon問題83_反映検査.json`.
- Important: this is an **unapproved editorial candidate** and currently only a DOCX, not a refreshed EPUB. Schön primary-text/source verification and updated academic audit decision needed before freezing. No publish or changes to 2026 edition; W6 stopped/read-only. Master 500 full field audit and EPUBCheck/Kindle Previewer still required. release_ready=false.

## 2026-10-23 Round 34: integrated fourth DOCX Schön changes into split EPUB
- Starting from preserved `2027_パーフェクト問題集_分割検証版_未承認.epub`, created separate `2027_パーフェクト問題集_第4次編集稿反映_EPUB_未承認.epub`, SHA256 `ac5ee36def603a8e5fffc154fdfa05fe27134fc262b45a948fcd2523f265491a`.
- Matched 9 old paragraph texts of Ch3 Q83 and its 4 explanatory verdicts to part003.xhtml/part010.xhtml, substituted exact new text from fourth Word draft preserving strong emphasis labels, IDs, and package/spine/nav structure. All 9 new snippets appear in resulting EPUB. ZIP integrity passes; 2117 relative internal href references checked with 0 missing resources or anchors. Text updates solely 9 paragraph elements; preceding EPUB left intact.
- Report `2027_第34次_第4次稿EPUB反映検査.json` is saved in this conversation, not GitHub tracked. Fourth Word and fourth EPUB are unpublished editorial candidates only. Official EPUBCheck and Kindle Previewer not run, W6 academic master all-field comparison still outstanding. W6 read-only; release_ready=false.

## 2026-10-23: Two-edition release plan adopted (2026 revision first, 2027 content upgrade later)
- User instructed to produce **2026-year immediate-prep book revised edition** first, holding all 500 question contents/answers/explanations unchanged, with title/preface edits only; only afterwards continue substantive 2027 Perfect Problem Book improvement.
- Derived the separate `2026年登録日本語教員試験_直前対策500問_改訂版_未承認.docx` from 2027 FOURTH editorial DOCX (which already includes approved-by-audit-candidate Schön Q83 revision). Changed only frontmatter paragraphs indices 0,1,2,5,7,9. Automated paragraph text diff: exactly those 6 changes; all 7,292 paragraphs from index 37 onward identical to fourth DOCX. Original 2027 fourth DOCX preserved.
- Created corresponding `2026年登録日本語教員試験_直前対策500問_改訂版_未承認.epub` from split fourth EPUB, changing frontmatter/title OPF/navigation while preserving the questions/explanations. ZIP and XML parsing passed, 2,099 internal fragment links checked, zero broken. EPUB SHA256 b066fb5b94f003217d34f1caff8a05be734e65393dfade5d30ed4d5838c115f5.
- Files provided within the user's current conversation (NOT stored as GitHub binaries). This is an **unapproved revision**, without official EPUBCheck, Kindle Previewer, full canonical academic-master comparison or publishing. Note 2026 revision contains the newer Schön Q83 content already present in 2027 fourth draft; 'unchanged' compares against that frozen draft, not the originally published 2026 file.
- Separate subsequent workstream: continue 2027 full academic/editorial upgrades only AFTER freezing 2026 revision candidate; do not propagate later 2027 question edits into 2026 revision unless expressly requested. W6 stays read-only, no KDP publication without permission.

## 2026-10-23: Mandatory frontmatter deletions and hard page starts (BOTH 2026 and 2027 editions)
USER EDITORIAL RULE (carry into every future export): (1) Delete frontmatter sentence beginning `なお、500問全体について学術監査正本との全文照合は継続中` from 2026 preface, without changing academic problem text. (2) Delete prefatory paragraph beginning `これは知識と解答時間の感覚を確かめるための独自演習で` through `聴解対策には、公式の音声付きサンプル問題などを併用してください。` (2027 variant: remove the analogous whole cautionary explanation after initial 75-question introductory sentence). (3) Remove only phrase `。聴解は音声付き教材で別途練習する` from STEP3. (4) New page before `はじめに`, `本書の使い方`, `目次`, all PART starts I/II/III, `解答・解説編`, appendices and `あとがき` in BOTH Word and EPUB. Never allow next major section to start on previous major section's page.
- Generated separate conversation artifacts `/mnt/data/2026_登録日本語教員試験_改訂レイアウト_未承認.docx` and `.epub`, and matching 2027 versions. In DOCX, 10 major Heading 1 page-break-before fields set; intro edits affect paragraphs 5,9,17 for 2026 and 9,17 for 2027 only. All question/choice/answer/explanation paragraphs left untouched. EPUB updated text nodes and major section starts via break-before:page/page-break-before:always CSS inline, including heading paragraphs carrying `nav-section-*` IDs for Part I/II/III. Prior manuscripts preserved.
- Rendered both DOCX to PDF: 373 pages; spot checked pages 1 title, 2 preface, 3 instructions, 4 TOC, 5 Part I, 171 answer section, 369 appendix, 373 afterword. Distinct-page boundary verified for those sampled sections. EPUB reader pagination is device/software-dependent and NOT verified in Kindle Previewer. Official EPUBCheck still outstanding. No KDP publishing or W6 changes.
