#!/usr/bin/env python3
"""Resolve indirect speech act ambiguity using Searle's worked example."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==799
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
qid='Q_5_077';reason='旧稿は「ペンを持っていますか」に所持確認と貸与依頼を区別する場面情報がなく、貸さない応答を一律に誤解とした。Searleの原著の映画への誘いと試験勉強の応答という明示された分析例へ置換。指導の最善策という未検証評価を撤去し、間接的発話行為の定義と推論条件だけを問う。'
stem='Searle（1979）の間接的発話行為の分析に従う。映画への誘いに、相手が「試験の勉強をしなければなりません」と答え、断りを伝える場面について、最も適切な説明はどれか。'
opts=['勉強する必要を述べる発話は、それだけで、どの場面でも必ず映画への誘いの拒否となる。',
 '勉強する必要を述べるという発話行為を通して、間接的に誘いを断る行為を行っている。',
 '間接的発話行為では、話し手と聞き手の共有知識や推論は、発話の理解に関係しない。',
 '間接的発話行為とは、話し手が何も伝える意図を持たず、聞き手が行動した場合だけを指す。']
exps=['原著の分析は、直前の映画への誘いと共有知識を用います。勉強の必要を述べる発話が、あらゆる場面で拒否となるわけではありません。',
 '原著第2章は、映画への誘いに試験勉強の必要を述べる応答を分析します。本問の条件では、一つの発話内行為を通して、別の発話内行為である断りを間接的に行っています。',
 '原著は、共有される言語的・非言語的な背景情報と、聞き手の推論能力を説明に用いています。無関係という記述は逆です。',
 '原著は、話し手が間接的な行為を意図して伝える場合と、依頼を意図も理解もしていないのに聞き手が行動する場合とを明確に区別しています。']
for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
 for i,(before,after) in enumerate(zip(old,new)):extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=['S97'],applied=True,before_version='第43修正バッチ作業稿'))
D[qid].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S97'],option_verdicts=['文脈を無視した必然化が誤り','原著の間接拒否の分析例に一致して正しい','共有知識・推論の役割を否定して誤り','伝達意図のある間接行為と単なる結果を混同して誤り'],reason=reason,stem_review='原著の誘いと応答を訳し、間接拒否として伝える条件を明示。',explanation_review='第2章30～34頁の定義・例・推論条件へ全4肢・全4解説を照合。',unresolved='',multiple_correct_risk='なし：文脈・共有知識・伝達意図を否定する3肢を除外',no_correct_risk='なし：独立正答2')
(b.OUT/'changes_batch44.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S97 | John R. Searle（1979）[Expression and Meaning 第2章 Indirect speech acts](https://wstarr.org/teaching/speech_acts/Searle-1979-Expression_and_Meaning.pdf) Cambridge University Press | 原著30～34頁（PDF43～47頁）。一つの発話内行為を通して別の発話内行為を行う定義、共有知識と推論、映画への誘いと試験勉強の応答の間接拒否分析。 | 2026-10-13全197頁PDF取得・該当本文照合。所持質問を文脈なしに依頼へ一律解釈しない。 | Q_5_077 |
''')
print('1 question; 9 edits')
