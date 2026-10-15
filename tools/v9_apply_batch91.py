"""One-time Thomas original-text review; never replay over later decisions."""
import json, html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text()); assert len(c)==2030
d=json.loads((b.OUT/'decisions.json').read_text())
_,q,a=qa.audit(str(b.DST)); qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_5_096':(1,'Thomas（1983）の区別に基づく社会語用論（sociopragmatics）の説明として、最も適切なものを一つ選びなさい。',[
'相手との関係や依頼の負担など、言語使用の社会的条件を扱う。',
'発話の意図や相手との関係を除外し、文の真偽条件だけを扱う。',
'言語形式の配列規則だけを扱い、使用場面は扱わない。',
'語用言語学との区別はなく、どちらも形態素の接続だけを扱う。'],[
'相手との距離、権利・義務、負担の評価などが対象となります。学問領域を単独の能力名とは同一視しません。',
'真偽条件だけに対象を限定すると、言語使用の社会的条件が抜け落ちます。',
'形式の配列だけに限定する説明は、ここで問う社会的条件を扱っていません。',
'語用言語学は形式と語用的な力の対応に関わります。形態素接続だけではありません。両領域の境界は連続的です。'],[
'正：社会的条件を対象にする','誤：社会的条件を除外','誤：使用場面を除外','誤：形式と語用的な力の対応を接続規則に限定']),
'Q_5_097':(3,'次は指導方針を考えるための架空の事例である。上級学習者Aは社員から飲み会に誘われ、「いいえ、行けません。その日は予定があります」と断った。社員は冷たい印象を受けたと述べた。Thomas（1983）のメタ語用的気づきを重視する立場に照らし、最も適切な指導方針を一つ選びなさい。',[
'社員の感想だけでAの人格を判断し、失礼な人だと指導する。',
'文法的な文なら検討は不要とし、意図や受け取り方は話し合わない。',
'Aの意図と社員の受け取り方を確かめ、関係や場面に応じた表現の選択肢を話し合う。',
'一つの断り方だけを全場面の規範として暗記させ、Aが別の表現を選ぶ余地は認めない。'],[
'この感想だけからAの人格や原因を決めることはできません。事例は実際の調査結果ではありません。',
'文法上の正しさだけでは、意図と解釈のずれを検討できません。',
'意図・解釈・場面を検討し、理解した上での選択を支えます。この日本語表現を常に不適切とはしていません。',
'唯一の規範への同調を強いる方針は、学習者の判断と選択を尊重する指定の立場に合いません。'],[
'誤：受け手の感想から人格を断定','誤：意図・解釈の検討を排除','正：意図と解釈を確かめ選択肢を検討','誤：全場面共通の唯一規範を強制']),
'Q_5_098':(3,'Thomas（1983）の区別に基づき、社会語用論的な行き違いを示すものを一つ選びなさい。以下は原因を明示した架空の事例であり、民族全体の慣習を述べたものではない。',[
'依頼してよい相手かという判断は共有されているが、学習者が表現に込めた依頼の強さと相手の解釈が異なった。原因はその表現の慣習的な力を知らないことだった。',
'相手との関係の判断にはずれがなく、記録では意図した語を発音し損ねたことだけが原因だった。',
'表現の意味や依頼の強さは共有されていたが、学習者は相手に頼んでよい事柄だと判断し、相手はその関係では頼まれるべきでない事柄だと判断した。',
'相手との関係の判断にはずれがなく、記録では意図した文と違う助詞を選んだことだけが原因だった。'],[
'ここで明示された原因は、形式と語用的な力の対応のずれであり、社会的判断のずれではありません。',
'この設定は発音上の誤りを原因としています。実際の会話の原因が常に一つだという主張ではありません。',
'頼んでよい事柄かという権利・義務の評価にずれがあります。発話の形だけから母語転移と診断していません。',
'この設定は助詞の選択を原因としています。敬語などの文法形式と社会的判断が一般に無関係という意味ではありません。'],[
'誤：明示された原因は語用的な力の対応','誤：明示された原因は発音の誤り','正：依頼してよい事柄かという社会的判断のずれ','誤：明示された原因は助詞選択'])}
extra=[]; removed=0
reason='S150 Thomas1983原論文の公開本文（99〜101、104〜105、109〜110頁）を照合。社会語用論と語用言語学の混同、単一の日本語規範の強制、褒めへの肯定応答を常に失敗とする断定を撤回。事例は原因を明示した教材用創作であり原論文の実証結果ではない。'
for k,(ans,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']!='確認済み' and int(a['A_'+k[2:]]['ans'])==ans
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']]
 assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S150'],applied=True,before_version='第90バッチ反映後の累積作業稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options': e['stem_context']=stem
   if field=='explanations': e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:
     extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問の継続段落を明示削除して統合。'+reason)); removed+=1
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S150'],reason=reason,option_verdicts=verdicts,stem_review='指定原著の区別・指導上の立場と、原因を明示した架空事例から全4肢を独立判定。単発の発話から人格や母語転移を推測しない。',explanation_review='4解説の根拠はS150本文99〜101、104〜105、109〜110頁。AI要約・検索抜粋は不使用。原著が示す境界の連続性と学習者の選択を保持。日本語固有の断り・褒め応答の実証研究を承認したものではない。',unresolved='',multiple_correct_risk='なし：指定の理論と明示条件に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27+removed
for name,obj in [('changes.json',c+extra),('changes_batch91.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(f'3 full reviews; {len(extra)} edits; {removed} explicit old-stem removals')
