# 統合系チェックポイント329：Kindle Previewer実行条件と最終検査票

日付：2026-10-25（JST）  
対象ブランチ：`audit/v9-integration-2026-10-21`  
基点HEAD：`d7acc7a24410ead88b77615b1e152dce92ba8983`

## 固定した対象

- Word：`audit/v9/integration/v9_integration_working_cp320.docx`
- Word SHA256：`d544cb33f760023b8030bb3ca36c6401b7297ef394156cfb944f046fd0bff1d3`
- EPUB：`audit/v9/integration/v9_integration_working_cp320_candidate.epub`
- EPUB SHA256：`358b7a80c18a992c07358123719ffd3679b12f1dbfb65964ededbe381a97db10`
- 内容採否分類：500/500問、未分類0
- Word表示監査：485/485頁、未確認0、開いている表示欠陥0
- EPUBCheck v5.4.0：fatal 0、error 0、warning 0、info 0、終了コード0

## 公式要件の再確認

Amazon KDP公式ヘルプはKindle Previewerの対応環境をWindows 10（64-bit）以降、Intel MacまたはApple Silicon MacのmacOS 12以降としている。Linux版は案内されていない。

- Kindle Previewer：https://kdp.amazon.com/help/topic/G202131170
- Kindleへのコンテンツ提供経路：https://kdp.amazon.com/help/topic/G79CTKR8BX79E96L
- アップロードとオンラインプレビュー：https://kdp.amazon.com/help/topic/G200641240

公式説明では、端末種別、縦横表示、フォント、文字サイズ、表・リンク等の要素別表示、Auto-Advance Viewによる全編確認が可能である。KDPのOnline PreviewerはBookshelfへの原稿アップロード後に利用する手順であり、今回の「明示承認前のKDPアップロード禁止」により代替経路として使用しない。

## 現在環境の実測

`Linux 6.18.55 x86_64`、`DISPLAY`なし。次の実行ファイルはいずれも見つからなかった。

- Kindle Previewer
- Wine / Wine64
- KindleGen
- Calibre / ebook-convert
- Chromium / Google Chrome / Firefox
- xvfb-run

したがって、このLinux実行環境内で公式Kindle Previewerによる変換・端末表示検査を実施する正当な経路はない。OS非対応アプリを非公式互換層へ導入して得た結果は、公式Previewerの検査結果として扱わない。

## Windows / macOSで実行する最終検査票

対象は上記SHAのEPUBに固定し、別SHAを読み込んだ場合は検査をやり直す。

1. 最新のKindle PreviewerへEPUBを読み込み、変換完了と警告・エラー一覧を保存する。
2. 端末種別を「Tablet」「Phone」「Kindle E-reader」で確認する。
3. TabletとPhoneは縦・横の両向き、各端末で最小・標準・最大の文字サイズを確認する。
4. 「View All」で目次、リンク、表を選び、61件の目次項目、10表、問題から解説・解説から問題への往復リンクを確認する。
5. 各章先頭、全15ケース、正答早見表、用語集、あとがきへ目次から遷移し、戻り操作を確認する。
6. Q_2_023、Q_5_094など長文事例、Q_2_034、A_2_030、Q_5_031、A_5_032、A_M_048、旧問題35相当箇所を重点確認する。
7. 日本語、欧文、記号、中国語例字「书」の欠字・豆腐表示・文字化けがないことを確認する。
8. 表の列見出しと本文が端末幅で判別でき、横スクロール、切れ、重なり、極端な余白がないことを確認する。
9. Auto-Advance Viewで全編を通し、空白画面、重複、順序逆転、孤立リンク、章飛びがないことを確認する。
10. Previewerのバージョン、OS、実行日時、対象SHA、端末モード別結果、警告・エラー、画面証跡を保存する。

## 合否基準

- **合格**：取込エラー0、重大警告0、上記全項目合格、対象SHA一致。
- **要修正**：変換失敗、リンク不達、目次不整合、表崩れ、欠字、重なり、読めない改頁、端末モード固有の表示不良が1件でもある。
- **未実施**：対象SHAまたはPreviewerバージョン・OS・端末モードの記録が欠ける。

現時点ではKindle Previewer未実施のため、出版判断は保留する。KDPへのアップロード、公開、既存ブランチへのマージは行っていない。
