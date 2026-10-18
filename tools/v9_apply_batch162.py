"""Cummins author chapter: conceptual distinction without individual diagnosis."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3227
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
reason='S190 Cummins2008著者原稿PDF2–5頁の定義・誤った評価事例・文脈支援と認知的要求の本文を取得し照合。会話の流暢さと学習場面の口頭・書記の言語使用を区別するが、概念区分だけで個人の能力不足や困難の単一原因を診断しない。ケースは設定として読み、ニーズに即した選択と理論の適用範囲を問う。'
items={
'Q_O_008':(1,'ケース2の「講義を聞いてノートを取る」ことへの不安に直接対応する学習目標として、BICS/CALPの区別も踏まえて最も適当なものを一つ選べ。',[
'講義で述べられる概念や要点を理解し、必要な内容を記録する力を育てる。',
'発音の正確さだけを高め、講義内容の理解や記録は目標に含めない。',
'日常会話の流暢さだけで講義理解も保証されるため、聴解・記録は扱わない。',
'あいさつ表現の暗記だけを目標とし、講義で用いる言語は扱わない。'],[
'CumminsはCALPを、学校での学習に関わる概念を口頭と書記の両方で理解・表現する力として説明しています。講義の概念・要点の理解と記録は、このケースの不安と目標に直接対応します。特定のノート指導法の効果を理論だけから保証する意味ではありません。',
'発音の正確さだけに目標を限定すると、ケースに明記された講義内容の理解と記録の課題を扱えません。発音練習一般の有用性を否定しているのではありません。',
'BICSとCALPは概念的に区別され、日常会話が流暢であることだけでは学習場面の言語使用まで保証されません。ただし、日常会話が学習に役立たないという意味でもありません。',
'あいさつの暗記だけでは、このケースで求める講義理解と記録を目標に含められません。日常のあいさつ自体を不要とする判断ではありません。']),
'Q_O_041':(2,'ケース9をCumminsのBICS/CALPの区別に照らして捉える説明として、最も適当なものを一つ選べ。',[
'日常会話ができるので、教科学習で必要な言語使用も十分だと判断できる。',
'会話の流暢さと教科学習の言語使用を区別し、文章題でどの表現や内容に困るかを確かめる。',
'文章題の理解に時間がかかるという事実だけで、児童の認知能力の不足を診断できる。',
'CALPは書き言葉だけの能力なので、教師の口頭説明の理解とは関係しない。'],[
'Cumminsは、会話の流暢さを学習場面の言語能力全体と同一視した評価・指導上の問題を示しています。会話ができることだけで教科学習に必要な言語使用が十分だとは判断できません。',
'BICSは会話の流暢さ、CALPは学習に関わる概念を口頭・書記で理解・表現する力という区別です。ケースの観察から両者を同一視せず、文章題の表現や内容のどこが難しいかを確認する説明が適切です。この観察だけでCALP不足や困難の原因を確定するものではありません。',
'著者は、第二言語での学習上の困難を適切に考慮しない評価が、認知能力や障害について不適切な判断につながった事例を論じています。文章題の理解に要する時間だけで認知能力の不足を診断することはできません。',
'CALPの定義は口頭と書記の両方を含みます。学習内容を伝える口頭説明の理解も関わり得るため、書き言葉だけに限定する説明は誤りです。'])}
extra=[]
for k,(key,stem,opts,exps) in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S190'],applied=True,before_version='第161バッチ反映後',block_context=ak if field=='explanations' else k)
   assert c['before']!=new
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==key else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S190'],reason=reason,option_verdicts=(['正：設定された講義理解・記録の目標と定義に合う','誤：発音だけに限定し明示された課題を除外','誤：会話の流暢さから学習言語を保証','誤：あいさつのみで講義の言語を除外'] if key==1 else ['誤：会話と学習言語を同一視','正：概念区分を用い困難の所在を確認する解釈','誤：単一の観察から認知能力不足を診断','誤：口頭も含むCALPを書記に限定']),candidate_answers=[],stem_review='対応ケースと全4肢を独立照合。ケースを実証調査と誤認せず、概念区分の適用を問う。',explanation_review='4解説をS190 PDF2–5頁の定義・評価事例・理論の範囲へ照合。個人診断・教授法効果・習得年数の一般化を残さない。',unresolved='',multiple_correct_risk='なし：指定理論とケースに合う肢のみ',no_correct_risk='なし：独立正答'+str(key))
assert len(extra)==18
for name,obj in [('changes.json',cs+extra),('changes_batch162.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'cummins162.pdf').read_bytes()
e=dict(source_id='S190',author='Jim Cummins',title='BICS and CALP: Empirical and Theoretical Status of the Distinction',publication_year=2008,url='https://eclass.upatras.gr/modules/document/file.php/PDE1535/CumminsBICSCALPSpringer2007.pdf',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope='著者原稿PDF2–5頁の本文を精読、PDF2・3・5頁画像も目視。本文の定義と評価事例、認知的要求・文脈支援の相対性。全参考文献の原著を取得したとはしない。',limitations='概念区分とケースの論理的対応。日本の児童への個人診断・特定指導法効果・普遍的習得年数の実証ではない。',full_source_redistributed=False)
(b.OUT/'evidence/batch162_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions /18 changes /keys1,2')
