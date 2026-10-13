#!/usr/bin/env python3
"""One-time evidence-bound revision of error analysis applications."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==1002
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,reason,sources,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   if html.unescape(before)==after:continue
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第52修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='取得した根拠本文と照合。著者の定義または明示された仮想事例の範囲で4肢を独立判定。',explanation_review='4解説を原論文または公式教材の本文へ個別照合。元の未照合補助主張は引き継がない。',unresolved='',multiple_correct_risk='なし：明示した定義・事例に一致するのは独立正答のみ',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_O_034',1,
 'このケースの教師が行う誤用の記録・分析について、Corder（1967）が述べる系統的な誤用の教師にとっての意義に合うものを、次の1〜4の中から一つ選べ。',
 ['系統的に分析すると、学習者が目標に向けてどこまで進み、何がまだ学習課題として残るかを知る手がかりになる。','学習者の誤用は、教師にとって学習の進展や残る課題を知る資料にはならない。','記憶の不調などによる偶発的な言い間違いと、学習者の現在の知識を反映する系統的な誤用は、同じものとして扱う。','Corderは、学習者の誤用は体系を示さず、全て互いに無関係な偶発的現象だと説明する。'],
 ['原論文167頁は、教師が系統的に分析すると、目標への進展と今後の学習課題を知ることができると説明しています。','同論文は、誤用が教師にもつ意義の一つとして進展と残る課題の把握を挙げています。','同論文166〜167頁は、偶発的な遂行上のmistakesと現在の知識を反映する系統的なerrorsを区別します。','同論文は、系統的な誤用を学習者がその時点で使う言語体系の証拠としています。'],
 '教師による系統的分析の意義を原論文へ照合。母語干渉・過剰般化という個別原因やクラス全員の共通性を資料なく推定する説明を撤去し、誤用と偶発的な言い間違いを区別。ケース中の個別例文の原因をこの資料で確定したとは扱わない。',['S118'],['原論文167頁の教師にとっての意義に一致','教師が進展と課題を知る意義を否定','原論文のmistakes/errorsの区別に反する','系統的な誤用を体系の証拠とする原文に反する'])
rewrite('Q_O_035',3,
 'このケースの誤用分析により、学習者に残る課題が明らかになったとする。Corder（1967）の、学習者の必要に合わせて指導を考える立場に沿って授業計画を検討する方法として、最も適当なものを一つ選べ。',
 ['分析で明らかになった学習者の課題を取り上げず、学習者が何を必要とするかは授業計画の検討から除外する。','第二言語と第一言語の学習順序は必ず同一だと決め、分析結果を使わず第一言語の習得順序をそのまま採用する。','分析で明らかになった課題に対応する練習を検討し、学習者の必要を踏まえて次回以降の指導を計画する。','誤用は学習者の現在の言語体系を知る手がかりにならないと決め、分析結果を今後の指導計画で使わない。'],
 ['原論文169頁は、学習者の必要に適応するという立場を述べています。この方法はその必要を検討から除外しています。','原論文165頁は、学習方略に共通性を仮定することが、両者の学習順序も同一だという意味にはならないと述べています。','教師が分析で残る課題を知り、学習者の必要に合わせて指導を考えるという議論を授業計画へ適用した例です。特定の練習が必ず効果を上げるという主張ではありません。','原論文166〜167頁は、系統的な誤用を現在の言語体系の証拠とし、教師が残る学習課題を知る意義を説明しています。'],
 '誤用分析の原論文の教師にとっての意義と学習者の必要への適応を、条件を明示した授業計画へ適用。練習を行えば必ず改善するとの推論はしない。通知による負担、評価除外の教育的価値などこの原論文で直接照合できない補助主張を撤去。',['S118'],['学習者の必要に適応する立場と不一致','方略共通性と学習順序同一を混同','残る課題の把握と必要への適応の適用例','誤用が現在の体系の証拠になる意義を否定'])
(b.OUT/'changes_batch53.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+"\n| S118 | S. P. Corder（1967）[The Significance of Learner’s Errors 原論文](https://files.eric.ed.gov/fulltext/ED019903.pdf)、[ERIC書誌ED019903](https://eric.ed.gov/?id=ED019903) | 全12頁PDF本文取得。原誌165頁の方略と順序の区別、166～167頁のmistakes/errorsと誤用の教師への意義、169頁の必要への適応を精読。PDF8・9・11頁の画像を本文と照合。 | 2026-10-13取得。著者の当時の定義と立場を明示。個別日本語例文の原因、全クラス共通性、具体的練習の必然的効果はこの論文から承認しない。 | Q_O_034、035 |\n")
print('2 questions /',len(extra),'edits')
