# Atlas データ仕様(v0.1)

**atlas/ が正本**。本(EPUB)、Webサイト(Evangelion Atlas)、JSON、その他のメディアは、すべてここから作る。
1項目 = 1ファイル = 先頭にYAML、本文はMarkdown。媒体(本・Web)に依存する書き方はしない。

## 種類(type)と配置
| type | ディレクトリ | idの接頭辞 | 例 |
|---|---|---|---|
| episode | `episodes/` | `ep-` | `ep-01` |
| work | `works/` | `work-` | `work-eoe` |
| character | `characters/` | `ch-` | `ch-shinji` |
| term | `terms/` | `term-` | `term-atfield` |
| theme | `themes/` | `theme-` | `theme-care` |
| event | `events/` | `ev-` | `ev-2026-02-23-announcement` |
| person(スタッフ等) | `people/` | `pe-` | (未作成) |
| source(出典) | `sources/` | `src-` | 出典1件=1ファイル(`title` `publisher` `url` `date` `kind` `accessed`) |
| angel(使徒) | `angels/` | `an-` | `an-sachiel`。`number` `name_en` `name_jp` `episodes`(登場話のリスト)。**図の生成に使う** |
| unit(エヴァ機体) | `units/` | `unit-` | `unit-01`。`name_jp` `name_en` `role` |
| debate(論点) | `debates/` | `db-` | `db-kaworu-suki`。**ネット上の議論を、主張者・根拠・証拠レベルつきで整理する**(`question` を持つ) |

## 共通フィールド
| フィールド | 必須 | 内容 |
|---|---|---|
| `id` | ◯ | ファイル名と一致。変更しない(他からの参照に使う) |
| `type` | ◯ | 上表のとおり |
| `status` | ◯ | `stub`(枠のみ) / `draft`(下書き) / `reviewed`(校閲済み) / `verified`(**一次資料で確認済み**) |
| `sources` | | 出典の id リスト。`verified` には必須 |
| `related` | | 関連項目の id リスト(Webの相互リンク、本の参照に使う) |
| `update_sensitive` | | 新作の続報で更新が必要な項目は `true` |

種類ごとの固有フィールド(`title_en` / `title_jp` / `name_en` / `term_en` / `number` / `air_date_jp` / `date` など)は自由に追加できる。

## 本文の書き方
- 事実は **Shown / Stated / Interpreted** を区別して書く(STYLE_GUIDE.md)。
- `verified` にできるのは、一次資料で確認できたものだけ。本文に `TODO` が残っていると `verified` にできない。

## 検証
```bash
python3 build/validate.py   # id重複、参照切れ、status、verifiedの条件を検査
```

## 出力
| 出力 | コマンド | 状態 |
|---|---|---|
| Webサイト(静的HTML) | `python3 build/atlas_site.py` → `build/site/` | **試作済み**(一覧・各項目・関連リンク・逆リンク) |
| JSON(アプリ・他メディア向け) | 同上 → `build/atlas.json` | **試作済み** |
| 本(EPUB) | `python3 build/build.py` | 章の原稿(`manuscript/`)から。**atlas からの自動組み込みは未実装** |

## 本とatlasの関係(次の設計)
- 各話ガイド(c03〜c06)は、`ep-01`〜`ep-26` の本文を**章に組み込む**形にして、同じ文章を本とWebの両方に出す。
- 解釈・批評(c15〜c17)は、本の章が主。Webでは `theme-*` に要約と本への導線を置く。
