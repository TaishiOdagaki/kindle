#!/usr/bin/env python3
"""One-time evidence-bound revision of error analysis applications."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==1020
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,reason,sources,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   if html.unescape(before)==after:continue
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第53修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='取得した根拠本文と照合。著者の定義または明示された仮想事例の範囲で4肢を独立判定。',explanation_review='4解説を原論文または公式教材の本文へ個別照合。元の未照合補助主張は引き継がない。',unresolved='',multiple_correct_risk='なし：明示した定義・事例に一致するのは独立正答のみ',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_4_074',1,
 'Burt（1974）による成人の英語学習者の誤りの分析で、「グローバル・エラー」と「ローカル・エラー」の区別に合うものはどれか。',
 ['グローバル・エラーは文全体の組織に関わり意思疎通を大きく妨げ、ローカル・エラーは一部の要素に関わり通常は大きく妨げない。','グローバル・エラーは発音の誤りだけを指し、語順や文をつなぐ表現の誤りを含まない。','グローバルとローカルは同じ範囲の誤りを指すため、文の組織に関わる範囲による区別は行われない。','ローカル・エラーは常に重大な誤解を招き、グローバル・エラーは文全体の組織には関わらない。'],
 ['原稿6〜8頁は、文全体の組織に関わる誤りと一部の要素に限られる誤りを、意思疎通への影響と関連づけて区別しています。ローカルの影響は通常小さいという条件です。','同原稿は、語順や文をつなぐ表現の誤りをグローバルの例として挙げています。発音だけに限定する説明は合いません。','同原稿は、文全体の組織と一部の要素という違いに基づいて両者を区別しています。','同原稿は、ローカル・エラーは通常、意思疎通を大きく妨げないとします。グローバルは文全体の組織に関わる分類です。'],
 '一般的な意思疎通の重大性だけの二分ではなく、分類を提示した原発表稿の文全体の組織／一部の要素の区別と結びつけた。ローカルが決して理解を妨げないという全称命題にせずusuallyの条件を保持。英語の当該分析を全言語・全状況へ一律適用しない。',['S119'],['原稿6〜8頁の組織範囲と通常の意思疎通への影響に一致','本文にある語順・接続表現の例を除外','原稿が明示する二分類の区別を否定','通常の条件とグローバルの組織範囲の両方に反する'])
(b.OUT/'changes_batch54.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+"\n| S119 | Marina K. Burt（1974）[Error Analysis in the Adult EFL Classroom 原発表稿](https://files.eric.ed.gov/fulltext/ED091950.pdf)、[ERIC書誌ED091950](https://eric.ed.gov/?id=ED091950) | 23頁PDF本文取得。原稿6～8頁：globalは全体の文組織、localは一部の要素。localの意思疎通への影響にusually等の条件。語順・接続表現の例。PDF8・9頁画像で定義を照合。 | 2026-10-13取得。1974-06-21発表稿の分類として指定。1975年の掲載版を取得したとはしない。全言語への普遍化、成人への訂正の心理的効果の一般化は承認範囲外。 | Q_4_074 |\n")
print('1 question /',len(extra),'edits')
