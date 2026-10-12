#!/usr/bin/env python3
"""Correct false error premises; never approve an unverified morphological analysis."""
import json, html
from docx import Document
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==351
_,Q,A=qa.audit(str(b.DST));extra=[]
def record(k,field,index,new,why,sources):
 old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][index] if field=='options' else A['A_'+k[2:]]['txt'][index]
 old=html.unescape(old)
 if old!=new:extra.append(dict(id=k,field=field,index=index,before=old,after=new,reason=why,sources=sources,applied=True,before_version='第19修正バッチ作業稿'))
w50='文科省公開資料に遅起きの実使用があるため、語そのものを必ず誤用とする前提を撤去。学習者の説明を明記して類推の仮説を問う。語構成の分類は未承認。'
record('Q_5_050','stem',None,'学習者が「遅起き」という語を使い、「『早起き』を参考にして、反対の意味になるよう『早』を『遅』に替えました」と説明した。この説明が示す語形成の過程として、最も適切なものはどれか。',w50,['S56'])
record('Q_5_050','options',0,'接頭辞の接続制限だけが原因であり、既存の語の形は語形成に関係していない。',w50,['S56'])
record('Q_5_050','options',1,'動詞の否定形を作る活用規則を適用して語を作った。',w50,['S56'])
record('Q_5_050','options',2,'外国語の語を翻訳せず、そのまま日本語に取り入れた。',w50,['S56'])
record('Q_5_050','options',3,'既存の「早起き」の形を手がかりに、反対の意味を表す要素へ置き換えて語を作った。',w50,['S56'])
e50=['学習者自身の説明には、既存の「早起き」を参考にしたことが示されています。接続制限だけを原因とし、既存語との関係を否定する説明とは一致しません。','学習者の説明は、「早」を「遅」に替えたというものです。動詞を否定形に活用したという説明ではありません。','学習者の説明は既存の日本語の形を利用したものであり、外国語の語をそのまま借用したという説明ではありません。','学習者が述べた語形成の手順に一致します。ただし、この手順を説明することと、できた語を誤用と判定することは別です。「遅起き」には文科省公開資料にも使用例があり、語そのものを一律に誤用とは扱いません。']
for i,t in enumerate(e50):record('Q_5_050','explanations',i,t,w50,['S56'])
w33='二つの内容は句点で文境界を明示することもでき、必ずので等の接続表現が欠落したとは言えない。書き言葉の句点欠落を問う条件へ限定。'
record('Q_O_033','stem',None,'作文に書かれた「この漢字が分かりませんでした教えてください。」について、文の区切りを明確にする修正として適切な説明を、次の1〜4の中から一つ選べ。',w33,['S57'])
opts=['漢字の読み仮名を付けるだけで、文の区切りも明確になる。','「分かりませんでした」の後に句点を置き、二つの文に区切る方法がある。','発音を変えるだけで、作文の文の区切りも明確になる。','意味を推測できる場合には、文の区切りを表記で示す必要はない。']
exps=['読み仮名は漢字の読みを示すものであり、二つの文の境界を示す句点の代わりにはなりません。','「この漢字が分かりませんでした。教えてください。」と、句点で二つの文の境界を示すことができます。「ので」などで因果関係を明示する書き換えも可能ですが、接続表現の欠落だけが唯一の分析ではありません。','設問は作文の表記を問っています。発音の変更だけでは、書かれた文の区切りを示せません。','読み手が意味を推測できることと、文の区切りが明確であることは別です。ここでは句点によって境界を明示できます。']
for i,t in enumerate(opts):record('Q_O_033','options',i,t,w33,['S57'])
for i,t in enumerate(exps):record('Q_O_033','explanations',i,t,w33,['S57'])
old='また、別の学習者の作文には「先生、この漢字が分かりませんでした教えてください。」という、文の区切りに助詞や接続表現が不足している文が見られた。'
assert sum(old in p.text for p in Document(b.DST).paragraphs)==1
extra.append(dict(id='CASE_O_07',field='case_text',index=None,before=old,after='また、別の学習者の作文には「先生、この漢字が分かりませんでした教えてください。」という、二つの文の境界が句点で示されていない記述が見られた。',reason=w33,sources=['S57'],applied=True,before_version='第19修正バッチ作業稿'))
(b.OUT/'changes_batch20.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D['Q_5_050'].update(status='要追加確認',fixes_applied=True,independent_answer=4,sources=['S56'],option_verdicts=['明示した自己報告と矛盾','否定活用でなく置換という自己報告','外国語借用でなく既存語の置換という自己報告','自己報告の手順に一致する候補'],reason=w50,stem_review='誤用の断定を撤去し、語形成の手順を自己報告として明示。',explanation_review='旧稿の形態分類と語種断定を撤去。実使用例は本文確認。類推の体系的な語形成論との照合は未了。',unresolved='改訂の語形成過程を形態論・類推の根拠本文と照合し、全肢・全解説を最終承認する。',multiple_correct_risk='改訂条件下で4候補。追加照合未了',no_correct_risk='誤用前提を撤去。独立正答4候補の根拠照合は未了')
D['Q_O_033'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S57'],option_verdicts=['読み仮名は文境界を示さず誤り','句点で文境界を示す修正で正しい','発音変更では作文の境界を示せず誤り','意味の推測と文境界の明確さを混同して誤り'],reason=w33,stem_review='ケースの接続表現欠落の断定を修正。書き言葉の句点による文境界明示に限定。',explanation_review='句点の辞典定義と二文への修正を4肢・4解説に照合。のでの使用を唯一の修正にしない。',unresolved='',multiple_correct_risk='なし：表記で境界を示す2のみ',no_correct_risk='なし：独立正答2')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''\n| S56 | 文部科学省公開 [楯中パワーアッププロジェクト報告](https://www.mext.go.jp/component/a_menu/education/detail/__icsFiles/afieldfile/2017/04/07/1383732_02.pdf) | PDF12頁の表に遅起きの実使用を確認。語そのものを一律誤用とする断定を撤去する根拠。問題中のサ変用法の自然さや、語形成の学説はこの資料から承認しない。 | Q_5_050 |
| S57 | 小学館デジタル大辞泉 [句点](https://kotobank.jp/word/%E5%8F%A5%E7%82%B9-484427) | 辞典本文の句点の機能を取得。句点で二文に区切る修正と因果接続を区別する判断は、設問条件・文面を合わせた監査判断。文化庁の歴史的案PDFは文字抽出不良で全文照合資料には未採用。 | Q_O_033 |\n''')
print('Recorded',len(extra),'repairs')
