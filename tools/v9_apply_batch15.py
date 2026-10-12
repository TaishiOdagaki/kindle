#!/usr/bin/env python3
"""Repair declaration example and false 'error' premise in aspect question."""
import json, html
from pathlib import Path
import v9_apply_batch1 as b
import quiz_audit as qa

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 309
_, Q, A = qa.audit(str(b.DST))
extra = []

def record(k, field, index, new, reason, sources):
    if field == 'stem':
        old = Q[k]['stem']
    elif field == 'options':
        old = Q[k]['opts'][index]
    else:
        old = A['A_' + k[2:]]['txt'][index]
    old = html.unescape(old)
    if old != new:
        extra.append(dict(id=k, field=field, index=index, before=old, after=new,
                          reason=reason, sources=sources, applied=True,
                          before_version='第14修正バッチ作業稿'))

why83 = ('Searle原典では宣言類の成功そのものが命題内容と現実を一致させ、通常は制度と話者の'
         '所定の地位を要する。単なる閉店予定の告知でも読める旧選択肢を、権限ある議長による'
         '閉会宣言へ置換し、他の三分類も原典の定義に照合。')
record('Q_5_083', 'stem', None,
       'Searle（1979）の発話内行為の分類において、「宣言類」に該当する発話はどれか。',
       why83, ['S49'])
record('Q_5_083', 'options', 3,
       '議長が所定の権限に基づいて「これをもって会議を閉会します。」と述べる。',
       why83, ['S49'])
for i, text in enumerate([
    '話し手を将来の行為に関与させる発話であり、コミット類です。',
    '聞き手に将来の行為をさせようとする発話であり、指示類です。',
    '感謝という心理状態を表す発話であり、表出類です。',
    '制度上の権限をもつ議長の発話が成功すると、その発話によって会議が閉会した状態になります。これは宣言類です。'
]):
    record('Q_5_083', 'explanations', i, text, why83, ['S49'])

why58 = ('「お腹がすいている」を誤用とする旧設問の前提は不成立。東京外国語大学の教材でも'
         '自然な日本語例として使われているため、「学習者の誤用」を中立的な「二つの表現」へ修正。'
         'アスペクト解説の正答は維持し、未取得の体系的根拠を理由に問題全体は確認済みにしない。')
record('Q_5_058', 'stem', None,
       '「私は今、お腹が【すいている】から、ご飯を食べたいです」と「（誰かが）電気を【つけている】」のアスペクト的違いの説明として、最も適切なものはどれか。',
       why58, ['S50'])

(b.OUT / 'changes_batch15.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(json.dumps(prior + extra, ensure_ascii=False, indent=2) + '\n')

D = json.loads((b.OUT / 'decisions.json').read_text())
D['Q_5_083'].update(
    status='確認済み', fixes_applied=True, independent_answer=4, sources=['S49'],
    option_verdicts=[
        '話し手の将来行為への拘束なのでコミット類',
        '聞き手に行為をさせる試みなので指示類',
        '感謝の心理状態を表すので表出類',
        '所定の権限をもつ議長の成功した発話が閉会状態を成立させるので宣言類'
    ],
    stem_review='原典の五分類、宣言類の成立効果、制度・地位条件を照合し、旧4肢の文脈不足を解消。',
    explanation_review='原典第1章の各分類の目的と宣言類の制度条件に4解説を個別照合。',
    multiple_correct_risk='なし：各肢の行為主体と目的を明示',
    no_correct_risk='なし：独立正答4', unresolved='')
D['Q_5_058'].update(
    status='修正必要', fixes_applied=True, sources=sorted(set(D['Q_5_058'].get('sources', []) + ['S50'])),
    stem_review='正用を誤用とした前提を公的大学教材の自然な用例に基づき撤去。',
    reason='設問前提の重大な誤りは修正したが、「つけている」の進行／結果状態の条件を含む全4肢・4解説の体系的根拠照合が未完了。',
    unresolved='「電気をつけている」の二義性と動詞分類を文法資料本文で再照合し、全4肢を独立判定する。')
(b.OUT / 'decisions.json').write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n')

p = b.OUT / 'sources.md'
p.write_text(p.read_text() +
    '\n| S49 | John R. Searle (1979), [Expression and Meaning: Studies in the Theory of Speech Acts](https://altexploit.files.wordpress.com/2019/10/john-r.-searle-expression-and-meaning-_-studies-in-the-theory-of-speech-acts-1979.pdf), Chapter 1 “A Taxonomy of Illocutionary Acts” | 原著全文を取得。pp.12–18（PDF 25–32頁）のassertives・directives・commissives・expressives・declarationsの定義、宣言の成立効果と制度・話者地位条件を照合。 | Q_5_083 |\n'
    '| S50 | 東京外国語大学言語モジュール「[招待する](https://www.coelang.tufs.ac.jp/mt/mn/dmod/class/ja_36.html)」 | 大学公開教材の日本語会話本文に「すごくおなかがすいているんだ」を確認し、当該形を一律に誤用とする前提を否定する根拠として限定使用。アスペクト体系全体の承認には使わない。 | Q_5_058 |\n')
print('Recorded', len(extra), 'repairs.')
