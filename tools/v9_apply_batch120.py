"""OPI2024 and scoring: one-time ordered revision after batch119."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2637
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第119バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問・全4肢をACTFL2024公式OPIガイド、2014Testing StandardsとCEFR/TKTの該当本文へ独立照合。OPIと能力記述ガイド全体の範囲、採点方式と測定全体を区別。',explanation_review='全4解説を本文へ照合。機械採点や多肢選択だけで誤差ゼロ・高信頼性を保証しない。OPIの各レベルで同じ段落構成課題が必須とはせず、認定・再調整と完全一致の実証を区別。',unresolved='',multiple_correct_risk='なし：独立正答'+str(key)+'のみ適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_1_036'
review(k,'ACTFLの2024年版OPI受験案内に基づく、評価基準や実施方法の説明として、最も適切なものを一つ選びなさい。',q[k]['opts'],[
'OPIは一対一の口頭面接で発話を引き出す方式です。筆記回答を機械採点して発話能力を決めるという説明ではありません。',
'ガイドは、機能・課題、正確さ、内容・文脈、テキスト型のFACTという観点を示し、それらを関連づけて全体的に評価します。文法的な正確さだけを唯一の基準とする説明は合いません。',
'このOPIの評価範囲はNoviceからSuperiorです。Novice・Intermediate・AdvancedにはLow・Mid・Highがありますが、Superiorを同じように三分割しません。能力記述ガイド全体にあるDistinguishedまでこのOPIが評価するわけでもなく、N1〜N5という区分ではありません。',
'テスターは応答に合わせて質問を調整し、必要に応じてロールプレイも用いて発話を引き出します。どの機能をどの文脈で継続して遂行できるかを、言葉のまとまりや正確さも含めて判断します。段落単位の発話などをすべてのレベルへ一律に要求する説明ではありません。'],4,['S185'],
'ACTFL自身の2024OPI受験案内3〜8頁を本文・画像照合。OPIのNovice〜SuperiorとGuidelines全体のDistinguishedを区別し、FACTと質問/ロールプレイの任意性を確認。以前から正しく修正済みのSuperiorの非三分割は保持し、新発見と数えない。JLPTのレベル表記という未照合の補助説明は除去。',
['誤：発話面接ではなく筆記機械採点とする','誤：FACTの他観点を排除し文法だけとする','誤：2024OPIの区分はN1〜N5ではない','正：一対一の対話で文脈・機能等を全体的に評価する'])
k='Q_1_037';opts=q[k]['opts'].copy()
opts[0]='テストが日々の学習や指導法に与える影響のことを、熟達度と呼ぶ。'
opts[1]='信頼性とは、得点の一貫性のことではなく、提案された用途のための得点解釈を証拠と理論がどの程度支持するかを指す。'
opts[2]='正答と配点をあらかじめ定めた多肢選択式問題では、その基準を同じように適用することで、採点者による判断の違いを抑えられる。'
review(k,'評価・採点とOPIの運用に関する説明として、最も適切なものを一つ選びなさい。',opts,[
'熟達度は、言語を使用する場面で何ができるかという能力に関わる概念です。テストが学習や指導に与える影響を熟達度と名づける肢とは対応しません。',
'2014年版Testing Standardsのこの説明は妥当性に対応します。同書は信頼性・精度を測定手続きの反復における得点の一貫性に関わる概念として扱い、採点者や課題等の変動を検討します。',
'正答と配点が決まり、同じ基準を適用するという条件では、応答の質について採点者が個別に判断する余地を抑えられます。ただし、採点処理の誤りが起きず、測定全体の誤差もなくなるという保証ではありません。',
'ACTFLの2024年版OPI受験案内8頁は、テスターの認定と基準調整、再認定の手続きを説明しています。訓練が一切不要という肢はこれと合いません。制度があることだけで、あらゆる採点で評価者が完全一致すると認定するものでもありません。'],3,['S185','S142','S179','S183'],
'2014Testing Standards11・33〜34頁、TKT Assessmentの客観採点、CEFR9.3.1の熟達度、ACTFL2024OPI8頁を照合。熟達度/影響、妥当性/一貫性を区別。多肢選択・マークシートなら主観も誤差も介入せず極めて高信頼性という元解説を、固定基準で判断差を抑える条件付き説明へ修正。未照合のJLPT個別運用や波及効果/転移の補助分類は除去。',
['誤：学習・指導への影響を使用能力の熟達度と取り違える','誤：妥当性の説明を信頼性とし一貫性を否定','正：固定した基準の適用は採点者の判断差を抑える','誤：OPIは認定・基準調整等を求め訓練不要ではない'])
assert len(extra)==13,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch120.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];meta=[]
for sid,name,url,scope in [('S185','opi.pdf','https://www.actfl.org/uploads/files/general/OPI_Familiarization_Guide_2024_FINAL.pdf','2024author guide3-8 complete text/image:interview,FACT,OPIrange/sublevels and tester certification; cited empirical validation studies and current accommodations not approved'),('S142','standards.pdf','https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf','2014printed11/PDF21 and33-34/PDF43-44 text/images;11-14 additional text read but no whole book endorsement')]:
 raw=(root/name).read_bytes();meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_read_scope=scope,retrieved='2026-10-16',full_source_redistributed=False))
(b.OUT/'evidence/batch120_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('2 questions/13 edits')
