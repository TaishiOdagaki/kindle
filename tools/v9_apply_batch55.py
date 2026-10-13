#!/usr/bin/env python3
"""One-time evidence-bound revision of transfer and overgeneralization items."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b


prior = json.loads((b.OUT / "changes.json").read_text())
assert len(prior) == 1133
_, questions, answers = qa.audit(str(b.DST))
decisions = json.loads((b.OUT / "decisions.json").read_text())
extra = []


def rewrite(qid, key, stem, options, explanations, reason, sources, verdicts):
    fields = [
        ("stem", [questions[qid]["stem"]], [stem]),
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
                    "sources": sources,
                    "applied": True,
                    "before_version": "敬語第2修正バッチ反映後の累積作業稿",
                }
            )
    decisions[qid].update(
        status="確認済み",
        fixes_applied=True,
        independent_answer=key,
        sources=sources,
        option_verdicts=verdicts,
        reason=reason,
        stem_review="取得した原論文本文に照らし、著者・年・概念の範囲を限定して4肢を独立判定。",
        explanation_review="4解説を原論文の該当箇所へ個別照合し、未照合の日本語例・効果・発達段階の一般化を撤去。",
        unresolved="",
        multiple_correct_risk="なし：原論文で明示された説明に一致するのは独立正答のみ",
        no_correct_risk="なし：独立正答" + str(key),
    )


rewrite(
    "Q_5_011",
    4,
    "Corder（1967）が述べる、第二言語学習における母語の役割について、最も適当なものを選べ。",
    [
        "第二言語学習者の誤用は、例外なく母語体系に由来し、目標言語内の学習方略を反映することはない。",
        "既に母語を身につけていることは第二言語学習を妨げるだけで、学習を助ける働きはない。",
        "母語と関係する誤用は学習初期だけに現れ、一定段階に達すると必ずすべて消える。",
        "母語体系に関係する誤用は多いがすべてではなく、既に母語をもつことは第二言語学習を助ける面もある。",
    ],
    [
        "原論文は、多くの誤用が母語体系に関係すると認める一方、すべての誤用を母語だけでは説明していません。学習者が用いる方略を示す誤用も論じています。",
        "原論文は、既に母語をもつことを第二言語学習の促進要因として扱っており、妨げだけだとはしていません。",
        "原論文は、母語と関係する誤用が初期だけに限られ、必ず消えるとは述べていません。この発達段階の全称命題は根拠本文にありません。",
        "原論文は、多くの誤用が母語体系に関係するがすべてではないと区別し、既に母語をもつことには学習を助ける面があると論じています。",
    ],
    "母語の正・負の転移全般を未取得資料で説明する旧稿を、Corder（1967）の原文で直接確認できる限定命題へ改稿。漢字圏学習者の個別例、語用論的転移、上級段階での残存・化石化は同論文から承認せず撤去した。",
    ["S118"],
    [
        "母語関連の誤用を全誤用へ一般化しており原文に反する",
        "母語保有の促進面を否定しており原文に反する",
        "初期限定・必然的消失という原文にない全称命題",
        "原論文が明示する二つの限定に一致",
    ],
)

rewrite(
    "Q_4_073",
    3,
    "Richards（1970）の誤用分析でいう「過剰般化」の説明として、最も適当なものを選べ。",
    [
        "母語と目標言語の違いだけから生じる誤用で、既に学んだ目標言語の構造は関係しない。",
        "待遇表現で丁寧体と普通体を場面に応じて切り替えることをいう。",
        "既に学んだ目標言語の構造を基に、その適用範囲を越えた形を作ることをいう。",
        "会話中に二つ以上の言語を切り替えて用いることをいう。",
    ],
    [
        "Richardsは、母語の違いだけでは説明できず、目標言語を学ぶ過程に由来する誤用を扱っています。過剰般化を母語干渉だけに限定する説明は合いません。",
        "これは文体・待遇上の切り替えの説明であり、Richardsが示す過剰般化の定義ではありません。",
        "原稿3.1節は、既に学んだ目標言語の構造を基に、その構造を許容範囲を越えて適用して新しい非目標形を作る現象として説明しています。",
        "これは複数言語の使用を切り替える現象の説明であり、Richardsが示す過剰般化の定義ではありません。",
    ],
    "用語だけを問う旧稿をRichards（1970）の原発表稿3.1節の定義へ結び付けた。母語干渉一般、待遇表現、コード・スイッチングとの区別を維持し、日本語の個別例の原因を原著が証明したとは扱わない。",
    ["S29"],
    [
        "母語差だけに限定し目標言語内の学習過程を除外",
        "過剰般化ではなく待遇表現の切り替え",
        "原稿3.1節の定義に一致",
        "過剰般化ではなく言語の切り替え",
    ],
)


(b.OUT / "changes_batch55.json").write_text(
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
source_marker = "S118追加照合：原誌169頁（PDF11頁）の末尾"
if source_marker not in source_text:
    with source_path.open("a") as source_file:
        source_file.write(
            "\nS29追加照合：§3.1の定義をQ_4_073の全4肢・全4解説へ適用。母語差だけの説明、待遇表現、コード・スイッチングを同義語として扱わず、原著の英語例を日本語の個別例の原因証明へ一般化しない。\n\n"
            "S118追加照合：原誌169頁（PDF11頁）の末尾で、多くの誤用が母語体系に関係するが、すべてではないこと、既に母語をもつことが促進要因になるという著者の限定を確認し、Q_5_011へ適用。正・負の転移研究全般、漢字圏学習者の個別例、語用論的転移、化石化をこの論文で一括承認しない。\n"
        )
print("2 questions /", len(extra), "edits")
