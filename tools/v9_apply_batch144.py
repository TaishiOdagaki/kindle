"""One-time teaching-method principles revision against acquired trainer text."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2954
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_4_031';ak='A_4_031';assert d[k]['status']=='修正必要' and a[ak]['ans']=='2'
stem='教授法と、その理念・指導上の特徴の組み合わせとして、最も適切なものを一つ選べ。'
opts=['TPR（全身反応教授法）― 聞いて理解することより、学習開始時から発話させることを優先し、身体動作を用いない。','オーディオリンガル・メソッド ― 言語学習を習慣形成として捉え、モデルの反復や文型練習、正の強化を重視する。','コミュニカティブ・アプローチ ― 文法形式の正確さだけを目標とし、場面に応じた言語使用や意味のやり取りを扱わない。','サイレントウェイ ― 教師のモデルをそのまま反復させることを中心とし、学習者自身による誤りの修正を避ける。']
exps=['TPRでは、まず聞いて理解することを重視し、教師の指示に身体動作で応じる活動を用います。学習者が話す準備のできる前から、発話を最優先にする説明とは異なります。','言語学習を習慣形成と捉える考え方に対応します。教師のモデルの反復、文型の置換練習や問答練習、正しい応答への肯定的な反応などが用いられます。これは教授法の理念・指導例の説明であり、学習効果を無条件に保証するものではありません。','コミュニカティブ・アプローチは、言語を使って伝え合うことを重視します。文法形式だけでなく、場面・話題・相手に応じた適切さや意味のやり取りも扱います。文法を不要とする意味でもありません。','サイレントウェイでは、学習者が自分の発話を確かめ、誤りを修正していくことが重視されます。教師のモデルをそのまま反復させることを中心とする説明とは異なります。']
reason='Diane Larsen-Freeman（1990）Language Teaching Methodsの教師用ハンドブック全65頁を米国国務省公式サイトから取得。導入1頁と、ALM2頁、TPR18–19頁、Silent Way32–33頁、Communicative Approach41–42頁の解説本文全体を精読。各方法の開始頁は画像でも確認。元の教授法の理念・理論的観点という学習領域を保ち、未取得の原著にまたがる広範な発展史・影響関係を、取得本文で直接比較できる理念と指導上の特徴へ改訂。Hymesの提唱を社会言語学的能力だけと同一視する帰属を撤回。Skinner・Bloomfield・Hymes・CLIL・直接法の未取得原著を取得済みとはせず、新稿にその補助主張を残さない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S208'],applied=True,before_version='第143バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S208'],reason=reason,option_verdicts=['誤：TPRの理解先行・身体反応を逆転','正：ALMの習慣形成・反復・文型練習・正の強化に一致','誤：CAの場面に適切な使用・意味のやり取りを否定','誤：Silent Wayの自己修正とモデル反復の位置付けを逆転'],stem_review='教授法の理念と指導上の特徴を問う対象へ明確化し、4肢をそれぞれの解説本文に独立照合。',explanation_review='全4解説をALM2頁、TPR18–19頁、Silent Way32–33頁、CA41–42頁に照合。方法の理念と効果の無条件な実証を区別し、CAでの文法不要という別の過剰一般化も避ける。',unresolved='',multiple_correct_risk='なし：取得本文の特徴と一致するのは2のみ',no_correct_risk='なし：独立正答2')
for n,obj in [('changes.json',cs+extra),('changes_batch144.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'teaching144.pdf').read_bytes()
e=dict(source_id='S208',title='Language Teaching Methods: Teacher’s Handbook for the Video Series',author='Diane Larsen-Freeman',year=1990,url='https://americanenglish.state.gov/files/ae/resource_files/language_teaching_methods_teachers_handbook.pdf',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=65,read_scope='表紙、導入印刷1頁、ALM2頁、TPR18–19頁、Silent Way32–33頁、Communicative Approach41–42頁の解説本文を精読。4方法の開始頁（PDF7・23・37・46頁）は画像でも照合。全65頁精読や授業動画自体の視聴ではない。',limitations='教授法の理念・指導例の説明に限定し、普遍的効果の実証とは扱わない。引用元の1986年書籍や各方法の創始者原著全冊の取得ではない。',full_source_redistributed=False)
(b.OUT/'evidence/batch144_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
