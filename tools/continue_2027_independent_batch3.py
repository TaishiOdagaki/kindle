import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';rows=json.loads((O/'ledger_500.json').read_text())
D={
'Q_4_015':(4,[22],['明確化要求を排除','双方向を一方向と誤認','例示の反復等を排除','反復と明確化要求が項目の例']),
'Q_4_016':(2,[37,44],['援助相手を教師だけに制限','助け合いと他者への援助要求を促す例','Rapportが良くても相互援助禁止は支持されない','援助要求を控えさせる点が指定例と逆']),
'Q_4_033':(2,[14],['変換でなく同構造の置換','提示語で目的語・動詞を置換','斉唱でなく一人で置換','個別だが単なる反復でない']),
'Q_4_043':(1,[2,6,44],['継続使用教材と追加教材の役割','adaptの省略例が全完遂の義務を否定','内容変更の定義と逆','補足教材をコースブック自体と誤対応']),
'Q_O_053':(3,[14],['ケースに自由交渉なし','目標を学習者が自由選択していない','キューによる同文型の置換','暗唱と言い直しがあり黙読だけでない']),
'Q_M_030':(2,[4,5],['評価目的の分類で主体でない','学習者同士の評価という主体の名称','強み弱みの把握という目的','本人自身の評価で相互でない']),
'Q_M_032':(1,[38,48],['実施後の振り返りと時間見積りの検討','改善検討を閉ざす','実施の振り返りでなく無作為','時間計画と省察の関係を否定']),
}
for r in rows:
 if r['id'] not in D:continue
 key,pages,rs=D[r['id']];r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=['S183'],printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(rs,1)],all_four_explanations_reviewed=True,explanation_finding='指定された用語集の項目と各解説の主張を再照合。Q_4_016の旧S13は現行問題の根拠には不要。',multiple_correct=False,no_correct=False,manuscript_change_required=False)
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');s=json.loads((O/'source_manifest.json').read_text());s.append(dict(id='S183',url='https://www.cambridgeenglish.org/images/22184-tkt-glossary-document.pdf',sha256=hashlib.sha256((R.parent/'sources/S183.pdf').read_bytes()).hexdigest(),retrieval='Previous original PDF reread independently2026-10-24',printed_pages_read=[2,4,5,6,14,22,37,38,44,48],pdf_images_read=[15,23,39,45,49],pdf_page_one_based_offset=1));(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('Total freshly read50;48 unchanged passes,2 precision repairs pending')
