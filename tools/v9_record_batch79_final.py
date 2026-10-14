"""Update batch79 evidence after the final Presentation wording clarification."""
from pathlib import Path
import hashlib,json,re
p=Path('audit/v9');render=Path('/tmp/batch79c-qa')
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
f=p/'README.md';s=f.read_text();assert '210問1704箇所' in s or '210問1705箇所' in s;f.write_text(s.replace('210問1704箇所','210問1705箇所'))
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;s=f.read_text();head,tail=s.rsplit('## 第79バッチ（2026-10-14）',1)
 tail=tail.replace('画像精読後に解説の曖昧な係り受け1箇所を追補修正した。合計5問46箇所。','画像精読後に解説の曖昧な係り受けと、初提示の段階区別の2箇所を追補修正した。合計5問47箇所。').replace('changes_batch79.jsonとchanges_batch79b.json','changes_batch79.json・changes_batch79b.json・changes_batch79c.json').replace('210問1704箇所','210問1705箇所')
 if '最終保存前の追補：' not in tail:
  tail+='\n最終保存前の追補：Q_4_064解説4で、新形式の初提示はPresentationの説明であると明示し、Productionとの違いを明確にした。正答番号・判定は変更なし。追補後の新しい出力先batch79c-qaに描画し直し、対象7頁を再目視した。\n'
 f.write_text(head+'## 第79バッチ（2026-10-14）'+tail)
f=p/'visual_qa.md';s=f.read_text();head,tail=s.rsplit('## 第79バッチ',1);tail=tail.replace('追補の文言修正後','二つの追補修正後').replace('変更46履歴','変更47履歴');f.write_text(head+'## 第79バッチ'+tail)
cs=sum([json.loads((p/name).read_text()) for name in ['changes_batch79.json','changes_batch79b.json','changes_batch79c.json']],[]);assert len(cs)==47
effective={(e['id'],e['field'],e['index']):e for e in cs};assert len(effective)==45
f=p/'evidence/batch79_review.json';e=json.loads(f.read_text());assert e['edits']==46
e['prior_46_edit_render']={k:e.pop(k) for k in ['docx_sha256','pdf_sha256','page_sha256','changed_strings_missing_in_pdf']}
e.update(edits=47,application_order=e['application_order']+['tools/v9_apply_batch79c.py'],final_wording_review='Q_4_064解説4で初提示はPresentationと明記。最終追補後の399頁描画のうち対象7頁を画像で再目視。最終PDF・PNG一時ファイルは実行環境更新後に失われたため最終描画のハッシュと全文抽出検査は記録していない。46変更時点のハッシュはprior_46_edit_renderに区別して保存。',docx_sha256=sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'))
f.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
