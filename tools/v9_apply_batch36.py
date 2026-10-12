#!/usr/bin/env python3
"""Verify mora-nasal questions and repair three ambiguous phonetics questions."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 608
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
        'before_version': '第35修正バッチ作業稿',
    })


def rewrite(question_id, stem, options, explanations, reason, sources):
    record(question_id, 'stem', None, stem, reason, sources)
    for i, value in enumerate(options):
        record(question_id, 'options', i, value, reason, sources)
    for i, value in enumerate(explanations):
        record(question_id, 'explanations', i, value, reason, sources)


q24_reason = (
    '旧稿は音節構造の分析を正答条件に含め、解説で「切符」を[ kip ]と[ pu ]に分けていたが、'
    '資料本文だけではその音節境界を一義的に確定できない。東京外国語大学と国際交流基金が明示する'
    '拍の数え方に限定し、促音・撥音・長音も1拍、拗音は2字で1拍という規則を問う内容へ改稿した。'
)
rewrite(
    'Q_5_024',
    '日本語の拍（モーラ）の数え方に関する記述として、最も適切なものはどれか。',
    [
        '拗音「きゃ」は仮名2文字で書くため、「き」と「ゃ」の2モーラとして数える。',
        '促音「っ」、撥音「ん」、長音「ー」は独立した拍を持たず、モーラ数には含めない。',
        '「バレンタイン」は英語で3音節なので、日本語でも3モーラとして数える。',
        '「切符（きっぷ）」は「き・っ・ぷ」と分け、促音を含む3モーラとして数える。',
    ],
    [
        '東京外国語大学の教材では、拗音の小書き「ゃ・ゅ・ょ」は前の仮名と一緒になり、2文字で1拍と説明されています。「きゃ」は1モーラです。',
        '促音・撥音・長音はいずれも特殊拍で、それぞれ1拍分として数えます。モーラ数から除外するという説明は誤りです。',
        '国際交流基金の解説では、日本語の「バレンタイン」は「ン」をそれぞれ1拍として数える6拍語です。他言語の音節数をそのまま日本語のモーラ数にはできません。',
        '「切符」は「き・っ・ぷ」の3モーラです。促音「っ」も自立拍と同じく1拍の単位として認識されます。',
    ],
    q24_reason,
    ['S80', 'S81'],
)

q27_reason = (
    '旧正答は文末上昇に「確認・親愛」を一括して結び付けたが、東京外国語大学の教材は、'
    '文末上昇を疑問に、非上昇を相づち・納得・確認・提案などに区別している。'
    '不安定な機能列挙を撤去し、アクセントとイントネーションの水準差と意味機能を問う内容へ改稿した。'
)
rewrite(
    'Q_5_027',
    'アクセントとイントネーションの区別に関する記述として、最も適切なものはどれか。',
    [
        'アクセントは単語レベルの音の高さの変化、イントネーションは文レベルの音の高さの変化であり、イントネーションは文の意味や感情の表現に関わる。',
        'アクセントは文全体にだけ現れ、イントネーションは各単語に固定された辞書的な高低型である。',
        'イントネーションを変えても、疑問・納得などの発話意図や意味解釈には影響しない。',
        '疑問を表すときは単語のアクセント型を崩し、語全体を最初から最後まで一様に上昇させる。',
    ],
    [
        '東京外国語大学の教材は、アクセントを単語レベル、イントネーションを文レベルの高さの変化と区別し、イントネーションが意味や感情の表現に関わると説明しています。',
        '説明が逆です。単語レベルの高低型がアクセントで、文レベルの音調変化がイントネーションです。',
        '同じ「そうですか」でも文末の上昇の有無により、疑問、相づち、納得、落胆などの解釈が変わります。「影響しない」は誤りです。',
        '日本語の疑問文では、単語のアクセント型を保ちながら文末の最終拍を急上昇させます。語全体を一様に上昇させるという説明は誤りです。',
    ],
    q27_reason,
    ['S82'],
)

q28_reason = (
    '旧設問の音声表記[susi]と「英語のsue-sheに近い発音」は一致せず、誤用の対象音を特定できなかった。'
    '東京外国語大学の「し」の指導本文に合わせ、英語seaのような[si]又は唇を丸めすぎたshe型の発音を'
    '対象として明示し、唇の丸めと聞き分けを扱う単一正答問題へ改稿した。'
)
rewrite(
    'Q_5_028',
    '英語を母語とする学習者の「し」が、英語のseaのような[si]、または唇を強く丸めたsheに近い音になる場合の指導として、最も適切なものはどれか。',
    [
        '英語のsは常に有声化するため、鼻から息を出して「し」を鼻音化する練習を行う。',
        '日本語の「し」はseaのような[si]ではなくsheに近いが、唇を丸めすぎないよう注意させ、モデル音声を用いて調音と聞き分けを練習する。',
        '誤りは促音の欠落なので、「し」の直前に1拍分の閉鎖を置いて「っし」と発音させる。',
        '日本語らしくするため、声帯を強く振動させ、英語のsheよりも唇を大きく前へ突き出して発音させる。',
    ],
    [
        '「し」は鼻音ではなく摩擦音です。英語のsが常に有声化するという前提も、鼻音化による指導も誤りです。',
        '東京外国語大学の教材は、日本語の「し」は英語のseaのような音ではなくsheに近い一方、唇を丸めすぎないよう指導しています。対象となる違いに直接対応した説明です。',
        '設問の誤用は「し」の単音に関するもので、促音の欠落ではありません。閉鎖を加えると別の音韻構造になります。',
        '日本語の「し」は無声で、教材はsheに近くても唇を丸めすぎないよう注意しています。有声化と強い円唇化はいずれも逆方向です。',
    ],
    q28_reason,
    ['S83'],
)

D['Q_5_022'].update(
    status='確認済み', independent_answer=3, sources=['S78', 'S79'],
    option_verdicts=[
        'tの前ではnになり、ŋではないため誤り',
        'kの前ではŋになり、nではないため誤り',
        'pの前では両唇鼻音mになり正しい',
        '語末も鼻音であり口蓋帆を閉じて口からだけ呼気を出すという説明は誤り',
    ],
    reason='東京外国語大学の撥音教材で、後続子音による[m]・[n]・[ŋ]への同化と、語末でより奥に調音される鼻音を照合し、正答3を独立確定。',
    stem_review='反対・天気・散歩・語末の4環境を資料本文へ照合。',
    explanation_review='全4解説の調音位置、鼻腔通気、語末実現を照合。',
    unresolved='', multiple_correct_risk='なし：1・2・4は資料本文と不一致',
    no_correct_risk='なし：独立正答3')

D['Q_5_024'].update(
    status='確認済み', fixes_applied=True, independent_answer=4, sources=['S80', 'S81'],
    option_verdicts=[
        '拗音は2字で1モーラのため誤り',
        '促音・撥音・長音も各1モーラのため誤り',
        '日本語では6モーラであり英語の音節数を転用できないため誤り',
        '切符はき・っ・ぷの3モーラで正しい',
    ],
    reason=q24_reason,
    stem_review='音節境界の分析を撤去し、教材が明示するモーラ数に限定。',
    explanation_review='拗音、促音、撥音、長音とバレンタイン・切符の数え方を本文照合。',
    unresolved='', multiple_correct_risk='なし：4のみ資料本文の数え方に一致',
    no_correct_risk='なし：独立正答4')

D['Q_5_027'].update(
    status='確認済み', fixes_applied=True, independent_answer=1, sources=['S82'],
    option_verdicts=[
        'アクセントとイントネーションの水準及び意味機能に一致して正しい',
        '両者の水準を逆転しており誤り',
        'イントネーションで意味解釈が変わるため誤り',
        'アクセント型を保持して最終拍を上昇させるため誤り',
    ],
    reason=q27_reason,
    stem_review='「親愛」等の不安定な機能列挙を撤去し、単語／文レベルの区別へ限定。',
    explanation_review='疑問文の最終拍上昇、非上昇時の解釈、アクセント保持を本文照合。',
    unresolved='', multiple_correct_risk='なし：1のみ教材の定義と説明に一致',
    no_correct_risk='なし：独立正答1')

D['Q_5_028'].update(
    status='確認済み', fixes_applied=True, independent_answer=2, sources=['S83'],
    option_verdicts=[
        '鼻音化は対象音と無関係で誤り',
        'seaとの相違、sheへの近さ、円唇しすぎない指導に一致して正しい',
        '促音の問題ではないため誤り',
        '無声摩擦音を有声化し強く円唇化するため誤り',
    ],
    reason=q28_reason,
    stem_review='矛盾していたIPA表記と英語例を撤去し、対象となる誤用を明示。',
    explanation_review='4肢をTUFS「し」の指導本文と音声学的分類に照合。',
    unresolved='', multiple_correct_risk='なし：2のみ資料本文の指導に一致',
    no_correct_risk='なし：独立正答2')

(b.OUT / 'changes_batch36.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

sources = b.OUT / 'sources.md'
sources.write_text(sources.read_text() + '''
| S78 | 東京外国語大学言語モジュール [拍感覚（撥音－子音前）](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/02-03-01.php) | 後続するマ・パ・バ行前の[m]、タ・ダ・ナ行前の[n]、カ・ガ行前の[ŋ]と、撥音を1拍として扱う説明を確認。 | 2026-10-13本文取得。 | Q_5_022 |
| S79 | 東京外国語大学言語モジュール [拍感覚（撥音－母音前、半母音前、摩擦音前、語末）](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/02-04-01.php) | 母音・半母音前の鼻音化母音、語末・文末及びサ・ハ行前で[ŋ]より奥に調音される鼻音を確認。 | 2026-10-13本文取得。語末を単一IPAに固定しない。 | Q_5_022 |
| S80 | 東京外国語大学言語モジュール [拍感覚基礎](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/01-10-01.php) | 拍＝モーラ、拗音は2字で1拍、促音・撥音・長音・二重母音の第2要素も各1拍という説明を確認。 | 2026-10-13本文取得。等時性は「ほぼ均等」という指導上の説明に限定。 | Q_5_024 |
| S81 | 国際交流基金 戸田貴子 [日本語特殊拍の習得に関する研究](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/research/031.html) | 特殊拍も1拍、「バレンタイン」は6拍、拍と音節の相違、自然発話では機械的な1拍＝1ビートが実態に合わないことを確認。 | 2026-10-13本文取得。 | Q_5_024 |
| S82 | 東京外国語大学言語モジュール [イントネーション基礎](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/01-09-01.php) | アクセント＝単語レベル、イントネーション＝文レベル、文末上昇による疑問と非上昇時の相づち・納得・確認・提案等を確認。 | 2026-10-13本文取得。 | Q_5_027 |
| S83 | 東京外国語大学言語モジュール [単音「し」](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/03-04-01.php) | 日本語の「し」は英語seaの音ではなくsheに近いが、唇を丸めすぎないという指導を確認。 | 2026-10-13本文取得。 | Q_5_028 |
''')
print('Recorded', len(extra), 'repairs; verified 4 questions')
