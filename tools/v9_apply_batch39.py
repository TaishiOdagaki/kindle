#!/usr/bin/env python3
"""Repair and verify compound-verb and morphophonology questions."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 699
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
        'before_version': '第38修正バッチ作業稿',
    })


def rewrite(question_id, stem, options, explanations, reason, sources):
    record(question_id, 'stem', None, stem, reason, sources)
    for i, value in enumerate(options):
        record(question_id, 'options', i, value, reason, sources)
    for i, value in enumerate(explanations):
        record(question_id, 'explanations', i, value, reason, sources)


q43_reason = (
    '旧稿は「どのような動詞とも結合」「完全に二文へ還元」「熟句化」など、出典だけでは'
    '判定できない強い一般化を含んでいた。国立国語研究所研究者の論文が直接定義する'
    '「動詞（連用形）＋動詞」型と、同論文が明示する語彙的／統語的複合動詞の例だけで'
    '単一正答を判定できるよう全面改稿した。'
)
rewrite(
    'Q_5_043',
    '国立国語研究所の研究者による論文が扱う「動詞＋動詞」型の複合動詞について、最も適切な記述はどれか。',
    [
        '前項の動詞は終止形（辞書形）のまま後項動詞に続き、連用形になることはない。',
        '「生み出す」は、名詞「生み」と動詞「出す」からなるものだけを指し、「動詞＋動詞」型には含まれない。',
        '「食べ始める」は語彙的複合動詞の例であり、構成動詞から全体の意味をたどれない。',
        '「生み出す」のような複合動詞は、「動詞（連用形）＋動詞」という構造をもつ。',
    ],
    [
        '論文が対象とする型では、前項は終止形ではなく連用形です。',
        '論文は「生み出す」を「動詞（連用形）＋動詞」型の例として明示しています。ここでの「生み」は動詞「生む」の連用形です。',
        '論文は「食べ始める」を統語的複合動詞の例とし、「食べるのを始める」という補文的関係をもつ意味的に透明な合成だと説明しています。',
        '論文は、扱う複合動詞を「生み出す」のような「動詞（連用形）＋動詞」型と明記しています。',
    ],
    q43_reason,
    ['S89'],
)

q44_reason = (
    '旧稿は外来語での生産性や歴史的特徴を無根拠に一般化し、「かざぐるま」に含まれる'
    '後項の連濁を解説しなかった。日本語教師養成機関の解説本文が明示する、転音＝母音交替、'
    '連濁＝後項語頭の濁音化、ならびに両方が共起する「雨靴」の分析だけで判定する問題へ改稿した。'
)
rewrite(
    'Q_5_044',
    '複合語に見られる「転音」と「連濁」の説明として、最も適切なものはどれか。',
    [
        '連濁とは、複合語の前項末尾の母音が別の母音へ変わる現象だけをいう。',
        '転音とは、複合語の後項語頭の清音が濁音に変わる現象だけをいう。',
        '「風（かぜ）＋車（くるま）→風車（かざぐるま）」では転音だけが起こり、連濁は起こっていない。',
        '「雨（あめ）＋靴（くつ）→雨靴（あまぐつ）」では、前項の母音交替である転音と、後項語頭の濁音化である連濁がともに起こる。',
    ],
    [
        '前項の母音が変わる現象は転音（母音交替）です。連濁は、複合語の後項語頭が濁音化する現象です。',
        '後項語頭が清音から濁音へ変わる現象は連濁です。転音は母音が別の母音へ変わる現象です。',
        '「かぜ→かざ」には転音（/e/→/a/）があり、「くるま→ぐるま」には後項語頭の連濁があります。したがって両方が起こっています。',
        '「あめ→あま」は転音、「くつ→ぐつ」は連濁です。一つの複合語の中で二つの音変化が共起しています。',
    ],
    q44_reason,
    ['S90'],
)

updates = {
    'Q_5_043': (4, ['S89'], [
        '前項を終止形とするため誤り',
        '論文が動詞連用形＋動詞の例として明示しており誤り',
        '統語的複合動詞・意味的に透明とする本文に反しており誤り',
        '論文の対象定義と例に一致して正しい']),
    'Q_5_044': (4, ['S90'], [
        '転音と連濁の定義を取り違えており誤り',
        '連濁と転音の定義を取り違えており誤り',
        '転音に加えて連濁も生じるため誤り',
        '転音と連濁の共起を正しく分析している']),
}
reasons = {'Q_5_043': q43_reason, 'Q_5_044': q44_reason}
for qid, (answer, sources, verdicts) in updates.items():
    D[qid].update(
        status='確認済み', fixes_applied=True, independent_answer=answer,
        sources=sources, option_verdicts=verdicts, reason=reasons[qid],
        stem_review='根拠本文が直接定義・例示する範囲に限定して再構成。',
        explanation_review='改訂後の4選択肢と4解説を根拠本文へ個別照合。',
        unresolved='', multiple_correct_risk='なし：誤答肢は根拠本文の定義または例示と明確に不一致',
        no_correct_risk=f'なし：独立正答{answer}')

(b.OUT / 'changes_batch39.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

sources = b.OUT / 'sources.md'
sources.write_text(sources.read_text() + '''
| S89 | 山口昌也（国立国語研究所）[「複合動詞と構成要素動詞の格要素の対応関係分析」](https://www.anlp.jp/proceedings/annual_meeting/2012/pdf_dir/P3-2.pdf)『言語処理学会第18回年次大会発表論文集』 | PDF第1頁本文で、対象を「生み出す」のような「動詞（連用形）＋動詞」型と明記。語彙的複合動詞と統語的複合動詞を区別し、後者の例「食べ始める」を「食べるのを始める」という補文的関係・意味的に透明な合成と説明。 | 2026-10-13本文取得。論文の対象範囲と例示を超える「必ず」「すべて」の一般化は採用しない。 | Q_5_043 |
| S90 | TCJ日本語教師養成講座 大野綾香（2024年8月7日）[「日本語の変音について」](https://xn--euts3n8lg6bk91h.jp.net/tcj-column/%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%AE%E5%A4%89%E9%9F%B3%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/) | 本文で連濁を複合語の後項語頭の濁音化、転音を母音交替と定義。「雨靴」の「あめ→あま」を転音、「くつ→ぐつ」を連濁と説明し、「風車」の /e/→/a/ も例示。 | 2026-10-13本文取得。生産性・歴史的分布・外来語での頻度はこの資料から承認せず撤去。 | Q_5_044 |
''')
print('Recorded', len(extra), 'repairs; verified 2 questions')
