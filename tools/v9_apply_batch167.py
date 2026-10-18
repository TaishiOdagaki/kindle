"""Evidence versus grammatical impersonality in academic writing guidance."""
import json,html,hashlib
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3353
d=json.loads((p/'decisions.json').read_text());k='Q_4_089';ak='A_4_089';assert d[k]['status']=='要追加確認'
_,q,a=qa.audit(str(b.DST));assert a[ak]['ans']=='2'
block='';paras=[]
for para in Document(b.DST).paragraphs:
 for bm in para._element.iter(qn('w:bookmarkStart')):
  name=bm.get(qn('w:name'),'')
  if name.startswith(('Q_','A_')):block=name
 if block==k:paras.append(para.text)
oldfirst=paras[1];case=paras[2];assert q[k]['stem']==oldfirst+' '+case
stem='次の抜粋を、若者の読書傾向を論じるレポートとして見直す。名古屋大学「レポート課題に備える」の、問いへの答えと理由・根拠を吟味する方針に合う指導を一つ選べ。 '+case
opts=[
'「だから」を「したがって」に変えるだけで、主張を支える根拠を確かめずに完成とする。',
'扱う問いと結論を整理し、読書傾向についての主張を支える資料の出所・調査方法・対象範囲を確かめ、根拠と自分の考察を区別して書き直す。',
'自分の答えや考察をすべて削除し、集めた資料を問いとの関係を検討せずに並べる。',
'「悲しい」を強い感情表現に変えれば根拠は十分になるので、資料の検討は行わない。']
exps=[
'ガイドは、問いへの回答がなぜ合理的なのかを理由や根拠から検討するよう求めています。接続表現の置換だけでは、読書傾向についての主張が何に基づくかを確かめる作業は済みません。',
'ガイドは、自分の回答に理由や根拠を与え、資料を用いる際にも、なぜそう言えるか、どのような調査を経たのかを検討するよう示します。この方針を抜粋に適用し、限られた車内での観察から何が言えるかを吟味する指導です。「と思う」を「と考えられる」に換えるだけで、根拠の確かさが増すわけではありません。',
'ガイドは、自分の考えた部分と資料に書かれた部分を区別して提示することを重視します。自分の答えをすべて消すことでも、問いとの関係を検討せず資料を羅列することでもありません。',
'ガイドの方針は、回答の理由や根拠が十分かを検討することです。感情を強調しても、読書傾向についての主張を支える資料の質や、その主張との関連は確かめられません。']
reason='S225名古屋大学教養教育院・高等教育研究センターの大学教材（笠木雅史、2019-03-01改訂）の全文を取得。問い、理由・根拠、資料の調査過程、自分の考察との区別を全4肢全4解説へ照合。旧客観的文末への置換で客観化するという推論を撤回し、単発の体験を常に禁止する説明も避けた。読書離れの社会的実在は未調査なので、引用事例の主張として吟味する。設問が2段落なので旧第2段落を明示除去し引用の重複を防ぐ。'
def change(field,index,before,after,**kw):return dict(id=k,field=field,index=index,before=html.unescape(before),after=after,reason=reason,sources=['S225'],applied=True,before_version='第166バッチ反映後',block_context=ak if field=='explanations' else k,**kw)
extra=[change('stem',None,oldfirst,stem),change('stem',None,case,'',remove_paragraph=True,previous_paragraph=stem)]
for field,olds,news in [('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'stem_context':stem} if field=='options' else {'paragraph_prefix':str(i+1)+'（'+('正' if i==1 else '誤')+'）'}
  extra.append(change(field,i,old,new,**kw))
assert len(extra)==10
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S225'],reason=reason,option_verdicts=['誤：根拠を検討せず接続表現だけ変更','正：問い・結論と理由根拠の吟味','誤：自分の答えを全削除し無検討に資料羅列','誤：感情の強調を根拠の代用にする'],candidate_answers=[],stem_review='元の引用事例を保持し、大学教材の方針の適用を問う。旧第2段落を削除して単一段落に統合。',explanation_review='全4解説を取得本文へ照合。文末形式による客観性保証、観察や経験の全面禁止を採用しない。社会的読書傾向は独立に確定した事実ではない。',unresolved='',multiple_correct_risk='なし：2のみ理由・根拠を吟味',no_correct_risk='なし：2が条件に一致')
for n,obj in [('changes.json',cs+extra),('changes_batch167.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
f=Path(__file__).resolve().parents[2]/'nagoya167.html';raw=f.read_bytes();(p/'evidence/batch167_sources.json').write_text(json.dumps([dict(source_id='S225',url='https://web.cshe.nagoya-u.ac.jp/resources/asg/prepareessay.html',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-18',read_scope='教材本文全節。作成者・発行者・改訂日も確認。推薦書籍2冊は未取得、社会的読書統計は未取得。',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
