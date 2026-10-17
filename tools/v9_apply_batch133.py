"""One-time evidence-bounded drill classification revision."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2824
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_033';ak='A_4_033'
assert d[k]['status']=='修正必要' and a[ak]['ans']=='2'
stem='教師が「私はパンを食べます。寿司」と示すと、学習者一人が「私は寿司を食べます」と答えた。続いて教師が「買います」と示すと、同じ学習者が「私は寿司を買います」と答えた。語句の扱いに注目して、この練習の説明として適切なものを一つ選べ。'
opts=['変換練習として、肯定文を否定文にするなど、文の文法構造を変えている。','置換練習として、文の文法構造を保ちながら、示された語句を入れ替えている。','斉唱による反復練習として、教師の発話を変えずにクラス全員が一緒に繰り返している。','個別の反復練習として、教師の発話を変えずに学習者一人がそのまま繰り返している。']
exps=['用語集の変換練習は、文を別の文法構造に変えるものです。この例は肯定文を否定文にする操作ではなく、同じ構造で目的語や動詞を入れ替えています。','用語集の置換練習は、教師が示した語句を同じ構造の文に代入するものです。この例では「パン」を「寿司」に、続いて「食べます」を「買います」に替えています。','用語集の斉唱による反復では、教師が言った語や文をクラスで一緒に繰り返します。設問では一人が答え、発話内の語句も替えているため、この説明は合いません。','用語集の個別の反復では、一人が教師の言った語や文を繰り返します。設問でも一人が答えていますが、発話をそのまま反復せず、語句を文に代入しています。']
reason='S183 Cambridge TKT Glossary印刷14/PDF15のDrill全項目を本文・画像で再取得照合。変換・置換・斉唱反復・個別反復の定義に基づき、語句の操作と参加形態を明示した独自の日本語会話例で四肢を照合。結合・応答の未取得の定義と単一／複数スロット分類は改訂から除く。同じドリル分類の学習領域と正答2を維持。S195の列挙だけを定義の根拠にしない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S183'],applied=True,before_version='第132バッチ時点（原稿は第131バッチ）',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S183'],reason=reason,option_verdicts=['誤：否定などへの構造変換ではない','正：同じ文法構造で目的語・動詞を入れ替える','誤：全員斉唱でも原発話の同一反復でもない','誤：一人という点は合うが原発話をそのまま反復していない'],stem_review='語句の扱いを判断対象とし一人の応答を明示。選択肢を名称だけでなく定義付きにし、置換と個別という分類軸が併存する曖昧さを回避。',explanation_review='全4解説をDrill本文の4定義と独自会話に照合。未照合のスロット分類、結合・応答の定義、教授効果の主張は残さない。',unresolved='',multiple_correct_risk='なし：各肢の説明全体として正しいのは2',no_correct_risk='なし：独立正答2')
for name,obj in [('changes.json',cs+extra),('changes_batch133.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'tkt-glossary.pdf').read_bytes()
(b.OUT/'evidence/batch133_sources.json').write_text(json.dumps(dict(source_id='S183',url='https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf',retrieved='2026-10-17',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),body_and_image_read='printed 14 / PDF 15, entire Drill entry',scope='Four drill definitions only. No whole glossary or underlying learning-effect studies approval.',full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
