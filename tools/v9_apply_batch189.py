"""One-time revision against Canale and Swain original pages 29-31."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3849
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_2_018',1,'Canale・Swain（1980）のストラテジー能力の説明として適切なものを一つ選べ。',
['遂行上の要因や不十分な能力による伝達の破綻を補う、言語的・非言語的な方略に関わる。','語彙や文法の知識は含まれず不要になるので、文法能力を別に考える必要はない。','補償に用いるのは言語的な方略だけであり、非言語的な方略は含まない。','同論文の三要素には含まれず、コミュニケーション能力を文法能力だけとする。'],
['30頁の定義に合います。不十分な能力だけでなく遂行上の要因による破綻も対象とし、言語的・非言語的手段を含めます。','29頁は語彙や文法等の知識を文法能力に含めています。方略による補償を、その知識が不要になることと取り違えています。','30頁は言語的な方略に加え非言語的な方略を明示しています。言語だけに限る説明は合いません。','29～31頁には文法能力・社会言語学的能力・ストラテジー能力が示されています。文法だけとする説明は合いません。'],
['正：遂行・能力不足による破綻を言語・非言語で補償','誤：補償を文法知識の不要化とする','誤：非言語的方略を排除','誤：1980年モデルの構成を文法だけに縮減']),
('Q_3_007',3,'Canale・Swain（1980）30頁の談話規則の説明に照らし、結束性と一貫性の扱いとして適切なものを一つ選べ。',
['同論文では、結束性を、発話群のコミュニケーション機能を適切に組み合わせることとだけ説明する。','同論文では、一貫性を文法的な結び付きという意味に限り、コミュニケーション機能の組合せと結び付けない。','同論文は、談話規則を考える際に、文法的な結び付きとコミュニケーション機能の適切な組合せを区別する。','同論文の談話規則の焦点は単一の発話の文法的な形だけで、複数発話の組合せにはない。'],
['30頁では文法的な結び付きを結束性としています。この肢は、一貫性の側で示す機能の組合せと取り違えています。','30頁は一貫性をコミュニケーション機能の適切な組合せに結び付けています。文法的な結び付きだけにする点が合いません。','30頁で示す結束性と一貫性の区別に合います。ここでは同論文の説明を問い、後続研究のあらゆる定義と同一視しません。','30頁は、談話規則の焦点を単一発話の文法的な適格さではなく、発話とコミュニケーション機能の組合せに置いています。'],
['誤：結束性と一貫性を取り違え','誤：一貫性を文法的結合だけに限定','正：同論文の二側面の区別','誤：談話規則を単一発話の文法だけに限定'])]
reasons={
'Q_2_018':'S260 Canale・Swain1980原論文の第三者公開スキャン印刷1・29～31頁を原画像取得・直接精読。三要素、文法能力の知識、遂行要因または不十分な能力による破綻を言語的・非言語的方略で補う定義を全肢全解説へ照合。旧稿の一般的な円滑化・推進までを1980定義に含める拡張、教師介入が発達を阻害するという未実証の因果、1983年の談話能力追加史の未取得原著主張を撤回。全47頁や1983原著の取得ではない。',
'Q_3_007':'S260原論文30頁の談話規則における結束性・一貫性の説明を全肢全解説へ照合。同論文の説明に範囲を限定。旧稿の結束性皆無という断定やノックと入浴の架空対話の推論を撤回。Halliday・Hasan1976等の引用原著全文や一貫性の全流派を検証したとはしない。'}
extra=[]
for k,key,stem,opts,exps,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reasons[k],sources=['S260'],applied=True,before_version='第188バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S260'],reason=reasons[k],option_verdicts=verdicts,candidate_answers=[],stem_review='1980原論文の定義・説明に限定。',explanation_review='印刷29～31頁の原画像本文・留保を全肢全解説へ照合。未取得の1983原著・引用先原著や教育効果の因果を承認しない。',unresolved='',multiple_correct_risk=f'なし：{key}のみ当該本文と整合',no_correct_risk=f'なし：{key}の根拠本文取得')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch189.json',extra),('decisions.json',d)]: (p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
