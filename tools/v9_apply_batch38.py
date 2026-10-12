#!/usr/bin/env python3
"""Repair and verify three kanji-teaching and morphology questions."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 672
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
        'before_version': '第37修正バッチ作業稿',
    })


def rewrite(question_id, stem, options, explanations, reason, sources):
    record(question_id, 'stem', None, stem, reason, sources)
    for i, value in enumerate(options):
        record(question_id, 'options', i, value, reason, sources)
    for i, value in enumerate(explanations):
        record(question_id, 'explanations', i, value, reason, sources)


q37_reason = (
    '旧稿は漢字の構成要素指導によって未知漢字の推測力が「飛躍的に向上」すると効果量を断定し、'
    'トメ・ハネ、全音訓、構成要素指導の優先順位も一律に論じていた。国際交流基金の実教材が'
    '明示する、活動で扱う語として漢字の意味と読みを少しずつ学ぶ方針だけを問う形へ改稿した。'
)
rewrite(
    'Q_5_037',
    '国際交流基金『いろどり 生活の日本語』が示す漢字学習の進め方として、最も適切なものはどれか。',
    [
        '漢字を一字ずつ孤立して取り上げるのではなく、各課の活動で扱う語として学びながら、意味と読み方を少しずつ覚える。',
        '最初の課で常用漢字2,136字をすべて提示し、各字の全音読み・全訓読みを同時に暗記してから語彙学習へ進む。',
        '漢字の意味と読み方は扱わず、字形を図形として正確に複写できることだけを学習目標にする。',
        '各課の活動やそこで扱う語とは切り離し、漢字だけを必ず一字ずつ同じ順序で学習する。',
    ],
    [
        '国際交流基金の公式FAQは、漢字を一つ一つ取り上げるのではなく、各課の活動で扱う単語として学習しながら、少しずつ意味と読み方を覚える構成だと説明しています。',
        '同FAQが示すのは、活動で扱う語の中で意味と読み方を少しずつ学ぶ方法です。常用漢字の全字・全音訓を最初に一括暗記する方法ではありません。',
        '公式FAQは漢字の意味と読み方を学習対象として明記しています。字形の複写だけを目標にするという説明は一致しません。',
        '公式FAQは、漢字を一字ずつ孤立して取り上げず、各課の活動で扱う単語として学ぶと説明しています。この選択肢は方針を逆にしています。',
    ],
    q37_reason,
    ['S88'],
)

q41_reason = (
    '旧稿は「お／ご」の語種別対応や接頭辞の品詞転換を例外なく一般化し、接尾辞の品詞転換も'
    '「多い」と数量的に述べていた。公開大学教科書が示す接辞・接頭辞・接尾辞・自由／拘束形態素の'
    '定義と、辞典で確認済みの日本語接尾辞「めく」の例だけで判定できる問題へ改稿した。'
)
rewrite(
    'Q_5_041',
    '接辞・接頭辞・接尾辞の定義に関する記述として、最も適切なものはどれか。',
    [
        '接頭辞は基体の後ろに付き、接尾辞は基体の前に付く接辞である。',
        '接辞は他の形態素に付かなくても、必ず単独の語として現れる自由形態素である。',
        '接尾辞は基体の後ろに付く接辞であり、日本語の「春めく」の「めく」はその例である。',
        '複合語は接辞一つだけで作られ、語根や基体を含まない語である。',
    ],
    [
        '定義が逆です。接頭辞は基体の前、接尾辞は基体の後ろに付きます。',
        '接辞は基体に付く必要があり、単独で語として現れる自由形態素ではなく拘束形態素です。',
        '接尾辞は基体の後ろに付く接辞です。「春めく」は「春」に接尾辞「めく」が付いてできた派生語として辞典でも示されています。',
        '接辞は基体に付く形態素です。接辞一つだけで複合語ができ、語根や基体を含まないという説明は定義に反します。',
    ],
    q41_reason,
    ['S53', 'S87'],
)

q45_reason = (
    '旧稿は和語を日常的・感情的語彙の中心、漢語を抽象的・専門的語彙の「大半」とし、'
    '文体頻度や造語力も数量根拠なしに一般化していた。国立国語研究所の説明が直接区別する'
    '和語・漢語・外来語と、それぞれの由来の対応だけを問う定義問題へ改稿した。'
)
rewrite(
    'Q_5_045',
    '国立国語研究所の説明に基づく、日本語の語種に関する記述として最も適切なものはどれか。',
    [
        '日本語の語彙は大きく和語・漢語・外来語に分けられ、それぞれ大和言葉・古代中国語・西洋語に対応する。',
        '和語とは、古代中国語から取り入れた語だけをまとめた語種である。',
        '漢語とは、主として英語などの西洋語から近代以降に取り入れた語だけをまとめた語種である。',
        '語種とは、名詞・動詞・形容詞のように、文中での文法的な働きだけによって語を分ける分類である。',
    ],
    [
        '国立国語研究所は、日本語の語彙を大きく和語・漢語・外来語の三群に分け、それぞれを大和言葉・古代中国語・西洋語に対応させています。',
        '古代中国語に対応する語群は漢語です。和語は大和言葉に対応する語群です。',
        '主として西洋語に対応する語群は外来語です。漢語は古代中国語に対応します。',
        '名詞・動詞・形容詞は品詞の分類です。ここでいう語種は、和語・漢語・外来語という語の由来に関わる区別です。',
    ],
    q45_reason,
    ['S51'],
)

updates = {
    'Q_5_037': (1, ['S88'], [
        '公式教材の段階的・語彙文脈内の漢字学習方針に一致して正しい',
        '全字・全音訓の一括暗記を求めており公式方針と不一致',
        '意味と読みを学習対象から除外しており公式方針と不一致',
        '活動・語彙から切り離す点で公式方針と逆']),
    'Q_5_041': (3, ['S53', 'S87'], [
        '接頭辞と接尾辞の位置を逆にしており誤り',
        '接辞を自由形態素としており誤り',
        '接尾辞の定義と「春めく」の分析に一致して正しい',
        '接辞・基体・複合語の関係を誤っており誤り']),
    'Q_5_045': (1, ['S51'], [
        '国立国語研究所の語種三分類と由来の対応に一致して正しい',
        '和語と漢語を取り違えており誤り',
        '漢語と外来語を取り違えており誤り',
        '語種と品詞を取り違えており誤り']),
}
reasons = {'Q_5_037': q37_reason, 'Q_5_041': q41_reason, 'Q_5_045': q45_reason}
for qid, (answer, sources, verdicts) in updates.items():
    D[qid].update(
        status='確認済み', fixes_applied=True, independent_answer=answer,
        sources=sources, option_verdicts=verdicts, reason=reasons[qid],
        stem_review='根拠資料が直接支える定義または教材方針だけに限定して再構成。',
        explanation_review='改訂後の4選択肢と4解説を根拠本文へ照合。',
        unresolved='', multiple_correct_risk='なし：正答以外は根拠本文の定義・方針と明確に不一致',
        no_correct_risk=f'なし：独立正答{answer}')

(b.OUT / 'changes_batch38.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

sources = b.OUT / 'sources.md'
sources.write_text(sources.read_text() + '''
| S88 | 国際交流基金『いろどり 生活の日本語』[よくある質問 Q15](https://www.irodori.jpf.go.jp/faq.html) | 公式FAQ本文で、漢字を一字ずつ取り上げるのではなく、各課の活動で扱う単語として学びながら、少しずつ意味と読み方を覚える構成を確認。 | 2026-10-13本文取得。構成要素指導の効果量、トメ・ハネの優先順位、全音訓の指導順はこの資料から承認せず撤去。 | Q_5_037 |
''')
print('Recorded', len(extra), 'repairs; verified 3 questions')
