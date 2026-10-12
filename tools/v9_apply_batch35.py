#!/usr/bin/env python3
"""Verify four phonetics questions and repair overgeneralized devoicing/gemination claims."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 597
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
        'before_version': '第34修正バッチ作業稿',
    })


# Q5-019: remove the imprecise comparison with an undifferentiated English [u]
# and state the Tokyo/common-language devoicing environment with its conditions.
q19_reason = (
    '旧稿は日本語の「う」と英語bootの母音を単一記号で対比し、語末と文末も混同していた。'
    '東京外国語大学の教材と国立国語研究所のコーパス解説に合わせ、狭母音/i, u/の'
    '無声子音間・文末での無声化傾向と、アクセント等による非必然性を問う内容へ改稿した。'
)
q19_stem = '東京方言を基盤とする共通語の母音無声化について、最も適切なものはどれか。'
q19_options = [
    '母音「あ」「え」「お」だけに起こり、「い」「う」には起こらない。',
    '有声子音に挟まれた「い」「う」に限って必ず起こる。',
    '促音や撥音の直前だけに起こり、文末では生じない。',
    '母音「い」「う」は、無声子音に挟まれたときや、無声子音の後で文末に来るときに無声化しやすい。',
]
q19_explanations = [
    '国立国語研究所は、日本語の狭母音/i/と/u/に無声化の傾向があると説明しています。「い」「う」には起こらないという記述は逆です。',
    '典型的な環境は無声子音に挟まれた場合です。また、条件を満たしてもアクセント核などの影響で無声化しにくい場合があるため、「有声子音」「必ず」は誤りです。',
    '東京外国語大学の教材は、無声子音に挟まれた場合だけでなく、無声子音の後で文末に来る「です」「ます」の「す」なども無声化しやすいと説明しています。',
    '「い」「う」は無声子音に挟まれたときや文末で無声化しやすい狭母音です。アクセント核、隣接子音、発話速度などによって生起率は変わるため、ここで述べるのは傾向です。',
]
record('Q_5_019', 'stem', None, q19_stem, q19_reason, ['S76', 'S77'])
for i, value in enumerate(q19_options):
    record('Q_5_019', 'options', i, value, q19_reason, ['S76', 'S77'])
for i, value in enumerate(q19_explanations):
    record('Q_5_019', 'explanations', i, value, q19_reason, ['S76', 'S77'])


# Q5-023: retain the correct key while explicitly preserving attested exceptions.
q23_reason = (
    '旧解説は促音の実現を無声子音前に事実上限定していた。国際交流基金の本文は、'
    '典型的な無声子音前のほか、外来語の共鳴音前や「すっごい」のような濁音前も示す。'
    '正答4の「主に」を生かし、例外を排除しない説明へ修正した。'
)
q23_exp3 = (
    '促音/Q/は後続子音の閉鎖または摩擦の持続として現れ、独立した母音のような明瞭な分節音ではありません。'
    '「声帯を絶え間なく振動させ続ける連続音」という説明は誤りです。なお、話し言葉や外来語には'
    '有声子音・共鳴音の前の例もあり、実現を一律に無声と固定しません。'
)
q23_exp4 = (
    '「っ」は後続子音を長くする働きを持ち、共鳴音や濁音の前は一般に制約を受けます。'
    '選択肢は「主に無声子音の直前」と限定しており、典型的な促音を説明しています。'
    'ただし「アッラー」「すっごい」などの例もあるため、無声子音の前にしか現れないとは説明しません。'
)
record('Q_5_023', 'explanations', 2, q23_exp3, q23_reason, ['S74'])
record('Q_5_023', 'explanations', 3, q23_exp4, q23_reason, ['S74'])


D['Q_5_018'].update(
    status='確認済み', independent_answer=4, sources=['S21', 'S74', 'S75'],
    option_verdicts=[
        '鼻音は軟口蓋を下げて鼻腔へ通気するため誤り',
        'sとɕは摩擦音であり閉鎖音ではないため誤り',
        'ɸは両唇音でfの唇歯音とは異なるため誤り',
        'JF本文がtɕとtsを破擦音と明示しており正しい',
    ],
    reason='IPA公式チャートと国際交流基金・東京外国語大学教材で調音位置・方法を全4肢照合。正答4を独立確定。',
    stem_review='設問と4肢をIPAの調音位置・方法及び日本語の実現に照合。',
    explanation_review='4解説の鼻音・摩擦音・両唇音・破擦音の説明を本文照合。',
    unresolved='', multiple_correct_risk='なし：1～3は調音位置又は方法が資料と不一致',
    no_correct_risk='なし：独立正答4')

D['Q_5_019'].update(
    status='確認済み', fixes_applied=True, independent_answer=4, sources=['S76', 'S77'],
    option_verdicts=[
        '狭母音i・uに生じるという資料と逆で誤り',
        '無声子音環境を有声子音とし必然化して誤り',
        '文末でも生じるため誤り',
        'TUFSとNINJALの記述に一致して正しい',
    ],
    reason=q19_reason,
    stem_review='東京方言を基盤とする共通語へ範囲を限定し、英語母音との不精密な対比を撤去。',
    explanation_review='無声子音間、文末、アクセント核、隣接子音、発話速度の条件を4肢・4解説へ照合。',
    unresolved='', multiple_correct_risk='なし：4のみ取得本文の環境と条件に一致',
    no_correct_risk='なし：独立正答4')

D['Q_5_020'].update(
    status='確認済み', independent_answer=3, sources=['S21', 'S75'],
    option_verdicts=[
        'çは硬口蓋摩擦音で軟口蓋ではないため誤り',
        'h・ç・ɸはいずれも無声音であり誤り',
        'はへほ・ひ・ふの主要な子音実現に一致して正しい',
        '日本語のうを前舌母音とするため誤り',
    ],
    reason='IPA公式チャートと東京外国語大学のハ行発音教材で全4肢・4解説を照合し、正答3を独立確定。',
    stem_review='IPA記号と日本語ハ行の主要な異音の組合せを照合。',
    explanation_review='çの硬口蓋、ɸの両唇、hの声門及び無声性を照合。',
    unresolved='', multiple_correct_risk='なし：1・2・4は調音位置又は有声性が不一致',
    no_correct_risk='なし：独立正答3')

D['Q_5_023'].update(
    status='確認済み', fixes_applied=True, independent_answer=4, sources=['S74'],
    option_verdicts=[
        '促音・長音も1モーラであり数値が誤り',
        '長音を独立子音とするため誤り',
        '促音を常時有声の独立分節音とするため誤り',
        '「主に」と限定した典型的実現として正しい',
    ],
    reason=q23_reason,
    stem_review='典型的な促音と、共鳴音・濁音前の例外を区別して4肢を再判定。',
    explanation_review='JF本文の「子音を伸ばす」説明及びアッラー・すっごいの例を反映。',
    unresolved='', multiple_correct_risk='なし：4のみ典型的実現を「主に」と限定して記述',
    no_correct_risk='なし：独立正答4')

(b.OUT / 'changes_batch35.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

sources = b.OUT / 'sources.md'
sources.write_text(sources.read_text() + '''
| S74 | 国際交流基金 川原繁人（2023年2月）[音声学者が答える日本語の「なぜなぜ？ どうして？」](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/research/202302.html) | 本文のタ行 [ta]-[tɕi]-[tsu]-[te]-[to]、破擦音の定義、tɕ・ts、促音が後続子音を伸ばす説明、共鳴音・濁音前の制約と「アッラー」「すっごい」の例を確認。 | 2026-10-13本文取得。典型傾向と例外を区別し、「常に」「のみ」へ一般化しない。 | Q_5_018、Q_5_023 |
| S75 | 東京外国語大学言語モジュール [単音「ハ行音子音 は、ひ、ふ」](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/03-06-01.php) | はの声門側の息、ひの口蓋付近の摩擦、ふの上下両唇と英語fとの相違を確認。 | 2026-10-13本文取得。IPA公式チャートS21と併用。 | Q_5_018、Q_5_020 |
| S76 | 東京外国語大学言語モジュール [無声化母音の産出](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/03-03-01.php) | い・うが無声子音に挟まれた場合と文末で無声化しやすいこと、アクセント核で生じにくい条件を確認。 | 2026-10-13本文取得。語末と文末を区別。 | Q_5_019 |
| S77 | 国立国語研究所 日本語話し言葉コーパス [予備的分析6-3 母音の無声化](https://clrd.ninjal.ac.jp/csj/misc/preliminary/j6_1.html) | 狭母音/i, u/、無声子音間、東京方言で顕著、隣接子音・無声化連鎖・発話速度による生起率変動を確認。 | 2026-10-13本文取得。無声化を必然規則として扱わない。 | Q_5_019 |
''')
print('Recorded', len(extra), 'repairs; verified 4 questions')
