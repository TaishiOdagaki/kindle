"""One-time evidence-bounded listening and academic-writing revisions."""
import json, html, hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text()); assert len(cs)==2856
d=json.loads((b.OUT/'decisions.json').read_text()); _,q,a=qa.audit(str(b.DST))
items={
'Q_MO_003':dict(key=2,sources=['S99'],
 stem='このケースの画像提示を、メニューの文字を読ませるためではなく、料理の写真から注文場面の知識を思い出し、会話内容を予測させるために行う場合、その働きとして最も適切なものを一つ選べ。',
 opts=['音声を一音ずつ識別する処理だけを練習させる。','場面についての背景知識を使い、聞く内容を予測するトップダウン処理を促す。','著作権法上の要件を満たすことだけを目的とする。','聞こえた文の文法構造を分析する処理だけを練習させる。'],
 exps=['設問で明示した目的は、場面の知識を利用した内容の予測です。音声を細かく識別する練習だけを指すものではありません。','料理の写真から注文場面の知識を活性化し、聞く内容を予測するという条件は、背景知識を利用するトップダウン処理に当たります。','設問で明示した目的は、場面の知識を使った聴解の支援です。ここでは教材利用の著作権法上の適法性を判定していません。','設問は文法構造の分析だけではなく、場面の背景知識を使った予測を明示しています。実際の聴解ではトップダウン処理と音声の解読が併用されます。'],
 reason='S99の署名付き教育記事本文を再取得し、背景知識・場面・写真による予測と音声信号の解読、両処理の併用を照合。文字メニューの提示だけでトップダウン処理と断定する不備を解消。共通ケースは変更せず、当該設問で写真から場面知識を活性化する使用条件を限定した。著作権の適法性は判定しない。',
 verdicts=['誤：場面知識による予測を音声識別だけに限定','正：明示された背景知識による予測に一致','誤：明示された聴解支援の目的と異なる','誤：背景知識による予測を文法分析だけに限定']),
'Q_4_087':dict(key=4,sources=['S199'],
 stem='大学の授業で、問いに対する自分の主張を論証するレポートを書く留学生への指導として、最も適切なものを一つ選べ。',
 opts=['論証の順序や文章全体の構成を考えず、思い付いたことを並べればよいと教える。','他者の文章や意見を自分の主張に組み込めば、出典を示さずに自分の言葉として扱ってよいと教える。','自分の意見であることを示せば、それを裏付ける文献やデータなどの根拠は不要だと教える。','問いと主張の対応を確かめ、根拠を示して論証し、他者の意見を用いた部分は出典を示して自分の主張と区別するよう指導する。'],
 exps=['主張を読み手に伝えるには、論証の順序や構成を整理する必要があります。構成を考えずに列挙すればよいという指導は適切ではありません。','他者の意見や発見を自分のもののように示してはいけません。用いた部分を自分の主張と区別し、出典を示します。','論証するレポートでは、自分の意見にも根拠が必要です。意見であると明示するだけでは、その主張を裏付けたことにはなりません。','問いに対応する主張と、それを支える根拠を示します。他者の意見を用いた部分と出典を明確にすることは、読み手が主張を検討するためにも必要です。'],
 reason='早稲田大学ライティング・センター教員スタッフ監修の公開記事の定義・注意点・六つのポイント・引用の作法を本文で取得。主張の根拠、構成、問いと答え、他者の言と自分の言の区別へ全4肢・全4解説を照合。学習領域を維持し、未照合の「丁寧体や主観表現は一律不可」という一般化を撤回して、論証型レポートの根拠と引用を問う。書籍の参考文献欄だけでは原著を取得済みにしない。',
 verdicts=['誤：構成と思考の整理を不要とする','誤：他者の意見の出典と区別を不要とする','誤：自分の主張への根拠を不要とする','正：問いと主張、根拠、他者の言との区別を満たす'])}
extra=[]
for k,v in items.items():
 ak='A_'+k[2:]; assert d[k]['status']=='修正必要' and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=v['sources'],applied=True,before_version='第136バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=v['sources'],reason=v['reason'],option_verdicts=v['verdicts'],stem_review='改訂条件を明示して設問・全4肢を独立照合。共通ケースや他問は変更しない。',explanation_review='全4解説を取得本文に照合。未取得原著や法的判断、一般化した文体規範は承認しない。',unresolved='',multiple_correct_risk='なし：明示条件下で正答は一つ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==18
for name,obj in [('changes.json',cs+extra),('changes_batch137.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
sources=[]
for sid,file,url,scope in [('S99','morley137.html','https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/listening-top-down-and-bottom','Catherine Morley article complete body including activities and conclusion; references not acquired.'),('S199','waseda137.html','https://www.waseda.jp/inst/weekly/feature/2014/06/23/20860/','2014-06-23 Writing Center supervised article: definition, report precautions, six points, citation guidance; not cited book or current center service policy.')]:
 raw=(Path(__file__).resolve().parents[2]/file).read_bytes();assert len(raw)>50000
 sources.append(dict(source_id=sid,url=url,retrieved='2026-10-17',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch137_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 18 edits')
