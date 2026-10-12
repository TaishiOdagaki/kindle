#!/usr/bin/env python3
"""Replace unconditional ni/wo force/permission mapping with attested structures."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==488
_,Q,A=qa.audit(str(b.DST));extra=[]
why='ニ使役／ヲ使役と容認／強制を常に一対一とする読みを撤去。意志を持った人の自動詞使役では両格を取り得ることと、他動詞・無意志物の例を区別。'
stem='使役文で、動作を行う人や物を示す「に」「を」について、適切な説明はどれか。'
opts=['他動詞「食べる」の使役でも、「母が娘をご飯を食べさせる」のように、動作を行う人を必ず「を」で示す。','自動詞「走る」の使役では、人が動作を行う場合も「に」しか使えず、「父が息子を走らせる」は使えない。','意志を持たない物が変化する使役でも「に」しか使えず、「花に咲かせる」が基本形である。','意志を持った人が動作を行う自動詞の使役では、「父が息子に走らせる」「父が息子を走らせる」のように、両方の格を使える場合がある。']
exps=['他動詞の使役の基本形では、「母が娘にご飯を食べさせる」のように、動作を行う人を「に」、食べる対象を「を」で示します。選択肢のように必ず人を「を」で示す説明は誤りです。','意志を持った人が動作を行う自動詞の使役では、「に」と「を」の両方が使われる場合があります。「父が息子を走らせる」を排除できません。','意志を持たない物については、「花を咲かせる」のように「を」を使います。選択肢の「花に咲かせる」が基本形という説明は誤りです。','この条件では両方の形が使われます。ただし、どの動詞・動作主でも自由に交換できるとは述べていません。また、にとをの選択を、文脈を問わず許可と強制へ一対一に対応させることは避けます。']
for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
 for i,new in enumerate(vs):
  old=Q['Q_5_068']['stem'] if field=='stem' else Q['Q_5_068']['opts'][i] if field=='options' else A['A_5_068']['txt'][i]
  extra.append(dict(id='Q_5_068',field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S66'],applied=True,before_version='第27修正バッチ作業稿'))
(b.OUT/'changes_batch28.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D['Q_5_068'].update(status='確認済み',fixes_applied=True,independent_answer=4,sources=['S66'],option_verdicts=['他動詞の基本形と異なり人をヲに限定して誤り','人の自動詞使役のヲ格を排除して誤り','無意志物のヲ格を排除して誤り','人の自動詞使役で両格を取れる例に一致して正しい'],reason=why,stem_review='動詞の自他、動作主の意志性を明示し、許可／強制の無条件な一対一分類を撤去。',explanation_review='取得した篠崎大司のヴォイス教材PDF17–18頁の例28–32と本文に4肢・4解説を照合。',unresolved='',multiple_correct_risk='なし：4のみ限定した条件で両格の使用に一致',no_correct_risk='なし：独立正答4')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S66 | 篠崎大司 [日本語の構造 文法体系 ヴォイス](https://www.kanjifumi.jp/wp/wp-content/uploads/2020/11/ab5f12b9d332bb837b3ace2515df8133.pdf) | PDF17–18頁本文・例28–32を取得。人の意志的な自動詞使役のニ／ヲ、無意志物のヲ、他動詞使役のニ格を確認。この教材の使役受身の常に強制という一般化は別論文に留保があり、本問の承認根拠として用いない。 | Q_5_068 |\n')
print('Recorded',len(extra),'repairs')
