#!/usr/bin/env python3
"""Specify opposition framework and the source of suffix comparison."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text()); assert len(prior)==753
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def record(qid,field,i,after,reason,sources):
 before=Q[qid]['stem'] if field=='stem' else Q[qid]['opts'][i] if field=='options' else A['A_'+qid[2:]]['txt'][i]
 extra.append(dict(id=qid,field=field,index=i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第41修正バッチ作業稿'))
reason='旧稿は男女の現実を相補的な二分と断定し、上／下と行く／来るを一括して反転対義とした。Kroegerの指定体系では位置関係above／belowはconverse、移動come／goはreverseと区別されるため、指定著者の定義と本文例に限定し分類の混同を撤去した。'
record('Q_5_072','stem',None,'Kroeger（2019）『Analyzing meaning』第6章の対義関係の分類に従うと、最も適切な記述はどれか。',reason,['S95'])
opts=['同じ尺度の両端を表し中間があり得る big／small は、段階的対義語ではなく相補的対義語である。',
 'parent／child のように同じ非対称な関係を項の順序を入れ替えて表す語の対は、対転関係（converse pairs）である。',
 'above／below の位置関係は、移動の方向だけが逆になる reverse pairs の例として分類され、converse pairs には含まれない。',
 '二状態だけを区別するスイッチの on／off は、中間状態を持つ段階的対義語の典型例である。']
exps=['big／small のように同じ尺度の両端を表す対は、段階的（尺度的）対義語です。相補的対義語との分類が逆です。',
 '同書は parent／child を converse pairs の例に挙げ、同じ関係を二つの項の順序を入れ替えて表すものと説明しています。',
 '同書では above／below は converse pairs の例です。一方、come／go のような逆方向の移動・変化を表す対は reverse pairs として区別します。',
 '同書は on／off を相補的対義語の例としています。本問はオンかオフかの二状態だけを区別する場合に限定しており、中間状態を持つ尺度としては扱いません。']
for i,t in enumerate(opts):record('Q_5_072','options',i,t,reason,['S95'])
for i,t in enumerate(exps):record('Q_5_072','explanations',i,t,reason,['S95'])
D['Q_5_072'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S95'],option_verdicts=['段階的と相補的の分類が逆で誤り','converseの定義と例に一致して正しい','above／belowはconverseであり誤り','二値条件のon／offは相補的であり誤り'],reason=reason,stem_review='指定著者の分類体系と二値条件を明示。',explanation_review='109～112頁本文へ全4肢・全4解説を個別照合。',unresolved='',multiple_correct_risk='なし：指定体系に一致するのは2のみ',no_correct_risk='なし：独立正答2')
reason49='前バッチの「研究」という無名の帰属を、曾寶儀（2016）の指定資料と対象範囲へ明示。単一研究の比較結果を日本語全体の無条件の法則として読ませない。'
record('Q_5_049','stem',None,'曾寶儀（2016）「『～さ』派生名詞と『～み』派生名詞に関する一考察」の記述として、最も適切なものはどれか。',reason49,['S91'])
D['Q_5_049']['stem_review']='曾寶儀（2016）の指定研究の記述を問う範囲を明示。全肢・全解説の前バッチ判定を維持。'
(b.OUT/'changes_batch42.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S95 | Paul Kroeger（2019）[Analyzing meaning 第2訂正版](https://langsci-press.org/catalog/view/231/1727/1362-2) Language Science Press、第6章6.2.2 | 印刷109～112頁（PDF125～128頁）は相補・段階・対転・反転を区別。parent／child、above／below はconverse、come／goはreverse。 | 2026-10-13出版社配布原著PDF本文取得。語義と適用条件を指定し、男女の現実の二分を教材では断定しない。 | Q_5_072 |
''')
print('1 newly verified question; 10 edits including scope clarification')
