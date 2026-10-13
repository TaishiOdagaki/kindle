#!/usr/bin/env python3
"""One-time evidence-bound revision of typology and CEFR assessment items."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b


prior = json.loads((b.OUT / "changes.json").read_text())
assert len(prior) == 1178
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
                    "before_version": "第56バッチ反映後の累積作業稿",
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
        multiple_correct_risk="なし：根拠本文に一致するのは独立正答のみ",
        no_correct_risk="なし：独立正答" + str(key),
    )


rewrite(
    "Q_5_009",
    1,
    "Greenberg（1963）の語順類型論で述べられた一般化として、最も適当なものを選べ。",
    [
        "基本語順がSOVの言語は、偶然から期待されるより圧倒的に高い頻度で後置詞型である。",
        "基本語順がSOVの言語は、例外なく前置詞型である。",
        "基本語順がVSOの言語は、例外なく後置詞型である。",
        "基本語順がSVOであれば、形容詞は必ず名詞の後ろに置かれる。",
    ],
    [
        "原論文のUniversal 4は、通常の語順がSOVの言語は、偶然から期待されるより圧倒的に高い頻度で後置詞型であると述べています。前置詞型の例外も本文が明記する傾向命題です。",
        "原論文はSOVと後置詞型の強い相関を示しますが、前置詞型の例外もあると明記しています。前置詞型であるという方向も、例外なしという強さも誤りです。",
        "原論文のUniversal 3は、基本語順がVSOの言語は前置詞型であると述べています。後置詞型ではありません。",
        "原論文は英語を、SVO・前置詞型でありながら形容詞が名詞に先行する例として説明しています。SVOだけから形容詞位置を必然化できません。",
    ],
    "旧稿はGreenbergの傾向を『極めて高い』と説明しつつ、中国語・日本語・韓国語の個別特徴を無出典で組み合わせていた。原論文のUniversal 3・4と英語の反例説明へ直接対応する4肢に改稿し、傾向と絶対則を区別した。",
    ["S120"],
    [
        "Universal 4に一致",
        "方向と例外条件の双方が原文に反する",
        "Universal 3の前置詞型を逆転",
        "原文中の英語の説明が反例",
    ],
    "Greenberg（1963）原論文全21頁を取得し、基礎語順類型の定義、Universal 3・4及び英語の説明に限定して設問と4肢を独立判定。",
    "原論文76〜79頁相当の画像本文をOCR後にページ画像と照合。個別言語の無出典主張を撤去し、4解説を本文の一般化と反例へ対応させた。",
)

rewrite(
    "Q_5_095",
    3,
    "欧州評議会が公開するCEFR共通参照レベルのTable 1とTable 2の説明として、最も適当なものを選べ。",
    [
        "Table 1は、聞く・読む・やり取り・発表・書くという34の自己評価尺度を並べた表である。",
        "Table 2は、非専門家への伝達と教師・カリキュラム作成者の方向づけのため、各レベルを一つの記述に要約した全体尺度である。",
        "Table 1は共通参照レベルを全体的に要約した尺度で、Table 2は聞く・読む・話す・書く活動に分けた自己評価表である。",
        "Table 1とTable 2はいずれも採点者だけが使う試験用ルーブリックで、学習者の自己評価には用いない。",
    ],
    [
        "34の尺度を用いて聞く・読む・話す・書く活動を示すのは、欧州評議会が自己評価表と説明するTable 2です。Table 1ではありません。",
        "各レベルを全体的に要約し、非専門家への伝達や教師・カリキュラム作成者の方向づけに使えると説明されるのはTable 1です。Table 2ではありません。",
        "欧州評議会の公式説明では、Table 1は共通参照レベルのholisticな全体要約、Table 2は聞く・読む・話す・書く活動を34尺度で示す自己評価表です。",
        "Table 2は公式にself-assessment gridとされ、学習者が自己評価に用いる形式です。両表を採点者専用とする説明は誤りです。",
    ],
    "旧稿は分析的評価と印象的評価の一般論に、長所・課題への効果や評価者間信頼性、訓練の不可欠性まで無出典で含めていた。欧州評議会が全文公開するCEFR Table 1・2の用途と構成を問う設問へ改稿した。",
    ["S121"],
    [
        "Table 2の内容をTable 1へ誤配",
        "Table 1の内容をTable 2へ誤配",
        "欧州評議会の公式説明に一致",
        "自己評価表という公式用途を否定",
    ],
    "欧州評議会のCEFRレベル説明、Table 1公式ページ、Table 2公式ページの本文を取得し、表の名称・用途・活動区分を限定して4肢を判定。",
    "4解説を公式ページの記述に個別対応させ、旧稿の効果・信頼性・訓練に関する未照合主張をすべて撤去。",
)


(b.OUT / "changes_batch57.json").write_text(
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
if "| S120 |" not in source_text:
    with source_path.open("a") as source_file:
        source_file.write(
            "\n| S120 | Joseph H. Greenberg（1963）[Some Universals of Grammar with Particular Reference to the Order of Meaningful Elements](https://babel.ucsc.edu/~hank/114/greenberg.pdf)、[Stanford University Press版書誌](https://www.degruyterbrill.com/document/doi/10.1515/9781503623217-005/html) | 原論文全21頁を取得。76〜79頁相当の基礎語順類型、英語の混合的特徴、Universal 3・4を画像本文で照合。 | 2026-10-13取得。PDFはテキスト層がないため英語OCRを作成し、該当ページ画像と対照。30言語標本の一般化を現代の例外なしの法則とは扱わない。 | Q_5_009 |\n"
            "| S121 | Council of Europe [CEFR level descriptions](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions)、[Table 1: Global scale](https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale)、[Table 2: Self-assessment grid](https://www.coe.int/en/web/common-european-framework-reference-languages/table-2-cefr-3.3-common-reference-levels-self-assessment-grid) | Table 1をholisticな全体要約、Table 2を34尺度の自己評価表として示す公式本文を取得。聞く・読む・話す・書く活動区分と用途を確認。 | 2026-10-13本文取得。各表の用途と構成に限定し、採点の信頼性や指導効果へ一般化しない。 | Q_5_095 |\n"
        )
print("2 questions /", len(extra), "edits")
