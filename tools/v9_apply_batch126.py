"""One-time primary-author BICS/CALP audit. Never rerun on later judgments."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2725
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
reason='Cummins2008著者稿PDF2〜3・5頁の本文と画像を照合。BICS/CALPは会話の流暢さと学校の学術的な言語使用の概念的区別であり、全言語能力を尽くす二分法でも、知的能力の欠損診断でもない。CALPは口頭・書面の両方を含む。原稿の一律の習得年数、全JSL児童への同一の支援必須、文脈離脱という絶対化、未取得の言語間転移の保証を削除し著者の区別と教育的示唆に限定。引用された個別研究の再検証・日本の全児童への期間や効果の一般化は承認しない。'
data={
'Q_2_004':(3,'Cummins（2008）が説明するBICS（日常会話の流暢さ）とCALP（学習言語能力）の区別に関する記述として、最も適切なものを一つ選びなさい。',[
'CALPは日常会話の流暢さだけを指す用語であり、学校の教科で概念や考えを理解し表現する言語能力を含まない。',
'BICSとCALPの区別は言語能力全体を説明し尽くす理論であり、言語能力の重要な側面はこの二つ以外にはないとする。',
'日常会話が流暢であることだけから教科学習に必要な言語面にも問題がないと判断せず、学校での理解や表現も確認する必要がある。',
'BICSとは学校の学術的な概念を理解し表現する言語能力であり、日常会話の流暢さとは区別して定義される。'],[
'著者はBICSを会話の流暢さ、CALPを学校で必要な概念や考えを理解し表現する言語能力として区別します。日常会話の流暢さだけをCALPとする肢は、この対応を逆にしています。',
'著者は、この区別は言語能力全体の理論ではなく、ほかの重要な側面を排除しない概念的区別だと明記しています。二つだけで言語能力を説明し尽くすとする肢は誤りです。',
'著者は、会話の流暢さと教科学習上の言語能力を混同して学習上の困難を見落とす問題を指摘します。この区別からは、会話だけで判断せず学校での理解や表現も確認することが導かれます。全児童に共通の習得期限を定めるものではありません。',
'学校で必要な概念や考えを理解し表現する学術的な言語能力を指すのはCALPです。BICSは会話の流暢さを指すため、この肢は二つの用語を取り違えています。']),
'Q_4_084':(3,'Cummins（2008）によるBICSとCALPの説明とその教育的示唆を、外国にルーツを持つ児童生徒への支援で参照する際の理解として、最も適切なものを一つ選びなさい。',[
'日常会話を流暢に話せることだけで、教科書や授業の言語も十分に理解できると判断し、学習言語の支援の検討は不要とする。',
'CALPは書き言葉だけに限定された能力なので、教科学習に関する口頭での説明や理解は、その対象には含めない。',
'会話の流暢さだけでは教科学習に必要な言語能力を判断できないため、教科での理解や表現も確かめ、必要な言語面の支援を検討する。',
'課題の文脈的な支えの程度や認知的な要求の高さは、学習者の既有知識や関心とは無関係に、一律に決められる。'],[
'著者は、日常会話の流暢さを学術的な言語能力と同一視して、教科学習上の困難を見落とす問題を指摘しています。会話だけで支援の検討を不要とする判断は、その区別と矛盾します。',
'著者によるCALPの定義は、学校に関わる概念や考えを口頭と書面の両方で理解し表現する能力を含みます。書き言葉だけに限り、教科の口頭での説明や理解を除くことはできません。',
'会話の流暢さと学校で必要な言語能力を区別し、教科での理解や表現に応じて支援を検討する理解です。全児童の認知能力の不足を診断したり、全員に同一の支援や習得年数を当てはめたりする趣旨ではありません。',
'著者は、文脈的な支えと認知的な要求を二つの連続体として説明し、既有知識や関心などによって同じ課題の位置付けも変わると述べます。文脈が少ないことを文脈が皆無と解釈することも避ける必要があります。'])}
for k,(key,stem,opts,exps) in data.items():
 assert d[k]['status']=='要追加確認' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S190'],applied=True,before_version='第125バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==key else '誤')+'）'
   extra.append(c)
 verdicts=(['誤：BICSとCALPの定義を逆にする','誤：著者が否定する網羅的二分法','正：会話のみから学術的言語能力を推定しない','誤：CALPの定義をBICSと呼ぶ'] if k=='Q_2_004' else ['誤：会話の流暢さだけで教科の言語理解を認定','誤：CALPの口頭の側面を排除','正：教科の理解・表現も確かめ必要に応じて支援','誤：既有知識・関心による課題の相対性を否定'])
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S190'],reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢を著者2008稿PDF2〜3・5頁へ独立照合。JSLへの適用は教育的示唆であり日本の全児童の実証結果としない。',explanation_review='全4解説を本文と画像へ照合。口頭/書面、概念的区別の非網羅性、課題の相対性を保持。期間の固定値・能力欠損診断・転移効果の一般化を承認しない。',unresolved='',multiple_correct_risk='なし：独立正答3のみ適切',no_correct_risk='なし：独立正答3')
assert len(extra)==18
for name,obj in [('changes.json',cs+extra),('changes_batch126.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'cummins.pdf').read_bytes()
(b.OUT/'evidence/batch126_sources.json').write_text(json.dumps([dict(source_id='S190',title='Cummins (2008), BICS and CALP: Empirical and Theoretical Status of the Distinction',url='https://eclass.upatras.gr/modules/document/file.php/PDE1535/CumminsBICSCALPSpringer2007.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-16',body_read_scope='Author manuscript cover and PDF2-3,5 full text+images; definitions, non-exhaustive conceptual distinction, conversational/academic conflation, relative contextual/cognitive continua. No original cited-study verification or universal time/support effects.',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('2 questions/18 edits')
