# チェックポイント269 — 前付け改訂とEPUB初回検査

## 原稿
親Word SHA256 1554daab707ff2f1f0994acfde6749642b8718c19cbdb3456e55a7197d931740
新Word SHA256 1e6602ad3edb2c6c656ec986bc6771ebcfa20e8cb542fbafe4480372a9bd95fc
保存先 audit/v9/integration/v9_integration_working_cp269.docx

前付け8段落の修正前・後・理由を同フォルダのfrontmatter_changes_cp269.jsonへ記録。未確認の研究グループと実務年数、網羅性、合格・学習効果保証を撤回。500問の実構成を保持し、模擬試験が本番の構成そのままではなく音声未収録である点を明示。
初回検証コードはZipInfoを再利用した後の旧ZIP再読込でCRC例外になった。原ファイルを再オープンして再検証し、両ZIP CRC正常、変更は冒頭8段落のみ、以降全文・ブックマーク・リンク不変を確認。原本の変更なし。

## 表示検査
Noto Sans CJK JP Regular 16467736bytesを公式notofontsリポジトリから復旧しfc-match確認。
https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf
LibreOffice renderer、A4、485頁。
PDF SHA256 2983515594b280f29b20e750ec1993f23706537055ceb216a1f487a47cd501e8
実画像を確認した頁のみ：1–12。欠字・重なり・切れを認めず。問題6は7–8頁にまたがるが欠落なし。残473頁。旧Wordの確認頁数を新SHAへ合算しない。

## EPUB
Pandocで新WordからEPUB生成。
SHA256 1710f471db74d79ca42e4e6b1cd0c3264136b01a71e801b1d614924537e02d2c
EPUBCheck5.4.0取得元：
https://github.com/w3c/epubcheck/releases/download/v5.4.0/epubcheck-5.4.0.zip
実行：java -jar epubcheck.jar v9_integration_working_cp269.epub --json epubcheck.json
結果：fatal0/error0/warning0/info0。
別途構造検査：XHTML3、問題ID500/重複0、内部リンク2065/欠落0、表10/見出しセル20。
Pandocはja翻訳ファイルの不在とAbstract訳なしを警告。EPUBの構文適合と内容・アクセシビリティ全般・Kindle表示を同一視しない。

## 未完了
2系統の採否分類229/500、未分類271。内容の追加採用はQ_4_086まで。全4肢・全解説・ケースの残る根拠照合、前付け以外の保証/制作体制記述、全頁表示検査、Kindle Previewer、EPUBの実表示を継続。出版保留。
