"""Source-bounded cultural-identity rejudgment; do not approve unavailable CEFR."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3159
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_1_003';ak='A_1_003';assert d[k]['status']=='要追加確認' and a[ak]['ans']=='1'
raw=(Path(__file__).resolve().parents[2]/'rfcdc150.pdf').read_bytes()
digest=hashlib.sha256(raw).hexdigest();prior=json.loads((b.OUT/'evidence/batch157_sources.json').read_text())[0]
assert digest==prior['sha256'] and len(raw)==prior['bytes']==4154359
stem='欧州評議会のRFCDC第1巻（2018年）第5章が示す、文化的アイデンティティと文化への帰属の説明に合うものを一つ選びなさい。'
opts=list(q[k]['opts']);opts[0]='個人は複数の文化集団に同時に帰属し、状況や時間の経過に伴って、どの帰属が自分にとって重要かが変わり得る。';opts[3]='一つの文化集団への帰属を持つ個人が別の文化集団にも帰属するには、それまでの帰属を全て失わなければならない。'
exps=['29頁は文化集団への所属を基に作るアイデンティティを説明し、30頁は複数の文化集団への同時の帰属と、状況や時間に応じて帰属の重要さが変わることを示します。この枠組みの説明に合う肢です。特定の変容が起こる頻度を測定した説明ではありません。',
'30頁は、国家や民族だけでなく、宗教集団、都市、近隣地域、職業集団、家族などにも文化があると説明します。宗教や地域などを全て除外し、国家・民族への帰属だけに限定する点が誤りです。',
'30頁は、文化への帰属とアイデンティティの重要さが状況や時間に伴って変化し、文化集団自体も変わると説明します。幼少期に不可逆的に固定され、その後は変化しないという肢は、この説明に合いません。',
'30頁は、個人が複数の集団とその文化に同時に帰属し、それらの帰属が交差すると説明します。新たな帰属を持つには以前の帰属を全て失う必要があるという条件は、この枠組みの複数帰属と両立しません。第二言語学習後の同化の頻度や過程を実証した説明ではありません。']
verdicts=['正：29頁の文化的アイデンティティと30頁の同時の複数帰属・状況と時間による重要さの変動に対応','誤：30頁は宗教・地域・職業・家族等の文化を明示し、国家・民族のみという限定を認めない','誤：30頁の動的で流動的な帰属・アイデンティティに対し幼少期固定・成人後不変とする','誤：30頁の同時の複数帰属に、旧帰属の全喪失を必要条件とする肢は反する']
reason='S213 RFCDC2018第1巻の取得済み89頁原PDFを、GitHub第157バッチの原バイトSHA256・サイズと照合して同一性を確認。29–32頁本文を精読し29・30頁を全頁画像照合。個人の複数帰属と、状況・時間に応じた主観的重要さの変動へ限定。旧解説のハイブリッド化・CEFR・加算的バイリンガリズム・滅失的同化の補助的理論帰属や、共存・拡張が一般的という頻度断定を削除し、未取得理論の承認としない。旧肢4の第二言語学習による因果的置換を、同じ文化的アイデンティティ領域の複数帰属の必要条件を問う肢へ改訂した。全89頁精読や引用先原著の独立取得、全ての個人の変容・同化過程の実証ではない。今回の再取得はタイムアウトし、取得済み原本の再検証を用いたことを区別する。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  if html.unescape(old)==new:continue
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S213'],applied=True,before_version='第157バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(c)
assert len(extra)==7
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S213'],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='指定資料の第5章に限定した設問と全4肢を29–32頁へ独立照合。複数帰属と重要さの変動を個人の実測頻度・言語学習の因果効果へ拡張しない。',explanation_review='全4解説を29–30頁の本文へ照合。CEFR・加算的バイリンガリズム・同化理論等の未取得の補助的主張と頻度断定を除去。',unresolved='',multiple_correct_risk='なし：指定章の説明に合うのは1のみ',no_correct_risk='なし：独立正答1')
for name,obj in [('changes.json',cs+extra),('changes_batch158.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
e=[dict(source_id='S213',url=prior['url'],title=prior['title'],year=2018,original_acquisition_record='evidence/batch157_sources.json',revalidated='2026-10-18',bytes=len(raw),sha256=digest,pdf_pages=89,fresh_download_succeeded=False,read_scope='取得済み同一原PDFの29–32頁本文を精読。29・30頁（PDF31・32頁）を1800px全頁画像照合。',limitations='全89頁精読ではない。全心理学の統一定義、引用先理論原著、言語学習の因果効果・同化頻度の実証ではない。今回の公式URL再取得はタイムアウト。取得済み原本の再検証と明示。',full_source_redistributed=False)]
(b.OUT/'evidence/batch158_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
attempt=dict(date='2026-10-18',pending_question='Q_2_032',source_id='S179',urls=['https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16802fc1bf','https://rm.coe.int/16802fc1bf'],result='WebでPDF273頁の概要は一度得られたが、必要本文の再取得・find・画像確認はタイムアウト。短縮URLのcurlは45秒・受信0バイト、exit28。検索抜粋やPDF概要を根拠本文として承認しない。',status_unchanged='要追加確認',full_task_blocked=False)
(b.OUT/'evidence/batch158_source_attempts.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2)+'\n')
print('Q_1_003:7 edits / key1 / Q_2_032 remains pending')
