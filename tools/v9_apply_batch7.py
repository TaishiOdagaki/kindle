#!/usr/bin/env python3
"""One-time evidence-based accent repairs; cumulative rebuild is separate."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==158
_,Q,A=qa.audit(str(b.DST));extra=[]
def full(k,stem,opts,exps,why,sources):
 for f,old,new in [('stem',[Q[k]['stem']],[stem]),('options',Q[k]['opts'],opts),('explanations',A['A_'+k[2:]]['txt'],exps)]:
  assert len(old)==len(new)
  for i,(x,y) in enumerate(zip(old,new)):
   x=html.unescape(x)
   if x!=y:extra.append(dict(id=k,field=f,index=None if f=='stem' else i,before=x,after=y,reason=why,sources=sources,applied=True,before_version='第6修正バッチ作業稿'))
full('Q_5_025','共通語の単語アクセントを「下がり目」に着目して説明する考え方について、適切なものはどれか。',[
 '文の中でも全ての単語で1拍目と2拍目の高さは必ず異なり、文全体のイントネーションは考慮しなくてよい。',
 '単語の意味を区別するアクセントの下がり目と、文やフレーズの初めに現れる上昇は、必ず同じ機能を持つ。',
 '単語単独の発音で覚えた高低の並びをそのまま文中の全ての位置に当てはめれば、文の自然な音調を常に説明できる。',
 '単語ごとの下がり目の有無と位置を確認し、文やフレーズ全体のイントネーションとの関係も考えて発音を捉える。'],[
 '単独の語で示した高低の並びが文中でも常にそのまま実現するとは限りません。第1拍と第2拍はどんな場合にも必ず高さが違う、と一般化する旧説明は撤回します。',
 '下がり目による単語アクセントの説明では、語ごとの下がり目と文やフレーズの初めの上昇を区別します。上昇はフレーズの音調とも関わり、同じ機能とする説明は適切ではありません。',
 '単語だけの発音で示した高低と、文の中で実現する高さが一致しない場合があります。文全体の音調を無視して一律に適用する説明は適切ではありません。',
 '下がり目に着目する説明では、単語の下がり目があるか、あるならどこかを確認します。それに文やフレーズのイントネーションを合わせて考えることで、単語だけの高低表記と文中での実現を混同せずに捉えられます。'],
 '第1・2拍の高低は必ず異なるという無条件の旧正答を撤回。JF2025年の公式解説に基づき単語アクセントとフレーズ音調を区別。',['S35'])
full('Q_5_026','共通語アクセントの基本的な型を、語を単独のフレーズとして発音したときの高低で模式的に示す。助詞「が」が続く場合も含め、型と表記の正しい組合せはどれか。Hは高、Lは低を示す。',[
 '平板型の「はな（鼻）」＋「が」：L・H・L',
 '頭高型の「はし（箸）」＋「が」：H・L・L',
 '中高型の「あなた」＋「が」：L・H・H・H',
 '尾高型の「はな（花）」＋「が」：L・H・H'],[
 'この模式表記では、平板型の「鼻が」はL・H・Hとなります。選択肢は助詞で下降する表記になっており、平板型の説明と合いません。',
 '「箸」は第1拍にアクセント核があります。模式的には「は」が高く、「し」と後続助詞が低くなるH・L・Lであり、この組合せが正しいものです。',
 '「あなた」は第2拍「な」にアクセント核がある中高型です。この模式表記ではL・H・L・Lとなり、選択肢は下がり目を示していません。',
 '尾高型の「花が」は、語末「な」の後で下がるL・H・Lとなります。選択肢のL・H・Hはこの模式表記では平板型に対応します。'],
 '玉子を中高型の例とした旧解説を撤回し、TUFSが型と位置を明示した鼻・箸・あなた・花を使用。単独フレーズの模式表記である条件も明示。',['S35','S36'])
(b.OUT/'changes_batch7.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
for k,answer,s in [('Q_5_025',4,['S35']),('Q_5_026',2,['S35','S36'])]:
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=answer,sources=s,option_verdicts=[('条件と公式教材に一致' if i==answer else '改訂解説に示した型又は音調の説明と不一致') for i in range(1,5)],stem_review='下がり目の説明又は単独フレーズの模式表記の条件を明示し全4肢を判定。',explanation_review='JF2025年解説及びTUFSの型・語例・核位置に照合。',multiple_correct_risk='なし：4肢を独立再判定',no_correct_risk='なし：独立正答が存在',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print('Recorded',len(extra),'repairs.')
