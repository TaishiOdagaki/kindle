#!/usr/bin/env python3
"""One-time evidence-bound revision of two high-risk pragmatics/keigo items."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b


prior = json.loads((b.OUT / "changes.json").read_text())
assert len(prior) == 1235
_, questions, answers = qa.audit(str(b.DST))
decisions = json.loads((b.OUT / "decisions.json").read_text())
extra = []


def rewrite(qid, key, stem, options, explanations, reason, sources, verdicts,
            stem_review, explanation_review, multiple_correct_risk,
            no_correct_risk):
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
                    "before_version": "第59バッチ反映後の累積作業稿",
                }
            )
    decisions[qid].update(
        status="確認済み",
        fixes_applied=True,
        independent_answer=key,
        sources=sources,
        option_verdicts=verdicts,
        reason=reason,
        stem_review=stem_review,
        explanation_review=explanation_review,
        unresolved="",
        multiple_correct_risk=multiple_correct_risk,
        no_correct_risk=no_correct_risk,
    )


rewrite(
    "Q_O_056",
    4,
    "BrownとLevinsonのポライトネス理論に照らし、依頼が主として脅かす聞き手の欲求として最も適当なものを選べ。",
    [
        "場面に応じて言語変種を使い分けたいという欲求",
        "自分の欲求が少なくとも一部の他者にとって望ましいものであってほしいという欲求",
        "コード・スイッチング",
        "自分の行為を他者に妨げられたくないという欲求",
    ],
    [
        "言語変種の使い分けはダイグロシア等で論じられる現象であり、BrownとLevinsonが定義するフェイスの欲求ではありません。",
        "これは、自分の欲求が少なくとも一部の他者にとって望ましいものであってほしいというポジティブ・フェイスの定義です。依頼が聞き手に課す行為上の圧力を直接表すものではありません。",
        "会話中の言語・変種の切替えはコード・スイッチングであり、フェイスの欲求の定義ではありません。",
        "ネガティブ・フェイスは、自分の行為を他者に妨げられたくないという欲求です。依頼は聞き手に将来の行為を求めるため、聞き手のネガティブ・フェイスを脅かす行為に分類されます。",
    ],
    "旧稿の『行動の自由を制限したくない』は、他者を制限しないという依頼者側の志向にも読め、聞き手自身が妨げられたくないというnegative faceの定義を正確に表していなかった。原著の定義と依頼の分類へ設問・4肢・解説を直接対応させた。",
    ["S122"],
    [
        "誤答：社会言語学的な変種の使い分けでありフェイスの定義ではない",
        "誤答：ポジティブ・フェイスの定義",
        "誤答：コード・スイッチングでありフェイスの定義ではない",
        "正答：原著のネガティブ・フェイス定義と依頼のFTA分類に一致",
    ],
    "Brown & Levinson原著311〜315頁でpositive/negative faceの定義と依頼の分類を照合し、聞き手自身の行為が妨げられないことを問う文へ改稿。",
    "4解説をフェイス定義または非該当概念に対応させ、依頼者側と聞き手側を混同する表現を除去。",
    "なし：選択肢4だけが原著のnegative faceの定義に一致",
    "なし：独立正答4",
)


rewrite(
    "Q_4_091",
    4,
    "社員Aが先輩Bに資料の確認を依頼する場面について、敬語の仕組みの説明として最も適当なものを選べ。",
    [
        "『拝見する』はBの動作を高める尊敬語なので、『Bさんに拝見していただく』が適切である。",
        "『ご確認して差し上げる』はBに確認を依頼する謙譲語なので、適切である。",
        "Bの動作には謙譲語を用いるため、『Bさんがご確認いただく』が適切である。",
        "『Bさんにご確認いただく』は、Bの確認という行為を、Aが恩恵を受ける側から表す謙譲語Ⅰとして用いることができる。",
    ],
    [
        "『拝見する』は『見る』の謙譲語Ⅰで、見る人からその動作の向かう先を立てる語です。B自身の確認動作を高める尊敬語ではないため、この説明は不適切です。",
        "『ご確認して差し上げる』は、文の主語側が確認をして相手に恩恵を与えることを表します。Bに確認してもらう依頼の説明にはなりません。",
        "『いただく』は『もらう・受ける』側を主語とするため、『Bさんがご確認いただく』では、Bが別の人物から確認を受ける意味になります。AがBに確認してもらう関係を表していません。",
        "『お（ご）……いただく』は謙譲語Ⅰの一般形です。『AがBさんにご確認いただく』は、Bが確認し、Aがその恩恵を受ける関係をA側から表し、Bを立てることができます。",
    ],
    "旧稿は依頼の緊急度と回答期限が選択肢間で一致せず、『〜てください』や『ご＋外来語』を文脈を問わず誤用とする過剰な説明を含んでいた。文化審議会『敬語の指針』の謙譲語Ⅰと『いただく』の主語・恩恵関係を客観的に問う問題へ全面改稿した。",
    ["S04"],
    [
        "誤答：拝見するは見る側の謙譲語Ⅰで、Bの動作を高める尊敬語ではない",
        "誤答：確認する主体と恩恵の向きが依頼場面と逆",
        "誤答：いただくの主語・助詞関係が依頼場面と一致しない",
        "正答：お（ご）〜いただくの一般形と恩恵関係に一致",
    ],
    "文化審議会『敬語の指針』17頁・26頁・30〜31頁・40頁で、いただくの謙譲語Ⅰとしての働き、恩恵性、一般形、主語と助詞の関係を照合。主観的なビジネスマナー比較から敬語体系の判定へ改稿。",
    "4解説を動作主体、向かう先、恩恵を受ける側、いただくの主語関係に分解し、旧稿の一律禁止表現を撤去。",
    "なし：選択肢4だけがBの行為とAの受益関係を正しく説明",
    "なし：独立正答4",
)


(b.OUT / "changes_batch60.json").write_text(
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
source_text = source_text.replace(
    "Q_1_031、Q_2_019、Q_2_021、Q_2_023、Q_2_025 |",
    "Q_1_031、Q_2_019、Q_2_021、Q_2_023、Q_2_025、Q_4_091 |",
)
source_text = source_text.replace(
    "Q_5_079、Q_5_100 |",
    "Q_5_079、Q_5_100、Q_O_056 |",
)
source_path.write_text(source_text)

evidence = b.OUT / "evidence" / "batch60_source_review.md"
evidence.write_text(
    "# 第60バッチ原資料照合記録\n\n"
    "対象：Q_O_056、Q_4_091\n\n"
    "## Q_O_056\n\n"
    "Brown & Levinson（1987／2009再録）311〜315頁で、negative faceを自分の行為を他者に妨げられたくないという欲求、positive faceを自分の欲求が少なくとも一部の他者に望ましいものと評価されたいという欲求として照合した。依頼は、聞き手に将来の行為を求めて圧力をかけるため、聞き手のnegative faceを脅かす行為に分類される。旧稿の『行動の自由を制限したくない』は他者を制限しないという依頼者側の志向にも読めるため、聞き手自身が妨げられたくないという定義へ修正した。\n\n"
    "## Q_4_091\n\n"
    "文化審議会『敬語の指針』17頁で『いただく』を謙譲語Ⅰかつ恩恵を受ける意味を併せ持つ語として確認し、26頁で『お（ご）……いただく』を謙譲語Ⅰの一般形として確認した。30〜31頁では『いただく』が『もらう・受ける』側を主語とし、行為者には助詞『に』を付ける関係が説明され、40頁では『御利用いただく』が相手の行為を自分側の立場から表す用法として認められている。旧稿は緊急度と期限の条件が競合し、特定表現を一律に不適切とする説明を含んでいたため、動作主体・向かう先・受益関係を客観的に問う問題へ置換した。\n\n"
    "照合範囲は原著理論上のフェイス定義と公的指針の敬語体系であり、個別職場の慣行や依頼表現の丁寧さの序列までは承認していない。\n"
)
print("2 questions /", len(extra), "edits")
