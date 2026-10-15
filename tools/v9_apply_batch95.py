"""One-time S144 additional review; never replay over later decisions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2130
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_M_025':(3,'Richards（2006）28・30頁の内容中心教授法（CBI）の説明に対応するものを一つ選べ。',[
'文法項目の順序を先に確定し、内容はその練習場面として後から選ぶことを、CBIの特徴としている。',
'CBIは必ず全カリキュラムに適用し、一つの単元だけに用いることはできないとしている。',
'扱う内容を出発点に言語面を組み立てる。一方、内容に焦点を当てるだけで言語の正確さも十分育つかは、実施上の論点になる。',
'CBIでは内容知識と言語使用のどちらを評価するかを検討する必要はないとしている。'],[
'28頁では、文法などを先に決めてから内容を選ぶ編成と、内容を出発点にするCBIを対比しています。この肢は対応を逆にしています。',
'28頁はCBIを一つの単元の枠組みにも使えると説明しています。全カリキュラムへの適用だけに限定していません。',
'内容から編成する説明は28頁、言語の正確さの発達に関する論点は30頁に対応します。CBIという名称だけで学習成果を保証しません。',
'30頁は、内容知識・言語使用・その両方のどれを評価するかを実施上の論点に挙げています。評価の検討を不要とはしていません。'],[
'誤：内容と言語項目の編成上の優先関係が逆','誤：単元での利用を否定','正：内容からの編成と正確さに関する留保','誤：評価上の論点を否定']),
'Q_M_040':(4,'ある言語授業で、班ごとに課題完成に必要な情報の一部だけを渡す。学習者は他の班と情報を伝え合い、断片を組み合わせて全体を完成させる。Richards（2006）19頁で、この構成を特徴として説明する活動名を一つ選べ。',[
'意見共有活動（opinion-sharing activities）',
'情報変換活動（information-transfer activities）',
'推論差活動（reasoning-gap activities）',
'ジグソー活動（jigsaw activities）'],[
'同頁の意見共有活動は、価値観・意見・信念を比較する活動です。本問が焦点を当てる、分有した情報の断片から全体を完成する構成とは異なります。',
'同頁の情報変換活動は、ある形式の情報を別の形式に表し直す活動です。本問は表現形式の変換を課題としていません。',
'同頁の推論差活動は、与えられた情報から推論などによって新しい情報を導く活動です。本問で明示した、情報断片の分有と統合という構成の名称ではありません。',
'同頁のジグソー活動の説明に対応します。各班が情報の一部を持ち、伝え合って全体を完成させます。単に役割を分けることだけではなく、情報を組み合わせる必要を明示しています。'],[
'誤：意見や価値観の比較とは異なる','誤：情報の表現形式の変換ではない','誤：明示された構成は推論による新情報の導出ではない','正：分有する情報断片を伝え合い全体を完成'])}
reason='S144著者公開52頁PDFを再取得し、印刷19・28・30頁を本文と版面で照合。CBIとCLILの同一視、未照合の他教授法の定義を残さず、内容からの編成と実施上の留保、著者自身の活動分類へ改訂。ジグソーはRichardsの言語授業活動の定義に限定し、Aronson原案全手順の取得確認とはしない。'
extra=[]
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S144'],applied=True,before_version='第94バッチ反映後の累積稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S144'],reason=reason,option_verdicts=verdicts,stem_review='著者本人の2006年の説明・分類を指定して全4肢を独立比較。Q_M_040は監査で構成した模式授業案で、原著の実験報告ではない。',explanation_review='全4解説を印刷19・28・30頁の本文・画像と照合。CBIとCLILの完全同義性、Aronsonの原案全手順、各方法の普遍的効果は承認対象から除いた。活動に複数の側面がありうることと、設問が明示した構成を区別する。',unresolved='',multiple_correct_risk='なし：指定資料で明示した構成・記述に対応する肢を一つ選ぶ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==18
for name,obj in [('changes.json',c+extra),('changes_batch95.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('2 full reviews /18 edits')
