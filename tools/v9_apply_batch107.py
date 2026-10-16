"""One-time evidence-based distinction of activity and competence Can-do."""
import json, html, gzip, hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2405
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_4_013':dict(key=2,stem='JF日本語教育スタンダードの活動Can-doを学習目標の設定に活用する利点として、最も適切なものを一つ選びなさい。',opts=[
q['Q_4_013']['opts'][0],
'実社会でどのようなコミュニケーション活動ができるかを具体的な目標として示し、学習者と共有できる点。',
q['Q_4_013']['opts'][2],q['Q_4_013']['opts'][3]],exps=[
'活動Can-doは、実社会で行うコミュニケーション言語活動を例示します。暗記した規則や語の数だけを示すものではありません。ただし、その活動に必要な語彙や文法の準備を不要とする考え方でもありません。',
'国際交流基金の公式解説は、活動Can-doを目標設定に利用でき、学習目標を教師と学習者で共有できると説明しています。実社会でできる言語活動を目標として示すという肢が対応します。',
'言語活動の達成を目標にするため、文法上の誤りの有無だけで評価し、課題の達成を除外する説明は適切ではありません。文法的正確さなどの言語能力を評価の観点に含めること自体はできます。',
'公式解説は、教育現場に合わせて目標を設定し、目標に合った授業や評価を設計する使い方を示しています。教師が教える順序や講義型授業を一律に固定するものではありません。'],verdicts=[
'誤：活動ではなく暗記量だけに限定','正：具体的な言語活動の目標設定と共有','誤：正確さ以外の課題達成を排除','誤：一律の教授順・講義型への固定ではない']),
'Q_4_026':dict(key=3,stem='JF日本語教育スタンダードの活動Can-doを用いた学習目標の設定について、最も適切な記述を一つ選びなさい。',opts=[
'活動Can-doは、実社会で行う言語活動ではなく、暗記した文法規則の数だけを記述するものである。',
'活動Can-doを使う場合、その活動に必要な語彙や文法項目を準備・検討する必要はない。',
'例えば「店員がゆっくり話してくれれば、飲食店で希望する料理を注文できる」のように、条件と具体的な言語活動を示して目標を設定する。',
'活動Can-doを学習者と共有することはできず、教師が授業内容を決めるためだけに使用する。'],exps=[
'公式解説では、活動Can-doは実社会で行う具体的なコミュニケーション言語活動の例です。暗記した文法規則の数だけを記述するという肢は、この説明と一致しません。',
'公式解説の留意点は、Can-doの達成に必要な語彙や文法項目などの準備も必要としています。言語活動を目標にすることは、言語知識を扱わないという意味ではありません。',
'これは、注文という具体的な言語活動に、相手の話し方という条件を付けた本問独自の目標例です。活動Can-doとして場面での課題遂行を記述する考え方に対応します。公式Can-doの引用や、特定レベルの認定例ではありません。',
'公式解説は、教師と学習者が目標を共有し、学習者が自分の日本語の力を自己評価する使い方を示しています。教師だけに利用を限る説明は誤りです。評価シートの作成には能力Can-doも参考にできます。'],verdicts=[
'誤：具体的な言語活動を暗記規則数へ置換','誤：必要な語彙・文法の準備まで不要とする','正：条件と具体的言語活動を示す自作例。レベルは未指定','誤：目標共有・自己評価での活用を排除'])}
extra=[]
reason='S11公式本文を再取得し活動Can-doと能力Can-doを区別。文法知識を一律に排除する一般化、教授順序の固定、自己評価効果の断定を避け、活動Can-doの目標設定に出題範囲を限定する。'
for k,v in items.items():
 assert d[k]['status']!='確認済み' and int(a['A_'+k[2:]]['ans'])==v['key']
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,old,new in [('stem',[parts[0]],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a['A_'+k[2:]]['txt'],v['exps'])]:
  for i,(o,n) in enumerate(zip(old,new)):
   o=html.unescape(o)
   if o==n:continue
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S11'],applied=True,before_version='第106バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=v['stem']
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==v['key']-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True))
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=['S11'],reason=reason,option_verdicts=v['verdicts'],stem_review='活動Can-doに限定した設問と全4肢を公式本文に照合。独立に正誤を判定。',explanation_review='全4解説を公式の定義・4種類・留意点・活用方法に照合。文法等を含む能力Can-doを否定せず、活動目標・評価観点・教授順序を区別。自作例にレベルや実証的効果を付与しない。',unresolved='',multiple_correct_risk='なし：活動目標と矛盾する3肢を区別',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==15
for name,obj in [('changes.json',c+extra),('changes_batch107.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
source_meta={}
for name in ['about','course','summary']:
 raw=Path('/workspace/scratch/697c245d9771/S11_107_'+name+'.html').read_bytes();assert '</html>' in raw.decode().lower() and 'Can-do' in raw.decode()
 source_meta[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 (b.OUT/f'evidence/S11_batch107_{name}.html.gz').write_bytes(gzip.compress(raw,mtime=0))
(b.OUT/'evidence/batch107_sources.json').write_text(json.dumps(source_meta,indent=2)+'\n')
print('2 complete reviews;15 actual edits')
