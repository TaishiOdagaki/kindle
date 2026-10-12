#!/usr/bin/env python3
"""Narrow Q5-022 word-final mora-nasal explanation to the retrieved TUFS wording."""
import html
import json

import quiz_audit as qa
import v9_apply_batch1 as b

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 635
_, _, A = qa.audit(str(b.DST))
before = html.unescape(A['A_5_022']['txt'][3])
after = (
    '東京外国語大学の教材では、語末の「ん」は舌を[ŋ]より奥に置く鼻音になることが多いと説明されています。'
    '鼻から呼気を出す鼻音であり、口蓋帆を閉じて息をすべて口から出すという説明は誤りです。'
)
entry = {
    'id': 'Q_5_022',
    'field': 'explanations',
    'index': 3,
    'before': before,
    'after': after,
    'reason': '旧解説は語末の撥音を小舌鼻音又は鼻音化母音と列挙したが、今回取得したTUFS本文の記述範囲を超えるため、[ŋ]より奥で調音されることが多い鼻音という取得本文の表現へ限定した。',
    'sources': ['S79'],
    'applied': True,
    'before_version': '第36修正バッチ初回作業稿',
}
(b.OUT / 'changes_batch36_followup.json').write_text(
    json.dumps([entry], ensure_ascii=False, indent=2) + '\n')
(b.OUT / 'changes.json').write_text(
    json.dumps(prior + [entry], ensure_ascii=False, indent=2) + '\n')
print('Recorded 1 follow-up repair')
