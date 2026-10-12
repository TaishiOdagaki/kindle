#!/usr/bin/env python3
"""Resolve the remaining analogy gate for the explicitly reported word formation."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==524
_,Q,A=qa.audit(str(b.DST))
new='学習者が述べた、既存語をモデルにして別の形を作る手順に一致します。これは類推の説明と整合します。ただし、本問は自己報告された手順を問うもので、「遅起き」の歴史的な成立過程や品詞・形態分類を確定する問題ではありません。また「遅起き」には文科省公開資料にも使用例があり、語そのものを一律に誤用とは扱いません。'
extra=[dict(id='Q_5_050',field='explanations',index=3,before=html.unescape(A['A_5_050']['txt'][3]),after=new,reason='取得した類推の項目本文と自己報告の語形成を照合。形成手順と語の歴史的由来・適否の断定を明確に分離した。',sources=['S56','S69'],applied=True,before_version='第30修正バッチ作業稿')]
(b.OUT/'changes_batch31.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D['Q_5_050'].update(status='確認済み',fixes_applied=True,independent_answer=4,sources=['S56','S69'],option_verdicts=['既存語を参照したという自己報告と矛盾して誤り','否定形の活用ではなく語要素の置換のため誤り','外国語の直接借用ではなく既存日本語を参照しており誤り','既存語をモデルにした置換という自己報告と類推の記述に一致して正しい'],reason='類推の項目本文を取得し、既存語をモデルとする明示的な自己報告に全肢を照合。遅起き自体の誤用断定・歴史的由来・形態品詞分類は採用内容に含めない。',stem_review='既存語参照の自己報告を明示している。語の使用実態と語形成手順を分離。',explanation_review='全4解説を設問の自己報告へ照合し、4を大辞泉と菊地康人執筆の類推の本文へ照合。遅起きの実使用は文科省資料本文。',unresolved='',multiple_correct_risk='なし：4のみ明示された手順に一致',no_correct_risk='なし：独立正答4')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S69 | 小学館 [類推](https://kotobank.jp/word/%E9%A1%9E%E6%8E%A8-150606)（大辞泉語義3・日本大百科全書の菊地康人執筆「言語学における類推」） | 項目全文を取得・精読。既存形式との関連・モデルによる別形式の生成、規則に合う類推もあることを照合。遅起きの歴史的由来や品詞分類を資料が説明しているとは扱わない。設問は明示された自己報告の手順に限定。 | Q_5_050 |\n')
print('Recorded',len(extra),'repair')
