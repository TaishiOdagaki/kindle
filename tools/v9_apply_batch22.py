#!/usr/bin/env python3
"""Source-gated particle and aspect corrections using public JF explanations."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==380
_,Q,A=qa.audit(str(b.DST));extra=[];D=json.loads((b.OUT/'decisions.json').read_text())
def item(k,stem,opts,exps,ans,why,sources,verdicts):
 for field,values in [('stem',[stem]),('options',opts),('explanations',exps)]:
  for i,new in enumerate(values):
   index=None if field=='stem' else i
   old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][i] if field=='options' else A['A_'+k[2:]]['txt'][i]
   old=html.unescape(old)
   if old!=new:extra.append(dict(id=k,field=field,index=index,before=old,after=new,reason=why,sources=sources,applied=True,before_version='第21修正バッチ作業稿'))
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=sources,option_verdicts=verdicts,reason=why,stem_review='場面と例文の意味を限定し、未提示の原因・学説分類を問わない。',explanation_review='取得した国際交流基金の文法解説本文に全4肢・4解説を照合。',unresolved='',multiple_correct_risk=f'なし：指定条件で{ans}のみ正しい',no_correct_risk=f'なし：独立正答{ans}')
item('Q_5_054','図書館から自宅へ移動したことを「昨日、図書館で本を借りました。それから家（ ）帰りました」と述べる。空欄に入る格助詞の説明として適切なものはどれか。',
 ['移動の起点を示すため、「から」が適切である。','帰還先を示すため、「に」または「へ」が適切である。','移動の経路を示すため、「を」が適切である。','本を借りる動作の場所を示すため、「で」が適切である。'],
 ['この場面の家は出発点ではなく帰還先です。「から」は場所の始まり・起点を示すため、提示した意味には合いません。','移動先を表す「へ」と帰着点を表す「に」は、この場面でどちらも使えます。「家へ帰りました」「家に帰りました」と言えます。','経路を示す「を」は、「橋を渡る」などに用いられます。この場面の家は通過する経路ではなく帰還先です。','本を借りた場所は前の文の図書館です。空欄では帰還先を示す必要があり、動作の場所を示す「で」ではその意味を表せません。'],2,
 '空欄を誤用とする前提を撤去したうえで、図書館から自宅への移動を明示。に／へと起点・経路・動作場所を区別し、場面不足を解消。',['S59'],['起点ではなく帰還先なので誤り','帰着点・移動先で正しい','経路ではないので誤り','帰還先でなく借用場所を問う説明なので誤り'])
item('Q_5_053','「部屋（ ）本を読む」と「部屋（ ）本がある」について、部屋で読書する動作と、部屋に本が存在する状態を表す場合、適切な助詞の組合せはどれか。',
 ['どちらも「に」を用いる。','どちらも「で」を用いる。','読書する動作の場所には「で」、本の存在場所には「に」を用いる。','読書する動作の場所には「に」、本の存在場所には「で」を用いる。'],
 ['「本を読む」の動作が行われる場所は「部屋で」と表します。どちらも「に」とする組合せは適切ではありません。','本が存在する場所は「部屋に本がある」と表します。どちらも「で」とする組合せは適切ではありません。','提示した意味では、動作の場所を「で」、物の存在場所を「に」で示します。「で」は出来事の発生場所にも用いられるため、「で＝動的、に＝静的」とだけ覚えるのは不十分です。','組合せが逆です。読書の動作場所は「部屋で」、本の存在場所は「部屋に」と表します。'],3,
 'ニとデを動的／静的で一律に分ける旧説明を撤去。読書動作と本の存在の明示例へ限定し、での出来事存在用法も区別。',['S59'],['動作場所のにが誤り','物の存在場所のでが誤り','動作場所で／物の存在場所にで正しい','組合せが逆で誤り'])
item('Q_5_057','次の二つの場面の「〜ている」について、適切な説明はどれか。①目の前で走っている人を見て「走っています」と言う。②車が衝突した後のバンパーを見て「壊れています」と言う。',
 ['①も②も、まだ起こっていない未来の予定だけを表す。','①も②も、毎日の習慣を表す。','①は動作の進行、②は壊れた結果の状態を表す。','①は走り終えた結果の状態、②は壊れる途中の進行を表す。'],
 ['①は現在目の前で起きている動作、②はすでに生じた変化の結果を述べています。未来の予定だけを述べる用法ではありません。','走っていますが習慣を表す文脈もありますが、①は目の前の動作を見て述べる場面です。②も毎日の習慣ではなく、壊れた後の状態です。','①は走る動作が進行中の場面、②は衝突によって壊れた後の状態を述べる場面です。動詞の意味に加えて提示した文脈を確認します。','説明が逆です。①は走っている途中、②は壊れた後の状態という条件が明示されています。'],3,
 '着る・かけるを無条件に瞬間動詞と分類する旧説明を撤去。国際交流基金の進行／結果状態の場面例に限定し、走っていますの習慣用法も区別。',['S58'],['現在の動作と結果を未来のみとして誤り','提示場面は習慣でなく誤り','提示場面の進行／結果状態で正しい','場面条件と逆で誤り'])
(b.OUT/'changes_batch22.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S59 | 国際交流基金 [助詞のまとめ](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00005/ja/render.do)、[へ](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00055/ja/render.do)、[に 帰着点](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00040/ja/render.do) | 3頁の全文を取得。場所の起点から、動作場所でと物の存在場所に、経路を、帰着点にと移動先へを確認。に／へでうちに帰る・うちへ帰るの例を取得。で＋あるの出来事用法も確認。原教材の旧JLPT級表示は現行試験仕様として転用しない。 | Q_5_053、054 |\n')
print('Recorded',len(extra),'repairs')
