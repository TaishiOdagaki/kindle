#!/usr/bin/env python3
"""Repair and verify two suffix-derivation questions."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 717
_, Q, A = qa.audit(str(b.DST))
D = json.loads((b.OUT / 'decisions.json').read_text())
extra = []


def record(question_id, field, index, after, reason, sources):
    if field == 'stem':
        before = Q[question_id]['stem']
    elif field == 'options':
        before = Q[question_id]['opts'][index]
    else:
        before = A['A_' + question_id[2:]]['txt'][index]
    extra.append({
        'id': question_id,
        'field': field,
        'index': index,
        'before': html.unescape(before),
        'after': after,
        'reason': reason,
        'sources': sources,
        'applied': True,
        'before_version': '第39修正バッチ作業稿',
    })


def rewrite(question_id, stem, options, explanations, reason, sources):
    record(question_id, 'stem', None, stem, reason, sources)
    for i, value in enumerate(options):
        record(question_id, 'options', i, value, reason, sources)
    for i, value in enumerate(explanations):
        record(question_id, 'explanations', i, value, reason, sources)


q48_reason = (
    '旧稿は、学習履歴を示さずに「味さ」を形容詞への「さ」の過剰一般化と断定し、'
    'さらに「味」を「和語（あるいは漢語的語彙）」と曖昧に説明していた。近年の研究要旨は'
    '接尾辞「さ」が一部の名詞等にも付き得ることを明記しており、当該一例だけから誤用原因を'
    '断定できない。研究本文が直接説明する形容詞語幹への接続と名詞化だけを問う問題へ改稿した。'
)
rewrite(
    'Q_5_048',
    '形容詞の語幹に接尾辞「さ」が付く語形成について、最も適切な記述はどれか。',
    [
        '「高い」の語幹「高」に「さ」が付き、「高さ」という派生名詞ができる。',
        '「走る」の連用形「走り」は、接尾辞「さ」が付いてできた派生名詞である。',
        '「春風」は、「春い」という形容詞の語幹に「さ」が付いてできた派生名詞である。',
        '「静かさ」の「さ」は、語基の前に付く接頭辞である。',
    ],
    [
        '形容詞の語幹に接尾辞「さ」が後続すると、程度・性質・状態などを表す派生名詞を作れます。「高い」の語幹は「高」で、「高さ」がその例です。',
        '「走り」は動詞「走る」の連用形を名詞として用いた形であり、この語形に接尾辞「さ」は現れていません。',
        '「春風」は名詞「春」と名詞「風」からなる複合語です。「春い」という形容詞や接尾辞「さ」による形成ではありません。',
        '「静かさ」の「さ」は語基「静か」の後ろに付く接尾辞です。語基の前に付く接頭辞ではありません。',
    ],
    q48_reason,
    ['S91', 'S92'],
)

q49_reason = (
    '旧稿は「～だす／～つづける」の意味・アスペクト・テンスを一問で扱い、各選択肢の強い一般化を'
    '直接支える資料が確保できなかった。推測で掲載せず、出典本文が接続制限・意味範疇・共起の'
    '差を明示する「さ／み」派生名詞の比較問題へ差し替えた。'
)
rewrite(
    'Q_5_049',
    '「さ」派生名詞と「み」派生名詞を比較した研究の記述として、最も適切なものはどれか。',
    [
        '「さ」派生名詞は「み」派生名詞より意味範疇が広く、共起する名詞や動詞にも多様性がある。',
        '接尾辞「み」は漢語・外来語の形容名詞語幹にもほぼ制限なく付き、「さ」より生産性が高い。',
        '味覚形容詞から作る「さ」派生名詞は、具体物を表す修飾語とは共起せず、抽象的な事柄だけに用いる。',
        '「さ」と「み」は接続制限も意味用法も同じで、同じ形容詞から作れば常に置き換えられる。',
    ],
    [
        '研究は、「さ」派生名詞の意味範疇が広く、共起する名詞・動詞が多様であるとまとめています。',
        '研究が紹介する先行研究では、「み」は和語語彙に限られ、漢語・外来語の形容名詞語幹には接続しないとされます。「さ」より生産性が高いという記述ではありません。',
        '研究では、味覚形容詞の「さ」派生名詞は具体的なものから抽象的な事柄まで幅広い修飾語と共起するとされます。',
        '研究は両者の接続制限・意味用法・共起表現の差を論じています。常に置換可能だとはしていません。',
    ],
    q49_reason,
    ['S91'],
)

updates = {
    'Q_5_048': (1, ['S91', 'S92'], [
        '形容詞語幹＋接尾辞「さ」の名詞化に一致して正しい',
        '動詞連用形であり「さ」がないため誤り',
        '名詞＋名詞の複合語であり説明が成立しないため誤り',
        '「さ」は後接する接尾辞であり誤り']),
    'Q_5_049': (1, ['S91'], [
        '研究の結論に一致して正しい',
        '研究が紹介する接続制限と逆であり誤り',
        '研究の用例分布と逆であり誤り',
        '研究が示す相違を否定しており誤り']),
}
reasons = {'Q_5_048': q48_reason, 'Q_5_049': q49_reason}
for qid, (answer, sources, verdicts) in updates.items():
    D[qid].update(
        status='確認済み', fixes_applied=True, independent_answer=answer,
        sources=sources, option_verdicts=verdicts, reason=reasons[qid],
        stem_review='根拠本文が直接説明する形態論・用例分布の範囲に限定して再構成。',
        explanation_review='改訂後の4選択肢と4解説を根拠本文へ個別照合。',
        unresolved='', multiple_correct_risk='なし：誤答肢は形態構造または根拠本文と明確に不一致',
        no_correct_risk=f'なし：独立正答{answer}')

(b.OUT / 'changes_batch40.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

sources = b.OUT / 'sources.md'
sources.write_text(sources.read_text() + '''
| S91 | 曾寶儀（2016）[「『～さ』派生名詞と『～み』派生名詞に関する一考察―共起表現をめぐって―」](https://www.cf.ocha.ac.jp/ccjs/j/menu/consortia/d002832_d/fil/jap2.pdf) 第11回国際日本学コンソーシアム日本語学・日本語教育学部会（お茶の水女子大学） | 本文1頁で形容詞語幹への接尾辞「さ」「み」と名詞化を説明。1～2頁で「さ」の高い生産性と名詞化機能、4～7頁で「さ」派生名詞の広い意味範疇・多様な共起、「み」との接続・用法差を示す。 | 2026-10-13 PDF本文取得。論文の調査範囲を超える全称命題は採用しない。 | Q_5_048, Q_5_049 |
| S92 | 劉宇佳（2022）[「現代日本語における名詞化接尾辞『さ』『み』について」学位論文要旨](https://koara.lib.keio.ac.jp/xoonips/modules/xoonips/download.php/AN00189695-20220300-0117.pdf?file_id=162975) 慶應義塾大学藝文学会『藝文研究』 | 要旨本文は「さ」がほとんどの形容詞・形容動詞だけでなく一部の名詞、副詞、動詞、助動詞にも付くとする先行研究を整理する。 | 2026-10-13 PDF本文取得。旧稿の「味さ」を単純な品詞規則違反と断定しない判断の補強に使用。 | Q_5_048 |
''')
print('Recorded', len(extra), 'repairs; verified 2 questions')
