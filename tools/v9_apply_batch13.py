#!/usr/bin/env python3
"""Repair no-answer premise and unrestricted you-ni-naru analysis."""
import json,html
from docx import Document
from docx.oxml.ns import qn
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==262
_,Q,A=qa.audit(str(b.DST));doc=Document(b.DST);extra=[]
def change(k,f,i,new,why,s):
 old=Q[k]['opts'][i] if f=='options' else A['A_'+k[2:]]['txt'][i]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=f,index=i,before=old,after=new,reason=why,sources=s,applied=True,before_version='第12修正バッチ作業稿'))
def full(k,stem,opts,exps,why,s):
 ps=doc.paragraphs;start=next(i for i,p in enumerate(ps) if any(t.get(qn('w:name'))==k for t in p._p.iter(qn('w:bookmarkStart'))));old=[]
 for p in ps[start+1:]:
  if p.text.startswith('1. '):break
  if p.text:old.append(p.text)
 assert ' '.join(old)==html.unescape(Q[k]['stem'])
 extra.append(dict(id=k,field='stem',index=None,before=old[0],after=stem,reason=why,sources=s,applied=True))
 for t in old[1:]:extra.append(dict(id=k,field='stem_continuation',index=None,before=t,after='',reason='全文改稿に伴い旧場面・例文段落を除去。',sources=s,applied=True,remove_paragraph=True))
 for f,ts in [('options',opts),('explanations',exps)]:
  assert len(ts)==4
  for i,t in enumerate(ts):change(k,f,i,t,why,s)
why='Oxfordの6分類を明示。連想記憶を認知方略とした分類混同と、質問行動は全て補償方略ではないという一般化を撤回。'
full('Q_O_071','Oxford（1990）の6分類では、学習計画を立て、進捗を定期的に自己評価する方略はどれか。',Q['Q_O_071']['opts'],['情意方略は感情の調整を扱います。','社会的方略は他者との相互作用を扱います。','この分類の認知方略には練習や分析などがあり、学習計画・自己評価は別の群です。','計画・自己モニタリング・自己評価はメタ認知方略です。'],why,['S47'])
full('Q_O_072','Oxford（1990）の6分類では、語彙を既知の語やイメージと関連づけ、記憶に定着させる方略はどれか。',['情意ストラテジー','記憶ストラテジー','メタ認知ストラテジー','補償ストラテジー'],['情意方略は感情の調整を扱います。','関連づけやイメージによる記憶は記憶方略に分類されます。','メタ認知方略は計画や自己評価を扱います。','補償方略は未知の意味の推測や言い換えなどで知識不足を補います。'],why,['S47'])
full('Q_O_073','Oxford（1990）の6分類では、相手の説明が不明なときに明確化を求めたり、自分の理解が合っているか相手に確認したりする質問は、どの群の例か。',Q['Q_O_073']['opts'],['補償方略にも援助を求める例はありますが、ここで指定した明確化・確認の質問は社会的方略の例です。','明確化・確認を求める質問は、社会的方略に含まれます。','記憶方略は情報の保持・取り出しを助ける方略です。','認知方略の練習・分析などと、指定された対人的な質問の分類は区別します。'],why,['S47'])
(b.OUT/'changes_batch13.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
vs={'Q_O_071':['感情調整ではない','対人的相互作用ではない','計画・評価は認知群と別','計画・自己評価はメタ認知群'], 'Q_O_072':['感情調整ではない','関連づけ・イメージは記憶群','計画・評価ではない','知識不足を補う推測・言い換えではない'], 'Q_O_073':['援助の例はあるが明示された明確化・確認は社会的群','表IIの質問例に一致','保持・取り出しの工夫ではない','表IIの対人的質問として分類される']}
for k,ans in [('Q_O_071',4),('Q_O_072',2),('Q_O_073',2)]:
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=['S47'],option_verdicts=vs[k],stem_review='Oxford1990の6分類と具体的行動を明示し全4肢を独立判定。',explanation_review='著者自身の章、印刷頁71–75の本文・表I/IIを4解説に照合。表は版面画像でも確認。体系をまたぐ一般化をしない。',multiple_correct_risk='なし：分類体系と行動を指定',no_correct_risk='なし：独立正答が存在',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(extra),'repairs.')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S47 | Rebecca L. Oxford (1990), Styles, Strategies, and Aptitude: Connections for Language Learning, in Parry & Stansfield (eds.), [Language Aptitude Reconsidered](https://files.eric.ed.gov/fulltext/ED321573.pdf), pp.67–125 | 著者本人の章の印刷頁71–75（PDF77–81頁）の本文と表I/IIを取得し、画像で分類の所属も確認。6分類、関連づけ・イメージの記憶群、計画・自己評価のメタ認知群、明確化・確認質問の社会的群。1990年単行本由来の表が本人の章に掲載。章全体の実証的主張を一括承認しない。 | Q_O_071–073 |\n')
