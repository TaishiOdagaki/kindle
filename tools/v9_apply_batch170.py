"""Citation conditions: section32 versus source attribution, no shortcut."""
import json,html,hashlib
from pathlib import Path
from lxml import etree
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3372
d=json.loads((p/'decisions.json').read_text());k='Q_M_042';ak='A_M_042'
assert d[k]['status']=='要追加確認'
_,q,a=qa.audit(str(b.DST));assert a[ak]['ans']=='4'
stem='教材に、著作権の保護対象となる公表済みの文章を複製して載せる。著作権法第32条第1項の引用と第48条の出所明示に関する説明として、最も適当なものを選べ。'
opts=[
'「引用」と表示すれば、公正な慣行や目的に照らした範囲を検討せず、どの作品も無制限に全文転載できる。',
'引用は他人の著作物を利用する行為には当たらないので、著作権法の検討は不要である。',
'出所を示しさえすれば、第32条第1項の他の条件を満たさなくても、許諾なしで掲載できる。',
'公正な慣行と引用目的に照らした正当な範囲を確かめ、引用部分を明確にし、利用態様に応じ合理的な方法・程度で出所を示す。']
exps=[
'第32条第1項は、引用が公正な慣行に合い、目的上正当な範囲内であることを求めます。「引用」と名付ければ無制限に転載できるという制度ではありません。一方、文化庁テキストは、俳句のような短い作品等で全部を引用する場合もあり得ると説明しており、全文の利用を例外なく禁止する趣旨でもありません。',
'第32条第1項は、他人の著作物を引用して利用できる条件を定めています。文化庁テキストも、引用を、許諾なしで利用できる場合の権利制限として説明します。著作物の利用とは無関係だとする説明は誤りです。',
'出所を示す義務と、第32条第1項の引用の条件は別々に確かめます。文化庁テキスト77頁は、出所を示しても法律上の利用条件を満たさない場合には了解が必要だと説明しています。出所の表示だけで他の条件を免除することはできません。',
'第32条第1項の条件と、第48条の出所明示をともに確認する方針です。文化庁テキスト75頁は、文章では括弧等で引用箇所を明確にすることや、本文との関係、利用分量を検討するよう説明します。第48条第2項の著作者名については、出所表示に伴い明らかになる場合や無名の著作物の場合の扱いもあります。出所表示だけで引用全体の適法性を保証する説明ではありません。']
reason='S26 e-Gov APIの第32条・第48条を再取得し本則本文へ照合。S227文化庁令和8年度著作権テキスト印刷75・77頁（PDF78・80頁）の本文・画像を取得照合。公表、公正慣行、目的上正当範囲、出所を別々に確認し、出所だけで許諾不要になる誤解を避ける。全部引用が可能な短い作品等の留保も反映し、全文引用は常に違法とはしない。S10は第35条資料であり本問根拠として引き継がない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==3 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
  extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S26','S227'],applied=True,before_version='第169バッチ後',block_context=ak if field=='explanations' else k,**kw))
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S26','S227'],reason=reason,option_verdicts=['誤：目的や慣行を検討せず全作品を無制限転載','誤：著作物の利用と法令の適用を否定','誤：出所表示で他の引用条件を免除','正：引用条件と出所明示を別途確認'],candidate_answers=[],stem_review='保護対象の公表済み文章を教材へ複製する場面に限定し、第32条第1項と第48条を問う。他の権利制限・許諾契約の全類型を扱わない。',explanation_review='全4解説を条文と令和8年度文化庁資料へ照合。全文引用の可能性、出所表示だけでは不足、著作者名表示の留保を含む。全119頁・全法改正・個別事件適法性を承認しない。',unresolved='',multiple_correct_risk='なし：4のみ引用条件と出所をともに確認',no_correct_risk='なし：4が対象条文の方針に一致')
for n,obj in [('changes.json',cs+extra),('changes_batch170.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'egov170.xml').read_bytes();t=etree.fromstring(raw);assert t.findtext('Result/Code')=='0'
entries=[]
for sid,fn,url,scope in [('S26','egov170.xml','https://laws.e-gov.go.jp/api/1/lawdata/345AC0000000048','本則第32条全項と第48条全項。第169バッチ時点以前の既取得応答とSHA256同一。API1の施行日メタデータは不明のため全改正・経過措置を確認済みとはせず、2026年度文化庁資料の対象説明と照合。'),('S227','bunka170.pdf','https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/pdf/94383901_01.pdf','令和8年度版、全119頁の原PDF取得。印刷75頁引用全条件・注記、印刷77頁出所説明の本文、PDF78・80頁画像。全119頁精読ではない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-18',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch170_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
