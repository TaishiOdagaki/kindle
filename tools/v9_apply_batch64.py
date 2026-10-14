"""Resolve question-type and wait-time definitions without universal effect claims."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1289
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
items={
'Q_4_080':(3,'Nunan（1990）が説明する提示質問と参照質問の区別について、最も適当な記述を選べ。',
['提示質問とは、質問者が答えを知らない質問である。','参照質問とは、質問者が答えを知っている質問である。','参照質問とは、質問者が答えを知らない質問である。','提示質問と参照質問の区別は、質問文が疑問詞を含むかどうかだけで決まる。'],
['質問者が答えを知らない質問は、原論文の区別では参照質問です。提示質問とする定義は逆です。','質問者が答えを知っている質問は、原論文の区別では提示質問です。参照質問とする定義は逆です。','原論文第5節では、参照質問を質問者が答えを知らない質問として説明しています。これは質問の知識状態による区別であり、特定の回答長や習得効果を保証するものではありません。','区別の基準は、質問者が答えを知っているかどうかです。疑問詞の有無だけで提示質問か参照質問かを決めることはできません。'],
['定義が逆','定義が逆','原著194頁の定義に一致','知識状態という分類基準と不一致'],['S124']),
'Q_4_081':(4,'Roweが区別したウェイト・タイム1とウェイト・タイム2の説明として、最も適当なものを選べ。',
['ウェイト・タイム1は、遅刻した学習者が着席するまでの時間である。','ウェイト・タイム2は、教師の質問が終わってから学習者の応答が始まるまでの時間である。','ウェイト・タイム1と2は、教師が授業の前に教材を準備する時間を二分したものである。','ウェイト・タイム1は教師の質問後に応答を待つ間、ウェイト・タイム2は学習者の応答後に教師が再び発話するまでに置く間を指す。'],
['ウェイト・タイム1は、教師の質問後に学習者の応答を待つ間です。遅刻者の着席を待つ時間の名称ではありません。','これはウェイト・タイム1の説明です。ウェイト・タイム2は学習者の応答後に教師が再び発話するまでに置く間に関係します。','いずれも授業中の質問・応答のやり取りにおける間の区別です。授業前の教材準備時間を分類したものではありません。','Roweは、教師の質問後の間をウェイト・タイム1、学習者の応答後の間をウェイト・タイム2として区別しています。この問題は間を置く位置の定義を問い、すべての授業に共通する最適な秒数や効果を主張していません。'],
['発問後の間と着席待ちを混同','ウェイト・タイム1と2を逆転','授業内の発話間隔と教材準備を混同','原著の二つの間の位置に一致'],['S125'])}
for key,(ans,stem,opts,exps,verdicts,sources) in items.items():
 reason='原著の分類基準を明示し、初級日本語授業全般への効果や最適秒数を無条件に一般化する説明を除く。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=sources,applied=True,before_version='第63バッチ反映後の累積作業稿')
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==ans else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='原著本文の定義と分類条件に限定して設問・全4肢を独立判定。',explanation_review='全4解説を原著の定義・分類基準に照合。研究効果の普遍化は撤去。',unresolved='',multiple_correct_risk='なし：指定された分類基準に一致する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch64.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
