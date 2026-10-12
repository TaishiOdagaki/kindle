#!/usr/bin/env python3
"""Source-gate modality distinctions and remove an indefinite-aru example."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==425
_,Q,A=qa.audit(str(b.DST));extra=[];D=json.loads((b.OUT/'decisions.json').read_text())
def item(k,stem,opts,exps,ans,why,source,verdicts):
 for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
  for i,new in enumerate(vs):
   old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][i] if field=='options' else A['A_'+k[2:]]['txt'][i]
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=[source],applied=True,before_version='第24修正バッチ作業稿'))
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=[source],option_verdicts=verdicts,reason=why,stem_review='根拠本文で確認できる接続・意味と明示した例に限定。',explanation_review='取得した国際交流基金本文に全4肢・4解説を照合。',unresolved='',multiple_correct_risk=f'なし：{ans}のみ本文と明示条件に一致',no_correct_risk=f'なし：独立正答{ans}')
item('Q_5_061','様態の「〜そうだ」と伝聞の「〜そうだ」について、適切な説明はどれか。',
 ['伝聞の「〜そうだ」では、情報源を「〜によると」などで示すことができない。','様態の「〜そうだ」は、肯定形では名詞に直接付けて「学生そうだ」と言う。','「雨が降りそうだ」と「雨が降るそうだ」は、接続も用法も同じである。','様態の「〜そうだ」には、現状から判断して今後起こる可能性を述べる用法があり、伝聞の「〜そうだ」は聞いたり読んだりした情報を伝える用法である。'],
 ['伝聞の「そうだ」では、情報源を「天気予報によると」などで示すことができます。','肯定形で名詞に直接「そうだ」を付ける「学生そうだ」は、様態の標準的な接続ではありません。「学生のようだ」などを用います。','「降りそうだ」は様態、「降るそうだ」は伝聞で、接続と用法が異なります。','様態の「そうだ」は、見た目の様子だけでなく、現状から今後の可能性を判断する場合にも使われます。伝聞の「そうだ」は他から得た情報を伝えます。様態を目で見た直後の変化だけに限定しません。'],4,
 '様態を視覚的観察直後だけに限定する説明と、らしいを客観情報のみとする説明を撤去。公的教材の様態・伝聞の接続と現状からの可能性判断に限定。','S62',['伝聞の情報源表示を否定して誤り','様態の名詞直接接続が誤り','様態と伝聞を同一視して誤り','公的教材の意味・用法に一致'])
item('Q_5_069','推量・様態・伝聞の表現の接続について、適切な説明はどれか。',
 ['様態の「そうだ」では、「降ります」から「降りそうだ」、「忙しい」から「忙しそうだ」となる。「いい」は「よさそうだ」となる。','伝聞の「そうだ」は動詞のマス形からマスを除いた形に付き、「雨が降りそうだ」が伝聞となる。','推量の「らしい」は名詞に接続するとき、必ず「名詞＋なの＋らしい」となる。','推量の「ようだ」は名詞に接続するとき、「名詞＋の＋ようだ」という形を使えない。'],
 ['様態の「そうだ」は、これらの動詞・形容詞では「降りそうだ」「忙しそうだ」となります。「いい」は例外的に「よさそうだ」です。','伝聞では「雨が降るそうだ」と、動詞の普通形に付きます。「降りそうだ」は様態の形です。','名詞に直接付く「雨らしい」などの形があります。「なの」を必ず挟むという説明は誤りです。典型性を表す「春らしい」などの用法とは、文脈で区別します。','推量では「雨のようだ」のように、名詞に「のようだ」が接続する形を使います。この接続を文法的に排除する説明は誤りです。'],1,
 '男らしいを推量の無条件な例とする解説を撤去。雨らしいと典型性用法を区別し、そうだの接続とよさそうだの例外を明示。','S62',['接続といいの例外が正しい','伝聞と様態の接続を混同して誤り','名詞直接接続を排除して誤り','名詞のようだを排除して誤り'])
item('Q_5_066','「机の上にある本」の「ある」の働きについて、適切な説明はどれか。',
 ['名詞と名詞を結び付ける助詞として使われている。','本がすでに行った過去の動作を表している。','名詞修飾では必ず過去形にするので、「ある」を「あった」に変えなければならない。','存在を表す動詞として使われ、「机の上にある」が名詞「本」を修飾している。'],
 ['「ある」はここでは存在を表す動詞であり、名詞同士を結ぶ助詞ではありません。','机の上に本が存在することを述べています。本が過去に何かをしたという意味ではありません。','存在を表す「ある」は「そこにある本」などの形で名詞を修飾できます。過去形「あった」に必ず変える必要はありません。','「机の上にある」が、本が存在する場所を述べて「本」を修飾しています。不特定の時を表す「ある日」の「ある」を、存在動詞の例として扱っていません。'],4,
 'ある日を存在動詞の連体修飾の例とする混同を撤去。存在場所を明示した連体修飾の例へ改題。旧稿のた／ているの置換の全称主張は承認せず撤去。','S63',['助詞でなく動詞なので誤り','存在と過去動作を混同して誤り','名詞修飾を過去形に限定して誤り','存在動詞の名詞修飾で正しい'])
(b.OUT/'changes_batch25.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''\n| S62 | 国際交流基金 [そうです 様態](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00094/ja/render.do)、[そうです 伝聞](https://www.jpf.go.jp/j/urawa/j_rsorcs/textbook/setsumei_pdf/setsumei19_4.pdf)、[そうだ／ようだ／らしい（1）](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/201012.html) | 3資料本文取得。現状からの可能性判断、伝聞の情報源表示、接続の差、いい→よさそう、名詞のようだ／名詞らしいを確認。記事の関心の度合いによる説明を全学説に普遍化しない。 | Q_5_061、069 |
| S63 | 国際交流基金 [V＋N](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00128/ja/render.do) | 本文・例文12のそこにある本を取得。存在動詞あるを含む節の名詞修飾を確認。ある日の不定用法やた／ているの全置換条件は本問から撤去し承認しない。 | Q_5_066 |\n''')
print('Recorded',len(extra),'repairs')
