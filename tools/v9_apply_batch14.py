#!/usr/bin/env python3
"""Repair no-answer premise and unrestricted you-ni-naru analysis."""
import json,html
from docx import Document
from docx.oxml.ns import qn
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==278
_,Q,A=qa.audit(str(b.DST));doc=Document(b.DST);extra=[]
def change(k,f,i,new,why,s):
 old=Q[k]['opts'][i] if f=='options' else A['A_'+k[2:]]['txt'][i]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=f,index=i,before=old,after=new,reason=why,sources=s,applied=True,before_version='第13修正バッチ作業稿'))
def full(k,stem,opts,exps,why,s):
 ps=doc.paragraphs;start=next(i for i,p in enumerate(ps) if any(t.get(qn('w:name'))==k for t in p._p.iter(qn('w:bookmarkStart'))));old=[]
 for p in ps[start+1:]:
  if p.text.startswith('1. '):break
  if p.text:old.append(p.text)
 assert ' '.join(old)==html.unescape(Q[k]['stem'])
 extra.append(dict(id=k,field='stem',index=None,before=old[0],after=stem,reason=why,sources=s,applied=True))
 for t in old[1:]:extra.append(dict(id=k,field='stem_continuation',index=None,before=t,after='',reason='全文改稿に伴い旧場面・例文段落を除去。',sources=s,applied=True,remove_paragraph=True))
 for f,ts in [('options',opts),('explanations',exps)]:
  assert len(ts)==4
  for i,t in enumerate(ts):change(k,f,i,t,why,s)
why='Grice原著の格率の定義とviolate/floutの区別に照合。含意が必ず生じるという断定を撤回し、実在商品の未確認の事実を問う例を架空の明示条件へ置換。'
full('Q_5_078','Grice（1975）の会話の協調原理と格率について、適切なものはどれか。',[
'量の格率は、偽だと信じることを述べないという要求を指す。','質の格率は、会話目的に必要な情報量を提供するという要求を指す。','関係の格率は、関連性のある発言をするという要求を指す。','格率の不遵守は、どのような場合でも会話的含意を生まない。'],[
'偽だと信じることを述べないという要求は、質の格率です。','必要な情報量に関する要求は、量の格率です。','関係の格率は関連性を求めます。','あからさまな不遵守（flout）が、協調原理を維持する解釈の下で含意を生む場合があります。密かな違反（violate）とは区別します。'],why,['S48'])
full('Q_5_084','Grice（1975）が区別した格率の不遵守の仕方について、適切なものはどれか。',[
'あからさまな不遵守（flout）は、常に協調の拒否を意味し、含意を生まない。','質の格率は、常に発話を最短にすることだけを要求する。','他の格率との衝突も協調の拒否もなく、聞き手を欺こうとしていないあからさまな不遵守では、協調原理との両立を考える推論が会話的含意を生むことがある。','様態の格率と関係の格率は、同じ内容を表す別名である。'],[
'あからさまな不遵守と、協調への参加を拒むこと（opt out）は区別されます。','質は真実性・証拠に関する要求です。不要な冗長さを避けることは様態の項目です。','提示された条件では、聞き手が協調原理との両立を推論し、含意を読み取る場合があります。全ての不遵守で必ず成功するという意味ではありません。','様態は表現の明確さ・簡潔さ・順序などを扱い、関係は関連性を扱います。'],why,['S48'])
full('Q_5_085','次は架空のお菓子「雪の実」を渡す場面である。Bは「名前と、何のお菓子かだけ教えて」と依頼した。Aは「雪の実というクッキーです」と答えた後、求められていない製造会社の沿革や各年の販売数量の説明を長く続けた。追加情報はすべて正確で、Aには十分な証拠があるものとする。この場面で「求められた以上の情報を提供する」という点に対応する格率はどれか。',[
'関係の格率であり、お菓子に関する情報はすべて話題と無関係である。','情報が正確なら、量の格率が問題になることはない。','量の格率であり、この会話で求められた情報量を超えている。','質の格率であり、設定上Aは偽の情報を述べている。'],[
'追加情報も同じお菓子の説明です。ここで問うのは情報量です。','正確さと必要な情報量は別の観点です。','量の格率には、会話の目的に必要な量を超えないという要求があります。','正確さと十分な証拠を設定しているので、偽の情報という分析は合いません。'],why,['S48'])
(b.OUT/'changes_batch14.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
vs={'Q_5_078':['質を量と取り違えている','量を質と取り違えている','関係の定義に一致','floutに伴う含意の可能性を排除して誤り'],'Q_5_084':['floutとopt outを同一視して誤り','質と様態を混同','原著49頁の条件に対応し可能性として正しい','関係と様態を同一視して誤り'],'Q_5_085':['同じお菓子の話を全て無関係とする誤り','質を満たせば量が常に適切という推論は成立しない','限定された依頼を超える情報量に一致','正確さ・証拠を明示した条件に矛盾']}
for k in vs:
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=3,sources=['S48'],option_verdicts=vs[k],stem_review='原著の定義・条件を明示し、架空場面では情報の真偽と必要量を独立に指定。全4肢を独立判定。',explanation_review='原著印刷45–46・49–50頁の本文を取得し、画像でOCR欠落箇所を補完。4解説の定義と限定条件に照合。',multiple_correct_risk='なし：4肢の誤り又は該当条件を特定',no_correct_risk='なし：独立正答3',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(extra),'repairs.')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S48 | H. P. Grice (1975), [Logic and Conversation](https://projects.illc.uva.nl/inquisitivesemantics/assets/files/papers/Grice1975.pdf), Syntax and Semantics 3, pp.41–58 | 大学公開の原論文全18頁を取得。印刷45–46頁の協調原理・4格率、49–50頁のviolate/opt out/clash/floutと含意の条件を本文・画像で照合。日本語の架空場面は本監査で構成した適用例。全18頁の学説を一括承認しない。 | Q_5_078・084・085 |\n')
