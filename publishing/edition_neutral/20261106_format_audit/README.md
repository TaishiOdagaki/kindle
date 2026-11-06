# EPUB出版前形式監査レポート

実施日：2026年11月6日

## 対象と結果

原本：2027年度版いろは　2026:10:28.epub（ユーザー指定の実在ファイル。依頼文中の「(1)」付き名とは異なる）。原本は上書きせず、work/final_audit/original.epub にバックアップした。

修正版：登録日本語教員試験_2027年度版_出版前形式修正版.epub

形式修正と機械検査は完了。Kindle Previewer変換は成功。ただしEPUBCheckと実画面の目視検証は未完了であり、KDPの最終表示確認済みとは扱わない。

## 発見した不具合と修正

1. 本文目次 part001_s04.xhtml：第III部の部見出し・内訳にリンクがなかった。第III部冒頭 nav-section-26 へのリンクを設定し、「基礎試験（問題1〜60）」→ part005_s16.xhtml#Q_M_001、「応用試験・読解（問題61〜75）」→ part006_s02.xhtml#Q_MO_001 の2項目を追加した。第I部、第II部、解答・解説編の見出しもリンク化。既存の各章・付録リンクも参照先を検査した。「巻末付録・あとがき」は下位項目をまとめる見出しとして維持した。
2. nav.xhtml と toc.ncx：第III部の基礎・応用読解を上記の問題1・61のIDに統一。全41項目の着地点を見出し文字列または問題番号と照合し、navとNCXの順序・参照先一致を検証した。
3. part006_s02.xhtml：問題61に直接移動するとケース文が画面上方になるため、「▲ この問題のケース文を読む」のリンクを設問冒頭に追加。ケース本文に practice-reading-case IDを追加。ケース本文や設問の文字列は変更していない。
4. part005_s01.xhtml：本文が空のままspineに含まれていた。ファイル・manifest項目・spine項目を除去。split-part-5 IDは次のpart005_s02.xhtmlに移し、参照を保持した。除去後の空本文・重複本文のspine項目は0件。
5. 各文書の nav-section-01〜40：通常段落だった見出し40件をh1/h2に変更し、既存IDと内側の文字列を保持。部・前後付はh1、章・ケース等はh2。見出しだけを読書アプリの画面末尾に残さない既存の保持指定も継承した。
6. stylesheet1.css：日本語フォント候補とserifの代替指定、行間1.7、相対サイズの見出しを設定。htmlの固定文字色・背景色を解除し、リンクは継承色と下線で識別できるようにした。大幅なデザイン変更は行っていない。
7. 表：従来のdisplay:blockと横スクロール前提をやめ、幅100%の固定列幅表、セルの折返し、上下揃え、行の分割回避を設定。解答早見表9表500行の全問題番号・ケース番号・正解が解説側と一致することを検証。巻末対応表のセル文字列と対応関係も原本と同一。実機での狭幅・大文字表示は未確認。
8. part006_s03.xhtml：解答・解説編の独立した扉を維持。他の部の扉と同じ見出しクラスに統一し、見出し自体への重複した強制改ページを解除。文書単位の読み順は維持した。

## 検査件数

| 検査 | 件数・結果 |
|---|---|
| 本文目次リンク | 17件、参照切れ0 |
| nav目次 | 41件、着地点・NCX整合確認 |
| NCX | 41件、navと同一順序・着地点 |
| 内部ナビゲーション全体 | 2150件、参照切れ0（上記を含む） |
| CSS・画像・OPF等の資源参照 | 116件、参照切れ0 |
| 問題→解説・解説→問題 | 500組・1000方向。各リンク直前の問題/解説IDと相手IDの対応を照合 |
| 解答早見表 | 9表500行、全正解・番号対応一致 |
| XHTML/XML/OPF/NCX | 60文書をXMLとして解析成功 |
| XHTML | 56文書 |
| manifest / spine | 59項目 / 55項目、idref対応確認 |
| 重複ID / 空本文 / 重複本文 | 0 / 0 / 0 |
| 外部参照 | 0件 |

## 内容保持検査

全XHTMLの本文テキストを原本と比較した。タグ変更・インデント空白を除き、問題文、選択肢、正解、解説、既存見出し、著者紹介は同一。追加文字列は本文目次の2項目とケース文へ戻るリンクのみ。問題・解説各500件のIDと順序は保持。早見表の500行を解説と照合した。書名・著者メタデータ、表紙画像は原本と同一。内容・学術的正確性の再監査は行っていない。

## 規格検査と表示確認の実施環境

- Kindle Previewer 4.0.0（macOS）のCLIでEPUB→KPF変換成功。Enhanced Typesetting Supported、変換エラー0、Quality Issue Count 0。
- EPUBCheck：この環境に実行ファイルがない。公式GitHub配布物の取得を試したがホスト名解決に失敗したため、未実施。XML解析、ID・資源参照、manifest/spine、ZIP構成の個別検査で補完したが、EPUBCheck合格とは表記しない。
- 画面表示：Playwrightの同梱ブラウザーがなく、代替としてインストール済みGoogle Chromeで起動を試したが、プロセスが終了し実施できなかった。Kindle変換は表示エンジンへの適合確認であり、実画面の目視や全リンクの実タップ確認を意味しない。

## 未解決・手動確認事項

1. EPUBCheckが使える環境で本修正版を検査する。
2. Kindle PreviewerまたはKindleアプリで、本文目次→第III部冒頭・問題1・問題61、問題61→ケース文、問題→解説→元の問題を実際に操作する。参照先IDと論理的な着地点は機械検査済み。
3. スマートフォン相当の画面幅、標準・大きい文字、明暗両モードで解答早見表と対応表を確認する。折返しCSSは調整済みだが、実機でのはみ出し・行途中の改ページ・見出し孤立は未確認。
4. 解答・解説編の扉を含む独立ページと強制改ページの見え方は、読書アプリの設定で変わるため目視確認する。
5. 表紙はユーザーが用意する。既存の埋込画像は今回保持しており、新しい表紙の制作・差し替えは行っていない。出版操作は行っていない。

## 修正ファイル一覧

- EPUB/content.opf
- EPUB/toc.ncx
- EPUB/nav.xhtml
- EPUB/styles/stylesheet1.css
- EPUB/text/part001_s02.xhtml
- EPUB/text/part001_s03.xhtml
- EPUB/text/part001_s04.xhtml
- EPUB/text/part001_s05.xhtml
- EPUB/text/part001_s06.xhtml
- EPUB/text/part001_s07.xhtml
- EPUB/text/part001_s08.xhtml
- EPUB/text/part002_s02.xhtml
- EPUB/text/part003_s02.xhtml
- EPUB/text/part004_s02.xhtml
- EPUB/text/part004_s03.xhtml
- EPUB/text/part004_s04.xhtml
- EPUB/text/part005_s02.xhtml
- EPUB/text/part005_s03.xhtml
- EPUB/text/part005_s04.xhtml
- EPUB/text/part005_s05.xhtml
- EPUB/text/part005_s06.xhtml
- EPUB/text/part005_s07.xhtml
- EPUB/text/part005_s08.xhtml
- EPUB/text/part005_s09.xhtml
- EPUB/text/part005_s10.xhtml
- EPUB/text/part005_s11.xhtml
- EPUB/text/part005_s12.xhtml
- EPUB/text/part005_s13.xhtml
- EPUB/text/part005_s14.xhtml
- EPUB/text/part005_s15.xhtml
- EPUB/text/part005_s16.xhtml
- EPUB/text/part006_s02.xhtml
- EPUB/text/part006_s03.xhtml
- EPUB/text/part006_s04.xhtml
- EPUB/text/part006_s05.xhtml
- EPUB/text/part007_s02.xhtml
- EPUB/text/part007_s03.xhtml
- EPUB/text/part008_s02.xhtml
- EPUB/text/part010_s02.xhtml
- EPUB/text/part012_s02.xhtml
- EPUB/text/part014_s02.xhtml
- EPUB/text/part015_s02.xhtml
- EPUB/text/part015_s03.xhtml
- EPUB/text/part015_s04.xhtml
- 削除：EPUB/text/part005_s01.xhtml

## ファイル識別

原本SHA-256：ac7cfc0ae45e620fcd2b495332d8eb3b72754b3a83b72524343dee034d993ed0

修正版SHA-256：64a2140a5562c86bb115c236108e329b0b7291322b8274c14db8ed2280c6eaee
