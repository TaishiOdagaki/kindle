# 需要シグナル集計(2026-10-05、随時更新)

方針: 「人気が出るはず」という見込みではなく、**測れる数字**を同じ書式で蓄積し、GitHubに履歴を残す。
各行に取得日・出典・取得方法を必ず付ける。取れなかったものは「未取得」と書く。

## 取得済み
| 指標 | 値 | 出典 | 取得日 | 信頼度 |
|---|---|---|---|---|
| r/evangelion 登録者数 | 約110万 | [GummySearch](https://gummysearch.com/r/evangelion/)(検索要約) | 2026-10-05 | 中(集計サイトの数値。Reddit本体で再確認) |
| MyAnimeList 全体会員数 | 約1,380万 | [thehiveindex](https://thehiveindex.com/communities/myanimelist/) | 2026-10-05 | 低(古い可能性) |
| 日本の非公式「謎」本 | 10タイトル確認([CSV](jp_unofficial_books.csv)) | web検索 | 2026-10-05 | 中(出版年は未確認。多くは中古市場の掲載) |
| 英語圏の非公式批評本 | `evangelion analysis` 上位は評価数 0〜11 | [COMPETITOR_RESEARCH.md](../COMPETITOR_RESEARCH.md) | 2026-10-05 | 中(Amazon.com上位4冊のみ) |

## 取得を試みて失敗
| 指標 | 理由 |
|---|---|
| Wikipedia 月間ページビュー(エヴァ/チェンソーマン/鬼滅) | 取得環境から API が応答せず。**ユーザー側のブラウザで取得**する |

## 人力で取得してほしい(各5分)
1. **Wikipedia ページビュー**: [pageviews.wmcloud.org](https://pageviews.wmcloud.org/) で `Neon Genesis Evangelion` / `Chainsaw Man` / `Demon Slayer: Kimetsu no Yaiba` を2019年〜現在の月次で比較し、グラフのスクリーンショットかCSVを貼る
2. **Google Trends**: 同3作品(+ `Evangelion analysis` / `Evangelion explained`)を「全世界・過去5年」で比較したスクリーンショット
3. **Amazon Best Sellers Rank**: 既に見た4冊と、エヴァ関連の英語書籍上位10冊の「Product details」欄
4. **YouTube**: `evangelion explained` / `evangelion ending explained` の上位動画の再生回数(解説需要の直接の指標)
5. **日本側**: Amazon.co.jp で、上の10タイトルのうち新品流通しているもの(=今も売れている/刊行が続いている)

## 解釈の注意
- 日本の「謎」本ブームは、**作品の人気が最高潮で未完結だった時期の需要**に強く依存している可能性がある。同じ状況が英語圏で再現する保証はない。
- 競合が少ない=市場が空白、とは限らない。**需要が小さいために供給がない**可能性も同程度にある。この区別がつくのは、上の1〜4の数字が揃ってから。
