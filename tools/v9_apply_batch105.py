"""One-time core-curriculum information-resource and licensing case audit."""
import json,html,gzip,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2348
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_O_050':(4,['S163'],'このケースの著作物の利用条件の確認を、令和6年4月1日決定の「登録日本語教員実践研修・養成課程コアカリキュラム」の観点から捉える。適切な説明を一つ選べ。',[
'情報資源の扱い方は事務担当者だけが学ぶ内容で、教師の養成で取り扱う必要はない。',
'著作権を学ぶことは日本語教育の実践と無関係であり、必須の教育内容に含まれない。',
'同資料の「著作権」の到達目標では、日本語教育活動で情報資源の扱い方を理解する必要はないとされる。',
'著作権は必須の教育内容に含まれ、日本語教育活動に必要な情報資源の扱い方の理解が到達目標とされる。'],[
'養成課程の一般目標⑫と必須の教育内容〈36〉は、教師の養成で情報資源の扱い方を理解することを求めています。事務担当者だけの学習内容とする肢は、この位置付けと異なります。',
'同資料は必須の教育内容〈36〉として著作権を挙げています。日本語教育活動に必要な情報資源の扱い方を学ぶ内容であり、教育実践と無関係として除外する肢は誤りです。',
'〈36〉の到達目標は、日本語教育活動を行う上で必要となる情報資源の扱い方について理解することです。理解が不要という肢は、目標の方向を逆にしています。',
'同資料の印刷13頁にある必須の教育内容〈36〉と到達目標に対応します。ケースの利用条件の確認は、この理解を授業準備に結び付ける取組として位置付けられます。ただし、確認しただけで個々の利用が必ず適法になるという意味ではありません。'],[
'誤：教師養成の一般目標⑫・必須内容〈36〉と異なる',
'誤：必須内容〈36〉に著作権が含まれる',
'誤：〈36〉の情報資源の扱い方の理解を不要と逆転',
'正：必須内容〈36〉とその到達目標に対応']),
'Q_MO_014':(2,['S163'],'このケースの配信前の事前確認を、日本語教師の資質・能力の観点からどう位置付けるか。担当者への確認だけで利用の法的適正が保証されるとはせず、適切な説明を一つ選べ。',[
'著作物の利用条件を調べることは、情報資源を扱う教師の学習や授業準備とは全く関係しない。',
'情報資源の扱い方を理解し、その知識を授業準備に生かすための取組として位置付けられる。',
'事務担当者に尋ねれば、教師自身が教材の利用条件を理解する必要はなくなる。',
'一度事前確認をすれば、その後に素材や配信方法が変わっても、利用条件を検討する必要はなくなる。'],[
'コアカリキュラムの一般目標⑫と〈36〉は情報資源の扱い方の理解を求め、表1の技能は学んだ知識の実践への活用を挙げています。条件を調べる行動を授業準備と無関係とする説明は対応しません。',
'表1の教育実践のための技能（3）は知識の現場での活用・具現化を挙げ、〈36〉は情報資源の扱い方の理解を求めます。これらに照らしたケースへの適用判断です。事前確認の有効性を、すべての問題を防ぐ実証済みの保証と解釈しません。',
'担当者との連携と、教師自身が情報資源の扱い方を理解することは両立します。〈36〉は教師養成の到達目標であり、担当者に任せれば理解が不要になるという説明ではありません。',
'本ケースの確認を、将来のあらゆる素材・配信方法への包括的な承認とは扱いません。情報資源の扱い方を理解して活用するという観点から、実際の利用条件に即して検討する必要があります。'],[
'誤：一般目標⑫・〈36〉と教育実践への知識活用を否定',
'正：情報資源理解と知識の実践活用に照らした適用判断',
'誤：教師養成で求める理解を担当者への委任で不要とする',
'誤：事前確認を条件変更後も含めた包括承認とする']),
'Q_MO_015':(2,['S163','S162','S26'],'このケースを踏まえて、次にオンデマンド配信を伴う授業を準備する。教材の内容と配信に必要な利用権限の両方を検討する対応として、適切なものを一つ選べ。',[
'オンデマンド授業は、素材の権利や利用条件がどうであっても、著作権法上必ず禁止されると扱う。',
'配信に必要な権利を確認した独自教材や、利用条件を満たすCC BY 4.0教材を、授業の目的・目標に合わせて選ぶ。',
'前回の素材について担当者に確認したので、今回使う別の素材や配信方法の条件は一切調べない。',
'CC BY 4.0教材では作者名だけを示し、ライセンス情報や改変の表示などの条件は確認せずに配信する。'],[
'著作権法第35条第1項の公衆送信はオンデマンドを一律禁止するものではなく、許諾等を根拠に利用する場合もあります。素材の権利・利用条件を問わず、方式だけで必ず禁止とする肢は誤りです。',
'コアカリキュラムは目的・目標に沿う授業計画と情報資源の扱い方の理解を求めます。独自教材でも他人の保護される表現を取り込んだり配信権限を持たなかったりする場合を自動的に安全とは扱わず、本肢は必要な権利を確認します。CC BY 4.0教材も第3条の条件に従います。',
'前回の確認は、新たな素材や配信方法についての権利処理まで不要にするものではありません。著作権法第35条による利用なら同条の条件を、ライセンスによる利用ならその条件を、実際の利用に即して検討します。',
'CC BY 4.0第3条a項では、提供されたクレジット情報等の保持に加え、改変の表示やライセンス情報の提供等も求めます。作者名だけで他の条件を確認しなくてよいという肢は誤りです。'],[
'誤：第35条と許諾による利用を含めオンデマンドを一律禁止',
'正：教育目標との適合と、独自教材・CC教材双方の利用権限を確認',
'誤：別の素材・配信方法の条件を過去の確認だけで省略',
'誤：CC BY 4.0第3条の条件を作者名だけに縮減'])}
extra=[]
for k,(ans,ss,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='要追加確認' and int(a['A_'+k[2:]]['ans'])==ans
 reason='文科省公式ページからリンクされた令和6年4月1日決定コアカリキュラム全15頁を取得し、一般目標⑫・必須内容〈36〉の到達目標、表1の知識の実践活用と照合。ケースへの教育的な適用判断を資料の逐語的な主張や事前確認による適法性の保証とは区別。教材選択ではCC BY 4.0本文第2・3条と保存済み著作権法第35条も参照し、独自教材という名称だけで権利処理が不要になるとの含みを除いた。'
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   assert html.unescape(old)!=new
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=ss,applied=True,before_version='第104バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=ss,reason=reason,option_verdicts=verdicts,stem_review='修正済みケース10又はオンデマンドケースの前提と整合させ、設問・全4肢を独立比較。資料の表の対応をPDF3・14頁の画像でも確認。',explanation_review='全4解説を原資料本文と照合。資料の到達目標・知識活用と、仮想ケースへの適用判断を区別。個別利用の法的適正やリスク低減の因果効果まで保証しない。',unresolved='',multiple_correct_risk='なし：情報資源理解・利用条件検討と整合する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27
for name,obj in [('changes.json',c+extra),('changes_batch105.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/697c245d9771/S163-105-retry.pdf').read_bytes();assert len(raw)==514031
(b.OUT/'evidence/S163_core_curriculum_20240401.pdf.gz').write_bytes(gzip.compress(raw,mtime=0))
assert gzip.decompress((b.OUT/'evidence/S163_core_curriculum_20240401.pdf.gz').read_bytes())==raw
print('3 full reviews/27 edits; primary PDF archived',hashlib.sha256(raw).hexdigest())
