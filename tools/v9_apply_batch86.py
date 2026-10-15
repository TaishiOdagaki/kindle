"""One-time full review of Q_4_041 and explicitly partial source checks of two others."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1890
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
key='Q_4_041';assert d[key]['status']=='要追加確認' and int(a['A_4_041']['ans'])==1
stem='Krashen（1982）『Principles and Practice in Second Language Acquisition』で述べられた仮説内の主張として、最も適切なものを一つ選びなさい。仮説の内容を問うのであり、その実証的な妥当性を判定する問題ではない。'
opts=[
'習得には現在の能力より少し先の構造を含む言語の理解が必要とし、理解可能なインプットの提供と低い情意フィルターを促す状況を重視する。',
'理解可能なインプットは必要なく、準備ができる前から発話を強制して反復させることだけで、習得が進むとする。',
'意識的に学習した文法規則は、練習を繰り返せばそのまま自動的に習得された知識へ転換するとする。',
'モニターは、時間、正確さへの注意、規則の知識の有無に関係なく、すべての発話に自動的に働くとする。']
exps=[
'印刷21〜22頁のインプット仮説と31〜32頁の情意フィルター仮説に対応します。著者は理解可能なインプットを提供し、不安が低くフィルターを低く保ちやすい状況を作ることを重視しています。ここでは著者の理論上の主張を確認しています。',
'著者は22頁で、発話能力は理解可能なインプットを通して現れ、初期の発話は本人の準備が整ったときに現れると述べています。インプットを不要とし、発話の強制だけを習得の仕組みとする説明は、この主張と逆です。',
'著者は10頁で習得と学習を区別し、83頁で学習が習得へそのまま転換するという考えを否定しています。これはこの著者の理論内での区別であり、すべての知識習得理論に共通する結論として扱いません。',
'著者は15〜16頁で、意識的な知識によるモニターの利用に、時間、形式・正確さへの注意、規則の知識という条件を挙げています。条件がそろえば必ず利用されるという十分条件でもなく、全発話に無条件で働くという説明にはなりません。']
reason='S13著者公開原著の印刷10・15〜16・21〜22・31〜32・83頁を本文・画像照合。KrashenとTerrellの共同著書全体の取得とはせず、1982年著書の仮説内の主張を問う。仮説・現在の実証的妥当性・教授法の効果保証を区別し、モニターの必要条件と十分条件も区別。'
extra=[]
for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_4_041']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S13'],applied=True,before_version='第85バッチ反映後の累積作業稿',block_context='A_4_041' if field=='explanations' else key)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(e)
d[key].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S13'],reason=reason,option_verdicts=['正：インプットと情意面に関する仮説の主張に対応','誤：インプットの役割と発話の出現に関する主張を反転','誤：学習が習得へ転換するという考えは83頁で否定','誤：モニターの条件を排除し十分条件とも混同'],stem_review='特定の著書の仮説内の主張を指定。全4肢を独立判定し1のみが対応。',explanation_review='S13原著209頁PDFを取得し指定8印刷頁の全文と画像を照合。PDF版には2009年インターネット版序文が付くため原刊1982年と区別。引用先原著や現在の理論的合意の確認とはしない。',unresolved='',multiple_correct_risk='なし：指定した著者の仮説に対応するのは1のみ',no_correct_risk='なし：独立正答1')
assert len(extra)==9
# Partial evidence never changes the two questions to approved status.
e=d['Q_4_016'];assert e['status']=='要追加確認'
e.update(sources=sorted(set(e.get('sources',[])+['S13'])),reason='S13印刷31〜32頁で、選択肢1の高不安・高フィルターを最大化すべきという説明は仮説に反すると照合。ラポールと心理的安全性の定義や指導効果まで同資料で承認しない。',option_verdicts=['誤：S13の仮説は低不安・低フィルターを重視','正答候補2だがラポールと心理的安全性の同一視・必要条件は未照合','誤答候補だが仲間関係の因果・範囲を原著照合未了','誤答候補だがフィードバックから上達・信頼への効果は未照合'],explanation_review='全4解説を再読しS13が支える範囲を限定。解説1は仮説の説明として照合。解説2〜4の定義・不可欠性・効果の根拠本文は未取得で承認しない。',unresolved='ラポールの定義と心理的安全性との関係、共感的受容の不可欠性、ピア関係の役割、リキャスト等から上達と教師への信頼への効果を一次資料と照合し、全問を再判定。')
e=d['Q_3_008'];assert e['status']=='修正必要'
e.update(sources=sorted(set(e.get('sources',[])+['S13'])),reason='修正必要を維持。S13印刷10頁は成人も習得可能とする一方、成人全員の母語話者同等到達を保証しない。LADは著者の理論内概念であり実証済みの普遍前提とはしない。L2でL1が既に確立という一般化は幼児L2を含めると範囲不足。',explanation_review='全4解説を再読。S13印刷10頁と31〜32頁の成人の習得・到達保証なし・情意面の理論上の位置づけだけを追加照合。幼児L2、転移、個人差、明示的指導の効果の全主張は未照合。',unresolved='L1/L2比較の対象年齢と条件を明示し、幼児L2や多言語発達を含む範囲、転移と個人差、明示的指導の効果を原著で照合。LADを普遍的確定事実とする記述とL1確立済みの一般化を修正した後に全4肢・4解説を再判定。')
for name,obj in [('changes.json',c+extra),('changes_batch86.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('1 full review / 9 edits; 2 partial source checks remain unapproved')
