#!/usr/bin/env python3
"""Resolve aspect ambiguity with explicit contexts; remove an empty-slot error label."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==370
_,Q,A=qa.audit(str(b.DST));extra=[]
def record(k,field,index,new,why,sources):
 old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][index] if field=='options' else A['A_'+k[2:]]['txt'][index]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=field,index=index,before=old,after=new,reason=why,sources=sources,applied=True,before_version='第20修正バッチ作業稿'))
w='国際交流基金の文脈を示した進行・結果状態の解説に合わせ、曖昧な空腹／電気の例を撤去し、シャッターの動作中と開店状態の継続を対比。自他だけで用法を固定しない。'
record('Q_5_058','stem',None,'次の二つの場面の「〜ている」の用法について、適切な説明はどれか。①シャッターが上がっている途中で「今、シャッターが開いています」と言う。②朝に店を開け、営業中の店について「この店は夜10時まで開けています」と言う。',w,['S58'])
opts=['①も②も動作が進行中であり、シャッターを動かす動作が夜10時まで続くことを表す。','①は動作の進行を、②は店を開けた後の状態を続けていることを表す。','①も②もまだ起こっていない未来の出来事だけを表す。','「開く」は自動詞、「開ける」は他動詞なので、②が状態を表すことはない。']
exps=['①はシャッターが動いている途中ですが、②はすでに店を開けて営業を続けている場面です。店を開ける動作そのものが夜10時まで進行するとは述べていません。','①は提示した場面で動作の進行を表します。②は朝に店を開けた結果の状態を続けていることを表し、開店状態を保つ動作主の行為や意志にも注意が向けられます。','①は現在進行中の動き、②は現在続いている開店状態を述べています。②には営業終了時刻への言及がありますが、未来の出来事だけを述べる用法ではありません。','自動詞・他動詞の違いだけで「〜ている」の意味を決めることはできません。国際交流基金の解説でも、この場面の「開いている」と「開けている」はどちらも状態を表します。']
for i,t in enumerate(opts):record('Q_5_058','options',i,t,w,['S58'])
for i,t in enumerate(exps):record('Q_5_058','explanations',i,t,w,['S58'])
record('Q_5_054','stem',None,'「昨日、図書館で本を借りました。それから家（ ）帰りました」の空欄に入る格助詞の説明として、最も適切なものはどれか。','空欄を補う課題には誤用が提示されていないため、学習者の誤用というラベルを撤去。各格助詞の説明の根拠照合は残す。',[])
(b.OUT/'changes_batch21.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D['Q_5_058'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S58'],option_verdicts=['状態の継続を動作進行と取り違えて誤り','明示した2場面の進行／状態の区別で正しい','現在の進行・状態を未来のみとするため誤り','他動詞のテイルの状態用法を否定して誤り'],reason=w,stem_review='進行の動作中と、朝開店して営業中という結果状態の文脈を明示。',explanation_review='国際交流基金文法を楽しく2013年12月の例(4)と解説本文に全4肢・4解説を照合。',unresolved='',multiple_correct_risk='なし：提示場面では2のみ',no_correct_risk='なし：独立正答2')
D['Q_5_054'].update(status='要追加確認',fixes_applied=True,reason='空欄未記入を学習者の誤用とする設問前提は撤去。帰還先を表すに／へ、から／を／での全肢・解説を公的文法教材で照合する必要が残る。',unresolved='全4肢・4解説の格助詞の用法と、帰還先の条件を原資料と照合する。')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S58 | 国際交流基金 市川保子 [文法を楽しく ている・ていた（1）](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/201312.html) | 例(4)と説明全文を取得・精読。動作中のシャッターと、開店した結果の状態を続ける場面を区別。他動詞の開けているも状態を表すことを確認し、文脈を指定して出題。原資料の例を基にした監査用の改題。 | Q_5_058 |\n')
print('Recorded',len(extra),'repairs')
