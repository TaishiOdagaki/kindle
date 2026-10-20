"""One-time audit of Hofstede with original-author article body."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3804
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_M_039';ak='A_M_039';assert d[k]['status']=='要追加確認' and a[ak]['ans']=='4'
stem='Hofstede（2011）の国・社会レベルの文化次元で、人々が集団にどのように統合されているかに関わるものを一つ選べ。個人の性格診断としては扱わない。'
opts=['不確実性の回避の次元','権力格差の次元','長期志向・短期志向の次元','個人主義・集団主義の次元']
exps=['論文8頁では、不確実性の回避を未知の将来に直面した社会のストレスの程度に関わる次元として挙げています。設問の集団への統合に対応する次元ではありません。','論文8頁では、権力格差を人間の不平等という基本的な問題への異なる対応に関わる次元として挙げています。設問の集団への統合とは区別されます。','論文8頁では、長期志向・短期志向を努力の焦点を将来に置くか、現在や過去に置くかに関わる次元として挙げています。設問の集団への統合を表す名称ではありません。','論文8頁の次元一覧と11頁の定義に対応します。11頁は個人の特性ではなく社会の特性として、人々が集団に統合される程度を述べています。8頁も国の文化得点を個人の固定観念に用いないよう明記しています。']
reason='S255 Hofstede本人の2011年論文PDF26頁を取得。本文6・8・11頁を画像精読。社会レベルと個人レベルの区別、次元一覧、個人主義・集団主義の定義を全肢全解説へ照合。旧稿の音韻論・下位分野・文法カテゴリーの未取得原典を承認せず、同じ文化次元の比較に差替え。国の得点から個人を類型化しない条件を明示。現在の国別得点や表3の言語・教育一般化は承認範囲外。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==3 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
  extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S255'],applied=True,before_version='第186バッチ後',block_context=ak if field=='explanations' else k,**kw))
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S255'],reason=reason,option_verdicts=['誤：未知の将来へのストレス','誤：不平等への対応','誤：努力の時間的焦点','正：社会における集団への統合'],candidate_answers=[],stem_review='社会レベルの定義と原著者2011年論文に限定。',explanation_review='本文6・8・11頁を全肢全解説へ照合。表3の補助一般化は採用しない。',unresolved='',multiple_correct_risk='なし：4のみ集団への統合に対応',no_correct_risk='なし：4の定義を本文で確認')
assert len(extra)==9
for n,obj in [('changes.json',cs+extra),('changes_batch187.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
