#!/usr/bin/env python3
"""Remove an ambiguous example from the derivational-morphology item."""
import json, html
import v9_apply_batch1 as b
import quiz_audit as qa

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 329
_, Q, A = qa.audit(str(b.DST))
extra = []

def record(k, field, index, new, reason, sources):
    if field == 'stem': old = Q[k]['stem']
    elif field == 'options': old = Q[k]['opts'][index]
    else: old = A['A_' + k[2:]]['txt'][index]
    old = html.unescape(old)
    if old != new:
        extra.append(dict(id=k, field=field, index=index, before=old, after=new,
                          reason=reason, sources=sources, applied=True,
                          before_version='第16修正バッチ作業稿'))

why = ('「子ども」を単純語と断定する旧解説には形態分析上の異論が生じ得るため、個別語の分析を競わせる構成を撤去。'
       '派生語を、独立した語に接頭語・接尾語が付いてできる語とする辞典本文に合わせ、複合・反復・単純・派生の定義を区別する設問へ全面改稿。')
opts = [
    '二つの語基が結合してできた語',
    '同じ語基を反復してできた語',
    '一つの語基からなり、接辞を含まない語',
    '語基に接頭辞または接尾辞が付いてできた語'
]
exps = [
    '二つの語基が結合してできた語は複合語です。派生語は、語基に接辞が付いてできた語を指します。',
    '同じ語基の反復によってできた語は畳語です。派生語の定義ではありません。',
    '一つの語基からなり、接辞を含まない語は単純語です。派生語の定義ではありません。',
    '派生語は、語基となる語に接頭辞または接尾辞が付いてできた語です。例えば「春めく」は「春」に接尾辞「めく」が付いた派生語です。'
]
for i,t in enumerate(opts): record('Q_5_042','options',i,t,why,['S53'])
for i,t in enumerate(exps): record('Q_5_042','explanations',i,t,why,['S53'])

(b.OUT/'changes_batch17.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D['Q_5_042'].update(status='確認済み',fixes_applied=True,independent_answer=4,sources=['S53'],
    option_verdicts=['複合語の定義であり誤り','畳語の定義であり誤り','単純語の定義であり誤り','接辞による派生語の定義で正しい'],
    stem_review='個別語の形態分析を競わせず、語構成の定義を区別する設問として再構成。',
    explanation_review='取得した辞典本文の派生語定義と「春めく」の例に全4肢・4解説を照合。',
    multiple_correct_risk='なし：4だけが語基への接辞付加を述べる',
    no_correct_risk='なし：独立正答4',
    reason='旧稿の「子ども＝単純語」という断定を撤去し、辞典本文で判定できる定義問題へ改稿。',
    unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md'
p.write_text(p.read_text()+
 '\n| S53 | 学研キッズネット辞典 [派生語](https://kids.gakken.co.jp/jiten/dictionary06100287/) | 出版社系辞典本文を全頁取得。独立した単語に接頭語・接尾語が付いてできた語という定義と、接尾辞による派生語の例「春めく」を確認。個別語「子ども」の形態分析は承認対象から撤去。 | Q_5_042 |\n')
print('Recorded',len(extra),'repairs.')
