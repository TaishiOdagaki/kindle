#!/usr/bin/env python3
"""Repair Q5-017 against Japan Foundation full-text explanations of wa and ga."""
import json, html
import v9_apply_batch1 as b
import quiz_audit as qa

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 588
_, Q, A = qa.audit(str(b.DST))
extra = []
key = 'Q_5_017'
reason = ('新情報／旧情報だけで「が」と「は」を一律対応させる旧説明と、'
          '「田中さんは」が他の全員の不来を必ず含意するという過剰断定を撤去。'
          '国際交流基金教材が示す主語・発見報告・選択の「が」と、主題・対比の「は」に限定した。')
stem = '日本語教育で「が」と「は」の働きを説明する記述として、最も適切なものはどれか。'
options = [
    '「は」は主格を表す場合にしか使えず、「には」「とは」のように他の助詞と組み合わせることはできない。',
    '「が」は常に新情報だけに付き、「は」は常に旧情報だけに付くので、文脈による使い分けを考える必要はない。',
    '「が」には主語を示したり疑問詞への答えを選んだりする働きがあり、「は」には主題を示したり他と対比したりする働きがある。',
    '「誰が発表しますか」への答えは必ず「山田さんは発表します」とし、「山田さんが発表します」は文法的に誤りである。',
]
explanations = [
    '国際交流基金の教材は、「は」が主題を示すほか、対比にも使われ、「には」「とは」「からは」のように他の助詞と一緒に使えると説明しています。「主格だけ」「組合せ不可」は誤りです。',
    '同教材は、共有された主題に「は」を用いる例や、発見・報告に「が」を用いる例を示しますが、働きを新情報／旧情報の二分だけに還元していません。「常に」と固定する説明は不適切です。',
    '同教材は、「が」の働きとして主語、発見・報告、主語の選択を挙げ、「は」の働きとして主題や対比を示しています。文脈に応じた複数の働きを区別する説明です。',
    '同教材は、「きょうは誰が発表するんですか」への答えとして「山田さんが発表します」を挙げています。「が」を文法的誤りとする説明は逆です。なお、別の文脈で「山田さんは発表します」が成り立つ可能性まで否定するものではありません。',
]
for field, values in [('stem', [stem]), ('options', options), ('explanations', explanations)]:
    for i, new in enumerate(values):
        old = Q[key]['stem'] if field == 'stem' else Q[key]['opts'][i] if field == 'options' else A['A_5_017']['txt'][i]
        extra.append(dict(id=key, field=field, index=None if field == 'stem' else i,
                          before=html.unescape(old), after=new, reason=reason,
                          sources=['S73'], applied=True, before_version='第33修正バッチ作業稿'))

(b.OUT / 'changes_batch34.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
D = json.loads((b.OUT / 'decisions.json').read_text())
D[key].update(
    status='確認済み', fixes_applied=True, independent_answer=3, sources=['S73'],
    option_verdicts=[
        'はと他助詞の組合せを否定して誤り',
        '新旧情報だけへ常に固定して誤り',
        '教材のが／はの機能整理に一致して正しい',
        '疑問詞への回答例と逆で誤り',
    ],
    reason=reason,
    stem_review='品詞名の細分類や新旧情報の絶対則ではなく、取得本文が明示する機能を問う形へ限定。',
    explanation_review='国際交流基金教材の該当本文で設問・4肢・4解説を照合。はの主題・対比・他助詞との共起、がの主語・発見報告・選択を確認。',
    unresolved='', multiple_correct_risk='なし：3のみ取得本文の機能整理に一致',
    no_correct_risk='なし：独立正答3')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')
p = b.OUT / 'sources.md'
p.write_text(p.read_text() + '\n| S73 | 国際交流基金『日本語教育通信』第54号（2006年1月）[「は」と「が」（1）](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/bn/dw_pdfs/nk54_01-18n.pdf)、みんなの教材サイト [は](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00038/ja/render.do) | PDF第12–13頁と教材本文全70行を2026-10-12取得。が＝主語・発見／報告・選択、は＝主題・一般的性質、現行教材の主題・対比・他助詞との共起・共有情報例を照合。新旧情報だけの絶対則や対比の必然的排他含意は採用しない。 | Q_5_017 |\n')
print('Recorded', len(extra), 'repairs')
