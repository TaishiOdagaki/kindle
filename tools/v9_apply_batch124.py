"""One-time review of worksheet guidance and rapport without universal guarantees."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2700
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第123バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢を明示した公式ガイドライン/用語集とKrashen原著の本文・画像へ独立照合。ガイドラインの適用例と理論内の主張を区別。',explanation_review='全4解説を照合。例題一つ以上の必須規則、特定手法の不安軽減・信頼向上の普遍保証、ラポールと心理的安全性の同一視を除く。',unresolved='',multiple_correct_risk='なし：独立正答'+str(key)+'のみ適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_4_047';opts=q[k]['opts'].copy()
opts[0]='読み手に必要な情報を整理し、イラストや図なども使って、作業の内容や手順がわかるようにする。文字の量や見やすさにも配慮する。'
opts[1]='読みやすさを検討せず、文字をできる限り小さく詰め込み、情報量を増やすことだけを優先する。'
opts[2]='読み手に必要であっても、不足している作業条件の補足は行わず、元の文章の一言一句に対応する内容だけを残す。'
review(k,'外国人学習者へ配るワークシートの作業案内を、2020年版「在留支援のためのやさしい日本語ガイドライン」の書き言葉の工夫に沿って作る例として、最も適切なものを一つ選びなさい。',opts,[
'ガイドラインは、必要な情報に絞り、不足する情報を補い、イラストや図などで視覚的にもわかりやすくすることを示しています。作業案内にこの工夫を用いるという肢は、その提案に沿う例です。図を入れるだけで誰にでも必ず伝わるとするものではありません。',
'同書は漢字とふりがな、行と行の間を空けるなどして見やすくし、読みやすいフォントを使うことも示しています。情報量だけを優先して文字を詰め込み、読みやすさを検討しない方針とは異なります。',
'必要なら不足している情報を補うという作成方針に反します。読み手に必要な条件を補うことと、あらゆるワークシートに例題を一つ以上必須とすることは別です。今回の作成ポイントから、そのような一律の鉄則を導くことはできません。',
'同書は、読み手の言語背景や日本語能力に応じて調節し、簡単な言葉やわかりやすい文にすることを求めます。理解しやすさを考えず、未習の複雑な文法で指示文自体を難しくする方針とは合いません。'],1,['S189'],'2020公式ガイドライン印刷5〜10頁を本文・画像照合した書き言葉の作成提案を、ワークシートの作業案内へ適用する例として限定。元解説の例題必ず一つ以上という鉄則、全初級学習者への強い認知負荷や効果の保証は根拠未取得につき除去。情報の整理/補足、視覚的補助、読みやすい表記と対象者別の調節へ根拠を明示。',['正：必要情報・視覚的補助・見やすさを考える例','誤：読みやすさの検討を排し詰込みだけを優先','誤：必要な補足を禁じ元文への一言一句対応だけを求める','誤：読み手の能力への調節に反し指示文自体を難しくする'])
k='Q_4_016';opts=q[k]['opts'].copy()
opts[1]='ラポールは教師と学習者の関係に関わる概念であり、良好な関係を築くことが重視される。支援的な雰囲気の例には、学習者同士が助け合ったり助けを求めたりすることを教師が促すことがある。'
opts[2]='TKT公式用語集でいう支援的な雰囲気とは、学習者同士が助け合うことや他者に助けを求めることを教師が認めない雰囲気である。'
opts[3]='フィードバックはラポールと同義であり、学習や活動がどの程度できているかを相手に伝えることは、フィードバックの意味に含まれない。'
review(k,'Krashen（1982）の情意フィルター仮説内の主張と、CambridgeのTKT公式用語集にあるラポールや支援的な雰囲気の説明について、最も適切なものを一つ選びなさい。',opts,[
'Krashenは低い不安と低い情意フィルターを促す状況を重視します。高い不安を維持すれば習得の効率が最大になるとする肢とは逆です。ここでは仮説内の主張を述べており、不安と習得のあらゆる因果関係が実証済みだとするものではありません。',
'TKT公式用語集はラポールを教師と学習者の関係に関わるものとし、良好な関係づくりを示します。支援的な雰囲気の例としては、学習者が助け合い、他者に助けを求めることを教師が促すことを挙げています。',
'支援的な雰囲気の説明では、教師が学習者同士の援助や質問を促す例を挙げています。そのような助け合いや助けを求める行為を認めないという肢は、示された例に反します。',
'同用語集ではフィードバックに、学習や活動がどの程度できているかを伝えることが含まれます。関係に関わるラポールと同義ではありません。特定の訂正手法を使えば必ず信頼が高まるという保証や、信頼形成のため全フィードバックを禁じるという一律規則を意味するものでもありません。'],2,['S13','S183'],'Krashen原著印刷31〜32頁とTKT公式用語集印刷16・37・44頁を本文・画像照合。情意フィルターは仮説内の主張として扱い、ラポールを心理的安全性そのものの定義にせず関係概念と支援的な雰囲気を区別。リキャスト等が必ず上達・信頼を生むという未取得の効果保証を除き、フィードバックとの語義の違いを問う。全フィードバック禁止を信頼形成の必須条件とする旧規則も残さない。',['誤：Krashenの低不安/低フィルターの方向と逆','正：関係概念と支援的雰囲気の例に対応','誤：支援的な雰囲気の援助・質問促進と逆','誤：フィードバックの意味を否定しラポールと同一視'])
assert len(extra)==16,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch124.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];meta=[]
for sid,name,url,scope in [('S189','easy.pdf','https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/pdf/92484001_01.pdf','2020 guide printed5-10/PDF6-11 already text+image read; application to worksheet instructions is an explicit example, not a worksheet experiment'),('S13','krashen1982.pdf','https://www.sdkrashen.com/content/books/principles_and_practice.pdf','printed31-32/PDF38-39 text+images: within-theory affective filter, not all underlying studies'),('S183','tkt.pdf','https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf','printed16/37/44 PDF17/38/45 text+images: Feedback, Rapport, Supportive; not psychological-safety construct or guaranteed correction effects')]:
 raw=(root/name).read_bytes();meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-16',body_read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch124_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('2 questions/16 edits')
