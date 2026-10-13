#!/usr/bin/env python3
"""Bound inference and listening claims to retrieved primary texts."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==808
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,reason,sources,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第44修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='根拠本文の指定例・概念・適用範囲を明示。',explanation_review='全4肢・全4解説を取得本文へ個別照合。',unresolved='',multiple_correct_risk='なし：定義・例と不一致の3肢を除外',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_5_086',3,
 'Kroeger（2019）第3章の前提と意味論的含意の区別について、最も適切な記述はどれか。',
 ['「私があなたの壺を壊した」が意味論的に含意する「あなたの壺が壊れた」は、「私があなたの壺を壊していない」からも必ず含意される。',
  '同書の「副大統領は歯科記録の偽造を後悔していない」という例は、副大統領が歯科記録を偽造していないことを前提とする。',
  '同書の regret（後悔する）の例では、肯定・否定・疑問のいずれでも、後悔の対象となる出来事が起きたという前提が示される。',
  '前提とは、話し手と聞き手が既に共有している実際に正しい事実だけであり、共有されていない情報が前提として示されることはない。'],
 ['肯定文のその含意は、同じ文を否定した場合には保証されません。壺が壊れたかどうかについて否定文は確約しません。',
  '同書の例で否定されるのは後悔であり、偽造したという前提は示されます。偽造していないという前提ではありません。',
  '同書はregretの例で、出来事が起きたという前提を肯定・否定・疑問で比較します。これは指定例の分析であり、すべての前提があらゆる文脈で例外なく維持されるという主張ではありません。',
  '同書は、前提が実際の共有知識に入っていない場合の前提不成立や、聞き手が新たに受け入れる収容を説明しています。常に既知で正しい事実だけとは限りません。'],
 '旧稿の前提は常に否定下で維持、含意は否定で常に消滅という広い一般化を撤去。Kroegerの指定例による比較へ限定し、前提と実際の共有知識・事実を区別した。',
 ['S98'],['否定文からその結果は保証されず誤り','後悔の否定を出来事の否定と混同して誤り','regretの指定例に一致して正しい','前提不成立・収容を排除して誤り'])
rewrite('Q_5_087',3,
 'Grice（1975）の会話的含意について、最も適切な記述はどれか。',
 ['会話的含意は話し手の悪意だけを指し、発話内容や会話状況を用いて推論する意味とは関係しない。',
  '会話的含意の真であることは、発話で述べた内容が真であるための必要条件であり、両者は同じ論理的内容である。',
  '一般化された会話的含意も、個別の場面では明示的な追加発言や文脈によって取り消され得る。',
  '会話的含意は、語の慣習的な意味だけに含まれ、協調原理や背景情報を考慮せずに決まる。'],
 ['原論文は、述べられた内容と協調原理・背景情報などから導かれる含意を論じています。悪意だけを指す用語ではありません。',
  '原論文58頁は、述べられた内容が真であるために含意が真である必要はないと説明し、両者を区別しています。',
  '原論文57頁は、一般化された含意でも個別の場面で、追加発言によって明示的に、又は文脈によって取り消され得ると説明しています。',
  '原論文57～58頁は、会話的含意の算出に述べられた内容、背景情報、協調原理などが関わることを説明します。慣習的な語の意味だけではありません。'],
 '旧稿の茶への誘いが会話の誘いを常に含意するように読める未指定例と、全含意を辞書的命題意味に還元する説明を撤去。Grice原著57～58頁の取消可能性・非真理条件性・算出条件に限定。',
 ['S48'],['悪意への限定が定義と不一致で誤り','含意と述べた内容の真理条件を同一視して誤り','原著の明示的・文脈的取消に一致して正しい','背景情報と協調原理の役割を否定して誤り'])
rewrite('Q_5_088',2,
 '聴解におけるトップダウン処理とボトムアップ処理の説明として、最も適切なものはどれか。',
 ['背景知識を使えば、入力された音声から単語をほとんど認識できなくても、常に内容を十分理解できる。',
  '背景知識・文脈を使う処理と音声信号を細部から解読する処理は、聴解で組み合わせて働き得る。',
  'トップダウン処理とは、背景知識を使わず、音声信号を細部から分割・解読する処理だけをいう。',
  'ボトムアップ処理とは、音声信号を解読せず、話題についての背景知識だけで内容を予測する処理をいう。'],
 ['British Councilの解説は、音声から何も理解できなければ話題も特定できず、トップダウン処理にも限界があると説明しています。',
  '同解説は、通常の流暢な聴解では両処理が同時に働き、状況や聴く目的によって重みが異なると説明します。必ず交互に切り替えるとはしていません。',
  '音声信号を細部から分割・解読する説明はボトムアップ処理です。トップダウン処理では背景知識や文脈を使います。',
  '話題の背景知識や予測を使う説明はトップダウン処理です。ボトムアップ処理は音声の解読などに関わります。'],
 '旧稿の全熟達者は必ず切替という読み、全読解・聴解研究で相互作用モデルが支持されるという一括帰属、初級者指導の効果断定を撤去。取得教材が直接説明する聴解の定義、同時併用と限界へ限定。',
 ['S99'],['音声理解が不足する場合の限界を否定して誤り','教材の併用・同時作動の説明に一致して正しい','ボトムアップと取り違えて誤り','トップダウンと取り違えて誤り'])
(b.OUT/'changes_batch45.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S98 | Paul Kroeger（2019）[Analyzing meaning 第2訂正版](https://langsci-press.org/catalog/view/231/1727/1362-2) 第3章3.4 | 印刷41～45頁（PDF57～61頁）は肯定・否定・疑問による前提と含意の区別、regretの例、共有知識と前提の不一致、前提不成立と収容を説明。 | 2026-10-13出版社配布原著本文取得。日本語全般の投射規則として一般化せず指定例の分析に限定。 | Q_5_086 |
| S99 | Catherine Morley, British Council TeachingEnglish [Listening: Top-down and bottom-up](https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/listening-top-down-and-bottom) | 本文は背景知識・文脈の利用、音声信号の分割・解読、両処理の同時併用、音声理解が乏しい場合のトップダウン処理の限界を明記。 | 2026-10-13本文取得。読解全般、全熟達者、特定指導法の最大効果へ一般化しない。 | Q_5_088 |
''')
print('3 questions; 27 edits')
