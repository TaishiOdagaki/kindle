#!/usr/bin/env python3
"""One-time evidence-bound revision of contrastive/error-analysis items."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b


prior = json.loads((b.OUT / "changes.json").read_text())
assert len(prior) == 1151
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
                    "before_version": "第55バッチ反映後の累積作業稿",
                }
            )
    decisions[qid].update(
        status="確認済み",
        fixes_applied=True,
        independent_answer=key,
        sources=sources,
        option_verdicts=verdicts,
        reason=reason,
        stem_review="取得した原発表稿本文に照らし、著者・年・概念の範囲を明示して4肢を独立判定。",
        explanation_review="4解説を原発表稿の該当箇所へ個別照合し、旧稿の過剰な一般化と無根拠な指導効果を撤去。",
        unresolved="",
        multiple_correct_risk="なし：取得した原文に一致するのは独立正答のみ",
        no_correct_risk="なし：独立正答" + str(key),
    )


rewrite(
    "Q_4_070",
    3,
    "Wardhaugh（1970）がいう対照分析仮説の強形の説明として、最も適当なものを選べ。",
    [
        "実際に観察された学習上の困難を出発点として、利用できる言語学的知識により事後的に説明する立場である。",
        "母語と目標言語の比較を行わず、学習者の発話に現れた誤用だけを任意に分類する立場である。",
        "母語と目標言語を体系的に比較し、学習前に困難となる型とならない型を予測できるとする立場である。",
        "二言語間の差は学習の難しさと無関係なので、教材作成では比較結果を一切使わないとする立場である。",
    ],
    [
        "これはWardhaughが区別する弱形の出発点に合います。弱形は、既に観察された困難を、利用できる言語学的知識で説明しようとします。",
        "Wardhaughの弱形も言語体系を参照します。発話例を任意に分類するだけという説明は、強形にも弱形にも合いません。",
        "原発表稿3頁はLadoの記述を強形の代表として引用し、母語と学習対象の言語・文化を体系的に比較して、困難となる型を予測・記述できるという要求を示しています。",
        "原発表稿は二言語間の差を無関係とはしていません。強形の予測可能性を批判しつつ、弱形には一定の利用可能性を認めています。",
    ],
    "旧稿は対照分析を一枚岩の予測手法として説明し、解説1で中間言語を分析手法ではないと断定していた。Wardhaugh（1970）の原発表稿に即して強形の予測要求を問い、弱形・誤用の任意分類・全面否定と区別した。",
    ["S115"],
    [
        "観察された困難から説明する弱形",
        "強形・弱形のいずれにも合わない",
        "強形の予測要求に一致",
        "原文が認める弱形の可能性まで否定",
    ],
)

rewrite(
    "Q_4_071",
    2,
    "Corder（1967）が述べる、第二言語学習者の言語体系と系統的な誤用の関係として、最も適当なものを選べ。",
    [
        "学習途中の発話は規則をもたず、正用も誤用も互いに無関係な偶発的現象である。",
        "学習者は発達の各時点で一定の体系を用いており、系統的な誤用はその時点の知識を再構成する証拠になる。",
        "正しい形を一度発話できれば、母語話者と同じ体系を完全に習得した証拠になる。",
        "疲労や記憶の不調による偶発的な言い間違いも、基礎的知識を示す系統的な誤用と区別しない。",
    ],
    [
        "原論文は、学習者が発達の各時点で一定の体系を用い、系統的な誤用がその体系の証拠になると述べています。すべてを偶発現象とはしません。",
        "原誌166〜167頁は、学習者が各時点で一定の体系を用いているとし、系統的な誤用から、その時点までの言語知識を再構成できると述べています。",
        "原論文は、正しい発話が聞いた文の反復である可能性を指摘し、一度の正用だけでは母語話者と同じ生成体系を習得した証拠にならないとしています。",
        "原論文は、疲労・記憶の不調などに由来する非系統的なmistakeと、現在の知識を反映する系統的なerrorを区別しています。",
    ],
    "旧稿の一般的な中間言語定義を、取得済みのCorder（1967）原論文が直接述べる限定命題へ改稿。発達の各時点の体系、系統的誤用の証拠性、一度の正用の限界、mistake/errorの区別を本文で照合した。Selinker（1972）の用語定義を未取得のまま代用しない。",
    ["S118"],
    [
        "体系性を否定し原文に反する",
        "原誌166〜167頁の説明に一致",
        "正用の証拠価値を過大評価",
        "原文が明示する非系統的・系統的の区別を否定",
    ],
)

rewrite(
    "Q_4_075",
    3,
    "Corder（1967）が区別するmistakeとerrorについて、最も適当なものを選べ。",
    [
        "mistakeは学習者の現在の言語知識を反映する系統的な誤用であり、規則として再構成できる。",
        "errorは疲労や記憶の不調だけから偶発的に生じ、本人が通常すぐ確実に自己訂正できる。",
        "mistakeは遂行上の偶発的で非系統的な誤り、errorは学習者の現在の知識を反映する系統的な誤用である。",
        "mistakeとerrorは原因・系統性・分析上の意義に違いがないため、両者を区別する必要はない。",
    ],
    [
        "これは原論文でerrorに割り当てられる説明です。系統的な誤用は学習者の現在の知識を再構成する資料になります。",
        "これは原論文でmistakeに割り当てられる説明です。疲労や記憶の不調などによる遂行上の誤りは非系統的とされます。",
        "原誌166〜167頁は、偶発的な遂行上の誤りをmistake、現在までの知識を示す系統的な誤用をerrorとして区別しています。",
        "原論文は両者の区別を重要とし、区別の判定自体には慎重な分析が必要だと述べています。",
    ],
    "旧稿は『まず行うべき作業』と問いながら選択肢3に分類・原因分析・指導利用を同時に含め、順序を判定できなかった。Corder（1967）が本文で明示するmistake/errorの区別へ差し替え、4肢と4解説を原文に直接対応させた。",
    ["S118"],
    [
        "errorの説明をmistakeへ逆転",
        "mistakeの説明をerrorへ逆転",
        "原誌166〜167頁の区別に一致",
        "原論文が重要とする区別を否定",
    ],
)


(b.OUT / "changes_batch56.json").write_text(
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
marker = "S115追加照合（第56バッチ）"
if marker not in source_text:
    with source_path.open("a") as source_file:
        source_file.write(
            "\nS115追加照合（第56バッチ）：原稿3〜4頁の強形と7〜8頁の弱形の区別をQ_4_070の全4肢・全4解説へ適用。Lado（1957）の原著を取得済みとはせず、Wardhaughが引用・評価する強形を問う。\n\n"
            "S118追加照合（第56バッチ）：原誌166〜167頁で、発達の各時点の一定の体系、系統的誤用の証拠性、mistake/errorの区別、一度の正用だけでは体系習得の証拠にならないという限定を再確認し、Q_4_071・Q_4_075へ適用。Selinker（1972）の用語定義や、特定の指導法の効果はこの論文から承認しない。\n"
        )
print("3 questions /", len(extra), "edits")
