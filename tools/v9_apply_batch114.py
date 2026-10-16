"""One-time Q_O_036 scholarly revision; S173 full original pp1-2."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text()); assert len(cs)==2523
d=json.loads((b.OUT/'decisions.json').read_text()); k='Q_O_036'; assert d[k]['status']=='修正必要'
_,q,a=qa.audit(str(b.DST)); assert a['A_O_036']['ans']=='1'
stem='FLN（2014）が区別するFlipped ClassroomとFlipped Learningの関係に照らし、このケースの記録から判断できることを一つ選びなさい。'
opts=[
'授業前に基本的な説明を学び、教室で応用活動を行う反転の設計は読み取れるが、この記録だけで四つの柱すべての実践を確認したことにはならない。',
'授業前の動画視聴を指示したという事実だけで、四つの柱すべてが実践されていると判断できる。',
'教室で教師が学習者を観察したり必要な支援を行ったりすることは、Flipped Learningの考え方から除かれる。',
'このケースのように動画を使う場合、文章など動画以外の教材を併用することは、Flipped Learningでは認められない。']
exps=[
'1頁は、授業を反転させることが必ずしもFlipped Learningにつながるとは限らないとし、その実践には四つの柱を含めると説明しています。このケースには事前の説明学習と教室の応用活動が記されていますが、全指標の実践までは記録されていません。',
'1頁はFlipped ClassroomとFlipped Learningを同じ意味では用いていません。動画視聴の指示だけから、柔軟な環境や学習文化など四つの柱をすべて実践したと結論することはできません。',
'2頁のF.2は観察と調整、P.1は必要に応じたフィードバックを挙げています。教師による観察や支援は除外されていません。このケースで各支援が実際に十分行われたかは、記録だけでは確定できません。',
'1頁は授業外での文章の読解も取り上げ、2頁のI.2は教材を通常は動画としています。動画以外の教材の併用を禁止していません。ケースの動画は事例の設定であり、すべての反転学習で必須となる媒体ではありません。']
reason='S173原著全2頁とケース8全3段落を照合。反転設計と四本柱の充足を区別する問いへ改訂し、未照合の他教授法やブレンディッド学習分類の断定を除去。動画指示だけで全指標を確認済みとせず、同じ反転領域で単一正答性を確定する。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_O_036']['txt'],exps)]:
 for i,(o,n) in enumerate(zip(olds,news)):
  o=html.unescape(o)
  if o==n:continue
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=o,after=n,reason=reason,sources=['S173'],applied=True,before_version='第113バッチ反映後',block_context='A_O_036' if field=='explanations' else k)
  if field=='options': c['stem_context']=stem
  if field=='explanations': c['paragraph_prefix']=str(i+1)+'（'+('正' if i==0 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S173'],reason=reason,stem_review='ケース8全文と原著1頁のClassroom/Learningの区別、2頁四本柱へ照合。動画指示と応用活動の記録を超えて全指標の実施を推測しない。',explanation_review='全4解説を原著1頁の区別・授業外の文章読解、2頁F.2/P.1/I.2へ照合。記録の十分性を問うもので、ケースに原著の定義を適用する独立判断。最適時間・効果実証・他教授法分類を主張しない。',option_verdicts=['正：反転の記録と全四本柱の確認を区別','誤：動画指示のみから全柱充足を推論','誤：原著の観察・支援を除外','誤：動画以外の教材を禁止'],unresolved='',multiple_correct_risk='なし：1だけが記録の範囲と原著の区別を満たす',no_correct_risk='なし：独立正答1')
for name,obj in [('changes.json',cs+extra),('changes_batch114.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Q_O_036 independently judged;9 ordered changes;key1 retained')
