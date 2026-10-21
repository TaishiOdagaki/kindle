# 第215チェックポイント：改訂系統比較と81〜120頁目視

出版判断は保留。最終v9は未制作である。

## 対象

- 専用監査ブランチ：`audit/v9-2026-10-12`、HEAD `ee1fafd645330ee060a36084fef647944cef78a9`
- 現行作業DOCX：SHA256 `aea97d09d9cefebbd4c2220c4728e8c01adaecfd97e832fc0963c053ac2d32ee`、395頁
- 別改訂系統：`claude/magical-cannon-2l4k5c`、HEAD `cc9eb4ce61a612c2dfe4ed3ec2860b20fb7264f7`
- Library DOCX：SHA256 `3a8f6e67dd217d9dbf94f28a61625024474022e290e053ed78a8471f92140d4a`、同系統報告では345頁
- 比較元報告：`監査報告/2026-10-21_v9学術原典照合_台湾初期教育史と学習方略.md`、SHA256 `fc86e3a28fdccacf93ddff4c0072550c0ca232059911e863146e82089edffb64`

## 全文差分

両DOCXを実取得し、500個の安定問題IDにより設問、1〜4肢、正答番号、1〜4解説を比較した。問題ID集合は一致し、493問に本文差、7問は全文一致した。一致したのは Q_1_031、Q_2_019、Q_3_036、Q_5_018、Q_5_020、Q_5_021、Q_M_003。正答番号差は0件。OOXMLパッケージで差があったのは `word/document.xml` のみである。

Library系統が明示したQ_1_006、Q_1_023、Q_1_025、Q_3_029を個別に比較した。専用監査系統はいずれも後発の改訂で、取得本文に直接対応する狭い設問へ変更されていた。Library側へ戻すと、複数の歴史事実や二次分類を含む広い主張を再導入するため採用しない。現行版を維持し、統合による本文・正答変更は0件とした。

根拠URL：

- Q_1_006（S244）：https://www.th.gov.tw/Epaper_Content/236/7518/
- Q_1_023（S200）：https://journal.takushoku-u.ac.jp/lcri/lcri_132.pdf
- Q_1_025（S261）：https://www.jasso.go.jp/about/organization/history/gakuyu.html
- Q_3_029（S148）：https://web.ntpu.edu.tw/~language/workshop/read2.pdf

完全な差分は `evidence/batch215_lineage_diff.json`、機械可読の採否は `evidence/batch215_lineage_adoption.json` に記録した。

## 画像目視

現行作業DOCXを完全CJK静的フォントでA4・395頁へ新規描画した。PDF SHA256は `053b95f9fe9b5bbf5ba1c7f5c1fe3606fc71a0f79659f5dfc5f5e53575a4d7ea`。CJK固有1379字、欠字0。81〜120頁を各頁独立に120dpiで画像化し、原寸で確認した。欠字、裁ち落ち、重なり、異常空白、孤立見出し・選択肢・リンク、意図しない改頁は認めなかった。

最初に試した可変フォントは破損・切詰め状態だったため、その描画は判定に使用しなかった。目視済みは累計126/395頁、残り269頁。次は未確認の121頁を確認後、既確認の122〜123頁を飛ばして124頁以降を進める。

## 未完了

- 未目視269頁
- 統合後最終SHAに対する全500問・全リンク・正答早見表・前付け・ケース・用語集の最終機械検査
- EPUB変換とKindle Previewer検査

以上が完了するまで出版可とは判定しない。KDPアップロード、公開、既存主ブランチへのマージは行っていない。
