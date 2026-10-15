"""Restore the unpushed safety-case review against the verified batch105 HEAD."""
import json,html,gzip
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2375
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={}
def add(n,key,ss,exps,stem=None,opts=None,verdicts=None):
 k=f'Q_MO_{n:03d}';items[k]=(key,ss,stem or q[k]['stem'],opts or q[k]['opts'],exps,verdicts)
add(6,1,['S164','S165'],[
'本ケースは、職場の指示・注意喚起とその理解を扱います。厚労省通知1ニも、災害防止の指示等を理解するために必要な日本語や基本的な合図の習得を挙げており、肢1の実践的なニーズと対応します。日本語指導だけで安全が保証されるという意味ではありません。',
'ケースの主目的は職場の指示等の理解で、文学作品の読解を目標とした指導とは示されていません。文学を扱う教育自体を否定する判定ではありません。',
'ケースには、書道や茶道などの伝統文化の知識を教える目標は示されていません。職場での指示理解という学習目標と一致しません。',
'主目的は職場で必要な指示等の理解であり、大学進学に向けたレポート作成とは異なります。就労者が別に進学のニーズも持ち得ることは否定しません。'],verdicts=['正：ケースの職場での指示理解と対応','誤：主目的は文学読解ではない','誤：伝統文化知識が主目的とは示されない','誤：主目的は大学のレポート作成ではない'])
opts=q['Q_MO_007']['opts'].copy();opts[1]='視覚教材を使えば、学習者が内容を理解したかを確認する必要は一切なくなる。'
add(7,3,['S164','S165','S26'],[
'著作権法第2条第1項第1号の定義に合う創作的な写真・イラストは、第10条第1項の例示にも含まれ得ます。写真・イラストという種類だけで対象外とはいえず、利用条件の確認も必要です。',
'通知1ハは、視聴覚教材等の活用と、理解度を確認しながら教育を繰り返すことを併せて示します。視覚教材の使用だけで理解確認を不要とする肢は対応しません。',
'通知1ロ・ハは、内容に適した視聴覚教材の整備・活用を挙げます。本ケースの写真やイラストは、言葉が指す物や状況を捉え、理解を支えるための工夫と位置付けられます。使用すれば必ず理解できるという効果保証ではありません。',
'通知1ニは、災害防止の指示等を理解するための日本語や合図の習得を挙げています。視覚教材による支援と、その学習が不要になるという主張は別です。'],opts=opts,verdicts=['誤：種類だけで著作権対象外にできない','誤：視覚支援でも理解確認は省略しない','正：物・状況と言葉の対応理解を支える意図','誤：必要な日本語学習が不要になるわけではない'])
opts=q['Q_MO_008']['opts'].copy();opts[2]='職場での指示理解とは関係なく、文学作品の文体を鑑賞することだけを目的とする日本語教育。';opts[3]='大学での論文執筆だけを目的として行う日本語指導。'
add(8,1,['S163','S164'],[
'コアカリキュラム〈31〉は、求められるプログラムの目的・目標を踏まえた目的・対象別日本語教育を扱います。本ケースは就労者と職場の指示理解という対象・目的に応じた例です。「〜よし」という形式だけでなく、学習目標に照らして分類します。',
'通知1ニにも、労働災害防止に必要な日本語や合図の習得が挙げられています。ケースでの職場の利用を、就労とは無関係として生活場面だけに限定する肢は誤りです。',
'このケースの指導目標は職場での指示・注意喚起の理解であり、文学作品の文体鑑賞だけを目標とするものではありません。',
'大学での論文執筆は、このケースの指導目標として示されていません。職場での指示等を理解する目的と一致しません。'],opts=opts,verdicts=['正：就労者と職場の指示理解という対象・目的に対応','誤：就労との関係を否定','誤：文学鑑賞だけという目標はケースと異なる','誤：大学論文だけという目標はケースと異なる'])
add(9,2,['S163','S164','S165'],[
'母語等を用いて理解を助けたり確かめたりすること自体は適切に行えます。本肢の問題は、目標とした日本語の指示理解を確認せず、無関係な雑談だけで理解済みとする点です。',
'コアカリキュラムの授業の目的・目標と評価、通知1ハの理解度確認に照らし、対象の指示等への応答を見るという方法を本ケースに構成できます。危険を伴う実作業ではなく安全な模擬場面で行い、この確認だけで職場全体の安全や法定教育の修了を認定しません。',
'通知1ハは、教育の実施だけでなく、理解度を確認しながら継続することを示します。授業を行った事実と、目標の内容を理解したことは同一ではありません。',
'無関係な文法問題の点数だけでは、対象の指示・注意喚起を理解したかを確認していません。文法問題や筆記確認を補助として使うこと自体を禁止する説明ではありません。'],stem='この授業で扱った日本語の指示・注意喚起の理解を、安全な模擬場面で確認する方法として、適切なものを一つ選べ。',opts=[
'対象の日本語の指示を理解できるかは確認せず、母語での雑談だけで理解済みとする。',
'安全な教室内の模擬場面で、対象の指示や合図を理解し、適切に応じられるかを確認する。',
'授業を実施したという事実だけで、学習者が内容を理解したと判定する。',
'対象の指示や注意喚起への応答を確認せず、無関係な文法問題の点数だけで理解済みとする。'],verdicts=['誤：母語自体ではなく、目標と無関係な雑談だけを根拠とする点が誤り','正：目標の理解を安全な模擬場面で確認','誤：授業実施と理解確認を同一視','誤：無関係な点数だけでは目標の理解を確認できない'])
opts=q['Q_MO_010']['opts'].copy();opts[0]='母語や日本語の理解度を把握し、母語等・視聴覚教材を活用して、内容の理解を確かめながら繰り返し扱う。'
add(10,1,['S164','S165'],[
'通知1の本文・ロ・ハは、理解できる方法の選択、日本語の理解度の把握、視聴覚教材等の活用、理解確認と継続的な教育を示します。母語等の使用も含め、学習者と内容に応じて工夫します。',
'通知1ニは、災害防止の指示等の理解に必要な日本語や合図の習得を挙げます。その学習を一律に対象外とする肢は誤りです。ただし、日本語教師の指導だけで事業者の安全衛生教育等を代替するものではありません。',
'通知は学習者が理解できる方法を選び、日本語の理解度を把握して教育することを求めます。理解度にかかわらず複雑な口頭説明を一度だけすればよいという肢は、この方針と合いません。',
'通知1ハは、理解度を確認しながら継続的に教育を繰り返すことを示します。理解の確認を不要とする肢は、その方向に反します。'],opts=opts,verdicts=['正：理解度・理解できる方法・反復を併せて確認','誤：安全上必要な日本語学習まで除外','誤：理解度に応じた方法を選ばない','誤：理解度を確認しない'])
extra=[]
for k,(ans,ss,stem,opts,exps,vs) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 reason='未保存稿の消失後、最新保存済み第105バッチから復旧。厚労省通知1本文・イ～ニと推進要綱4(4)・5(5)を再取得・照合し、ケースの指導意図と実証的効果保証、母語利用と目標理解を確認しない方法、事業者の教育・設備対策と日本語学習支援を区別。分類・評価はS163、著作物性はS26の各該当本文も照合。'
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old);new=html.unescape(new)
   if old==new:continue
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=ss,applied=True,before_version='第105バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=html.unescape(stem)
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=ss,reason=reason,option_verdicts=vs,stem_review='設問・全4肢と対応ケースを取得本文と独立比較。変更しない肢も照合し、語形式だけで分類しない。',explanation_review='全4解説を本文照合。通知の理解支援・理解確認と目的に対応する評価をケースへ適用した判断であり、事故防止・法定教育修了・指導効果の保証ではない。',unresolved='',multiple_correct_risk='なし：ケースの対象・目標に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
old='指導の際には、実際の作業服や器具の写真を使い、危険な場面のイラストを見せながら、何をすべきかを日本語で確認させる活動を行った。'
new='この授業では、作業服・器具の写真と危険場面のイラストを示し、何をすべきかを日本語で確認する活動を行った。本ケースは事業場の安全衛生担当者と連携した日本語学習支援であり、法定の安全衛生教育や設備対策を代替するものではない。練習は危険を伴わない安全な模擬場面で行う。'
assert sum(html.unescape(x['t'])==old for x in qa.load(str(b.DST))[0])==1
extra.append(dict(id='CASE_MO_02',field='case_text',index=None,before=old,after=new,reason='日本語学習支援が法定教育・設備対策の代替ではないという架空ケースの前提を追記し、安全な模擬場面で練習する。',sources=['S164','S165'],applied=True,before_version='第105バッチ反映後の保存済み稿',count=1))
assert len(extra)==30
for name,obj in [('changes.json',c+extra),('changes_batch106.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
for n in [164,165]:
 raw=Path(f'/workspace/scratch/697c245d9771/S{n}_restore.html').read_bytes();assert '</html>' in raw.decode().lower() and '理解度' in raw.decode()
 f=b.OUT/f'evidence/S{n}_safety_education_notice.html.gz';f.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(f.read_bytes())==raw
print('5 full reviews/29 question fields/1 case premise restored')
