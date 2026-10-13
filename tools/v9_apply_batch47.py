#!/usr/bin/env python3
"""Schema definitions bounded to Carrell/Eisterhold primary-text transcription."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==865
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,verdicts):
 reason='Carrell・Eisterhold（1983）原論文転記本文556–560頁へ限定。認識心理学という名称、毎回スキーマが更新されるという断定、病院の未知語補完の未照合例を撤去。定義と解釈の修正を区別。'
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=['S106'],applied=True,before_version='第46修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=['S106'],option_verdicts=verdicts,reason=reason,stem_review='原論文の著者・年と定義の範囲を指定。',explanation_review='全4肢・全4解説を原著転記本文556–560頁に照合。転記にない全称命題を撤去。',unresolved='',multiple_correct_risk='なし：原論文の指定概念に合致するのは正答のみ',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_3_003',3,
 'Carrell・Eisterhold（1983）の読解に関するスキーマの説明として、最も適切なものを選びなさい。',
 ['形式スキーマは、テキストの内容領域についての背景知識を指す。',
 'いったん得られた文章の解釈は、矛盾する情報を読んでも修正されない。',
 'スキーマは既に獲得した知識構造であり、読解は背景知識とテキストの相互作用として説明される。',
 'スキーマ、スクリプト、フレームは、技術的にも完全に同一で交換可能な用語である。'],
 ['内容領域の背景知識は内容スキーマです。',
 '論文は新しい情報との不一致による解釈の修正を説明します。',
 '既有の知識構造と、背景知識・テキストの相互作用が示されています。',
 '論文の脚注は、関連する概念でも同一・交換可能ではないと区別します。'],
 ['内容スキーマとの混同で誤り','解釈修正の例と不一致で誤り','556頁の定義に一致して正しい','556頁脚注の技術的区別を否定して誤り'])
rewrite('Q_5_089',3,
 'Carrell・Eisterhold（1983）による内容スキーマと形式スキーマの区別として、最も適切なものはどれか。',
 ['内容スキーマは、文章の修辞的な構成様式についての背景知識である。',
 '読解では、書き手が想定するスキーマを読み手が持っていなくても、理解に影響することはない。',
 '内容スキーマはテキストの内容領域、形式スキーマはテキストの修辞的な構成様式についての背景知識である。',
 '形式スキーマは、テキストの構成様式に関わる知識を含まない。'],
 ['修辞的な構成様式の知識は形式スキーマです。',
 '論文は、適切なスキーマの欠如や活性化の不成立を理解の困難と結び付けています。',
 '論文560頁は、内容領域と修辞的な構成様式の背景知識を区別します。',
 '形式スキーマには、異なる種類のテキストの構成様式についての知識が含まれます。'],
 ['形式スキーマとの混同で誤り','560頁の理解困難の説明を否定して誤り','560頁の二分類の定義に一致して正しい','形式の背景知識を定義から排除して誤り'])
(b.OUT/'changes_batch47.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S106 | Carrell, P. L.・Eisterhold, J. C.（1983）[Schema Theory and ESL Reading Pedagogy 原論文転記](https://doczz.net/doc/8055403/schema-theory-and-esl-reading-pedagogy)、[出版社書誌](https://onlinelibrary.wiley.com/doi/abs/10.2307/3586613) | 原著556–560頁の転記本文を取得。556頁の既有知識構造・相互作用、脚注の概念の区別、559頁の新情報による解釈修正、560頁の内容・形式の定義と欠如／活性化の問題を精読。 | 2026-10-13取得。第三者サイトの原論文転記であり出版社全文ではない。書誌は出版社と照合。PDFダウンロード403、viewer410で画像照合未取得。転記で明瞭な定義に限定し、学説の普遍性・効果量・原著引用先の直接照合を主張しない。 | Q_3_003、Q_5_089 |
''')
print('2 questions /',len(extra),'edits')
