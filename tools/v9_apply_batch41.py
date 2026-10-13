#!/usr/bin/env python3
"""Evidence-based revisions of loanword formation and near synonyms."""
import html,json
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text()); assert len(prior)==735
_,Q,A=qa.audit(str(b.DST))
D=json.loads((b.OUT/'decisions.json').read_text()); extra=[]

def rewrite(qid,stem,opts,exps,reason,sources,verdicts):
    for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
        for i,(before,after) in enumerate(zip(old,new)):
            extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第40修正バッチ作業稿'))
    D[qid].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='取得した根拠本文の定義と明示された範囲に限定。',explanation_review='全4選択肢・全4解説を本文照合。',unresolved='',multiple_correct_risk='なし：誤答肢は本文と明確に不一致',no_correct_risk='なし：独立正答2')

rewrite('Q_5_051',
 '国立国語研究所の解説で和製英語とされる「クールビズ」の語形成について、最も適切な記述はどれか。',
 ['「クールビズ」は、オランダ語の一語を音形も意味も変えずに日本語へ借用した語である。',
  '「クールビズ」は、英語の cool と business の略語 biz を合成し、涼しく働く姿を意図して作られた語である。',
  '「クールビズ」の biz は日本語の「美術」の略語であり、英語の語を組み合わせたものではない。',
  '「クールビズ」は漢字の音読みだけを組み合わせた漢語であり、英語由来の要素を含まない。'],
 ['国語研の解説は、英語由来の二つの要素を合成した和製英語と説明しています。オランダ語一語の借用ではありません。',
  '国語研の解説が明示する構成と命名意図に一致します。ここでは、個別の語形成を問い、和製英語全般の英語話者への通用性は断定していません。',
  '国語研の解説では biz は business の略です。「美術」の略ではありません。',
  '構成要素は英語の cool と biz です。漢字の音読みだけから作られた漢語ではありません。'],
 '旧稿の「英語圏では通用しない」という全称的説明、ハンドルの語形成を新造複合語と一括する例、出典未照合の歴史・指導効果を撤去。国語研本文が構成要素と命名意図を直接示すクールビズの例に限定し、和製英語の語形成という元の出題領域を維持した。',
 ['S93'],['オランダ語一語の借用ではなく誤り','国語研本文の構成要素と命名意図に一致して正しい','bizはbusinessの略であり誤り','英語由来の構成要素を否定しており誤り'])

rewrite('Q_5_071',
 '類義語の意味・用法を分析する際のコロケーションの扱いとして、最も適切なものはどれか。',
 ['類義語は同じ訳語を持てば、共起する語や使用文脈もすべて同じになるため、辞書の短い訳語だけで使い分けを説明できる。',
  '類義語は意味や用法が重なっていても違いがあり、実際の文脈でどの語と共起するかを調べることが使い分けの分析に役立つ。',
  'コロケーションの分析とは、単語を文脈から切り離し、構成音素の数だけを比較することである。',
  '形容詞がどの名詞を修飾するか、名詞がどの動詞の主語や目的語になるかは、コロケーションの分析対象から除外する。'],
 ['同じ訳語で表せる類義語でも、より広い意味・用法には違いがあります。短い定義や訳語だけでは、自然な使用に必要な情報を尽くせません。',
  'Backhouseの原論文は、類義語の意味・用法の重なりと相違を説明し、実例のコロケーションを調べることが自然な語彙使用の分析に役立つと論じています。',
  'ここでいうコロケーションは、語が構文や文脈の中で他の語と共起する傾向を扱います。音素数だけの比較ではありません。',
  '原論文は、形容詞が修飾する名詞や、名詞が主語・目的語になる動詞など、同じ構文内に現れる語の結びつきを分析対象として挙げています。'],
 '旧稿は「直す」は機嫌にも使えるという未照合例や、和語・漢語全般の意味範囲を一括する説明、特定指導法が最も効果的という未検証評価を含んでいた。原論文本文の類義語定義とコロケーション分析の範囲へ限定し、全肢の正誤を直接判定できるよう改稿した。',
 ['S94'],['同じ訳語でも意味・用法が異なり得るため誤り','原論文の目的と定義に一致して正しい','語の共起分析を音素数の比較と取り違えており誤り','原論文が明示する対象を除外しており誤り'])

(b.OUT/'changes_batch41.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md'
p.write_text(p.read_text()+'''
| S93 | 柏野和佳子（国立国語研究所）[「急速に普及する外来語には、人を引き付ける何かがあるのでしょうか」](https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-90/)（2020年4月13日公開、初出2006年） | 本文「節電効果、経済効果を上げた『クールビズ』」は cool と business の略 biz の合成、涼しく働く姿を意図した和製英語と明記。 | 2026-10-13本文取得。通用性の全称命題や他語の語史へ一般化しない。 | Q_5_051 |
| S94 | Anthony E. Backhouse [Collocational aspects of near-synonyms: Illustrations from a small corpus](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/45637/BISC007_004.pdf) 北海道大学留学生センター紀要7、50–68頁 | 原論文50–52頁の導入は類義語の意味・用法の重なりと相違、定義・訳語を超える情報の必要性、構文内での共起関係を説明。 | 2026-10-13原論文PDF本文取得。小規模コーパスの結果を全和語・漢語へ一般化せず、本文の分析方法に限定。 | Q_5_071 |
''')
print('2 questions; 18 edits')
