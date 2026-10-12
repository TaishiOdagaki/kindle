#!/usr/bin/env python3
"""Use Inoue's explicit modality taxonomy and attested modal-ta examples."""
import json, html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text()); assert len(prior)==497
_,Q,A=qa.audit(str(b.DST)); extra=[]
D=json.loads((b.OUT/'decisions.json').read_text())
def item(k,stem,opts,exps,ans,why,verdicts):
 for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
  for i,new in enumerate(vs):
   old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][i] if field=='options' else A['A_'+k[2:]]['txt'][i]
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S67'],applied=True,before_version='第28修正バッチ作業稿'))
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=['S67'],option_verdicts=verdicts,reason=why,stem_review='井上優の記述に範囲を限定し、学説間の相違と文脈依存性を混同しない設問へ改訂。',explanation_review='国立国語研究所公開の井上優「モダリティ」133–135頁の本文・分類・例6–7に全4肢・4解説を照合。',unresolved='',multiple_correct_risk=f'なし：{ans}のみ指定した記述に一致',no_correct_risk=f'なし：独立正答{ans}')
item('Q_5_059','井上優「モダリティ」で説明される「ムードのタ」について、適切な説明はどれか。',
 ['「タ」を含む文は、例外なく過去の出来事の時間的位置だけを表す。','「あ、あった」のような発見や、「確か井上さんでしたっけ」のような思い出しを表す用法が挙げられている。','「タ」は、現在の発見を表すことが文法的にできない。','「タ」を含む文はすべて命令文であり、相手の行為を禁止する。'],
 ['同資料には、発見や思い出しを表す用法も示されています。すべてを過去の時間的位置だけで説明することはできません。','同資料の例6は、発見と思い出しを「ムードのタ」の例として示しています。設問はこの記述を問うもので、タ形の全用法をこの二つに限定していません。','同資料には、その場での発見を表すタの例があります。現在の発見には使えないという説明は誤りです。','同資料の発見・思い出しの例は、相手の行為を禁止する命令ではありません。タを含む文をすべて禁止の命令文とする説明は誤りです。'],2,
 '買うんだったの文脈依存性と電車が来たの完了／発見の重なりを撤去し、取得した原著のムードのタの記述を限定して問う。',
 ['発見・思い出しを排除して誤り','原著の例6に一致して正しい','原著の発見の例を否定して誤り','発見・思い出しを禁止命令に誤分類して誤り'])
item('Q_5_060','井上優「モダリティ」の分類において、「聞き手に対する発話態度・伝達態度を表すもの」（対人的モダリティ）の例に該当するのはどれか。',
 ['命令・依頼・勧誘など、聞き手への働きかけ。','「なければならない」が表す必要性の判断という、価値判断の基本分類。','「かもしれない」が表す蓋然性の判断という、真偽判断の基本分類。','「らしい」「ようだ」が表す証拠性の判断という、真偽判断の基本分類。'],
 ['同資料は、命令・依頼・禁止・勧誘などの働きかけを、聞き手に対する発話態度・伝達態度の分類に含めています。','同資料の基本分類では、必要性は価値判断のモダリティに置かれます。ただし判断を表す形式が、文脈によって聞き手への働きかけとしても使われることまで否定していません。','同資料では、かもしれないによる蓋然性判断は真偽判断のモダリティに置かれます。設問が問う働きかけの基本分類ではありません。','同資料では、らしい・ようだによる証拠性判断は真偽判断のモダリティに置かれます。対人的な働きかけの例として挙げる説明ではありません。'],1,
 '対事／対人の分類を唯一の統一見解とする読みを撤去し、井上優の体系を明示。形式の基本分類と文脈による発話機能を区別した。',
 ['発話・伝達の働きかけに分類され正しい','指定体系では判断側に置かれ誤答','指定体系では真偽判断側に置かれ誤答','指定体系では真偽判断側に置かれ誤答'])
(b.OUT/'changes_batch29.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S67 | 井上優 [モダリティ](https://www2.ninjal.ac.jp/takoni/DGG/09_modarityi.pdf)（国立国語研究所公開） | 133–135頁の本文、例6、判断／発話・伝達の分類、文脈で機能が変わる例7を取得・精読。学説・用語の相違を著者自身が明記。体系を指定して全肢・全解説を照合した。 | Q_5_059、060 |\n')
print('Recorded',len(extra),'repairs')
