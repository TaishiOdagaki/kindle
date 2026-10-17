"""One-time mother-tongue support audit from Cummins's signed 2001 article."""
import json,html,hashlib
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2833
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_093';ak='A_4_093'
assert d[k]['status']=='修正必要' and a[ak]['ans']=='1'
stem='Cummins（2001）の母語保持に関する記事の説明を踏まえた、二言語で学ぶ子どもへの支援方針として適切なものを一つ選べ。'
opts=['二言語を使い学ぶ機会を用意し、母語で育った概念や読み書きの力を、学校の言語での学習にも関連付ける。','二言語の概念や知識には関係がないため、母語で既に理解した概念も、学校の言語では初めから学び直させる。','学校に適応すれば母語は自然に維持されるため、家庭や地域で母語を使う機会を用意する必要はないとする。','学校の言語の学習と母語の保持は両立しないため、家庭でも母語を使うことを禁止する。']
exps=['記事は、概念や読み書きの力の言語間の関連と、二言語に接する教育環境の重要性を述べています。この方針はその説明に沿います。','記事は言語間の概念や知識の関連を認めています。母語で理解した概念を、別の言語では初めから学び直すとする方針とは異なります。','記事は母語の減退の程度や速さが環境によって異なると述べ、家庭や地域で使う機会を増やすことを勧めています。学校への適応だけで維持を保証しません。','記事は二言語を使える環境を重視しています。母語の保持と学校の言語の学習を両立しないものと決め付け、家庭の母語使用を禁止する方針とは逆です。']
reason='Jim Cummins署名のSprogforum19（2001）15–20頁の原記事全6頁を取得・通読、17–19頁の母語発達、概念・読み書きの言語間関連、両言語へのアクセス条件と母語減退の環境差を照合。原著者の説明を踏まえた支援方針に限定。無条件の能力向上・全児童の急速喪失、セミリンガルという欠損的診断、家庭言語禁止による重大な情緒影響の一律断定は撤回する。引用先研究を個別取得した実証評価ではなく、2001年記事の提案への適合を判定。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S196'],applied=True,before_version='第133バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S196'],reason=reason,option_verdicts=['正：言語間の関連と両言語へのアクセスを生かす','誤：概念・知識の言語間関連を否定','誤：環境条件と母語使用機会を不要として維持を保証','誤：両言語へのアクセスを重視する説明と反対'],stem_review='著者と年を特定し母語保持に関する説明に沿う支援方針を問う。日本の全児童の習得効果を一律に保証する問いではない。',explanation_review='全4解説を記事17–19頁へ照合。欠損的診断・無条件の喪失や情緒影響・学習効果の断定を残さない。',unresolved='',multiple_correct_risk='なし：著者の説明に沿う1のみ',no_correct_risk='なし：独立正答1')
for name,obj in [('changes.json',cs+extra),('changes_batch134.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
f=Path(__file__).resolve().parents[2]/'cummins2001.pdf';raw=f.read_bytes();pdf=PdfReader(f,strict=True);assert len(pdf.pages)==6
(b.OUT/'evidence/batch134_sources.json').write_text(json.dumps(dict(source_id='S196',title="Bilingual Children's Mother Tongue: Why is it important for education?",author='Jim Cummins',publication='Sprogforum 19, 2001, pp.15–20',url='https://lavplu.eu/central/bibliografie/cummins_eng.pdf',hosting_note='原記事誌面の公開ミラー。著者署名・誌名・巻号年頁を原PDFで照合。',retrieved='2026-10-17',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),body_read='all 6 pages',used_scope='printed17–19 / PDF3–5, mother tongue development, transfer, access to both languages, variation in attrition and use opportunities',images_read=[4,5],not_approved='Referenced studies and books, all empirical effect estimates, universal attrition times, rights/law claims and current Japanese policy not independently verified.',full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
