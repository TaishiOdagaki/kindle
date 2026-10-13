#!/usr/bin/env python3
"""Evidence-bound reading/listening revisions. One-time batch 49."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==911
_,Q,A=qa.audit(str(b.DST));D=json.loads((b.OUT/'decisions.json').read_text());extra=[]
def rewrite(qid,key,stem,opts,exps,reason,sources,verdicts):
 for field,old,new in [('stem',[Q[qid]['stem']],[stem]),('options',Q[qid]['opts'],opts),('explanations',A['A_'+qid[2:]]['txt'],exps)]:
  for i,(before,after) in enumerate(zip(old,new)):
   if html.unescape(before)==after:continue
   extra.append(dict(id=qid,field=field,index=None if field=='stem' else i,before=html.unescape(before),after=after,reason=reason,sources=sources,applied=True,before_version='第48修正バッチ作業稿'))
 D[qid].update(status='確認済み',fixes_applied=True,independent_answer=key,sources=sources,option_verdicts=verdicts,reason=reason,stem_review='取得した本文の定義と条件に限定し、4肢を独立判定。',explanation_review='全4解説を根拠本文へ照合。本文にない一般的効果・全称命題を撤去。',unresolved='',multiple_correct_risk='なし：指定された定義・手順に合うのは正答のみ',no_correct_risk='なし：独立正答'+str(key))
rewrite('Q_3_002',1,
 '聴解授業で、背景知識を使って音声の内容を予測するトップダウン処理の練習として、最も適切な活動を選びなさい。',
 ['聞く前に話題や場面を示し、そこでどんな内容が語られそうか、知っていることをもとに予測させる。','音声の流れを単語に分け、聞こえた単語の数を数えさせる。','聞こえた文を文字で確認し、つながった音の中で単語の境界がどこにあるか確かめさせる。','背景知識による予測を行わず、音声の細部を区切って解読する練習だけを行わせる。'],
 ['British Councilは、話題・場面・絵などを手がかりに事前予測する活動を、トップダウン処理の練習として説明しています。','同教材は、単語数を数える活動を、単語間の区切りを認識するボトムアップ処理の練習として示しています。','同教材は、聞いた文と正しい文を比較して単語の境界を意識する活動を、ボトムアップ処理の練習として説明しています。','音声の細部を区切って解読する説明はボトムアップ処理です。設問の背景知識による予測の練習とは異なります。'],
 '語彙の予習が常にボトムアップだけになるという一律の分類と、1.5倍速の未照合条件を撤去。公式教材が説明する具体的活動の区別へ改訂。',['S99'],['教材の背景知識による事前予測に一致','教材では単語区切りの認識練習','教材では音声・単語区切りの確認練習','背景知識による予測を明示的に排除'])
rewrite('Q_5_090',3,
 '【事例】学習者Aさんが架空の記事「火災の現場で、救急隊は住民の傷病の有無を確認した」を読んでいる。Aさんは「傷病（しょうびょう）」を知らなかったが、「傷」はけが、「病」は病気に関わる字だと考え、さらに「救急隊」「有無を確認した」という周囲の記述も使い、「けがや病気」という意味を推測した。この事例で明示された手がかりの利用として、最も適切なものはどれか。',
 ['周囲の記述だけを使い、語を構成する漢字の意味は使っていない。','品詞の特定だけを行い、具体的な意味の推測は行っていない。','語を構成する漢字と周囲の記述の両方を手がかりとして、意味を推測している。','語を構成する漢字だけを使い、周囲の記述は使っていない。'],
 ['設問には、語を構成する漢字の意味も使ったと明記されています。','設問には「けがや病気」という意味を推測したと明記されています。品詞だけの判断ではありません。','設問に示された二種類の手がかりをともに説明しています。「傷病」の意味は辞典でも「けがや病気」と確認できます。手がかりの種類を、そのままトップダウン／ボトムアップの一対一の分類に置き換える必要はありません。','設問には「救急隊」「有無を確認した」という周囲の記述も使ったと明記されています。'],
 '語の構成要素・周囲の記述とトップダウン／ボトムアップを一律に対応させる未照合の説明と、効果的な典型例という評価を撤去。辞典本文で意味を確認した傷病を用い、仮想事例に明示した手がかりの利用を独立判定。',['S107','S108'],['漢字の利用という明示条件と不一致','具体的意味を推測した条件と不一致','両方の明示手がかりと辞典語義に一致','周囲の記述の利用という明示条件と不一致'])
(b.OUT/'changes_batch49.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'''
| S107 | 小学館デジタル大辞泉 [傷病](https://kotobank.jp/word/%E5%82%B7%E7%97%85-533076) | 辞典項目の語義「けがや病気」を確認。 | 2026-10-13項目本文取得。傷病者の法的な範囲や実在災害をこの項目から承認しない。 | Q_5_090 |
| S108 | Kozo Kamimura（2020）[Retention of Inferred L2 Word Meaning Based on Morphological and Contextual Clues](https://www.jstage.jst.go.jp/article/arele/31/0/31_161/_pdf/-char/ja) ARELE31、161–176頁 | 原論文163–164頁の本文に、語自体と周囲の文脈による手がかり、利用できる手がかりの組み合わせが整理されている。 | 2026-10-13全16頁PDF本文取得。日本語の漢字語について同じ効果量・因果関係が実証されたとは扱わない。問題は作成した事例の明示条件の分析に限定。 | Q_5_090 |
''')
print('2 questions /',len(extra),'edits')
