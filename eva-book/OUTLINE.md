# 章立て v0.4(書籍版)

**規模**: 全45ファイル・目標 約33.7万語。**第1版(Tier A)= 約26.7万語**、増補(Tier B)= 約7万語。
`chapters.csv` が進捗の正。`python3 build/build.py --tier-a` で第1版だけをビルドできる。
**この規模は目標であり、品質より優先しない**。各章は「正確 → 網羅 → 読みやすさ」の順で優先する。

**本書の背骨(仮説)**: エヴァは「他者との接触」という同じ問いに、TV版・旧劇場版・新劇場版でそれぞれ違う答えを出した。その変化は、制作者と観客との26年の関係の変化と重なって読める。→ 第26章で展開し、各章の証拠で検証する。通らなければ修正する。

---

## 設計原則(正確性と網羅性を両立させる仕組み)

1. **証拠の3階層**: 本書のすべての主張に **Shown(作中)/ Stated(制作者の発言・公式資料)/ Interpreted(解釈)** を付ける。
2. **版(Version)の明示**: エヴァには複数の版がある(TV放映版、各種再編集版・ディレクターズカット、旧劇場版の公開形態、新劇場版の各作品)。**どの版の話かを必ず書く**(要検証: 各版の正確な構成)。
3. **論点(debate)として整理**: ネット上の議論は「誰が・何を主張し・根拠は何か」の形で整理する。`atlas/debates/` が正本。**議論の紹介は、意見を事実として扱わない**。
4. **3つの読み方**: 各章の冒頭に **At a glance**(1分で読める要約)、本文(標準)、**Deep dive**(根拠・異説・出典の詳細)を置く。初心者も熟練ファンも使える。
5. **相互参照**: 各章の末尾に「関連する論点(db-)」「次に読む章」を置く。巻末に論点索引。
6. **新作の影響範囲の隔離**: 更新が要るのは c35 / fm2 / b01 / b04 のみ。

## 各話ガイドの型(c05〜c09、全26話に同一構造)
1. **Synopsis**(Shownのみ。ネタバレ範囲を明示)
2. **What the episode establishes**(世界設定・人物の新事実。atlas項目へリンク)
3. **Character beats**(人物の動機・変化)
4. **Direction and style**(演出・音楽・映像の特徴)
5. **Production notes**(Stated のみ。出典つき)
6. **Interpretation and open questions**(関連する debate へリンク)
7. **Why it matters later**(後の話・旧劇・新劇への接続。ネタバレ注意の表示)
8. **Version notes**(版による差異がある場合)

---

## Front matter
| 章 | 内容 | Tier |
|---|---|---|
| fm1 How to Read | 証拠3階層、版の表記、ネタバレ方針、略称、3つの読み方、引用ルールの説明 | A |
| fm2 Primer(ネタバレなし) | 作品の全体像、何を観る順か、各作品の位置づけ、**新作についての現状(更新対象)** | A |

## Part I — Context and Creator
| 章 | 問い・節 | Tier |
|---|---|---|
| c01 1995 | 1995年の日本(社会・経済・事件の影響は**断定せず出典で示す**)/ 当時のアニメ産業 / ガイナックスの成り立ち / 放映枠 | A |
| c02 Anno Before Evangelion | 庵野秀明の経歴: 参加作品、監督作、作風の形成 / 本人の発言 | B |
| c03 Making the TV Series | 企画の経緯 / スタッフ(キャラクター、メカ、音楽、脚本)/ 制作スケジュールと予算 / 最終2話の事情(**Stated と Interpreted を分離**)/ 放映と視聴率 | A |
| c04 The Phenomenon | 放映中の反響 / 雑誌・ファンコミュニティ / 商品展開の始まり / 社会現象としての受容 | B |

## Part II — The Television Series
| 章 | 内容 | Tier |
|---|---|---|
| c05 Episodes 1–7 | 各話ガイド(上記の型) | A |
| c06 Episodes 8–13 | 同上 | A |
| c07 Episodes 14–20 | 同上 | A |
| c08 Episodes 21–24 | 同上。**21〜24話は版による差異(要検証)** | A |
| c09 Episodes 25–26 | 同上。最終2話の構造 | A |
| c10 The World | **確定事項表**: 使徒、エヴァ(ユニット)、NERV/GEHIRN、SEELE、MAGI、セカンドインパクト、死海文書、ロンギヌスの槍、アダムとリリス、人類補完計画。各項目に Shown / Stated / Interpreted を付す | A |
| c11 The Characters | 主要人物の詳細。人物ごとに **経歴/動機/関係/変化/版による違い/論点**。(シンジ、レイ、アスカ、ミサト、ゲンドウ、リツコ、加持、カヲル、ユイ、冬月、キール、マリ ほか) | A |
| c12 Direction, Style, Music | 演出の特徴、映像言語、文字カット、劇伴・主題歌・使用楽曲(**使用楽曲は事実確認**)| A |

## Part III — The 1997 Films
| 章 | 内容 | Tier |
|---|---|---|
| c13 The Films and Their Versions | 旧劇場版の公開形態と各版の関係(**要検証**)/ 何を観ればよいか | A |
| c14 The End of Evangelion | 場面ごとの解説 | A |
| c15 Two Endings Compared | TV25–26話と旧劇の対照表 / **db-ending-mirror**(鏡か補完か)/ db-instrumentality | A |
| c16 Reception and Aftermath | 公開当時の反応(日本・海外)/ 制作者の発言 / 論争 | B |

## Part IV — Between Eras
| 章 | 内容 | Tier |
|---|---|---|
| c17 Evangelion After Evangelion | 漫画版 / ゲーム / 商品展開 / パチンコ等(**事実確認要**)/ ガイナックスとカラー | B |

## Part V — Rebuild
| 章 | 内容 | Tier |
|---|---|---|
| c18 Why Rebuild? | カラー設立と再始動の経緯 / 企画意図の発言 | A |
| c19 1.0 | 場面ガイド+TV版との対照 | A |
| c20 2.0 | 場面ガイド+新要素(マリ等)| A |
| c21 3.0 | 場面ガイド / **受容が割れた理由の整理(db-q-reception)** | A |
| c22 3.0+1.0 | 場面ガイド / 結末 / db-thrice-ending | A |
| c23 What Changed | TV・旧劇・新劇の比較表(人物・設定・場面・結末)| A |
| c24 The Loop Question | **db-rebuild-loop** / 他の新劇場版論 | A |

## Part VI — Interpretation and Debate
| 章 | 内容 | Tier |
|---|---|---|
| c25 A Map of Interpretations | 日本語圏の考察文化、英語圏のファン議論、学術研究を**地図として整理**(誰の議論か、何を根拠にするか)| B |
| c26 Themes | 他者/親子/身体/ケア/成熟。**背骨を展開する中心章**。ヤマアラシのジレンマ | A |
| c27 Borrowed Symbols | 宗教・心理学・神話の引用: 構造か装飾か(**制作者の発言を確認**)| B |
| c28 Gender, Sexuality, Representation | 女性像、性、**カヲルの台詞と翻訳論争**、批判の変遷 | B |
| c29 The Author in the Work | 伝記的読解とその限界。**慎重に扱う** | B |
| c30 The Great Debates | 論点(`db-*`)19件を主張と根拠つきで整理 | A |

## Part VII — Evangelion in English
| 章 | 内容 | Tier |
|---|---|---|
| c31 Release History | 英語圏への流通史: VHS/DVD、旧英語版、2019年の配信と新吹替、新劇場版の配信(**要検証**)| A |
| c32 Translation Problems | 題名・用語・台詞の訳の問題。**db-kaworu-suki**、db-netflix-dub | A |
| c33 Western Fandom | 英語圏ファンコミュニティの歴史と議論の特徴 | B |

## Part VIII — Legacy
| 章 | 内容 | Tier |
|---|---|---|
| c34 Legacy and Influence | **影響を明言した発言のみ**を根拠に | B |
| c35 The New Era | 完全新作について**確定していること**(2026-02-23 制作発表。公開時期は未発表)| A・**更新対象** |

## Part IX — Answers
| 章 | 内容 | Tier |
|---|---|---|
| c36 FAQ | よくある質問への**短い答え+証拠レベル+章への導線**。海外ファンの典型的な疑問(ネット上の質問を収集して選ぶ)| A |

## Back matter
| 章 | 内容 | Tier |
|---|---|---|
| b01 Timeline | 制作・公開・出来事の年表(更新対象)| A |
| b02 Glossary | 用語集(atlas `term-*` から生成)| A |
| b03 Reference Tables | 人物・ユニット・スタッフ・クレジットの表 | A |
| b04 Viewing Order | 観る順ガイド(更新対象)| A |
| b05 Bibliography | 日本語・英語の一次/二次資料 | A |
| b06 Index of Debates | 論点索引 | A |

---

## 「ネット上の知見」の取り込み方(正確性を保つ手順)
1. **論点を `atlas/debates/` に登録**(現在19件。質問・関連項目・出典)。
2. 各論点に、**主張者(媒体名・著者・日付)/ 主張 / 根拠 / 証拠レベル / 出典**を記録する。
3. ファンWiki・まとめ記事は**手がかりのみ**。事実の根拠にするのは、作品そのもの・公式資料・制作者の一次発言。
4. 同じ主張を複数の出典が支持しても、**出典同士が互いを引用しているだけ**でないかを確認する。
5. 日本語圏の議論は、書名・媒体・年を記録し、**自前の要約・翻訳**で紹介する。
6. FAQ(c36)は、英語圏で実際に多い質問(Reddit FAQ、検索の関連質問等)を収集して選ぶ。

## 新作の続報があったときの更新手順
1. `atlas/events/` に公式発表を日付つきで追加し、`atlas/works/work-new.md` を更新
2. c35 を更新(確定情報のみ。推測は **Interpreted** と明記)
3. fm2 / b01 / b04 の該当箇所を更新
4. `python3 build/build.py --release` → KDPで更新版を公開

## 優先順位(執筆の進め方)
1. **c10 世界設定の確定事項表**(他のすべての章の土台)
2. **c05 各話ガイドの1〜2話分**で型と文体を確定
3. **c30 論点の整理**(ネット上の知見の取り込みが機能するかの検証)
4. 残りを Tier A から順に
