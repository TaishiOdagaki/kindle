"""One-time independent review against Long's full paper and Richards's syllabus description."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1759
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
assert 'S146' not in (b.OUT/'sources.md').read_text()
items={
'Q_4_022':(2,'Longの論考「Focus on form in Task-Based Language Teaching」の図2に示されたTBLTプログラム設計・実施の七つの段階で、最初に挙げられている手続きを一つ選びなさい。',[
'タスクに基づく基準準拠型のパフォーマンス・テストで評価する。',
'学習者の現在または将来の目標タスクを特定するため、タスクに基づくニーズ分析を行う。',
'特定された目標タスクを、目標タスクの類型に分類する。',
'目標タスクの類型から、教室で扱う教育的タスクを導き出す。'],[
'図2では、タスクに基づく基準準拠型のパフォーマンス・テストによる評価は第6段階です。指定された図の最初の手続きではありません。',
'図2の第1段階と、その直後の本文の説明に一致します。ここではLongの特定の設計案を問うのであり、すべてのコース設計を一つの不可逆な手順に固定するものではありません。',
'目標タスクを類型化するのは図2の第2段階です。その前に、ニーズ分析によって目標タスクを特定する段階が置かれています。',
'教育的タスクを導き出すのは図2の第3段階です。本文では学習者の年齢や熟達度などに応じて調整すると説明されており、最初の手続きとは区別されます。'],[
'誤：指定図の第6段階','正：目標タスクを特定する第1段階','誤：特定後に行う第2段階','誤：類型化後に行う第3段階'],['S146']),
'Q_4_023':(2,'文法項目を配列の単位にする「構造シラバス（文法シラバス）」の構成例として、最も適切なものを一つ選びなさい。',[
'環境問題などの話題を単位にし、文法項目の配列順は定めず、各話題について読む・話す活動を組み合わせる。',
'文法項目を単位にし、導入する順序とレベルを定めて、各項目に対応する練習を配置する。',
'謝罪や依頼などの言語機能を単位にし、文法項目の順序ではなく、その機能を実行するために必要な表現をまとめる。',
'口座開設などの達成すべき作業を単位にし、文法項目の順序ではなく、作業を遂行して結果を得る活動を配列する。'],[
'この案は話題を配列の単位とし、文法項目の順序を編成の基準にしていません。話題に関連して文法を学ぶ場合があることと、シラバスの配列単位とは区別します。',
'文法項目を単位にしてレベルや順序を定める点が設問の条件に対応します。Richards（2006）10頁の伝統的なシラバスの説明とも整合します。すべての構造シラバスが語彙・音声まで同じ基準で配列するという定義にはしません。',
'この案は言語機能を配列の単位にしています。機能を実行するために文法表現を扱うことだけで、文法項目を単位とする編成と同一になるわけではありません。',
'この案は達成すべき作業を配列の単位にしています。「口座開設」という語だけで場面シラバスと断定せず、何を単位にして編成しているかを判定します。'],[
'誤：話題を配列単位と明示','正：文法項目を配列単位と明示','誤：言語機能を配列単位と明示','誤：達成作業を配列単位と明示し場面との曖昧さを解消'],['S144','S146']),
'Q_4_038':(3,'Longの論考「Focus on form in Task-Based Language Teaching」におけるFocus on Formの説明として、最も適切なものを一つ選びなさい。',[
'学習者に生じた理解や産出の問題とは無関係に、外部で決めた言語項目の順序だけに従って各項目を教えることを指す。',
'意味中心の授業では言語形式を学習対象として取り上げることを一切認めず、理解や産出に問題があっても形式への注意を排除する。',
'授業の主な焦点を意味やコミュニケーションに置き、その中で生じた学習者の理解や産出の問題を契機に、文脈内の言語要素へ一時的に注意を向ける。',
'言語形式に注意を向ける指導全般を指し、意味中心の授業と無関係に事前に予定した文法項目の演習もすべて同じ概念に含める。'],[
'同論考のOption 1のFocus on Formsで記述される、外部の言語項目配列を基準とする扱いに対応します。学習者の問題を契機とするOption 3の説明とは区別されます。',
'同論考のOption 3は、意味中心の授業の中で言語を学習対象として扱う注意の移行を認めています。形式への注意を排除する説明は逆です。意味中心の授業やイマージョン一般を一律に否定する判断ではありません。',
'Option 3の定義に対応します。対象として語、連語、文法構造、語用上のパターンなどが挙げられ、授業の中心的な意味への焦点と、一時的な形式への注意を両立させています。',
'同論考はFocus on Formを、より広いform-focused instructionと区別しています。事前に予定した形式演習まで無条件に同じ概念へ含める説明は、その区別を失っています。'],[
'誤：外部の言語項目順序に従うFocus on Formsとの取り違え','誤：Option 3が認める形式への注意を排除','正：意味中心の文脈と学習者の問題を契機とする一時的注意が定義に一致','誤：上位のform-focused instructionと同一視'],['S146'])}
extra=[]
for key,(ans,stem,opts,exps,verdicts,sources) in items.items():
 assert int(a['A_'+key[2:]]['ans'])==ans and d[key]['status']=='修正必要'
 reason='Long本人の取得論考のOption 1〜3と図2、Richards2006の印刷10頁の記述へ限定。普遍的固定順序、構造シラバスの範囲拡大、場面と達成課題の混同、過度のイマージョンという価値判断を除去。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第81バッチ反映後の累積作業稿',block_context='A_'+key[2:] if field=='explanations' else key)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='設問と4肢を独立判定。Q_4_022はLongの特定図の段階を指定、Q_4_023は文法項目という配列単位を明示し架空案を比較、Q_4_038は取得論考のOption 3を指定。',explanation_review='全4解説をS146の本文に照合。公開複製11頁版で、本文に1997年秋への言及がある。PDF1・3・5〜7頁を画像照合し、1991年章や1998年版の取得とは混同しない。S144は52頁冊子の印刷10頁を本文・画像照合。引用先の全実証研究を読んだとは扱わず、教授法の普遍的効果や全学習者の気づき・習得は保証しない。',unresolved='',multiple_correct_risk='なし：指定した出典・配列単位に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==27
for name,obj in [('changes.json',c+extra),('changes_batch82.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('3 questions / 27 edits; keys unchanged')
