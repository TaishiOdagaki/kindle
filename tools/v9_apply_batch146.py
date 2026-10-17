"""One-time methodology selection revision against author conclusion."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2972
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_M_028';ak='A_M_028';assert d[k]['status']=='要追加確認' and a[ak]['ans']=='1'
stem='Larsen-Freeman（1987）の教授法の選択に関する結論に沿う考え方として、最も適切なものを一つ選べ。'
opts=['目標や学習者、授業の状況を踏まえて方法を選び、その選択が目的に合っていたかを確かめる。','複数の方法を使うなら、選択の理由を考えず、無作為に組み合わせればよい。','一つの教授法は、教師・学習者・状況にかかわらず常に最も優れていると考える。','方法を自由に選べるなら、教師はその選択による結果を評価する必要がない。']
exps=['著者は、知見に基づいて状況に応じた選択を行い、その選択が目的に合うかを確かめることを重視しています。複数の方法を無条件に混ぜればよいという意味ではありません。','著者が述べる選択は、達成したい目的に導かれたものです。無作為に方法を組み合わせることとは異なります。','著者は、あらゆる教師・学習者・状況に対する一つの方法の優越性を実証できているという立場を取りません。これは1987年の論考の結論についての問題であり、現在までの全研究を網羅した結論ではありません。','著者は、教師が自分の選択の結果を評価する役割を重視しています。選択の自由を、結果を確かめなくてよいことと結び付ける説明は不適切です。']
reason='S209 Diane Larsen-Freeman（1987）From Unity to Diversityの2012年再掲全11頁PDFを米国国務省公式サイトから取得し、印刷36–37頁のConclusion全体を精読、同頁画像で照合。未確認の折衷的アプローチという用語定義問題から、同じ教授法の選択・組合せという学習領域を保ち、取得した著者結論への理解を問う問題へ改訂。原著者の立場に限定し、万能教授法の否定を2026年現在の全研究の実証結果として一般化しない。用語自体を確認済みにしたものではない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S209'],applied=True,before_version='第145バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S209'],reason=reason,option_verdicts=['正：目的・学習者・状況に基づく選択と目的との適合の点検に一致','誤：著者は選択を無作為としない','誤：すべての条件での一方法の優越性という著者の採らない立場','誤：選択結果を評価する教師の役割を否定'],stem_review='1987年論考の結論に対象を限定。折衷法という未確認の用語そのものを承認せず、教授法選択の学習領域を維持。',explanation_review='Conclusion全体の目的に基づく選択、非無作為性、全条件での優越性への留保、教師による結果評価に全4解説を照合。2026年の最新研究総括とは区別。',unresolved='',multiple_correct_risk='なし：結論に一致するのは1のみ',no_correct_risk='なし：独立正答1')
for n,obj in [('changes.json',cs+extra),('changes_batch146.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'larsen145.pdf').read_bytes()
e=dict(source_id='S209',title='From Unity to Diversity: Twenty-five Years of Language-Teaching Methodology',author='Diane Larsen-Freeman',original_year=1987,reprint='English Teaching Forum 50(2), 2012, 28–38; first published 25(4), 1987',url='https://americanenglish.state.gov/files/ae/resource_files/50_2_6_larsen-freeman-pp28-38_0.pdf',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=11,read_scope='印刷36–38頁本文・文献を精読。36–37頁のConclusion全体を画像でも照合。全11頁の精読ではない。',limitations='著者自身の教授法選択の立場を問う。折衷法という用語定義の確認ではなく、2026年現在の教授法効果研究の総括でもない。初回37頁画像は不正な画像データのため読了画像から除外し、単頁再描画版で照合。',full_source_redistributed=False)
(b.OUT/'evidence/batch146_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
