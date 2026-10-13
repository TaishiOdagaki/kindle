#!/usr/bin/env python3
"""One-time evidence-bound revision of two corrective-feedback items."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b


prior = [
    change for change in json.loads((b.OUT / "changes.json").read_text())
    if change.get("before_version") != "第58バッチ反映後の累積作業稿"
]
assert len(prior) == 1214
_, questions, answers = qa.audit(str(b.DST))
decisions = json.loads((b.OUT / "decisions.json").read_text())
extra = []


def rewrite(qid, key, stem, options, explanations, reason, verdicts,
            stem_review, explanation_review, stem_parts=None):
    old_stem = stem_parts[0] if stem_parts else questions[qid]["stem"]
    fields = [
        ("stem", [old_stem], [stem]),
        ("options", questions[qid]["opts"], options),
        ("explanations", answers["A_" + qid[2:]]["txt"], explanations),
    ]
    for field, old_values, new_values in fields:
        for index, (before, after) in enumerate(zip(old_values, new_values)):
            if html.unescape(before) == after:
                continue
            extra.append(
                {
                    "id": qid,
                    "field": field,
                    "index": None if field == "stem" else index,
                    "before": html.unescape(before),
                    "after": after,
                    "reason": reason,
                    "sources": ["S123"],
                    "applied": True,
                    "before_version": "第58バッチ反映後の累積作業稿",
                }
            )
    if stem_parts:
        for old_part in stem_parts[1:]:
            extra.append(
                {
                    "id": qid,
                    "field": "stem",
                    "index": None,
                    "before": old_part,
                    "after": "",
                    "reason": reason,
                    "sources": ["S123"],
                    "applied": True,
                    "before_version": "第58バッチ反映後の累積作業稿",
                    "remove_paragraph": True,
                }
            )
    decisions[qid].update(
        status="確認済み",
        fixes_applied=True,
        independent_answer=key,
        sources=["S123"],
        option_verdicts=verdicts,
        reason=reason,
        stem_review=stem_review,
        explanation_review=explanation_review,
        unresolved="",
        multiple_correct_risk="なし：Lyster & Ranta（1997）の6分類で独立正答のみが定義に一致",
        no_correct_risk="なし：独立正答" + str(key),
    )


rewrite(
    "Q_2_035",
    1,
    "LysterとRanta（1997）の訂正フィードバック分類に照らし、次の教師の応答に最も当てはまるものを選べ。学習者：『昨日、図書館へ行きますした。』教師：『「行きますした」とは言いません。「行きました」と言います。』",
    [
        "明示的訂正",
        "リキャスト",
        "明確化要求",
        "誤りの反復",
    ],
    [
        "教師は誤りであることを明示したうえで、正しい形『行きました』を直接与えています。これは明示的訂正です。",
        "リキャストは、通常、誤りだと明示せずに学習者の発話の全部または一部を正しい形へ言い換えるものです。この例は『とは言いません』と誤りを明示しています。",
        "明確化要求は、聞き取れなかったことや発話に問題があることを示し、反復・言い換えを求めます。この例では教師自身が正しい形を提示しています。",
        "誤りの反復は、教師が学習者の誤った発話を単独で繰り返し、多くの場合イントネーションで誤りを際立たせるものです。この例は正しい形も直接提示しています。",
    ],
    "旧稿はポルトガル語を含む発話への翻訳・言語説明をリキャストと断定し、心理的安全性や複言語教育の効果まで根拠なく一般化していた。原著46〜49頁の6分類に一致する明示的訂正の事例へ全面改稿した。",
    [
        "正答：誤りの明示と正しい形の直接提示を併せ持つ",
        "誤答：暗示的な正形式への言い換えではない",
        "誤答：反復・言い換え要求ではなく正形式を提示",
        "誤答：誤形だけを単独で反復する事例ではない",
    ],
    "Lyster & Ranta（1997）原著46〜49頁で明示的訂正、リキャスト、明確化要求、誤りの反復の定義を照合し、発話例を一義的に分類できる条件へ改稿。",
    "4解説を各分類の必要条件へ直接対応させ、旧稿の心理的効果・複言語主義に関する未立証の補助主張を撤去。",
    [
        "ある多文化共生推進事業での「日本語ボランティア教室」の授業風景を以下に示す。",
        "受講生Aさん（ブラジル出身）：「先生、土曜日のイベント、 Eu vou（私は行きます） ！ 友達もjunto（一緒に）いきます。」",
        "支援者Bさん：「あ、Aさん、来てくれるんですね！ 『Eu vou』はポルトガル語ですね。日本語で『いきます』ですね！ 友達も『一緒に』ですね、嬉しいです！」",
        "このやり取りにおけるコミュニケーションおよび言語使用に関する分析として、最も適切なものを一つ選びなさい。",
    ],
)

rewrite(
    "Q_4_068",
    3,
    "LysterとRanta（1997）の訂正フィードバック分類に照らし、次の教師の応答に最も当てはまるものを選べ。学習者：『昨日、図書館へ行って、勉強しなかったでした。』教師：『勉強しなかったでした？』学習者：『あ、勉強しませんでした。』",
    [
        "リキャスト",
        "明示的訂正",
        "誤りの反復",
        "メタ言語的フィードバック",
    ],
    [
        "リキャストなら教師が誤りを除いた正しい形へ言い換えます。この例では教師は誤った部分をそのまま繰り返しています。",
        "明示的訂正なら、誤りであることを明示し、正しい形を直接与えます。この例では教師は正しい形を提示していません。",
        "教師は学習者の誤った部分を単独で繰り返し、疑問調のイントネーションで誤りを際立たせています。原著の『repetition（誤りの反復）』に当たります。",
        "メタ言語的フィードバックは、正しい形を直接与えずに、発話の適格性についてコメント・情報・質問を示すものです。この例には文法用語や適格性へのコメントがありません。",
    ],
    "旧稿は説明文では反復を記述していたが選択肢に分類名がなく、さらに許容される『勉強しなかったです』への注意書きが実際の誤形『勉強しなかったでした』と混線していた。原著の分類名を4肢に明示して単一正答化した。",
    [
        "誤答：教師は正形式へ言い換えていない",
        "誤答：誤りの明示と正形式の直接提示がない",
        "正答：誤形を単独で疑問調に反復",
        "誤答：適格性へのコメント・情報・質問がない",
    ],
    "原著48頁のrepetition定義（誤った発話を単独で繰り返し、多くの場合イントネーションを調整）と他3分類を照合。誤形は『なかったでした』に固定。",
    "4解説を原著の分類条件に対応させ、『なかったです』を一律に誤用と扱わないという別論点を設問から分離。",
)


(b.OUT / "changes_batch59.json").write_text(
    json.dumps(extra, ensure_ascii=False, indent=2) + "\n"
)
(b.OUT / "changes.json").write_text(
    json.dumps(prior + extra, ensure_ascii=False, indent=2) + "\n"
)
(b.OUT / "decisions.json").write_text(
    json.dumps(decisions, ensure_ascii=False, indent=2) + "\n"
)
source_path = b.OUT / "sources.md"
source_text = source_path.read_text()
if "| S123 |" not in source_text:
    with source_path.open("a") as source_file:
        source_file.write(
            "\n| S123 | Roy Lyster & Leila Ranta（1997）[Corrective Feedback and Learner Uptake: Negotiation of Form in Communicative Classrooms（著者アップロード全文）](https://www.researchgate.net/publication/252160472_CORRECTIVE_FEEDBACK_AND_LEARNER_UPTAKE_Negotiation_of_Form_in_Communicative_Classrooms)、[Cambridge University Press書誌・要旨](https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/abs/corrective-feedback-and-learner-uptake/59229F0CA2F085F5F5016FB4674877BF)、[McGill公開記録](https://www.escholarship.mcgill.ca/concern/articles/0p096b84r?locale=en) | 原著46〜49頁の6分類を全文で照合。明示的訂正は誤りを明示して正形式を与える、リキャストは誤りを除いた言い換え、反復は誤形を単独で繰り返し多くの場合イントネーションで強調する。複合フィードバックの優先規則も確認。 | 2026-10-14取得。著者アップロード全文を本文確認し、出版社書誌・DOIと同定。観察研究内の分類を問うにとどめ、各技法の普遍的な教育効果や心理的効果は承認しない。 | Q_2_035、Q_4_068 |\n"
        )

evidence = b.OUT / "evidence" / "batch59_source_review.md"
evidence.write_text(
    "# 第59バッチ原資料照合記録\n\n"
    "対象：Q_2_035、Q_4_068\n\n"
    "Lyster & Ranta（1997）の著者アップロード全文と出版社書誌を同定し、原著46〜49頁の訂正フィードバック6分類を精読した。明示的訂正は誤りを明示して正しい形を与える。リキャストは通常、誤りを明示せずに誤りを除いた形へ言い換える。反復は誤った発話を単独で繰り返し、多くの場合イントネーションで誤りを際立たせる。原著は、正しい形をメタ言語的に枠づけて提示する場合は明示的訂正として扱うことも説明している。\n\n"
    "旧Q_2_035は翻訳・言語説明・リキャスト・複言語教育の評価を一つの正答に混在させていたため、原著の明示的訂正を一義的に問う事例へ置換した。旧Q_4_068は実質的には反復を記述していたが分類名がなく、許容形『なかったです』と実際の誤形『なかったでした』が解説内で混線していたため、誤形の単独反復と疑問調を明示した。\n\n"
    "照合範囲は分類定義であり、訂正技法の普遍的な優劣、心理的安全性、複言語教育一般への効果は承認していない。\n"
)
print("2 questions /", len(extra), "edits")
