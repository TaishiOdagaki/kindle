import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';rows=json.loads((O/'ledger_500.json').read_text());D={
'Q_4_052':(2,[218,221],['基準準拠の説明を規範と誤対応','定義領域と参照集団分布の区別','規範準拠の説明を基準と誤対応','特定参照集団が定義にある']),
'Q_4_053':(2,[79],['全体一得点は総合的採点','観点ごと独立の得点','いずれも明示的基準が必要','人の判断と訓練監視不一致解消は残る']),
'Q_4_056':(1,[33,34],['測定反復の得点一貫性と誤差要因','完全同一は通常保証されない','採点者差も変動に含まれる','能力不変の仮定を無視']),
'Q_4_057':(4,[11,14],['印象だけで根拠検討を省けない','一根拠で全用途保証はしない','用途ごとの裏付けが必要','用途別得点解釈を証拠理論で検討']),
'Q_4_115':(1,[215,217],['実施方式と過去反応による項目選択の区別','CBTとCATの関係を逆にする','固定項目でもコンピュータ実施ならCBT','項目選択を画面調節と誤認']),
}
for r in rows:
 if r['id'] not in D:continue
 key,pages,rs=D[r['id']];r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=['S142'],printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(rs,1)],all_four_explanations_reviewed=True,explanation_finding='全肢・全解説を共同標準2014本文・用語集に再照合。妥当性の用途別解釈、反復の仮定、人の判断、実施方式と適応的選択を区別。追加修正不要。',multiple_correct=False,no_correct=False,manuscript_change_required=False)
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');s=json.loads((O/'source_manifest.json').read_text());s.append(dict(id='S142',url='https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf',sha256=hashlib.sha256((R.parent/'sources/S142.pdf').read_bytes()).hexdigest(),retrieval='Previous original PDF independently reread2026-10-24',printed_pages_read=[11,14,33,34,79,215,217,218,221],printed_images_read=[33,34,79,215,217,218,221],pdf_page_one_based_offset=10));(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print('Fresh total102/500')
