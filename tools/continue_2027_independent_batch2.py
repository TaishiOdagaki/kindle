"""Explicit batch2 findings; preserve all previous independent judgments."""
import json,hashlib,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';rows=json.loads((O/'ledger_500.json').read_text());D={
'Q_4_008':(3,['S147'],[8,20],['フォワードの方向','セントラルの方向','学習成果を出発点にする図4','授業後の得点による後付けではない']),
'Q_4_029':(1,['S147'],[13,20,30],['表2セントラルの活動基盤・交渉・発展','交渉を否定して固定','交渉を除外して発音のみに限定','表2の学習者と教師の役割と逆']),
'Q_4_049':(1,['S144','S147'],[7],['言語機能を編成基準にする','文法を場面と誤対応','主題名をタスクと誤対応','目標書式から内容編成は決まらない']),
'Q_4_062':(2,['S147'],[28],['成果が後回しで図と逆','図10の段階順序に一致','成果を最後にする順序は異なる','図10の成果と教材・テストを除外']),
'Q_1_031':(2,['S04'],[13,14,18,21,22,44],['尊敬語と謙譲語Ⅱの混同','5分類と3分類の対応は13頁に一致','美化語を尊敬語へ一括する誤り','社外でも必ず上司を立てるという誤り']),
'Q_2_019':(4,['S04'],[13,15,16,18,19,21],['美化語を尊敬語に含める誤り','向かう先への謙譲ⅠをⅡと誤分類','謙譲Ⅱの働きをⅠと誤分類','原則として正しいが本人のみでなく自分側を含む点と例外を補う']),
'Q_2_020':(1,['S04'],[18,22,43,44,51],['自分側の父に申すを使える','自分側を必ず立てる説明は原則と逆','申すは謙譲Ⅱであり尊敬語でない','社内外の選択変更を禁止していない']),
'Q_2_021':(1,['S04'],[30],['同語に同種類の敬語を重ねる','て連結でなく同語に重ねる形','一文に二種類あるだけでは二重でない','読むといるの敬語連結']),
'Q_2_023':(3,['S04'],[18,24,48,49],['参るは謙譲Ⅱ','形式だけで適切さは保証されない','分類と依頼の場面条件を区別','目上への一律禁止はない']),
'Q_2_024':(2,['S04'],[50],['品を立てる形式を推奨していない','型を基礎に表現の工夫を継続','若者だけに特有と明確に否定','態度と言葉の不一致も問題']),
'Q_2_025':(3,['S04'],[14,15,18,19,20],['参るは行為者を立てる尊敬語でない','ですますは話文章の相手への丁寧さ','立てる対象と丁重丁寧に述べる相手を区別','向かう先と話相手が異なれば働きも違う']),
'Q_4_090':(1,['S04'],[7,18,48,49],['場面・負担・関係による選択','前置き全省略は負担への配慮と不一致','立てるべき相手の行為に参るを必須とできない','正しい形式だけでは場面の適合性は決まらない']),
'Q_4_091':(4,['S04'],[16,26,27,40],['拝見は謙譲Ⅰ','確認する主体と恩恵の向きが逆','いただくの主体がBとなり指定関係と違う','A側からBの確認の恩恵を受ける']),
'Q_4_092':(1,['S04'],[48,49],['急な依頼の負担を示す前置き','敬語形式のみでは配慮を保証しない','同僚でも負担の配慮が必要な指定場面','簡潔な依頼の適切な場合もある']),
'Q_5_099':(2,['S04'],[7,10,11,44,51],['場面を無関係とする誤り','指定関係と負担で選ぶ練習','親しさ等を無視する説明は原則と逆','方言敬語の身内敬語等を無視']),
'Q_O_011':(3,['S04'],[14,18,44],['おっしゃっての活用は正しい','社内の上下のみで固定できない','取引先へは部長を自分側として扱う','おっしゃるは尊敬語']),
'Q_O_014':(4,['S04'],[10,11,44],['場面を除くドリルでは目的に不一致','場面による選択も指導の対象','扱わない方針では目的に不一致','社内外の具体的比較が目的に対応']),
'Q_O_015':(2,['S04'],[10,11],['形式だけに限定して場面選択を除外','仕組み・複数例・選択と実践を併用','唯一表現の固定は指針と逆','経験だけで意図的学習を除くのは指針と逆']),
'Q_M_013':(1,['S04'],[2,5,48,49],['敬語は敬意表現に含まれる','敬意表現の範囲を狭めている','人間関係を表す働きを否定','前置き等を含む敬意表現をですますに限定']),
'Q_M_014':(1,['S04'],[18,22,44],['社内外の社長の例に対応','例示された使い分けを否定','自分側でも聞き手へ丁重に述べられる','場面選択を敬語全廃と誤解']),
'Q_M_055':(4,['S04'],[27,40],['使用頻度から適切さは決まらない','いただくは謙譲Ⅰ','基本条件の許可と恩恵を除外','許可・恩恵の事実や気持ちという条件']),
}
for r in rows:
 if r['id'] not in D:continue
 key,src,pages,reasons=D[r['id']];r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=src,printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(reasons,1)],all_four_explanations_reviewed=True,explanation_finding='全4解説と補助的主張を原資料へ照合。個人差・基本原則・指定モデルと効果保証を区別。',multiple_correct=False,no_correct=False,manuscript_change_required=r['id'] in ['Q_1_031','Q_2_019'])
 if r['manuscript_change_required']:r.update(status='修正待ち',explanation_finding='自分自身への限定を避け、基本的に自分側、第三者・事物への使用もあるという18頁の範囲へ補正する。正答番号は維持。')
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
s=json.loads((O/'source_manifest.json').read_text());s.extend([dict(id='S147',url='https://www.professorjackrichards.com/wp-content/uploads/Curriculum-Approaches-in-Language-Teaching.pdf',sha256='b1585867ba0fb153a9d273bbacba268008025d5f970c2efcd6e4c7cc23386de0',retrieved='2026-10-24',pdf_pages=29,printed_pages_read=[7,8,13,20,28,30],printed_images_read=[7,8,28,30],pdf_page_one_based_offset=-4),dict(id='S04',url='https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/keigo_tosin.pdf',sha256='3a567c6d85e990e0f90f0698c1403ba5826c7c6f9e7e50c93ea5d4da9336882d',retrieval='Previous downloaded original PDF reread independently2026-10-24; not a new download',printed_pages_read=[2,3,4,5,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22,23,24,26,27,30,38,39,40,43,44,48,49,50,51],printed_images_read=[13,18,30,40,44,49,50,51],pdf_page_one_based_offset=3)])
(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('Batch2:',len(D),'total read:',sum(x['reviewed_this_pass'] for x in rows))
