"""Record explicit new judgments; no inherited pass or answer inference."""
import json,sys,hashlib
from pathlib import Path
from audit_2027_epub import read_epub
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';p=R/'publishing/2027/round40/2027_review_manuscript.epub';_,_,qs,_,_=read_epub(p)
# Manually written after reading the current question and the specified original pages.
D={
'Q_4_002':(3,[5],['教師の発話再現のみで協働を除外','正確さのみを役割に限定','促進・見守りが指定の参加を支える','学習者の責任と参加を除外']),
'Q_4_009':(1,[12],['職務上の言語使用を調査する案','目次を調査結果の代わりにする','職務差を未調査で否定','語彙以外の特徴を排除']),
'Q_4_011':(1,[11],['四技能と下位技能を編成単位にする','機能の基準を文法と誤対応','文法順序をタスクと誤対応','技能の基準を機能と誤対応']),
'Q_4_014':(1,[28,29,30],['主題を先に置き複数活動を編成','設問と編成の順序が逆','主題の編成機能を除外','設問にある技能の結合を否定']),
'Q_4_020':(4,[19],['一人で完結し情報交換不要','完成回答の復唱のみ','個別に完結して交換しない','分有情報の交換で全体を完成']),
'Q_4_023':(2,[10,11,28,31],['話題を配列単位にする案','文法項目のレベル・順序で編成','機能を単位にする案','達成作業を単位にする案']),
'Q_4_024':(4,[11],['文法項目の順序が基準','作業が基準','技能と下位技能が基準','言語機能に沿って語彙文法を選ぶ']),
'Q_4_025':(2,[11],['分野名だけでは編成基準にならない','設問の機能単元と文法一覧を両方認識','明示された機能の関与を否定','明示された文法の関与を否定']),
'Q_4_032':(4,[7],['初段階の教科書不参照と反対','最小限の文法説明と反対','直接即時の訂正と反対','原著に記された段階1〜3の順序']),
'Q_4_035':(2,[31],['特定形式が必要な教室用タスクを誤排除','意味・成果・既有資源という特徴','意味への焦点を除外','教室用タスクを誤排除']),
'Q_4_040':(2,[18],['未知情報を求めない復唱','互いに見えない絵の情報差','未知情報取得を含めないと明示','個人書換えで交換なし']),
'Q_4_042':(2,[18,31],['音声再現だけが成果','情報差を使い乗継案を決める成果','例文提出だけが成果','文型の文をそろえるだけが成果']),
'Q_4_044':(4,[20,21],['無加工の普遍的優位は資料にない','文化情報を利点から否定','批判と作成教材の可能性を否定','利点と難点を併記した議論']),
'Q_4_045':(3,[20],['読み一覧のみでは指定情報を確認しない','音声再現のみでは指定情報を確認しない','地区と品目を照合して指定情報を選ぶ','文末転記のみでは指定情報を確認しない']),
'Q_4_063':(2,[8],['新形式提示・理解確認を除外','Presentationに対応','Practiceに対応','Productionに対応']),
'Q_4_064':(2,[8],['自由な使用への移行を除外','制御練習から自分の情報を使う運用へ','Productionを除外','Productionを初提示と誤対応']),
'Q_4_065':(1,[8],['提示・制御練習・自分の内容での運用','応用も固定ドリルのまま','形式の初提示が最後で順序が異なる','応用に使用活動なし']),
'Q_4_066':(4,[16,17],['人数だけの分類ではない','個人情報の文完成A/Bを誤排除','有意味な選択を排除','意味理解を要する条件による区別']),
'Q_O_052':(4,[8,31,32,33,34],['指定文再現だけで依頼達成を除外','言語整理を一律禁止する誤り','設問の活動先行をPPP順序と誤認','既有資源で依頼し事後に形式整理']),
'Q_O_055':(3,[14,15,16],['形式練習を全排除','目標と活動の焦点の区別を無視','目標と観察に応じ双方を関連付ける','正確さ活動は後にも置ける']),
'Q_M_025':(3,[28,30],['内容先行の順序が逆','一単元の利用を誤排除','内容先行と正確さの論点を両立','評価を実施上の論点から除外']),
'Q_M_040':(4,[19],['価値観等の比較であり分有統合でない','形式変換であり分有統合でない','新情報の推論が指定の構成名でない','分有情報を統合して全体を完成']),
}
rows=[]
for q in qs:
 row=dict(id=q['id'],status='未着手',current_question_sha256=hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),reviewed_this_pass=False)
 if q['id'] in D:
  key,pages,reasons=D[q['id']];assert key==q['answer'] and len(reasons)==4
  row.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=['S144'],printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(reasons,1)],all_four_explanations_reviewed=True,explanation_finding='各肢の判定理由・補助的主張を指定頁へ照合。効果保証とモデル記述を区別しており追加修正不要。',multiple_correct=False,no_correct=False,manuscript_change_required=False,scope='Richards2006自身の説明と架空の適用を確認。引用された他著者の原著全体を確認した意味ではない。')
 rows.append(row)
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(O/'source_manifest.json').write_text(json.dumps([dict(id='S144',url='https://www.professorjackrichards.com/wp-content/uploads/Richards-Communicative-Language.pdf',sha256='47b6df7be48b29e4f54873536db95e29d9f7a4efe3223c7222e3a0b7ee1791e6',retrieved='2026-10-24',pdf_pages=52,printed_pages_read=[5,7,8,10,11,12,14,15,16,17,18,19,20,21,28,29,30,31,32,33,34,35,45],printed_images_read=[7,11,17,19,28,31],pdf_page_one_based_offset=4)],ensure_ascii=False,indent=2)+'\n')
(O/'retrieval_limits.json').write_text(json.dumps([dict(source='S213',url='https://rm.coe.int/16807bc66c',local_pdf_download='HTTP403',web_text_available=True,web_screenshots='several cache misses',status='本文照合中・画像未完了、19問を確認済みに自動計上しない'),dict(question='Q_4_049',source='S147',status='Richards2006部分は確認。2013論文7頁の追加根拠が未取得のため未承認')],ensure_ascii=False,indent=2)+'\n')
print('New primary-source judgments recorded:',len(D),'of500')
