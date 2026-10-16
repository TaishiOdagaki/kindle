"""One-time primary-text review of Schon 1983, pp21,40,61-63."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2420
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_4_001':dict(stem='ショーン（Schön, 1983）の省察的実践についての説明に合うものを一つ選びなさい。',opts=[
'省察では、自分の行為に暗黙に含まれる理解を検討せず、外部から与えられた評価だけを判断の根拠とする。',
'経験を積んで身に付けた理解や対応は、その後に新たな状況へ出会っても問い直す必要がない。',
'科学的な理論や技術を適用して問題を解くことだけで、何を問題とするかを定める過程も十分に説明できる。',
'自らの行為に含まれる理解を問い直し、不確実な状況を捉え直して、対応を試みることがある。'],exps=[
'61〜62頁では、繰り返す実践の中で暗黙になった理解、判断の基準、問題の捉え方などを省察の対象にしています。外部の評価を利用すること自体ではなく、自分の理解を検討対象から除く点が誤りです。',
'61頁は、反復する実践によって見方が固定し、合わない現象に注意を向けなくなる可能性と、その理解を問い直す省察を論じています。経験を積めば以後の再検討が不要になるという説明とは異なります。',
'21頁の技術的合理性は、科学的理論・技術を適用する道具的な問題解決のモデルです。40頁は、何を問題とし、目標や手段をどう定めるかという問題設定を、それだけでは説明できないと論じます。単に教案を機械的に進めることの別名ではありません。',
'61〜63頁の説明に対応します。実践の理解を表面化して批判的に検討し、新たな捉え方や試行につなげる過程です。ここでは原著の概念を問うており、特定の日本語指導の効果を実証したという意味ではありません。'],vs=['誤：自らの暗黙の理解を省察対象から除外','誤：経験から得た理解の再検討を一律不要とする','誤：問題解決だけで問題設定も十分説明できるとする','正：暗黙の理解の再検討・捉え直し・試行']) ,
'Q_4_004':dict(stem='授業中、教師Aさんは学習者の「て形」の誤りに気付き、「自分の説明では形の違いが伝わっていないのではないか」と捉え直した。そこで予定していた練習を一時中断し、対比例を示して学習者の反応を確かめることにした。ショーン（1983）の概念をこの架空事例に当てはめた説明として、最も適切なものを一つ選びなさい。',opts=[
'授業が終わった後に、完了した実践を振り返ることだけがこの場面で行われている。',
'予定した練習を変えたという事実だけで、教師の知識不足と指導の失敗が確定する。',
'当初の状況理解を一切検討せず、決めていた手順だけをそのまま遂行している。',
'実践が進行する中で状況の理解を問い直し、別の対応を試しているため、「行為の中の省察」の例と解釈できる。'],exps=[
'Aさんの再検討と対応の試行は、授業が進行している間に記述されています。61頁に示される、経験済みの実践を後から振り返る場面だけを述べた肢とは一致しません。',
'事例が示すのは、当初の説明の捉え直しと対応の試行です。計画を変えたという事実だけから、知識不足や指導の失敗が確定するとは判断できません。逆に、変更しただけで効果や指導の成功が保証されるわけでもありません。',
'事例には「説明では伝わっていないのではないか」という再検討と、別の対応を試す判断が明記されています。当初の理解を検討せず手順をそのまま遂行するという肢は、その記述に反します。',
'61〜63頁の、進行中の実践で理解を問い直し、捉え直しを試す過程に対応する適用例です。62頁では、この省察の時間幅は実践によって異なるとされ、常に瞬時に完了する判断に限定されません。'],vs=['誤：進行中の再検討を授業終了後だけとする','誤：計画変更だけで能力不足・失敗を断定','誤：明示された再検討と試行を否定','正：理解の再検討と試行を含む進行中の省察']) ,
'Q_4_083':dict(stem='ショーン（Schön, 1983）の省察についての説明に合うものを一つ選びなさい。',opts=[
'「行為の中の省察」は、どのような実践でも、必ず数秒以内に完了しなければならない。',
'省察の対象は結果の成否だけであり、行為に含まれる判断の基準や問題の捉え方は含まれない。',
'省察は、完了した実践を後から振り返る場合にしか生じず、実践の進行中には生じない。',
'反復する実践で暗黙になった理解を問い直し、不確実な状況の新たな意味を捉えようとすることがある。'],exps=[
'62頁は、行為の中の省察が必ずしも速いとは限らず、行為がなお状況に影響し得る時間幅の中で起こると説明します。その時間幅は実践によって異なり、数秒以内という一律の制限はありません。',
'62頁は、判断を支える暗黙の基準、行動に含まれる方略や理論、問題の枠付け、自らの役割なども省察の対象に挙げています。結果の成否だけに限定する説明は誤りです。',
'61〜62頁では、過去の実践を振り返る場合に加えて、実践が進行する中で省察する場合も説明されています。省察を終了後だけに限定することはできません。',
'61頁の説明に対応します。繰り返す実践から生まれた暗黙の理解を検討することが、見方の固定を問い直す働きを持ち得ると論じられています。全教師での効果や、実践的知識を得る唯一の方法を立証した説明ではありません。'],vs=['誤：原著が留保する時間幅を数秒へ固定','誤：省察対象を結果の成否だけへ限定','誤：進行中の省察を否定','正：暗黙の理解の再検討と新たな意味づけ'])}
extra=[]
reason='S166原著21・40・61〜63頁を本文・画像照合。技術的合理性を固定教案の機械的遂行へ還元せず、問題設定との区別、暗黙の理解の再検討、実践ごとのaction-presentを反映。日本語授業例は自作の適用例で効果保証としない。'
for k,v in items.items():
 assert d[k]['status']!='確認済み' and int(a['A_'+k[2:]]['ans'])==4
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,old,new in [('stem',[parts[0]],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a['A_'+k[2:]]['txt'],v['exps'])]:
  for i,(o,n) in enumerate(zip(old,new)):
   o=html.unescape(o)
   if o==n:continue
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S166'],applied=True,before_version='第107バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=v['stem']
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問の継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S166'],reason=reason,option_verdicts=v['vs'],stem_review='原著の説明に範囲を限定し、設問と全4肢の対応を独立判定。Q4_004は思考の捉え直しを架空事例に明記。',explanation_review='全4解説の主張を21・40・61〜63頁に照合。経験や科学的知識を全面否定しない。省察を常に瞬時・効果保証・唯一の知識獲得法としない。',unresolved='',multiple_correct_risk='なし：原著の説明に対応する肢は4のみ',no_correct_risk='なし：独立正答4')
assert len(extra) in (27,28)
for name,obj in [('changes.json',c+extra),('changes_batch108.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=Path('/workspace/scratch/697c245d9771/schon108.pdf').read_bytes();assert len(raw)==28811364
(b.OUT/'evidence/batch108_source.json').write_text(json.dumps(dict(id='S166',author='Donald A. Schön',title='The Reflective Practitioner How Professionals Think in Action',original_copyright=1983,scan='Basic Books later printing; scan date is not publication date',url='https://www.socialworkerskills.eu/uploads/1/4/4/7/144711219/sch%C3%B6n_d._a.__1983_._the_reflective_practitioner.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=380,read_printed_pages=[21,40,61,62,63],image_review_pdf_pages=[3,30,49,70,71,72],scope='Question approval rests on printed21,40,61-63; entire book not fully read; PDF body obtained locally, not redistributed'),ensure_ascii=False,indent=2)+'\n')
print('3 complete reviews;',len(extra),'edits')
