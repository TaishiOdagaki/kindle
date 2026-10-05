# Evangelion 決定版(英語Kindle)— 制作ハブ

**目的**: これまでのエヴァの情報を網羅した決定版を、**いつでも出版できる状態**で保つ。
完全新作(2026-02-23 制作発表済み・公開時期未発表)が海外展開を強めた時点で、すぐ刊行できるようにする。

## 言語の運用(2026-10-05 決定): 日本語版を先に、英語版はその後
1. **日本語版(`manuscript/ja/`)が正本**。まず日本語で書き、全話視聴にもとづく確認(`[[CHECK]]` の解消)を済ませる。
2. 日本語版の確認が済んだ章から、**英語版(`manuscript/en/`)へ翻訳**する(確認済みの内容だけを訳す)。
3. 日本語版自体も、日本語圏向けの書籍として出せる。
4. 現在の `manuscript/en/` は、初期の下書きとスタブ。**第10章の英語版は旧稿(参考)**で、日本語版の確認後に訳し直す。

```bash
python3 build/status.py              # 日本語の進捗(既定)
python3 build/status.py --lang=en    # 英語の進捗
python3 build/checks.py              # 未確認の印の一覧(data/verification/CHECKLIST.md)
python3 build/build.py               # 日本語の下書きEPUB
python3 build/build.py --lang=en     # 英語の下書きEPUB
```

## 分冊構成(2026-10-05 決定)
三冊に分ける。第1巻「背景とTVシリーズ」/ 第2巻「旧劇場版と新劇場版」/ 第3巻「解釈・英語圏・FAQ」。詳細は [`OUTLINE.md`](OUTLINE.md)。
`chapters.csv` の `volume` 列が各章の所属(共通の章は `1|2|3`)。

```bash
python3 build/build.py --vol=1       # 第1巻のみ(--vol=2, --vol=3 も同様)
python3 build/build.py               # 全巻を1冊にした編集用コピー
python3 build/status.py --vol=2      # 第2巻の進捗
python3 build/build.py --vol=1 --release   # 第1巻のリリースゲート
```

## デザイン(巻のイメージカラー)
第1巻=赤 / 第2巻=黄 / 第3巻=青(2026-10-05 決定)。仕様は [`design/DESIGN.md`](design/DESIGN.md)、図表の方針は [`FIGURES.md`](FIGURES.md)。

```bash
python3 build/design_check.py        # 色のコントラスト・グレースケールの段差を検査
python3 build/figs.py --lang=both    # 図・話数カードを再生成
python3 build/cover.py --lang=both   # 表紙(仮)を再生成
```

## 全体像: 「正本」はテキスト、本とWebはその出力
```
atlas/(項目ごとのデータ) ─┬→ 本(Kindle EPUB)
manuscript/(章の原稿)  ───┤→ Webサイト「Evangelion Atlas」
                          └→ JSON(アプリ・動画・SNS等の素材)
```
GitHub上のテキストが正本。形式(本/Web/その他)は後から増やせる。

## 設計の核心: 「完成した本体」+「差し替えモジュール」
- 本体(第1〜15章+巻末)は**新作に左右されない**。先に完成・検証しておく。
- 新作に左右される部分は**3か所だけ**に隔離: `c19`(The New Era)、`fm2`(Primer)、`b01`/`b03`(年表・観る順)。`chapters.csv` の `update_sensitive` で管理。
- 新作の続報が出たら、この3か所だけを更新して再ビルドする。本体は触らない。
- Kindleは刊行後も原稿を更新でき、増補版として出し直せる。

## ディレクトリ
| パス | 内容 |
|---|---|
| [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md) | 企画書(方針・権利・体制) |
| [`OUTLINE.md`](OUTLINE.md) | 章立て(各章の問い・必要な証拠) |
| [`STYLE_GUIDE.md`](STYLE_GUIDE.md) | 文体・引用ルール・証拠の3階層 |
| [`SOURCES.md`](SOURCES.md) | 資料の優先順位と検証手順 |
| [`COMPETITOR_RESEARCH.md`](COMPETITOR_RESEARCH.md) | 競合調査 |
| [`atlas/`](atlas/SCHEMA.md) | **正本**。項目ごとのデータ(各話・作品・人物・用語・テーマ・出来事・出典) |
| [`data/`](data/) | 需要データ、競合データ |
| `manuscript/` | 原稿(1章1ファイル) |
| `chapters.csv` | 章の進捗管理(status / fact_check / update_sensitive) |
| `build/` | EPUBビルドと進捗表示 |

## コマンド
```bash
pip install pypandoc_binary          # 初回のみ
python3 build/status.py              # 進捗表
python3 build/build.py               # 下書きEPUB(build/draft.epub)
python3 build/build.py --release     # リリースゲート(未完成なら失敗)
python3 build/validate.py            # atlas の検査
python3 build/atlas_site.py          # Webサイト(build/site/)とJSON(build/atlas.json)
```
**リリースゲート**: 全章が `status=final` かつ `fact_check=done` で、`TODO` が残っていないと、リリース用EPUBは作られない。

## 出版可能状態のチェックリスト
**原稿**
- [ ] 全章 `final` / `fact_check=done`
- [ ] atlas の本に使う項目がすべて `status: verified`
- [ ] 全引用が STYLE_GUIDE の基準内
- [ ] 奥付の文言を確定(PROJECT_BRIEF §5)
- [ ] 英語ネイティブ校閲済み

**KDP(要・実際の入力画面で最新要件を確認)**
- [ ] AI生成コンテンツの申告方針を決定し、入力画面で申告する
- [ ] 書名・サブタイトル・著者名・説明文(4000字以内を想定)・キーワード・カテゴリ
- [ ] 表紙(独自制作。作品素材なし)
- [ ] EPUBを作成し、KDPのプレビューアで目視確認
- [ ] 価格と販売地域

## 現在の状況
- 2026-10-05: 企画書、競合調査、需要データ(Wikipedia、公式動画の参考値)、章立て、ビルド環境を作成。**原稿は未着手(スタブのみ)**。
- 2026-10-05: 日本語版 第10章(世界設定)の初稿(約1.7万字・目標2.8万字の約6割)。作品との照合が必要な箇所に `[[CHECK]]` を約200件。
- 次: 全話視聴にもとづく第10章の確認 → 第10章の増補(発言の層の補強)→ 第11章。
