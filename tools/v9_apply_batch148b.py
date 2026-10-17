"""One-time correction after checking the linked non-progressive teiru uses."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3000
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
k='Q_O_031';ak='A_O_031';assert a[ak]['ans']=='4'
oldcase=next(p.text for p in Document(b.DST).paragraphs if p.text.startswith('中級クラスの学習者が提出した作文に、次のような文があった。'))
newcase='中級クラスの学習者が提出した作文に、次のような文があった。「わたしは日本に来る前に、日本語を三年間勉強しています。」この学習者は作文を書いた時点で既に来日している。教師は、来日前の学習だから文末の「ています」は誤用だと判断した。しかし、別の教師から、過去の学習経験を述べる用法も考えられるので、本人の意図や文脈を確認して検討しようという提案があった。'
stem='ケースの「日本語を三年間勉強しています」という表現の検討として、最も適当なものを一つ選べ。'
opts=['「日本語」「勉強」という漢字表記そのものが誤っていると断定する。','「ています」は進行しか表さないので、過去の経験を述べる用法は認められないとする。','「日本語を」の「を」は誤りなので、文脈にかかわらず「日本語に」に直す。','「ています」には過去の経験や記録を述べる用法もあるため、来日前のことだという理由だけで誤用と断定せず、意図や文脈を確かめる。']
exps=['大学教材にも「日本語を勉強しています」という表記の例があります。漢字表記そのものを誤りとする根拠はありません。','「ています」は進行のほか、結果の状態、動きの繰り返し、過去の経験や記録などを表すことがあります。進行だけに限定する説明は誤りです。','大学教材にも「日本語を勉強しています」という例があります。「を」を文脈にかかわらず「に」に替える必要はありません。','大学教材には、過去の経験を述べる「3年前アメリカで勉強しています」という例があります。この用法を考慮すると、来日前の学習というだけでは誤用と断定できません。過去の継続を述べたいなら「勉強していました」なども検討できますが、どの形が意図に合うかは文脈とともに確認します。']
reason='S211のリンク先S212「Vています（状態）」本文全体を追加取得・精読。第5項は過去の経験・記録、例5は3年前アメリカで勉強していますを示す。直前の暫定改訂でも過去の期間という条件だけで現在継続形の誤用と扱った点を、公開前の拡張照合で撤回。教師の最初の断定をケース中の検討対象として明示し、単一正答4は「ている」の複数用法を考慮した文脈・意図確認とした。Q_O_032も誤用を確定した前提でなく、教師が当初そう判断した表現の背景検討へ問いを限定し、同問の資料照合未了は維持。'
extra=[dict(id='CASE_O_07',field='case_text',index=None,before=oldcase,after=newcase,reason=reason,sources=['S211','S212'],applied=True,before_version='第148バッチ初稿適用後・公開前追加照合')]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  assert html.unescape(old)!=new
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S211','S212'],applied=True,before_version='第148バッチ初稿適用後・公開前追加照合',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
k2='Q_O_032';newstem='教師が当初誤用と判断した表現の背景を、母語の影響と目標言語内部の規則の適用という観点から検討する際、確認すべきこととして最も適当なものを一つ選べ。'
extra.append(dict(id=k2,field='stem',index=None,before=html.unescape(q[k2]['stem']),after=newstem,reason=reason,sources=['S211','S212'],applied=True,before_version='第148バッチ初稿適用後・公開前追加照合',block_context=k2))
assert len(extra)==11
d[k].update(sources=['S211','S212'],reason=reason,option_verdicts=['誤：教材にもある漢字表記自体を誤りと断定','誤：過去経験・記録等の用法を排除','誤：教材にもあるをを一律ににへ替える','正：過去経験・記録の用法を考慮し、時点だけで誤用と断定しない'],stem_review='過去の学習経験を述べる用法を認め、教師の誤用という断定自体を検討対象に修正。',explanation_review='S211・S212本文全体の進行・過去形・結果状態・反復・過去経験と例文に全4解説を照合。',multiple_correct_risk='なし：教材の複数用法に合うのは4のみ',no_correct_risk='なし：独立正答4')
assert d[k2]['status']=='要追加確認'
d[k2]['reason']+=' 第148バッチ追加照合：設問の誤用確定前提を、教師の当初の判断という対象へ限定。ているの過去経験用法を排除しない。'
d[k2]['unresolved']='選択肢4と全4解説の原因分析の根拠および、誤用が確定していないケースとの整合を再照合する。追加改訂が必要であり確認済みにはしない。'
for n,obj in [('changes.json',cs+extra),('changes_batch148b.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'tufs045-148.html').read_bytes()
e=dict(source_id='S212',title='Vています（状態） 解説',institution='東京外国語大学言語モジュール',url='https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/045.html',retrieved='2026-10-18',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope='解説本文1〜9・例文1〜10・注記を全て精読。特に第5項の過去経験・記録と例5を照合。',limitations='個別の学習者の発話意図をこの資料だけで確定しない。過去の話だからているは誤用という断定を撤回。',full_source_redistributed=False)
(b.OUT/'evidence/batch148b_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('11 follow-up edits; Q_O_032 remains unverified')
