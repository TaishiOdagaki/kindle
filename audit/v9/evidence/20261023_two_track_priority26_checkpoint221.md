# v9二系統統合チェックポイント221：優先26問の採否確定

実施日：2026-10-23。作業先：`audit/v9-integration-2026-10-21`。**出版保留・`release_ready=false`**。

## 対象と手順

- GitHub専用監査系DOCX SHA256：`aea97d09d9cefebbd4c2220c4728e8c01adaecfd97e832fc0963c053ac2d32ee`
- ライブラリ系DOCX SHA256：`c19bc83a517805bb1235ce2e124b127e5b6c6219f37691bf61d4c1cbb6e73e6a`
- 完全diff JSON SHA256：`d66ac5ccd19cbee348223a27013cf866d70da0b035abc29260618ce19fbee497`
- 判定台帳：専用監査ブランチHEAD `59d01867eea303ed99f7957a7c44c8ac8b06db4c`、`decisions.json` blob `2fb43017ad5a0a5b11be00fce1fb734442937e29`

前回取得した両DOCXの実バイナリ完全diffを再利用し、設問比較を繰り返していない。既存の低文字一致優先26問について、差のある設問・ケース・4肢・4解説を、各問の独立正答、原典照合記録、未確認欄と突合した。

## 判定結果

優先26問・230差異フィールドは、すべて`accept-github`と判定した。全26問で`status=確認済み`、`fixes_applied=true`、`unresolved`空欄である。ライブラリ版の一括排除ではなく、各問について次の理由を確認した。

| 問題ID | 差異数 | 根拠ID | 採否理由の要約 |
|---|---:|---|---|
| `Q_2_013` | 9 | S149 | 原論文表5の回避・達成補償・時間稼ぎに直接対応し、旧版の分類混同を除去 |
| `Q_4_021` | 9 | S149 | 原論文表5の明確化・確認要求・理解チェックの発話例に限定 |
| `Q_4_022` | 9 | S146 | Long本人の図2の七段階を直接問う形で、一般的コース設計論との混同を回避 |
| `Q_4_104` | 9 | S214・S216 | 欧州評議会資料のロールプレイ・固定観念の検討へ限定し、未取得の教授法一般論を除去 |
| `Q_4_117` | 9 | S173 | FLN本人の定義と四本柱へ限定し、動画時間・効果の普遍断定を除去 |
| `Q_5_094` | 10 | S45 | CEFR補遺版の主題展開・結束性に照合し、短文からの過剰診断を撤回 |
| `Q_M_009` | 9 | S298 | Trudgill原著の潜在的威信・過少申告へ直接照合 |
| `Q_M_041` | 9 | S265 | UNESCOの人間中心・プライバシー・倫理的検証に限定し、製品効果や法的結論を除去 |
| `Q_3_029` | 10 | S148 | Oxford本人の6分類へ限定し、別分類との混同を除去 |
| `Q_4_045` | 9 | S144 | Richards本人の活動分類・論争整理に限定し、教材形式の一律優劣を撤回 |
| `Q_4_105` | 9 | S253 | Hall原著の高低文脈・連続体に照合し、国籍から個人を推測する一般化を撤回 |
| `Q_4_121` | 9 | S162 | CC BY 4.0リーガルコード第2・3条へ直接照合 |
| `Q_O_036` | 9 | S173 | FLNの反転設計と四本柱の充足を区別 |
| `Q_O_038` | 8 | S173 | FLNの観察・調整・アクセス配慮・形成的評価をケースへ限定適用 |
| `Q_M_058` | 9 | S153 | Rosch原著の典型性と階層、モデル上の留保を反映し語源・普遍効果の断定を除去 |
| `Q_5_098` | 9 | S150 | Thomas原論文の社会語用論・語用言語学の区別に照合 |
| `Q_4_034` | 9 | S242 | Larsen-Freeman & Anderson原著の直接法の原則へ直接照合 |
| `Q_M_011` | 9 | S254 | Sacks・Schegloff・Jefferson原論文の話者交替規則へ差替え・照合 |
| `Q_M_046` | 9 | S76 | 東京外大教材の無声化条件・声帯振動・アクセント核を反映 |
| `Q_O_030` | 6 | S179 | CEFRの共通基準・複数判断を架空ケースへの編集提案として限定 |
| `Q_M_047` | 9 | S158 | 東京外大教材の語中`[g]/[ŋ]`と意味不変へ限定し、分布の過度な一般化を撤回 |
| `Q_4_083` | 9 | S166 | Schön原著の行為の中の省察・暗黙の理解の再検討へ直接照合 |
| `Q_4_124` | 9 | S26 | e-Gov著作権法第35条全3項へ直接照合し、補償金と同時授業送信の例外を区別 |
| `Q_M_050` | 9 | S159 | 文化庁2022年建議の読点位置・意味・必要時の書換えへ限定 |
| `Q_4_060` | 7 | S179・S142 | CEFRの直接/間接と主観/客観を区別し、採点方式・コストの普遍断定を除去 |
| `Q_5_103` | 9 | S151 | Fisher・Ury・Patton原著の利害・複数案・非保証に限定し、文化類型の未照合断定を除去 |

主要根拠URL：

- S149：<https://b9f19ceb-f720-4252-a2be-ccde56c0821f.filesusr.com/ugd/ba734f_1c905f1db74f488d924e158afdb63986.pdf?index=true>
- S146：<https://woucentral.weebly.com/uploads/7/4/6/9/7469707/long_1997_intro_focus_on_form.pdf>
- S214：<https://www.coe.int/en/web/compass/using-compass-for-human-rights-education>
- S216：<https://rm.coe.int/16808ce258>
- S173：<https://flippedlearning.org/wp-content/uploads/2016/07/FLIP_handout_FNL_Web.pdf>
- S45：<https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4>
- S298：<https://web.stanford.edu/~eckert/PDF/trudgill1972.pdf>
- S265：<https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=195885>
- S148：<https://web.ntpu.edu.tw/~language/workshop/read2.pdf>
- S144：<https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf>
- S253：<https://monoskop.org/images/6/60/Hall_Edward_T_Beyond_Culture.pdf>
- S162：<https://creativecommons.org/licenses/by/4.0/legalcode.ja>
- S153：<https://escholarship.org/content/qt0sz9c8qh/qt0sz9c8qh_noSplash_9502f78e7451b3a9cbc24a68329e0890.pdf>
- S150：<https://doi.org/10.1093/applin/4.2.91>
- S242：<https://elearning.usm.md/pluginfile.php/190241/mod_resource/content/2/Larsen-freeman%203rd%20ed_techniques-in-language-teaching.pdf>
- S254：<https://www.conversationanalysis.org/wp-content/uploads/2019/06/04_Sacks_Schegloff_Jefferson_A_simplest_systematics_fir_the_organization_of_turn-taking_for_conversation_Language_.pdf>
- S76：<https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/03-03-01.php>
- S179：<https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf>
- S158：<https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/02-12-01.php>
- S166：<https://www.socialworkerskills.eu/uploads/1/4/4/7/144711219/sch%C3%B6n_d._a.__1983_._the_reflective_practitioner.pdf>
- S26：<https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048>
- S159：<https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf>
- S142：<https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf>
- S151：<https://siptulearn.ie/wp-content/uploads/2018/01/Fisher-Urry-Getting-to-yes.pdf>

## 累積分類と訂正

チェックポイント220の「残る485差異問」は算術誤りだった。全差異493問のうち、その時点で分類済みの差異問は`Q_5_022`の1問だけであり、正しくは492問だった。完全一致7問は差異問の母数に含まれない。

今回までの累積は次のとおり。

| 分類 | 問題数 |
|---|---:|
| `equivalent` | 7 |
| `accept-github` | 27 |
| `accept-library` | 0 |
| `manual-rewrite` | 0 |
| 分類済み合計 | 34 |
| 未分類の差異問 | **466** |

26問は現行統合作業稿がすでに採用対象のGitHub本文と一致するため、Word本文の変更は0件。ライブラリ版からの逆戻しも行っていない。判定内容は`20261023_two_track_classifications_checkpoint221.json`へ保存する。

## 残件

1. 残る466差異問を同じ4分類で処理し、根拠ID・対象フィールド・採用理由を記録する。
2. `accept-library`または`manual-rewrite`が発生した場合のみ、新しい統合版Wordへ順序付きで反映する。
3. `Q_5_015`・`Q_5_021`の表示重なりを統合版で修正し、固定SHAの統合稿を再描画する。
4. 統合稿で全500問、目次・リンク・章別件数・表見出し、全頁表示、EPUBCheck、Kindle Previewerを再検査する。

統合稿・EPUB・最終全頁QAが未完了のため、出版可能とは判定しない。
