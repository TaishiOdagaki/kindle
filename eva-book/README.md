# Evangelion 決定版(英語Kindle)— 制作ハブ

**目的**: これまでのエヴァの情報を網羅した決定版を、**いつでも出版できる状態**で保つ。
完全新作(2026-02-23 制作発表済み・公開時期未発表)が海外展開を強めた時点で、すぐ刊行できるようにする。

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
| [`data/`](data/) | 需要データ、競合データ、**事実DB(`data/facts/`)** |
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
- 次: 事実DBの検証 → 第3章(各話ガイド)の試作 → 文体の確定。
