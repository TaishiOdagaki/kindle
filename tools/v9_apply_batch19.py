#!/usr/bin/env python3
"""Correct the purpose of vocabulary preparation without inferring processing type."""
import json, html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text())
assert len(prior)==346
_,Q,A=qa.audit(str(b.DST))
extra=[]
why='語彙確認だけから既有知識の活性化・主目的トップダウンと確定する旧説明を撤去。ケースとBritish Councilの教師向け本文に合わせ、後続の聴解への語彙準備として問う。'
def record(field,index,new):
 old=Q['Q_MO_002']['opts'][index] if field=='options' else A['A_MO_002']['txt'][index]
 if html.unescape(old)!=new:extra.append(dict(id='Q_MO_002',field=field,index=index,before=html.unescape(old),after=new,reason=why,sources=['S55'],applied=True,before_version='第18修正バッチ作業稿'))
record('options',1,'教材の理解に関係する語彙を事前に確認し、後続の聴解に備えること')
exps=['ケースで追加したのは、後続の聴解に備える語彙確認です。発音を採点・評価する手順は示されていません。','聴解前の語彙確認は、教材の理解に必要な語彙を準備する活動です。既知語の活性化か未習語の事前指導かなど、活動の内容によって支援の働きは異なります。活動名だけからトップダウン処理に限定することはできません。','語彙確認は教材理解への準備であり、利用許諾などの著作権確認とは別の課題です。ケースにも著作権確認を追加した記述はありません。','聴解前活動は、後続の聴解に備える活動です。ケースでは画像を見せながら聞かせることも予定されており、聴解活動を省略することではありません。']
for i,t in enumerate(exps):record('explanations',i,t)
(b.OUT/'changes_batch19.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D['Q_MO_002'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S55'],option_verdicts=['評価手順のない語彙準備を発音評価とするため誤り','教材理解のための事前語彙準備で正しい','語彙準備と著作権確認を混同して誤り','後続聴解への準備を聴解省略とするため誤り'],stem_review='レストランの注文場面のケース全段落と隣接問題を確認。語彙確認の目的を問い、処理分類の断定を撤去。',explanation_review='ケースと取得した聴解前活動・トップダウン／ボトムアップの本文に4肢・4解説を照合。教育効果の普遍化はしない。',reason=why,multiple_correct_risk='なし：ケースに整合する語彙準備は2のみ',no_correct_risk='なし：独立正答2',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S55 | British Council TeachingEnglish [Pre-listening](https://www.teachingenglish.org.uk/professional-development/teachers/teaching-knowledge-database/n-p/pre-listening)、Catherine Morley [Listening Top-down and bottom-up](https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/listening-top-down-and-bottom) | 本文全体を取得。語彙の事前指導・活性化等の複数目的、背景知識による理解と音声信号の分割・解読の区別、双方の組合せを確認。語彙確認だけでは主目的の処理分類を確定できない点は設問条件と合わせた監査判断。 | Q_MO_002 |\n')
print('Recorded',len(extra),'repairs')
