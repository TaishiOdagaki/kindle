"""Source-scoped CLIL and ethnocentrism audit without effect guarantees."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3245
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data={
'Q_O_066':(1,['S191'],'ケース14の授業をCLIL（内容言語統合型学習）として設計する際の目標設定として、最も適切なものを一つ選べ。',[
'環境問題に関する内容の理解と、その内容を日本語で理解・表現するための言語の学習を結び付ける。',
'環境問題は日本語を話すための話題にすぎないので、内容の理解を学習目標から除く。',
'環境問題の知識だけを目標とし、資料読解や意見交換で必要な日本語は学習対象に含めない。',
'内容と言語の二つの目標は両立しないので、どちらか一方の学習だけをCLILの原則とする。'],[
'Bower・Cross・Coyleの説明では、CLILは内容と言語の二重の焦点をもち、内容の目標から必要な言語を検討します。環境に関する資料を読み、話し合い、比較レポートを書くケースに、この二重の目標を具体化した設計です。',
'CLILのContentは、主題についての知識・概念・技能を含みます。話題を用いるだけで内容の理解を目標から除く説明では、内容と言語を統合する二重の焦点を満たしません。',
'Communicationは、学ぶ知識・概念・技能について意味を作り伝える言語に関わります。資料読解や意見交換に必要な日本語を学習対象から除く設計は、言語も焦点とする説明と合いません。',
'取得した著者の枠組みは、内容の目標と言語の要求を結び付けて設計するものです。二つは両立しないという説明は反対です。二重の目標を設定することと、全員の学習効果を保証することは別です。'],
'S191出版社公開章抜粋の印刷9–11頁（PDF8–10頁）を再取得して本文照合、9–10頁画像も確認。旧問の教授法名の識別を、同じCLILの二重焦点をケースへ具体化する目標設定に改訂。文法訳読法・サイレントウェイ・ALMの未取得原著による説明を解説から除き、内容目標と言語の要求という取得範囲へ限定する。ケース本文は保持し、単なる話題利用と内容学習を区別。教授法の効果や引用先の実験結果の承認ではない。'),
'Q_4_099':(1,['S213'],'欧州評議会RFCDC第1巻の自民族中心主義の定義と文化差への姿勢の説明に合うものを一つ選べ。',[
'自民族中心主義は、自分の主要な文化を中心に置き、それを基準として他の文化を評価する見方を含む。',
'他者への尊重は、その人の文化的な信念や慣行をすべて自分も採用することを必要とする。',
'他の文化に開かれるには、自分の世界観や慣行を当然のものとして問い直さない姿勢が必要である。',
'他者の文化を尊重するためには、人間の尊厳や人権を侵害する慣行の内容も無条件で肯定しなければならない。'],[
'用語集73頁は、自分の主要な文化を中心に据え、それを参照して他を評価する見方を自民族中心主義として説明します。自集団のやり方を優越視する偏見も含みます。常に無意識である、常に蔑視を伴う、という条件には限定されません。',
'42頁のRespectは、他者の尊厳と権利を尊重することを、相手の信念や慣行への同意・採用・改宗と区別しています。相手の文化的実践をすべて自分も採用する必要があるという説明は誤りです。',
'41頁のOpennessは、他者への判断をいったん留保し、自分の世界観・信念・慣行が当然だという見方を問い直す意思を挙げています。自分の前提を問い直さないという説明は逆です。',
'42–43頁は尊重に限界を設け、他者の尊厳・人権・自由を損なう信念や慣行の内容を尊重の対象としません。文化差を理解しようとすることと、すべての行為を無条件に肯定することは区別されます。'],
'S213 RFCDC第1巻の41–43頁（Openness・Respect、注7・8含む）と用語集73頁を本文照合、42・73頁画像を確認。既取得PDFのSHA256を第156バッチ記録と照合した。旧解説の無意識・歪曲・蔑視という必須条件化と、文化相対主義が柔軟な異文化適応につながるという一律の効果説明を撤回。文化相対主義の全学説の定義をこの政策枠組みで代用せず、RFCDC自身の自民族中心主義・開放性・尊重の説明と人権上の限界に設問を明示限定。')}
extra=[]
for k,(key,sources,stem,opts,exps,reason) in data.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第162バッチ反映後',block_context=ak if field=='explanations' else k)
   assert c['before']!=new
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==key else '誤')+'）'
   extra.append(c)
 verdicts=(['正：内容目標と言語の要求を結び付ける','誤：内容の学習目標を除外','誤：言語の学習対象を除外','誤：二重焦点を否定'] if k=='Q_O_066' else ['正：用語集の中心・評価基準の説明に一致','誤：尊重と同意・採用を同一視','誤：自分の前提を問う開放性の説明と逆','誤：人権・尊厳上の尊重の限界を無視'])
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='全4肢を設問で指定した取得本文へ独立照合。CLILはケース14の読解・対話・比較レポートと目標の対応を確認。',explanation_review='全4解説の定義・適用範囲を照合。未取得教授法原著・哲学的文化相対主義の全体系・教授法効果や適応効果を承認しない。',unresolved='',multiple_correct_risk='なし：指定枠組みと合うのは1のみ',no_correct_risk='なし：独立正答1')
assert len(extra)==18
for name,obj in [('changes.json',cs+extra),('changes_batch163.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];e=[]
for sid,filename,url,scope in [('S191','clil163.pdf','https://assets.cambridge.org/97811087/29734/excerpt/9781108729734_excerpt.pdf','出版社公開抜粋の印刷9–11/PDF8–10頁本文、9・10頁画像。Coyleを含む著者自身の概念枠組み。引用実験の原データ再検証ではない。'),('S213','rfcdc150.pdf','https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c','41–43頁本文（注7・8含む）、用語集73頁本文。42・73頁画像。29–30頁本文も参照。第156バッチ原バイトとハッシュ一致確認。Web再取得はタイムアウトしたため、検証した取得済みPDFを使用。')]:
 raw=(root/filename).read_bytes();digest=hashlib.sha256(raw).hexdigest()
 if sid=='S213':assert digest=='a93866bccc575a825b4cc9e9b5f25c115d7c1ffd29dc677a1acc0aa226daa612'
 e.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=digest,checked='2026-10-18',read_scope=scope,full_source_redistributed=False))
(b.OUT/'evidence/batch163_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions /18 edits /keys1,1')
