"""Resolve two recast examples against Lyster and Ranta's six-category taxonomy."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==1260
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
items={
 'Q_4_019':(3,
 'LysterとRanta（1997）の分類に照らし、次の教師の応答のうちリキャストに当たるものを一つ選びなさい。',
 [
 '学習者：「昨日、服を買いました。安かったではありません。」教師：「『安かったではありません』ではなく、『安くなかったです』と言います。」',
 '学習者：「昨日、服を買いました。安かったではありません。」教師：「すみません、もう一度言ってください。」',
 '学習者：「昨日、服を買いました。安かったではありません。」教師：「ああ、安くなかったんですね。」',
 '学習者：「昨日、服を買いました。安かったではありません。」教師：「今の否定の形に誤りがあります。イ形容詞の過去の否定形を確認しましょう。」'],
 [
 '誤った表現を特定し、正しい形を明示しているため、明示的訂正に当たります。',
 '教師は正しい形を提示せず、学習者に発話の反復を求めています。原論文の明確化要求に対応し、教師自身が誤りを取り除いて言い換えるリキャストではありません。',
 '教師は誤りを明示的に指摘せず、学習者の発話の一部を誤りのない形へ言い換えています。原論文のリキャストの分類に対応します。',
 '発話の形式に関するコメントを与え、正しい形そのものは提示していないため、メタ言語的フィードバックに当たります。'],
 ['明示的訂正：誤りの特定と正用提示','明確化要求：反復要求、正用提示なし','リキャスト：暗示的な正用への再定式化','メタ言語的フィードバック：形式へのコメント、正用提示なし']),
 'Q_4_039':(1,
 'LysterとRanta（1997）の分類に照らし、次の教師の応答に含まれる訂正の技法として最も適当なものを選べ。学習者：「映画はとても面白かったでした。」教師：「ああ、とても面白かったんですね。」',
 ['リキャスト','明示的訂正','明確化要求','誘導（エリシテーション）'],
 [
 '教師は誤りを明示的に指摘せず、学習者の発話を誤りのない形へ言い換えています。原論文のリキャストに対応します。この分類だけから、学習者が訂正に気づいたか、習得が進んだかまでは判断できません。',
 '明示的訂正は、発話が誤っていることを明確に示し、正しい形を提示する方法です。この応答には誤りを明示する表現がありません。',
 '明確化要求は、発話の理解や形式に問題があることを伝え、反復や言い換えを求める方法です。この応答では学習者への反復要求ではなく、教師自身が正しい形を示しています。',
 '誘導は、空欄を補う発話や正しい言い方を尋ねる質問、言い直しの要求などを用いて、学習者自身から正しい形を引き出す方法です。この応答では教師が正しい形を提示しています。'],
 ['リキャスト：暗示的な再定式化','誤りの明示がなく明示的訂正でない','反復・言い換えの要求でない','学習者から正用を引き出す要求でない'])}
for key,(ans,stem,opts,exps,verdicts) in items.items():
 reason='原著46–49頁の6分類に条件を対応させ、分類の混線と効果の無条件な一般化を除く。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   entry=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S37'],applied=True,before_version='第61バッチ反映後の累積作業稿')
   if key=='Q_4_039' and field=='stem':
    entry['before']='以下の授業場面において、教師が行っているフィードバックの技法として最も適切なものはどれか。'
    extra.append(entry)
    for text in ['学習者：「昨日、友達と映画に行きました。とても面白かったでした。」','教師：「あぁ、映画がとても『面白かった』んですね。誰と行ったんですか？」']:
     extra.append(dict(entry,field='case_text',before=text,after='',remove_paragraph=True,reason='設問が3段落に分かれているため旧会話段落を明示的に除去。'))
    continue
   if field=='options':entry['stem_context']=stem
   if field=='explanations':entry['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==ans else '誤')+'）'
   extra.append(entry)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S37'],option_verdicts=verdicts,reason=reason,stem_review='原著の6分類を指定し、誤り指摘・正用提示・反復要求・学習者の正用産出要求を独立に比較。',explanation_review='4解説を原著46–49頁の分類条件へ照合。分類と気づき・長期習得効果を区別。',unresolved='',multiple_correct_risk='なし：明示した応答と原著分類に一致する選択肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',cs+extra),('changes_batch62.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
