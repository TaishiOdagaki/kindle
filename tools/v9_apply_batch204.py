"""One-time glossary validity/reliability clarification from the full primary book."""
import json
from pathlib import Path
import quiz_audit as qa
p=Path('audit/v9');cs=json.loads((p/'changes.json').read_text());assert len(cs)==4315
old='妥当性／信頼性　測定したいものを正しく測れているかという妥当性と、結果の安定性を示す信頼性。'
paras,_=qa.load(str(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'));assert sum(x['t']==old for x in paras)==1
new='妥当性／信頼性　2014年版Testing Standardsでは、妥当性は、提案された用途に対するテスト得点の解釈を証拠と理論が支持する程度をいう。信頼性・精度は、測定手続を反復したときの得点の一貫性に関わり、課題・時点・採点者などによる変動を検討する。'
c=dict(id='APPENDIX_GLOSSARY',field='glossary',index=None,before=old,after=new,reason='S142公式全240頁PDFを再取得し、印刷11頁と33～34頁の本文を精読、11・33頁の画像を照合。測定したいものを正しく測るという用語集の簡略説明を、改訂問Q_1_037等と同じ用途別得点解釈の根拠へ合わせ、信頼性・精度も反復と課題・時点・採点者の変動を明示。版と資料体系を指定し、最新全学説・個別試験の品質保証とはしない。',sources=['S142'],applied=True,before_version='第203バッチ後',glossary_head='妥当性／信頼性')
(p/'changes.json').write_text(json.dumps(cs+[c],ensure_ascii=False,indent=2)+'\n');(p/'changes_batch204.json').write_text(json.dumps([c],ensure_ascii=False,indent=2)+'\n')
