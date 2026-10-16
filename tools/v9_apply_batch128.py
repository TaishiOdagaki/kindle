"""One-time CLIL evaluation/support and WHO occupational burnout scope audit."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2770
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
reasons={
'Q_O_069':'ケース14の内容と言語の両目標をもつ単元の評価計画に限定。CambridgeのTKT:CLIL公式handbook印刷15/PDF16にcontent and/or language、認知・コミュニケーション技能、基準、支援方略を確認し、Coyleを含む著者の二重焦点の本文と照合。全個別課題が常に両面同時採点必須という誤読を避け、単元全体の学習目標の取りこぼしを問う。',
'Q_O_070':'Coyleを含む著者の枠組み印刷9〜11/PDF8〜10とTKT:CLIL公式handbook印刷14〜15/PDF15〜16を本文・画像照合。思考・内容と言語を結び付ける設計意図、言語支援や負担の調整を確認。CLILは必ず効果が高い/負担によって効果が下がる根拠はないという未取得実証の全面断定を撤回。実践の設計と全員の効果保証を区別。',
'Q_M_019':'WHO公式FAQの定義全文を2026-10-17取得。職業場面の慢性的ストレス、三側面、medical conditionとは分類しない点を照合。教師と学習者の一般的疲弊を一律にWHO定義へ当てはめていた原設問を修正。学習者バーンアウト研究や一般心理概念との全比較、診断・治療法は未取得で承認しない。'}
data={
'Q_O_069':(3,'ケース14のように内容と言語の双方に学習目標を置いたCLIL単元について、単元全体の目標達成を把握する評価計画として、最も適切なものを一つ選べ。',[
'環境問題の理解を目標に含めていても、その到達を確かめる機会を設けず、言語面だけを単元の評価対象とする。',
'内容を日本語で伝え合うことも目標に含めていても、その運用は確かめず、文法や発音の正確さだけで全目標の達成を判断する。',
'内容の理解・思考と言語面の運用を、設定した目標や基準に応じて単元全体で捉える。個別課題の評価焦点や必要な支援は調整する。',
'内容・言語の目標は立てるが、その達成を確かめる評価は一切行わず、授業が楽しかったかという感想だけで達成を判断する。'],[
'内容の理解を目標としている単元で、それを確かめる機会を除くと、その目標の到達を把握できません。内容も評価対象として検討する必要があります。',
'内容を伝え合う言語の運用を目標としているなら、正確さだけでなく、その運用の達成も捉える計画が必要です。文法や発音だけで全目標の達成を判断する説明では不十分です。',
'公式handbookは内容や言語、認知・コミュニケーション技能などの評価焦点と基準・支援方略を挙げます。この単元では内容と言語の両目標を全体で捉えますが、全個別課題で両面を同時に同じ重みで採点するという規則ではありません。',
'感想を集めることはできますが、楽しさの感想だけでは設定した内容・言語の目標達成を判断できません。学習成果を確かめる評価を全く行わないという計画は、設問の目的に合いません。']),
'Q_O_070':(3,'CLILの内容と言語を結び付ける枠組みに沿って日本語の授業を設計する際の説明として、最も適切なものを一つ選べ。',[
'CLILという名称を用いれば、学習者の条件や課題の設計にかかわらず、他の授業より全員に高い学習効果が必ず生じる。',
'CLILの枠組みが扱う言語は英語に限られるため、教科内容を学ぶ言語として日本語を用いる授業には適用を検討できない。',
'内容について考え、その意味を日本語で理解し伝える学習を結び付ける。そのために必要な言語面の支援や課題の負担も検討する。',
'内容を日本語で扱うことにすれば、それだけで全員が授業を理解できるため、語彙・表現や活動手順の支援は不要になる。'],[
'取得した枠組みは授業設計の観点を述べたもので、名称を付ければ学習者や課題の条件と無関係に全員に優越した効果が出るという保証ではありません。',
'著者らは内容と言語の二重焦点を述べ、英語だけを対象言語とする原則にはしていません。日本語を教科内容の学習に用いる設計を、英語ではないことだけで除外する説明は誤りです。',
'内容に関わる思考と言語の使用を結び付ける設計です。公式handbookは語彙・文の枠組みや視覚的な支え、課題の分割・調整などを挙げます。設計上の意義と支援を述べ、全員への効果を保証する説明にはしていません。',
'公式handbookは内容と言語の双方への足場掛けや、学習者に応じた課題の調整を扱っています。内容を日本語にするだけで全員が理解し、言語や手順の支援が不要になるという説明とは異なります。']),
'Q_M_019':(4,'WHOのICD-11に関する説明で、バーンアウトの位置付けとして適切なものを一つ選べ。',[
'職業に限らず、学校や家庭で感じるすべての疲労に適用する医学的疾患である。',
'短時間でも疲れを感じれば、それだけでバーンアウトと判断できるとする。',
'仕事への心理的距離や職業上の効力感は関係なく、疲弊の一側面だけで定義する。',
'対処できていない慢性的な職場ストレスに関連する職業上の現象で、医学的疾患とは分類しない。'],[
'WHOの説明は職業場面に限定し、生活の他領域の経験へ当てはめないとします。学習者の疲労全般と同一視できません。',
'慢性的な職場ストレスと三つの側面を挙げています。一時的な疲れだけで判断する説明ではありません。',
'疲弊、仕事への心理的距離の増大や否定的態度、職業上の効力感の低下の三側面を挙げています。',
'WHOの位置付けに対応します。職業場面に関する定義の理解を問うもので、個人を診断する基準を示したものではありません。'])}
verdicts={
'Q_O_069':['誤：内容目標の達成を未評価','誤：言語運用目標を正確さだけで代用','正：両目標を単元全体で捉え課題の焦点を調整','誤：感想だけで全目標達成を代用'],
'Q_O_070':['誤：全員への比較優位を保証','誤：対象言語を英語のみに限定','正：内容・言語を結び支援と負担を検討','誤：教授言語変更だけで支援不要とする'],
'Q_M_019':['誤：職業場面限定と非疾患分類の両方に反する','誤：一時的疲労だけへ縮減','誤：三側面のうち二つを排除','正：WHOの職業上の現象という位置付けに対応']}
for k,(key,stem,opts,exps) in data.items():
 assert d[k]['status'] in ['要追加確認','修正必要'] and a['A_'+k[2:]]['ans']==str(key)
 sources=['S193'] if k=='Q_M_019' else ['S191','S192'];reason=reasons[k]
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第127バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==key else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts[k],stem_review='設問条件と全4肢を取得した公式本文へ独立照合。CLILの2問はケース14本文・目標との整合も確認。WHOの定義を学習者全般の疲労や医療診断に拡張しない。',explanation_review='全4解説を根拠本文へ照合。評価課題ごとの焦点調整と単元全体の両目標、設計意図と実証効果、職業場面限定と疾患分類の区別を確認。',unresolved='',multiple_correct_risk=f'なし：独立正答{key}のみ適切',no_correct_risk=f'なし：独立正答{key}')
assert len(extra)==27
for name,obj in [('changes.json',cs+extra),('changes_batch128.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];e=[]
for sid,f,url,scope in [('S192','tkt-clil-retry.pdf','https://www.cambridgeenglish.org/images/22191-tkt-clil-handbook.pdf','Official handbook full31-page PDF acquired; printed14-15/PDF15-16 body+images. Assessment content and/or language, criteria, scaffolding, differentiation. No cited efficacy-study approval.'),('S193','who-burnout.html','https://www.who.int/standards/classifications/frequently-asked-questions/burn-out-an-occupational-phenomenon','Complete FAQ definition body, occupational context, three dimensions, not a medical condition. No learner burnout/diagnosis/treatment approval.')]:
 raw=(root/f).read_bytes();e.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-17',body_read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch128_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('3 questions/27 edits')
