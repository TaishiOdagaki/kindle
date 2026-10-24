"""Two source-driven scope repairs, always build from frozen round40."""
import json,zipfile,hashlib,copy
from pathlib import Path
from lxml import etree as E
from apply_2027_round38 import docx_records,equivalent,rewrite_word,rewrite_xml
from audit_2027_epub import read_epub
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';S=R/'publishing/2027/round40';out=O/'working';out.mkdir(exist_ok=True)
d,W,wn=docx_records(S/'2027_review_manuscript.docx');z,roots,Q,en,_=read_epub(S/'2027_review_manuscript.epub');B={q['id']:q for q in Q};changes=[]
def change(id,reason,**fields):
 a=copy.deepcopy(B[id]);a.update(fields);changes.append(dict(id=id,before=B[id],after=a,reason=reason,source='S04',printed_pages=[14,15,16,18,19]))
e=list(B['Q_1_031']['explanations']);e[0]='相手側や第三者の行為・ものごと・状態などについて、その人物を立てて述べるのは尊敬語です。謙譲語Ⅱ（丁重語）は、基本的には自分側の行為・ものごとなどを、話や文章の相手に丁重に述べます（例：「参ります」「いたします」）。行為者を立てる働きとは区別します。';change('Q_1_031','謙譲語Ⅱを自分自身の動作だけに狭めず、自分側・話や文章の相手という基本的範囲を明示。',explanations=e)
o=list(B['Q_2_019']['options']);o[3]='「謙譲語Ⅱ（丁重語）」は、基本的には自分側の行為・ものごとなどを、話や文章の相手に丁重に述べる。立てるのにふさわしい「向かう先」があってもなくても使うことができる。'
e=list(B['Q_2_019']['explanations']);e[1]='行為の向かう先を立てるのは謙譲語Ⅰ（例：「伺う」「申し上げる」）です。謙譲語Ⅱは、話や文章の相手に丁重に述べる働きであり、両者は立てる対象と丁重に述べる相手を区別して考えます。';e[2]='話や文章の相手に丁重に述べるという中心的な働きは、謙譲語Ⅱの説明です。謙譲語Ⅰは、行為・ものごとなどの「向かう先」を立てます。この「向かう先」には、借りる物の出どころや、指導を受ける相手も含まれ、単なる動作の受け手に限りません。';e[3]='指針18〜19頁の基本的な定義と、「向かう先」の有無に関する説明に対応します。「自分側」には家族なども含まれます。また、「バスが参りました」など、第三者や事物について話や文章の相手に丁重に述べる用法もあります。立てるべき人物の行為を「先生が参ります」のように述べてよいという意味ではありません。';change('Q_2_019','指針18頁の自分側・第三者や事物への用法、16頁の向かう先の説明を反映し、自己行為・行為受け手だけへの限定を修正。',options=o,explanations=e)
changes.extend(json.loads((O/"reader_wording_changes.json").read_text()))
changed=set()
for c in changes:
 id=c['id']
 for f in ['stem','options','explanations']:
  before_values=[c['before'][f]] if f=='stem' else c['before'][f];after_values=[c['after'][f]] if f=='stem' else c['after'][f]
  for k,(before,after) in enumerate(zip(before_values,after_values),1):
   if before==after:continue
   v=str(k)+'. '+after if f=='options' else after;label=None if f in ['stem','options'] else str(k)+'（'+('正' if k==c['after']['answer'] else '誤')+'）'
   rewrite_word(wn[id][f][k-1],v,label);t=en[id][f][k-1];rewrite_xml(t,v,label)
   for n,r in roots.items():
    if t.getroottree().getroot() is r:changed.add(n)
wp=out/'2027_independent_working.docx';ep=wp.with_suffix('.epub');d.save(wp)
with zipfile.ZipFile(ep,'w') as oz:
 for i in z.infolist():oz.writestr(i,E.tostring(roots[i.filename],encoding='utf8',xml_declaration=True) if i.filename in changed else z.read(i.filename))
_,NW,_=docx_records(wp);_,_,N,_,qa=read_epub(ep);WM={q['id']:q for q in NW};assert len(N)==500 and all(equivalent(q,WM[q['id']]) for q in N);assert all(q['answer']==B[q['id']]['answer'] for q in N)
(O/'manuscript_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n');(O/'working_verification.json').write_text(json.dumps(dict(questions=500,word_epub_question_fields_match=500,keys_changed=0,docx_sha256=hashlib.sha256(wp.read_bytes()).hexdigest(),epub_sha256=hashlib.sha256(ep.read_bytes()).hexdigest(),epub_qa=qa,visual_qa_completed=False,publication_approved=False),ensure_ascii=False,indent=2)+'\n')
rows=json.loads((O/'ledger_500.json').read_text());NM={q['id']:q for q in N}
for r in rows:
 if r['id'] not in [c['id'] for c in changes]:continue
 r['current_question_sha256']=hashlib.sha256(json.dumps(NM[r['id']],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 r['manuscript_change_applied']=True
 if r['id'] in ['Q_1_031','Q_2_019']:
  r.update(status='修正反映・再確認済み',manuscript_change_required=False,explanation_finding='修正後の選択肢・解説を指針16・18〜19頁へ再照合。正答は一意に維持。')
 elif r['reviewed_this_pass']:
  r.update(status='再確認済み',editorial_change_required=False,editorial_finding='内容を再確認したうえで制作履歴だけを整理。')
 else:r['editorial_finding']='制作履歴の表現のみ整理。原典の新規再監査は未着手のまま。'
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('12 repairs applied;500 full-field matches;0 key changes;visualQA pending')
