#!/usr/bin/env python3
"""Four Austin questions, verified directly against the 1962 text."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==763
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,answer,stem,opts,exps,reason,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=['S96'],applied=True,before_version='第42修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=answer,sources=['S96'],option_verdicts=verdicts,reason=reason,stem_review='Austin（1962）の講義・用語体系を明示して原著本文へ照合。',explanation_review='全4肢と全4解説を原著該当頁の画像本文へ個別照合。',unresolved='',multiple_correct_risk='なし：用語定義を取り違える3肢を除外',no_correct_risk='なし：独立正答'+str(answer))

rewrite('Q_5_076',3,
 'Austin（1962）の第VIII講義における「発話内の力（illocutionary force）」の説明として、最も適切なものはどれか。',
 ['発話内の力は、声の大きさや音圧だけを指し、同じ音量なら警告と命令は同じ行為になる。',
  '発話内の力は、聞き手が実際に説得されたかどうかという結果だけを指す。',
  '発話内の力は、警告・約束・命令など、当該場面で発話をどの行為として行っているかに関わる。',
  '発話内の力は、用いた語の意味と指示対象だけであり、同じ語ならどの場面でも同じ力を持つ。'],
 ['原著は警告・約束・命令などの発話の機能を区別しています。音量の大小だけをいう概念ではありません。',
  '実際に説得するという結果・効果は発話媒介行為に関わります。発話内の力との分類が異なります。',
  '第VIII講義は、同じ発語を助言・提案・命令・約束などのどの行為として用いるかを区別し、発話内の力として扱います。',
  '原著は、意味を語の意味と指示という範囲で捉える場合、それと力を区別します。同じ語でも、警告か別の行為かは発話場面に関わります。'],
 '旧稿はAustinとSearleの体系を一括し、発声行為をlocutionary act全体と同義に扱った。Austinの第VIII講義のforceとsense／reference及び結果の区別に限定して改稿。',
 ['音圧との同一視が誤り','発話媒介行為の効果との混同が誤り','第VIII講義98～100頁の区別に一致','意味と力を同一視しており誤り'])

rewrite('Q_5_080',2,
 'Austin（1962）が第I講義で導入する「遂行発話（performative utterance）」の説明として、最も適切なものはどれか。',
 ['遂行発話は、話し手が行為をしたことを後から報告する発話だけを指す。',
  '適切な状況で発することが、特定の行為を行うこと、またはその行為の一部となる発話である。',
  '遂行発話は、発話の内容が真か偽かを判定するための事実の記述だけを指す。',
  '遂行発話は、どの人物がどんな状況で発しても、言葉を発しただけで必ず効力を持つ。'],
 ['第I講義の導入では、行為を報告することと、その発話によって行為を行うことを区別します。後からの報告だけではありません。',
  '原著5～8頁の導入に一致します。発話は行為の実行、またはその一部であり、成立には適切な状況が必要です。これは第I講義の導入上の説明です。',
  '第I講義は、この型を真偽を判定する事実の記述として導入していません。後の講義で二分法自体を再検討することとは区別します。',
  '原著は、言葉を発することが通常重要でも、それだけが行為成立の唯一の条件ではないと説明しています。人物や状況などの条件を無視できません。'],
 '遂行／事実描写を原著全体の固定的二分法と読ませないよう第I講義の導入に範囲を明示。発話だけで無条件に成立するという解釈を排除し、原著の適切な状況という条件を反映。',
 ['報告と遂行を取り違えて誤り','第I講義5～8頁に一致して正しい','導入上の遂行発話を事実記述と同一視して誤り','状況・人物の条件を否定して誤り'])

rewrite('Q_5_081',1,
 'Austin（1962）の第II講義で示される遂行発話の適切性条件A・Bについて、最も適切な説明はどれか。',
 ['慣習的な効果を持つ承認された手続が存在し、それを用いる人物・状況が適切で、手続が正しく完全に実行される必要がある。',
  '人物や状況が不適切でも、辞書の最初の語義だけを使えば、条件A・Bはすべて満たされる。',
  '手続を途中で中断しても、音声を録音して文字化できれば、条件A・Bはすべて満たされる。',
  '手続が承認されていなくても、文の文法に誤りがなければ、条件A・Bはすべて満たされる。'],
 ['原著14～15頁のA.1・A.2・B.1・B.2は、承認された慣習的手続、適切な人物と状況、手続の正しい実行と完了を求めています。本問はこの4条件に限定します。',
  '人物・状況の適切さはA.2の条件です。辞書の語義を使うだけで代替できません。',
  '手続の完了はB.2の条件です。録音や文字化の可否で代替できません。',
  '承認された慣習的手続の存在はA.1の条件です。文法の正しさだけで代替できません。'],
 '旧稿は手続不成立と誠実性欠如による濫用を区別せず、全遂行発話の効力を一括した。原著14～15頁のA・B条件のみを明示して出題し、意図・誠実性に関するΓ条件を本問の範囲から分離。',
 ['A.1・A.2・B.1・B.2に一致して正しい','A.2を否定して誤り','B.2を否定して誤り','A.1を否定して誤り'])

rewrite('Q_5_082',3,
 'Austin（1962）の第VIII講義における発語行為（locutionary act）の説明として、最も適切なものはどれか。',
 ['聞き手を実際に説得したり、行動させたりする結果・効果だけをいう。',
  '警告するか約束するかという、その場での発話内の力だけをいう。',
  '一定の音を発し、語彙・文法に従う語を用い、それを一定の意味と指示で発するという全体の行為をいう。',
  '語彙や文法、意味や指示とは無関係に、音を出す物理的な行為だけをいう。'],
 ['原著101～102頁では、実際に説得するなどの結果・効果を発話媒介行為と区別しています。発語行為だけの説明ではありません。',
  '原著98～100頁では、警告・約束などの発話内の力を、語の意味と指示に関わる発語行為から区別しています。',
  '原著94～95頁は、音を発するphonetic act、語彙・文法に従うphatic act、意味と指示を持つrhetic actを区別し、これらを含む通常の意味での発語行為を説明しています。',
  '音を出すだけのphonetic actは発語行為全体の一側面です。語彙・文法、意味・指示を除いた説明では不十分です。'],
 '旧稿の物理的発声と発語行為全体の混同及びSearleへの曖昧な帰属を修正。Austinのphonetic／phatic／rheticの区別を原著画像で確認し、全体の行為として明示した。',
 ['結果・効果は発話媒介行為であり誤り','力は発話内行為に関わり誤り','第VIII講義94～95頁に一致して正しい','音を出す一側面のみで全体を説明しており誤り'])

(b.OUT/'changes_batch43.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S96 | J. L. Austin（1962）[How to Do Things with Words](https://silverbronzo.wordpress.com/wp-content/uploads/2017/10/austin-how-to-do-things-with-words-1962.pdf) Oxford Clarendon Press | 原著174頁PDF取得。印刷4～8、14～16、94～95、98～103頁を画像本文で照合。第I講義の遂行発話導入、A・Bの条件、phonetic／phatic／rhetic、力と意味及び結果の区別。 | 2026-10-13取得。スキャンPDFにテキスト層なし。画像で確認。Pennsylvania大学版は502、Max Planck版は403のため取得済みとは記録しない。 | Q_5_076・080・081・082 |
''')
print('4 questions; 36 edits')
