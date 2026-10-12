#!/usr/bin/env python3
"""Separate generic conditionals from past discovery; avoid blanket ba restrictions."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==452
_,Q,A=qa.audit(str(b.DST));extra=[];D=json.loads((b.OUT/'decisions.json').read_text())
def item(k,stem,opts,exps,ans,why,verdicts):
 for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
  for i,new in enumerate(vs):
   old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][i] if field=='options' else A['A_'+k[2:]]['txt'][i]
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S64'],applied=True,before_version='第25修正バッチ作業稿'))
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=['S64'],option_verdicts=verdicts,reason=why,stem_review='一般条件・過去の発見・個人的願望の条件を区別して限定。',explanation_review='国際交流基金と（条件）本文と過去形・と／たらの表に全4肢・4解説を照合。ば／ならの全用法は承認しない。',unresolved='',multiple_correct_risk=f'なし：{ans}のみ指定条件と本文に一致',no_correct_risk=f'なし：独立正答{ans}')
item('Q_5_062','条件表現「と」の用法について、適切な説明はどれか。',
 ['「と」は自然科学的な法則だけを表し、日常的な習慣を表すことはない。','「と」は一般的・習慣的な関係を表すほか、後件が過去形の場合に発見や出来事のきっかけを表す用法もある。','「と」を用いた文の後件は必ず非過去形であり、過去形になることはない。','個人的な願望を述べる「大学生になると、ラグビーをしたいです」は、後件の願望表現に制約がない典型例である。'],
 ['「と」は自然現象だけでなく、一般的な事実や習慣的な関係にも用いられます。','一般的・習慣的な関係のほか、過去の事態では、ある行動をきっかけに別の出来事が起きたり、行動後に何かを発見したりする用法もあります。とを自然法則・習慣だけに限定しません。','国際交流基金の解説には、教室へ行くと授業がすでに始まっていたという発見や、呼ばれると立ち上がったというきっかけの例があります。後件が過去形になる場合を排除できません。','一回の個人的な願望を述べるこの意味では、「大学生になったら、ラグビーをしたいです」のように「たら」を用います。このと（条件）の後件に願望表現を無制限に置けるという説明は誤りです。'],2,
 'とを自然科学的・習慣的な確定関係だけに限定する読みを撤去。公的教材の後件過去形の発見・きっかけの用法も反映。',['自然現象だけに限定して誤り','一般習慣と過去発見・きっかけの用法で正しい','後件過去形を排除して誤り','個人的願望の後件を無制限に認めて誤り'])
item('Q_5_063','学習者が将来一度日本を訪れ、その際に富士山へ登りたいという自分の希望を「日本へ行くと、富士山に登りたいです」と表した。この意味に合う修正の説明として、適切なものはどれか。',
 ['「行くと」のままでよい。このと（条件）の後件には個人的な願望を制限なく置ける。','「日本へ行ったら、富士山に登りたいです」として、訪日した場合の希望を「たら」で表す。','「行くと」のとをどと発音すれば、この作文の条件表現を修正できる。','「行ったら」に直すと、後件に希望を置けなくなるため修正できない。'],
 ['提示した一回の訪日と希望を述べる文では、と（条件）の後件の願望表現が問題になります。とをそのままにして制約がないと説明するのは適切ではありません。','「たら」は、話し手が想定した条件の後に願望を述べる場合にも使えます。提示した意味では「日本へ行ったら、富士山に登りたいです」と表せます。これを唯一可能な日本語表現だとは断定していません。','設問の問題は、書かれた条件表現と願望の組合せです。発音を濁らせても、その組合せを修正したことにはなりません。','国際交流基金の解説には、大学生になったらラグビーをしたいという条件と願望の例があります。たらの後件に希望を置けないという説明は誤りです。'],2,
 '動詞前件のばに後件希望は一律不可という旧解説を撤去。一回の将来の訪日と本人の願望を明示し、と／たらの改訂に限定。',['と後件の願望を無制限に認めて誤り','想定条件後の希望をたらで表し正しい','発音で条件表現を修正できず誤り','たら後件の希望を否定して誤り'])
(b.OUT/'changes_batch26.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S64 | 国際交流基金 [と 条件](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00030/ja/render.do) | 全本文、先生へ欄、後件過去形の表、と／たら比較表を取得。一般・習慣・自然現象に加え過去の発見・きっかけを確認。個人の想定条件＋願望でたらを用いる例を確認。ば／ならの体系全体は本問から撤去し未承認。 | Q_5_062、063 |\n')
print('Recorded',len(extra),'repairs')
