# 2026年試験直前500問：第3次監査（2026-10-22）

**指定書名：2026年登録日本語教員試験　直前対策５００問＋詳細な解説**

## 制作状況
前回GitHub学術監査稿を統合した単一Wordを基準に、正答肢の長さ差20字以上32問を優先精査。前回改稿20問に、今回出典・ケースの原文確認を伴う12問の正答肢の短文化を追加した。元原稿は上書きしない。**出版判定は保留。**

### 今回の追加12問と照合根拠
- `Q_M_002`　国際交流基金EPA教育事業：https://www.jpf.go.jp/j/project/japanese/education/training/epa/about.html
- `Q_2_012`　国立国語研究所外来語言い換え：https://www2.ninjal.ac.jp/gairaigo/Teian1_4/Words/informed_consent.gen.html
- `Q_2_025`　文化庁敬語の指針：https://www.bunka.go.jp/seisaku/kokugo_nihongo/kokugo_shisaku/keigo/chapter2/detail.html
- `Q_2_009`　外務省・自由権規約第27条：https://www.mofa.go.jp/mofaj/gaiko/kiyaku/2c_004.html
- `Q_M_055`　文化庁「させていただく」の条件：https://www.bunka.go.jp/seisaku/kokugo_nihongo/kokugo_shisaku/keigo/chapter3/detail.html
- `Q_1_024`　アジア歴史資料センター台湾総督府国語学校：https://www.jacar.go.jp/exhibition/glossary/term2/0050-0010-0010-0010-0220.html
- `Q_4_125`　著作権法32条・48条：https://www.cric.or.jp/db/domestic/a1_index.html
- `Q_3_011`　Atkinson & Shiffrinの短期貯蔵/制御過程：https://www.sciencedirect.com/science/chapter/bookseries/pii/S0079742108604223 （原著全頁再読は未完）
- `Q_5_028`　東京外国語大学「し」の発音：https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/03-04-01.php
- `Q_O_031`　東京外国語大学「Vています」過去経験：https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/045.html
- `Q_O_063`　原稿内「ケース13」本人同士の多数決・全員納得の対立説明を本文対照
- `Q_MO_005`　聴解トップダウン/ボトムアップ：https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/articles/listening-top-down-and-bottom

### 完成度の数値
| 項目 | GitHub統合直後 | 20問修正後 | 今回12問追加後 |
|---|---:|---:|---:|
| 正答だけが次点より20字以上長い | 32 | 12 | **0** |
| 正答が最初の最長選択肢 | 290 | 284 | **284** |
| 正答が次点より10字以上長い | 122 | 105 | **99** |

大きな手がかりを解消したが、最長が正答284/500、誤答肢の断定「必ず・一切・すべて」等による手がかりも残る。**選択肢品質の最終学術検証は未完。**

### 最新ローカル原稿と検査
- Word：`2026_登録日本語教員試験_直前対策500問_v9_選択肢精査32問_要最終確認.docx`　SHA256 `e9bcdb59cf562f8a0e84f3a905e2fb4e73d8bc85e848e5710cade38f738457c8`
- EPUB：`2026_登録日本語教員試験_直前対策500問_v9_選択肢精査32問_要最終確認.epub`　SHA256 `98fca3e9157d7e3433dc631ee28278a8c70a20746d351c57c219a93876e4298c`
- 追加改稿12件では設問・誤答・正答番号・肢別解説の変更**0件**。500問／500解答ブロックを対照して差分は意図どおりの正答肢12件だけ。
- Word内部リンク2,060件・EPUB内部リンク2,102件・参照先欠落0。
- EPUBの500問、500解答、4肢、4解説、正誤、正答についてWordとの不一致0。全2000解説本文一致。
- EPUB独自パッケージ検査11/11。**公式EPUBCheck・Kindle Previewerの実行ではない**。
- LibreOfficeのPDF新描画は373頁。空白頁・領域外テキスト・置換欠字などの**機械検査警告0**。今回影響12頁をPNG画像にして縮小一覧で直接確認。**全373頁の原寸逐頁確認は未完了**。

## 今後の出版ゲート
(1) 改稿32問の独立学術再確認、(2) 出題品質の偏り・簡単すぎる誤答肢の再設計、(3) 公式EPUBCheckとKindle Previewer、(4) 全頁原寸目視、(5) 新表紙とタイトル・著者経歴・出典/権利・AI申告・旧版開示・価格の確認、(6) ユーザー公開承認。

**release_ready=false。** このレポートは作業を記録するものであり、KDPに提出することを承認しない。DOCX/EPUB本体は別途コンテナに生成、GitHubへのバイナリのアップロードは未実施。
