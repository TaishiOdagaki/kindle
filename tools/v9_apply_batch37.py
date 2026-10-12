#!/usr/bin/env python3
"""Repair and verify four character-system and morphology questions."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 636
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
        'before_version': '第36修正バッチ作業稿',
    })


def rewrite(question_id, stem, options, explanations, reason, sources):
    record(question_id, 'stem', None, stem, reason, sources)
    for i, value in enumerate(options):
        record(question_id, 'options', i, value, reason, sources)
    for i, value in enumerate(explanations):
        record(question_id, 'explanations', i, value, reason, sources)


q31_reason = (
    '旧稿は平仮名・片仮名の成立に性別や文書用途の一般化を加え、万葉仮名の借音・借訓の例も'
    '未照合のまま示していた。文化庁の国語審議会資料と国立国会図書館の調査記録が直接確認できる、'
    '万葉仮名の表音使用、草体・略体、字音・字訓の借用に論点を限定した。'
)
rewrite(
    'Q_5_031',
    '万葉仮名と平仮名・片仮名の成立に関する記述として、最も適切なものはどれか。',
    [
        '平仮名は漢字の一部を省略した略体から、片仮名は漢字全体を崩した草体から成立した。',
        '平仮名と片仮名は万葉仮名とは無関係に、外国の表音文字をそのまま取り入れて成立した。',
        '平仮名・片仮名はいずれも漢字を表音的に用いた万葉仮名に由来し、平仮名は草体、片仮名は略体を基礎として成立した。',
        '万葉仮名は漢字の意味だけを用いる表意的な書記であり、漢字の字音や字訓を日本語の音の表記に利用しなかった。',
    ],
    [
        '対応が逆です。文化庁資料の「草体及び略体」はそれぞれ平仮名・片仮名へつながるもので、平仮名は草体、片仮名は略体を基礎とします。',
        '文化庁資料は、漢字を表音的に用いる万葉仮名から仮名による日本語表記が始まり、草体・略体の仮名文字が用いられるようになったと説明しています。',
        '万葉仮名という漢字の表音的使用を母体に、草体の仮名文字から平仮名、略体の仮名文字から片仮名が成立したという説明です。',
        '国立国会図書館の調査記録では、万葉仮名は漢字の字義を離れ、字音または字訓を借りて表音的に用いた文字とされています。意味だけを用いたという説明は誤りです。',
    ],
    q31_reason,
    ['S84'],
)

q32_reason = (
    '旧稿は「武＝戈＋止」の字源解釈と形声文字の割合という、字源説・対象字集合に依存する補助断定を含んでいた。'
    '東京大学OCWの六書整理が明示する、象形・指事、形声（音と義）、会意（義と義）の関係だけを問う問題へ改稿した。'
)
rewrite(
    'Q_5_032',
    '漢字の造字法を説明する六書のうち、象形・指事・会意・形声の関係について最も適切なものはどれか。',
    [
        '象形と指事は、既にある漢字を同じ意味または同じ音で別の語に転用する運用法である。',
        '形声は、音を示す要素だけを二つ以上組み合わせ、意味を示す要素を含まない造字法である。',
        '会意は意味に関わる要素同士を組み合わせ、形声は意味に関わる要素と音に関わる要素を組み合わせる造字法である。',
        '会意と形声はどちらも意味に関わる要素だけを組み合わせるため、両者を区別する基準はない。',
    ],
    [
        '東京大学OCW資料では、象形・指事は字形と意味に基づく造字法として整理されています。既存字の転用を述べたこの説明は誤りです。',
        '形声は音と意味の要素を組み合わせる造字法です。音を示す要素だけから成るという説明は誤りです。',
        '同資料は、形声を「音と義」、会意を「義と義」の組合せとして区別しています。この記述はその関係に一致します。',
        '会意は意味に関わる要素同士、形声は意味と音に関わる要素の組合せなので、両者は区別されます。',
    ],
    q32_reason,
    ['S85'],
)

q36_reason = (
    '旧稿は和語と訓読み、漢語と音読みの一般的対応を「すべて」と逆転して説明し、'
    '個別字「行」の呉音・漢音・唐音の例にも出典がなかった。文化庁の音訓資料と国立国会図書館の'
    '専門書書誌・要約により、音読みの由来、複数層、訓読みの意味対応を限定して再記述した。'
)
rewrite(
    'Q_5_036',
    '漢字の音読みと訓読みに関する記述として、最も適切なものはどれか。',
    [
        '音読みは中国語の漢字音に由来し、伝来した時代や経路などの違いにより、呉音・漢音・唐音などの層がある。',
        '訓読みは中国語の発音をそのまま日本語の音として写した読みで、漢字の意味との対応を必要としない。',
        '和語はすべて音読みで、漢語はすべて訓読みで表されるという例外のない規則がある。',
        '一つの漢字が持てる音読みは必ず一種類だけで、複数の音読みを持つ漢字はない。',
    ],
    [
        '国立国会図書館の専門書情報は、音読みが中国語に由来し、呉音・漢音・唐音などが伝来時期や経路の違いに応じて成立したことを示しています。',
        '訓読みは、漢字の意味に対応する日本語の語を当てて読むものです。中国語音の写しとする説明は音読みとの混同です。',
        'この選択肢は音読みと訓読みの一般的な対応を逆にしているうえ、「すべて」「例外のない規則」と断定しています。音訓と語種は一対一に固定されません。',
        '音読みには呉音・漢音・唐音などの複数の層があります。国立国会図書館の専門書要約も「行」にコウ・ギョウ・アンの複数の読みを挙げています。',
    ],
    q36_reason,
    ['S86'],
)

q40_reason = (
    '旧稿は「自由異形」という不適切な別名、語幹と音声単位の混同、音素を単なる音声単位とする説明を含んでいた。'
    '公開大学教科書の定義に合わせ、形態素、自由形態素、拘束形態素、音素の区別を直接問う内容へ改稿した。'
)
rewrite(
    'Q_5_040',
    '形態素と、自由形態素・拘束形態素の区別に関する記述として、最も適切なものはどれか。',
    [
        '自由形態素は単独では語として現れず、必ず別の形態素に付いて現れる形態素である。',
        '拘束形態素は単独で語として現れることができず、接辞「さ」のように他の形態素と結び付いて現れる。',
        '音素は語彙的意味または文法的機能を担う最小単位なので、形態素と同じ単位である。',
        '形態素は文法的機能だけを担う単位であり、語彙的意味を持つ語根は形態素に含まれない。',
    ],
    [
        '説明が逆です。自由形態素は、それだけで一つの語として現れることができる形態素です。',
        '拘束形態素は単独で語として現れず、他の形態素を伴って現れます。接辞は基体に付く必要があるため拘束形態素です。',
        '形態素は形式と意味または文法機能の最小の体系的対応です。音素は意味の違いを生じさせる音韻上の単位で、形態素とは同じ単位ではありません。',
        '形態素には、文法機能を示す接辞だけでなく、語彙的意味の中心を担う語根も含まれます。',
    ],
    q40_reason,
    ['S87'],
)

updates = {
    'Q_5_031': (3, ['S84'], [
        '平仮名と片仮名の草体・略体を逆にしており誤り',
        '万葉仮名との歴史的連続を否定しており誤り',
        '万葉仮名、草体、略体の関係に一致して正しい',
        '字音・字訓を借りた表音使用を否定しており誤り']),
    'Q_5_032': (3, ['S85'], [
        '象形・指事を既存字の転用とするため誤り',
        '形声から意味要素を除外しており誤り',
        '会意＝義と義、形声＝音と義の区別に一致して正しい',
        '会意と形声の区別を否定しており誤り']),
    'Q_5_036': (1, ['S86'], [
        '音読みの中国語由来と複数層に一致して正しい',
        '訓読みを中国語音の音写とするため誤り',
        '音訓と語種を逆転し例外なく固定するため誤り',
        '複数の音読みが存在するため誤り']),
    'Q_5_040': (2, ['S87'], [
        '自由形態素と拘束形態素の定義を逆転しており誤り',
        '拘束形態素と接辞の定義に一致して正しい',
        '音素と形態素を同一視しており誤り',
        '語彙的意味を持つ語根を形態素から除外しており誤り']),
}
reasons = {'Q_5_031': q31_reason, 'Q_5_032': q32_reason,
           'Q_5_036': q36_reason, 'Q_5_040': q40_reason}
for qid, (answer, sources, verdicts) in updates.items():
    D[qid].update(
        status='確認済み', fixes_applied=True, independent_answer=answer,
        sources=sources, option_verdicts=verdicts, reason=reasons[qid],
        stem_review='根拠資料が直接支える定義と対立だけに限定して再構成。',
        explanation_review='改訂後の4選択肢と4解説を根拠本文へ照合。',
        unresolved='', multiple_correct_risk='なし：正答以外は定義と明確に不一致',
        no_correct_risk=f'なし：独立正答{answer}')

(b.OUT / 'changes_batch37.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

sources = b.OUT / 'sources.md'
sources.write_text(sources.read_text() + '''
| S84 | 文化庁 第15期国語審議会 [第5回総会報告](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kakuki/15/sokai005/02.html)、[仮名遣い委員会審議経過](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kakuki/15/tosin01/02.html)、国立国会図書館 [万葉仮名調査記録](https://crd.ndl.go.jp/reference/detail?page=ref_view&id=1000272912) | 文化庁本文で万葉仮名という漢字の表音的使用、9世紀の草体・略体を確認。国会図書館記録で字義を離れ字音・字訓を借りる定義と典拠を確認。 | 2026-10-13本文取得。個別の字母、性別・用途の社会史は本問の承認対象から撤去。 | Q_5_031 |
| S85 | 東京大学OCW 斎藤希史 [東アジア教養学「漢字の基本概念」](https://ch.u-tokyo.ac.jp/ocw-files/lecture_files/11365/4/notes/ja/04saito20141104final.pdf) | PDF9頁の六書整理で、象形・指事、形声＝音と義、会意＝義と義を確認。 | 2026-10-13本文取得。個別字「武」の字源説と形声文字の比率は承認対象から撤去。 | Q_5_032 |
| S86 | 文化庁 [当用漢字音訓表](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kakuki/syusen/tosin04/index.html)、国立国会図書館 [『漢字と音読みの謎を解く』書誌・要約](https://ndlsearch.ndl.go.jp/books/R100000137-I9784121029249) | 文化庁本文で字音に漢音・呉音・唐音・慣用音があることを確認。国会図書館の専門書情報で中国語由来、伝来時期・経路による層、「行」のコウ・ギョウ・アンを確認。 | 2026-10-13本文取得。書誌・要約で確認できる範囲に限定。 | Q_5_036 |
| S87 | Catherine Andersonほか [Essentials of Linguistics, 2nd ed. 5.1](https://ecampusontario.pressbooks.pub/essentialsoflinguistics2/chapter/5-1-what-is-morphology/)、[5.2](https://ecampusontario.pressbooks.pub/essentialsoflinguistics2/chapter/5-2-types-of-morphology-affixes-and-beyond/) | 形態素を形式と意味・文法機能の最小の体系的対応とする定義、自由形態素は単独語になり、拘束形態素は他の形態素を伴うこと、接辞は拘束形態素であることを確認。 | 2026-10-13公開大学教科書本文取得。日本語の個別分析は定義から直接判定できる接辞「さ」に限定。 | Q_5_040 |
''')
print('Recorded', len(extra), 'repairs; verified 4 questions')
