#!/usr/bin/env python3
"""One-time evidence-bound revision of two Brown/Levinson face items."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b


prior = json.loads((b.OUT / "changes.json").read_text())
assert len(prior) == 1196
_, questions, answers = qa.audit(str(b.DST))
decisions = json.loads((b.OUT / "decisions.json").read_text())
extra = []


def rewrite(qid, key, stem, options, explanations, reason, sources, verdicts,
            stem_review, explanation_review):
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
                    "before_version": "第57バッチ反映後の累積作業稿",
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
        multiple_correct_risk="なし：原著の定義・分類に一致するのは独立正答のみ",
        no_correct_risk="なし：独立正答" + str(key),
    )


rewrite(
    "Q_5_079",
    3,
    "BrownとLevinsonがフェイスの二側面を基本的欲求として定義した説明として、最も適当なものを選べ。",
    [
        "ポジティブ・フェイスとは、自分の行為を他者に妨げられたくないという欲求である。",
        "ネガティブ・フェイスとは、自分の欲求が少なくとも一部の他者にとって望ましいものであってほしいという欲求である。",
        "ネガティブ・フェイスは自分の行為を他者に妨げられたくないという欲求、ポジティブ・フェイスは自分の欲求が少なくとも一部の他者にとって望ましいものであってほしいという欲求である。",
        "フェイスは聞き手だけがもつ公的自己像であり、話し手自身のフェイスが発話行為で脅かされることはない。",
    ],
    [
        "原著が『自分の行為を他者に妨げられたくない欲求』と定義するのは、ネガティブ・フェイスです。名称が逆です。",
        "原著が『自分の欲求が少なくとも一部の他者にとって望ましいものであってほしい欲求』と定義するのは、ポジティブ・フェイスです。名称が逆です。",
        "原著はネガティブ・フェイスを行為が他者に妨げられないことへの欲求、ポジティブ・フェイスを自分の欲求が少なくとも一部の他者にとって望ましいことへの欲求と定義しています。",
        "原著は聞き手のフェイスを脅かす行為だけでなく、謝罪など、話し手自身のフェイスを脅かす行為も分類しています。",
    ],
    "旧稿の正答はポライトネスを言語的・非言語的ストラテジー全般と広く要約し、4肢も原著定義・ストラテジー例・文化的含意を混在させていた。原著311〜315頁のフェイス定義と話し手／聞き手の区別だけを問う4肢へ全面改稿した。",
    ["S122"],
    [
        "ネガティブ・フェイスの定義をポジティブへ誤配",
        "ポジティブ・フェイスの定義をネガティブへ誤配",
        "原著の二定義に一致",
        "原著が明記する話し手自身へのFTAを否定",
    ],
    "Brown & Levinsonの原著章全文14頁を取得し、311〜315頁のフェイス定義、聞き手へのFTA、話し手へのFTAを画像本文とOCRで照合して4肢を独立判定。",
    "4解説を原著の二定義と話し手／聞き手の分類へ直接対応させ、旧稿の広い効果説明と選択肢番号参照を撤去。",
)

rewrite(
    "Q_5_100",
    3,
    "BrownとLevinsonが挙げるフェイス侵害行為（FTA）の分類として、最も適当なものを選べ。",
    [
        "依頼は、聞き手への否定的評価を示すため、主として聞き手のポジティブ・フェイスを脅かす行為に分類される。",
        "謝罪は、聞き手の将来の行為に圧力をかけるため、主として聞き手のネガティブ・フェイスを脅かす行為に分類される。",
        "依頼は聞き手の将来の行為に圧力をかけるため主として聞き手のネガティブ・フェイスを脅かし、謝罪は過去のFTAを悔いることを示すため話し手自身のポジティブ・フェイスを直接傷つける。",
        "依頼も謝罪も、聞き手のポジティブ・フェイスだけを脅かす行為であり、話し手自身のフェイスには関係しない。",
    ],
    [
        "原著は依頼を、聞き手の将来の行為に圧力をかけ、聞き手のネガティブ・フェイスを主に脅かす行為として挙げています。否定的評価を示す行為との説明は一致しません。",
        "原著は謝罪を、過去のFTAを悔いることを示して話し手自身のポジティブ・フェイスを直接傷つける行為として挙げています。聞き手の将来行為に圧力をかける依頼とは分類が異なります。",
        "原著の分類では、依頼は聞き手のネガティブ・フェイスへのFTA、謝罪は話し手自身のポジティブ・フェイスへのFTAです。両者の対象とフェイスの側面を区別しています。",
        "原著は聞き手のポジティブ・フェイスだけでなく、聞き手のネガティブ・フェイスと話し手自身のフェイスを脅かす行為も明示的に分類しています。",
    ],
    "旧稿は『依頼や謝罪』を一括して相手のネガティブ・フェイスへの配慮とし、謝罪が話し手自身のポジティブ・フェイスを直接傷つけるという原著分類と整合しなかった。依頼と謝罪の対象・側面を分離して全面改稿した。",
    ["S122"],
    [
        "依頼の対象とフェイス側面を誤分類",
        "謝罪の対象とフェイス側面を誤分類",
        "原著の依頼・謝罪分類に一致",
        "原著の複数のFTA分類を一種類へ縮減",
    ],
    "Brown & Levinson原著章311〜315頁を取得し、依頼・謝罪を含むFTA一覧と話し手／聞き手、ポジティブ／ネガティブの二軸を独立照合。",
    "依頼と謝罪を一括しない4解説へ改稿し、各誤答の誤りを原著の対象とフェイス側面の双方から明示。",
)


(b.OUT / "changes_batch58.json").write_text(
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
if "| S122 |" not in source_text:
    with source_path.open("a") as source_file:
        source_file.write(
            "\n| S122 | Penelope Brown & Stephen C. Levinson（1987／2009再録）[Politeness: Some universals in language usage, Chapter 1 reprint（Max Planck Institute公開PDF）](https://www.mpi.nl/publications/item64421/politeness-some-universals-language-usage-chapter-1-reprint)、[Cambridge University Press書誌](https://www.cambridge.org/highereducation/books/politeness/89113EE2FB4A1D254D4A8D2011E542E4) | 公開PDF全14頁を取得。311〜315頁のnegative/positive faceの定義、聞き手のフェイスを脅かす行為、話し手自身のフェイスを脅かす行為を画像本文で照合。依頼は聞き手のnegative face、謝罪は話し手自身のpositive faceへのFTAとして記載。 | 2026-10-13取得。PDFは画像のみのため英語OCRを作成し、該当ページ画像と対照。原著理論の定義・分類を問うにとどめ、文化普遍性の妥当性や教育効果は承認しない。 | Q_5_079、Q_5_100 |\n"
        )
print("2 questions /", len(extra), "edits")
