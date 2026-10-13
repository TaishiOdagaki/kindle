#!/usr/bin/env python3
"""Evidence-bound reading/listening revisions. One-time batch 51."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==974
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,reason,sources,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   if html.unescape(before)==after:continue
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第50修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='取得した本文の定義と条件に限定し、4肢を独立判定。',explanation_review='全4解説を根拠本文へ照合。本文にない一般的効果・全称命題を撤去。',unresolved='',multiple_correct_risk='なし：指定された定義・手順に合うのは正答のみ',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_5_030',3,
 '東京外国語大学公開教材「朝鮮語を知る―音韻」の音韻体系の説明に照らし、最も適切なものはどれか。',
 ['母音/a/は存在せず、単母音の表にも含まれない。','子音はすべて摩擦音であり、[p]・[t]・[k]のような閉鎖音は存在しない。','平音・激音・濃音の区別があり、平音の表には一つの音素の無声・有声の実現が示される。','鼻音/m/・/n/・/ŋ/は存在せず、子音の表にも含まれない。'],
 ['教材の単母音の表には/a/が含まれています。','教材の平音・激音・濃音の表には[p]・[t]・[k]などがあり、大学の別解説でも閉鎖音を説明しています。','教材は三系列の区別と、例えば平音の[k/ɡ]という実現を示しています。日本語の清濁の音素対立と、同一音素の実現の違いを区別する必要があります。','教材の子音表には/m/・/n/・/ŋ/が含まれています。'],
 '語中で自動的に有声化という環境条件を欠く断定と、個別学習者の誤りを音韻体系だけで必然的に説明する主張を撤去。取得した大学教材が説明する音素・音声の区別と三系列に限定。方言や世代全体をこの教材の説明で一括承認しない。',['S113','S114'],['単母音表の/a/と不一致','閉鎖音の存在を否定して誤り','三系列と同一音素の実現の区別に一致','鼻音表の3音を否定して誤り'])
(b.OUT/'changes_batch51.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S113 | 東京外国語大学公開専門教材 [朝鮮語を知る―音韻](https://www.tufs.ac.jp/ts/personal/choes/bibimbab/siru/siru02.html) | 単母音表、子音表、音素／音声記号の注、平音・激音・濃音の区別を本文取得。 | 2026-10-13取得。古い教材であることを踏まえ、その体系の説明を問う。母音数の現状・世代全体・実際の学習者の誤用原因を普遍的に承認しない。 | Q_5_030 |
| S114 | 野間秀樹（東京外国語大学）[朝鮮語 発音と文字](https://www.tufs.ac.jp/common/fs/ilr/archive/kor/kor2.html) | 子音の節と終声の解説で[p][t][k]の閉鎖音、三系列の存在を確認。 | 2026-10-13本文取得。ハングル等の文字化けがあるので、その字形や不明な記号を根拠にしない。明瞭なラテン音声記号と本文だけを照合。 | Q_5_030 |
''')
print('1 question /',len(extra),'edits')
