"""One-time environment analysis scope correction from Nation's public manuscript."""
import json,html,hashlib
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2842
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_028';ak='A_4_028'
assert d[k]['status']=='修正必要' and a[ak]['ans']=='4'
stem='環境分析の対象のうち、学習者の能力や目標ではなく、コースを実施する時間や資源の条件を具体的に示したものを一つ選べ。'
exps=['既習の文法や語彙数は、学習者が現在何を知っているかに関する情報です。この設問が焦点を当てる、時間や利用可能な資源の条件とは異なります。','将来達成したい言語行動は、学習者が何を必要とし、何を学びたいかに関する情報です。この設問が焦点を当てる、時間や資源の条件とは異なります。','学習者のアイデンティティの変化を記述しており、時間や資源の条件を具体的に示す項目ではありません。学習者に関する要因が環境分析から一切除かれるという意味ではありません。','Nationの説明では、環境分析にコースの時間、クラスの人数、利用可能な資源などが含まれます。この肢は設問の対象に当たります。ただし、環境分析全体は学習者・教師・状況に関する要因も含みます。']
reason='Paul Nation著者公式大学サイトの公開稿What Should Every ESL Teacher Know?を取得。印刷/PDF12–14頁のNeeds Analysis・Environment Analysisの定義と例を本文・画像精読。環境分析が学習者・教師・状況に関する要因を含むことを確認し、物理的条件だけという排他的な定義を撤回。設問を時間・人数・利用可能資源という下位範囲の識別に限定し、全4肢と解説を独立判定。ニーズ分析と環境分析を常に排他的とせず、現在の知識や目標にも分析上の価値があることを維持。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S197'],applied=True,before_version='第134バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
assert len(extra)==5
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S197'],reason=reason,option_verdicts=['誤：既習知識であり時間・資源条件ではない','誤：目標とする言語行動であり時間・資源条件ではない','誤：アイデンティティ変化であり時間・資源条件ではない','正：時間・人数・利用可能な設備や機材を示す'],stem_review='環境分析全体を時間・資源に限定せず、今回問う下位範囲を明示。4肢の記述内容を範囲条件に対して独立照合。',explanation_review='全4解説を原著の定義・例と選択肢本文へ照合。ニーズと環境の分類を排他的とせず、アイデンティティを一般的に教育上無関係とはしない。',unresolved='',multiple_correct_risk='なし：時間・資源の具体的条件を示すのは4',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',cs+extra),('changes_batch135.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
f=Path(__file__).resolve().parents[2]/'nation2013.pdf';raw=f.read_bytes();assert len(PdfReader(f,strict=True).pages)==192
(b.OUT/'evidence/batch135_sources.json').write_text(json.dumps(dict(source_id='S197',author='Paul Nation',title='What Should Every ESL Teacher Know?',version_note='著者公式大学サイト公開稿。ファイル名2013-02-13、本文から刊年は確定しない。',url='https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/paul-nations-publications/publications/documents/what-should-every-esl-teacher-know-13-feb-2013-pdf',retrieved='2026-10-17',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),downloaded_pages=192,body_and_image_read='printed/PDF12–14: chapter2 introduction and complete Needs Analysis/Environment Analysis introductory sections',scope='Definitions and examples only; not whole book, cited 2000 article or universal teaching effect approval.',retrieval_note='Web retrieval reported410, but ordinary direct download succeeded with complete 192-page PDF; no protected access used.',full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
print('1 question / 5 edits')
