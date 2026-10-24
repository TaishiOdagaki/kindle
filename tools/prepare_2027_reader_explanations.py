"""Explicit reader-facing wording repairs; never assign scholarly approval."""
import json,copy
from pathlib import Path
from audit_2027_epub import read_epub
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';_,_,qs,_,_=read_epub(R/'publishing/2027/round40/2027_review_manuscript.epub');B={q['id']:q for q in qs};changes=[]
for id in ['Q_1_008','Q_1_034','Q_1_035','Q_2_014','Q_3_019','Q_3_029','Q_4_036','Q_4_037','Q_O_066','Q_O_070']:
 b=B[id];a=copy.deepcopy(b)
 if id in ['Q_1_008','Q_1_034']:a['stem']=a['stem'].replace('2026年10月18日に取得した','2026年10月18日時点の')
 e=a['explanations']
 if id=='Q_1_034':
  e[0]=e[0].split('EJUを研究能力全般')[0];e[3]=e[3].split('旧稿の')[0]
 if id=='Q_1_035':
  e[1]=e[1].split('旧解説の')[0];e[3]=e[3].split('旧稿の')[0]
 if id=='Q_2_014':e[1]=e[1].split('旧稿の')[0]
 if id=='Q_3_019':e[3]=e[3].replace('日本語例はRichardsの概念を用いて本監査で構成したものです。','日本語例はRichardsの概念を用いて構成した架空の例です。')
 if id=='Q_3_029':e[3]=e[3].split('旧稿の')[0]+'本問では語の内部構造の分析や他者への質問などを除き、文脈を手掛かりに未知語の意味を推測する行動に限定しています。'
 if id=='Q_4_036':e[0]=e[0].replace('取得した本人の記事','本人の記事')
 if id=='Q_4_037':e[1]=e[1].replace('取得したCLIL','CLIL')
 if id=='Q_O_066':e[3]=e[3].replace('取得した著者','著者')
 if id=='Q_O_070':e[0]=e[0].replace('取得した枠組み','この枠組み')
 assert a!=b and a['answer']==b['answer'] and all(a['explanations'])
 changes.append(dict(id=id,before=b,after=a,reason='制作履歴・取得作業の説明を監査記録へ分離し、読者向けの内容説明と参照時点の表示に整える。学術的な追加承認を与える変更ではない。',category='reader_facing_editorial_cleanup'))
(O/'reader_wording_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n');print('10 explicit wording repairs prepared')
