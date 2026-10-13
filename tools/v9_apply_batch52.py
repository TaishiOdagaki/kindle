#!/usr/bin/env python3
"""One-time evidence-bound revision of contrastive analysis and classifiers."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==983
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,reason,sources,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   if html.unescape(before)==after:continue
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第51修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='取得した根拠本文と照合。著者の定義または明示された仮想事例の範囲で4肢を独立判定。',explanation_review='4解説を原論文または公式教材の本文へ個別照合。元の未照合補助主張は引き継がない。',unresolved='',multiple_correct_risk='なし：明示した定義・事例に一致するのは独立正答のみ',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_5_007',1,
 'Wardhaugh（1970）が区別する強形・弱形の対照分析仮説について、最も適切なものはどれか。',
 ['弱形は、実際に観察された第二言語学習の困難を出発点として、利用できる言語学的知識によって説明しようとする。','弱形は、観察された困難を出発点とせず、言語体系の比較だけで困難をあらかじめ予測することを要求する。','強形は、学習上の困難を予測することを要求せず、観察された干渉現象を説明するだけの立場である。','Wardhaughは、弱形の分析では言語体系を参照せず、誤りを任意の方法で分類するだけでよいとする。'],
 ['原論文7～8頁は、観察された困難や干渉の証拠を出発点とする弱形を説明しています。','困難の予測を要求するのは、同論文で区別される強形です。','困難の予測は、同論文が強形に要求されるものとして述べる特徴です。','原論文は弱形でも体系を重視し、任意の誤り分類だけにはしないと明記しています。'],
 '完全に類似するという前提と使用条件の相違を持ち出す解説の矛盾、差の大小だけで難易度を決める単純化を撤去。未取得の中間言語論へ広げず、強形と弱形を区別した原論文の定義で全肢を再構成。',['S115'],['原論文7～8頁の観察された困難からの説明に一致','弱形の説明を強形の予測要求と取り違え','強形から予測要求を除外して誤り','弱形も体系を重視する原文と不一致'])
rewrite('Q_5_010',3,
 '中国語の量詞と日本語の助数詞を比較する、次の架空の学習場面について、最も適切なものはどれか。学習者は書籍を2冊買い、「本を二本買いました。中国語で書籍を数える『本』を、そのまま日本語でも使いました」と説明した。',
 ['書籍を2冊買った場面では、助数詞だけでなく数詞の「二」も必ず誤りであり、「二冊」とも言えない。','学習者の自己説明は、助数詞の選択ではなく、動詞と目的語の語順を取り違えたことだけを示している。','中国語で書籍を数える量詞「本」と日本語の助数詞「本」を同じ対象に使えると考えた、選択の取り違えが示されている。','中国語には物を数える量詞が存在しないので、学習者が使った「本」は中国語の量詞ではない。'],
 ['国際交流基金の助数詞表では書籍に「冊」を使い、2の欄に「にさつ」があります。数詞の二自体を誤りとはしません。','架空の学習者は中国語の量詞を日本語でそのまま使ったと説明しています。語順だけの問題とする選択肢は、その説明に合いません。','東京外国語大学の教材では「三本书」を「3冊の本」と訳し、国際交流基金の教材では書籍に「冊」、鉛筆などに「本」を示しています。同じ字でも対象の対応は同じではありません。','東京外国語大学の教材は中国語の量詞を説明し、書籍の例で「本」を示しています。'],
 '衣服の二本を対象未指定で誤用とする前提と、出身言語だけから転移原因を断定する説明を撤去。書籍・数量・学習者の自己説明を明示した架空事例とし、取得した大学と基金の具体的対応を問う。中国語の体系が日本語以上に豊富で厳密という未照合比較も撤去。',['S116','S117'],['二冊の二を必ず誤りとする主張は公式表に反する','明示された自己説明は助数詞選択であり語順だけではない','中国語の本と日本語の冊の対応・仮想自己説明に一致','大学教材にある量詞と書籍例の存在を否定'])
# Word stores the original case statement in two paragraphs. Preserve explicit removal.
stem=next(c for c in extra if c['id']=='Q_5_010' and c['field']=='stem')
first,second=stem['before'].split(' 学習者の発話：',1);stem['before']=first
r=dict(stem);r.update(field='stem_continuation',before='学習者の発話：'+second,after='',remove_paragraph=True,reason=stem['reason']+' 旧設問の独立した発話段落を明示的に除去し、旧例を改訂例と併存させない。');extra.append(r)
(b.OUT/'changes_batch52.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S115 | Ronald Wardhaugh（1970）[The Contrastive Analysis Hypothesis 原発表稿](https://files.eric.ed.gov/fulltext/ED038640.pdf)、[ERIC書誌ED038640](https://eric.ed.gov/?id=ED038640) | 全15頁PDF本文取得。原論文3～4頁の強形の予測要求、7～8頁の弱形の観察された困難・干渉の説明と体系への強調を精読。7～8頁の画像でOCRを照合。 | 2026-10-13取得。PDFの表紙を含むページ番号とは区別。1957年Ladoの引用を原著取得済みとは扱わない。1970年の著者の区別を問う。現代研究全体の結論は承認しない。 | Q_5_007 |
| S116 | 東京外国語大学 [中国語 量詞](https://www.coelang.tufs.ac.jp/mt/zh/gmod/courses/c01/lesson04/step2/explanation/020.html) | 全47行本文取得。19～29行の名量詞と数詞＋量詞＋名詞、35～38行の三本书と3冊の本の対応。 | 2026-10-13取得。個人の実際の誤り原因を証明する研究ではない。架空の自己説明を設問に明示。 | Q_5_010 |
| S117 | 国際交流基金 [教科書を作ろう 資料 助数詞](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00010/ja/render.do) | 全52行本文取得。物を数える表：本・ノート・辞書と冊、えんぴつ等と本、2の欄ににさつ。 | 2026-10-13取得。衣類全体への本の使用可否をこの表だけで一括判定しない。書籍の具体例で照合。 | Q_5_010 |
''')
print('2 questions /',len(extra),'edits')
