"""One-time audit of the pedagogical role of early Taiwanese translation material."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2874
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_1_023';ak='A_1_023'
assert d[k]['status']=='修正必要' and a[ak]['ans']=='4'
stem='伊沢修二の時期の台湾の日本語対訳教材について、渡邉俊彦の教材分析（2015）が示す特徴に合う説明を一つ選べ。'
opts=['日本語の意味を説明する際、台湾語を媒介として用いることを一切認めていなかった。','台湾語の訳文を載せる主な目的は、日本語の理解を助けることではなく、模範的な台湾語の文章表記法を確立することだった。','台湾語の対訳文は、原文の日本語の語順や表現の影響を全く受けていなかった。','日本語の原文に漢字表記の台湾語の訳文を並べ、日本語の理解を助けるために利用していた。']
exps=['教材分析は、理解の導入段階に台湾語を媒介させる方針を示しています。台湾語を一切排除するという説明は合いません。','分析では、台湾語文は日本語の理解を助ける用途とされ、台湾語の文章表記法や模範的な台湾語を制定することが目的だったとは言い難いと述べられています。','分析では日本語の語順に即した対訳例を取り上げています。台湾語の対訳文が日本語の影響を全く受けていないとは説明できません。','分析は、日本語に漢字を用いた台湾語の訳文を並べる方法と、日本語理解を助ける役割を示しています。台湾語を日本語の意味理解に用いる対訳教材の特徴に合います。']
reason='渡邉俊彦（2015）の大学紀要論文を含む第132号PDF全312頁を取得・全頁テキスト読込みし、当該論文の印刷170–178頁（PDF181–189頁）の本文を精読。対訳例とその用途、語順への影響、1895年教授書からの引用を前後の解釈と照合。印刷177–178頁を画像でも確認した。歴史・教授法の領域を維持し、取得した教材分析の説明を問う条件へ限定。原問の学堂設立年・事件・後続制度への発展、未取得の山口教授法との比較は撤回し、未照合の歴史事実を追加承認しない。1895年教授書の全冊そのものは未取得であり、原著全冊を精読したとの扱いにはしない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S200'],applied=True,before_version='第137バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S200'],reason=reason,option_verdicts=['誤：理解導入で台湾語を媒介に用いる方針に反する','誤：模範的台湾語の制定を主目的とする説明は分析に反する','誤：日本語の語順に即した例が分析されている','正：漢字表記の台湾語訳文と日本語理解の支援が分析に合う'],stem_review='特定の取得済み教材分析の記述に限定し、対訳教材の媒介言語・用途・文体の全4肢を独立に照合。',explanation_review='全4解説を印刷170–178頁の本文・教材例・引用と照合。論文中で可能性として述べられる教育観を普遍的事実にはしない。',unresolved='',multiple_correct_risk='なし：分析に合うのは独立正答4のみ',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',cs+extra),('changes_batch138.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
f=Path(__file__).resolve().parents[2]/'takushoku132.pdf';raw=f.read_bytes()
(b.OUT/'evidence/batch138_sources.json').write_text(json.dumps(dict(source_id='S200',author='渡邉俊彦',title='対訳日本語教材における伊沢修二の教育観とその台湾語の文体',journal='拓殖大学語学研究132（2015年3月）169–193頁',url='https://journal.takushoku-u.ac.jp/lcri/lcri_132.pdf',retrieved='2026-10-17',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),downloaded_pdf_pages=312,read_scope='Printed170–178 / PDF181–189 body and examples; printed177–178 visually inspected. Complete issue acquired, not all articles closely read.',historical_primary_book_status='1895 original book full volume not acquired; quotations and analysis in Watanabe only.',full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
