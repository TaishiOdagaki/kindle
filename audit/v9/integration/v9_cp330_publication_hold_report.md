# cp330 統合稿・出版判断報告（Kindle Previewer未実施）
更新日：2026-10-25
基点コミット：85a44d46d9a12e57e6192f580f4f9b4c81cb5798
対象：cp320 Wordおよびcp327候補EPUB。原本の上書きなし。

## 判断
**出版保留。最終承認版ではない。**
内容統合・紙面表示・EPUB仕様検査は記録上完了。Kindle Previewerの変換および端末表示検査は未実施であり、EPUBCheck合格をKindle表示合格と読み替えない。

## 成果物と固定ハッシュ
|成果物|GitHubパス|SHA256|
|---|---|---|
|統合Word候補|audit/v9/integration/v9_integration_working_cp320.docx|d544cb33f760023b8030bb3ca36c6401b7297ef394156cfb944f046fd0bff1d3|
|EPUB候補|audit/v9/integration/v9_integration_working_cp320_candidate.epub|358b7a80c18a992c07358123719ffd3679b12f1dbfb65964ededbe381a97db10|

## 今回実行した追加検証
- 現物のWord・EPUBのSHA256を上記値と再照合。
- Wordの500問題ID・500解説IDとEPUBの同ID集合が完全一致。
- ID別の問題500ブロック・解説500ブロックが空白除去のみで全文一致。句読点・数字・正答・語句は正規化していない。
- 500問すべてに順序1〜4の選択肢と順序1〜4の正誤解説がある。
- 全500問で正解番号が一つあり、「正」タグの肢と一致。
- 早見表500行が現物の解説正答と一致。応用はケース内番号を全75問IDへ対応、模試応用は問題61〜75をMO_001〜015へ対応。
- Word全8,359段落がEPUB本文内に存在し欠落0（存在検査は順序保証ではないが、問題・解説の順序は各IDブロックの全文一致で別途検査）。
- Word全10表の先頭行に見出し行属性を確認。
- Q_4_111の解説1には原著704頁を記載し、旧700頁は残存しない。
- 採否台帳500IDの集合が現物と完全一致。GitHub採用492、同文7、手動改稿1、未分類0。
- 章別数：第1章41、第2章36、第3章41、第4章127、第5章105、応用75、模試基礎60、模試応用15、合計500。
- これらは構造・変換保持の検査であり、新たな学術原典の再審査やKindle端末目視を行ったことにはならない。

## 監査記録の正本
- 採否の個別理由：audit/v9/evidence/20261025_two_track_classifications_checkpoint308.json
- 原典照合・判定：audit/v9/decisions.json
- 専用系累積修正前後：audit/v9/changes.json
- 前付け修正：audit/v9/integration/frontmatter_changes_cp269.json
- Q_4_111参照頁修正：audit/v9/integration/changes_cp275.json
- 500問閲覧用台帳：audit/v9/integration/v9_cp320_500_question_audit_ledger.csv
- 今回の実測結果：audit/v9/evidence/20261025_cp330_verification.json
- Word全485頁表示：audit/v9/evidence/20261025_checkpoint325.md
- 公式EPUBCheck：audit/v9/evidence/20261025_epubcheck_5.4.0_result.json
- Kindle最終検査票：audit/v9/evidence/20261025_checkpoint329_kindle_previewer_handoff.md

## 差分・採否の解釈
専用監査系とLibrary系の493問差を無条件に上書きせず、500問の採否理由をcp308へ集約した。最終500問CSVは旧v8台帳の本文ではなく、SHA固定のcp320現物から正答・ID・本文ハッシュを再抽出している。原典URLと本文根拠の詳細は個別採否理由およびdecisions.jsonに遡る。CSVのsource_ids欄が空欄の行は根拠不存在を意味せず、cp308で構造化IDがない行は個別basis記述を参照する。

## 残る実行条件
対応Windows/macOS上のKindle Previewerで、固定SHAのEPUBを取り込み、cp329検査票の端末種別・縦横・文字サイズ・目次・表・リンク・全編表示を検査し、バージョン・OS・証跡と結果を保存する。LinuxでのEPUB仕様検査やWordの485頁QAは代替しない。
その結果により修正が必要なら新規版へ保存し、対象SHAに応じて影響検査を再実施する。合格後にのみ出版判断報告を更新する。KDPアップロード、公開、メインへのマージは別途明示承認が必要。
