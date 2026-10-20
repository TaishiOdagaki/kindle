"""Record glossary source clarification after affected-page image inspection."""
import json,hashlib,subprocess,html,tempfile
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa202b');BASE='bc373c1326a7efdac27e49df3999ae64972800fb'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def old(n):return subprocess.check_output(['git','show',BASE+':audit/v9/'+n])
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'
with tempfile.TemporaryDirectory(prefix='v9-202-') as t:
 f=Path(t)/'prior.docx';f.write_bytes(old(doc.name));_,q0,a0=qa.audit(str(f));paras0,_=qa.load(str(f))
_,q,a=qa.audit(str(doc));paras,_=qa.load(str(doc));assert q==q0 and a==a0 and len(q)==len(a)==500
cs=json.loads((p/'changes_batch202.json').read_text());assert len(cs)==1
assert json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
assert [x['t'] for x in paras]==[x['t'].replace(cs[0]['before'],cs[0]['after']) for x in paras0]
assert (p/'decisions.json').read_bytes()==old('decisions.json') and (p/'ledger.json').read_bytes()==old('ledger.json')
assert sha(Path('登録日本語教員試験決定版問題集_v8_修正版.docx'))=='4aef79631da7096e5837dd31473978d40d4932ba3cf8473c52138662a843d498'
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(old('postfix_machine.json'))
assert len(machine['issues'])==159
assert [x for x in machine['issues'] if x[0]!='V1']==[x for x in prior['issues'] if x[0]!='V1']
matches=json.loads((r/'matches202.json').read_text());assert len(matches)==1 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns});count=len(PdfReader(r/'qa.pdf').pages)
source=Path('../inoue202.pdf');assert len(PdfReader(source).pages)==18
e=dict(batch=202,base_remote_commit=BASE,source=dict(id='S67',title='井上優 モダリティ',url='https://www2.ninjal.ac.jp/takoni/DGG/09_modarityi.pdf',retrieved='2026-10-20',pages=18,sha256=sha(source),bytes=source.stat().st_size,body_read='印刷133～135頁/PDF1～3の全本文。133頁のムードの狭い用法、134頁の二群と学説差の留保。'),edited_block='APPENDIX_GLOSSARY',edits=1,question_edits=0,all_500_question_answer_text_unchanged=True,decisions_and_ledger_unchanged=True,total_edits=4315,raw_machine_warnings=159,warning_disposition=dict(code='V1',result='用語範囲の留保を用語集へ反映。指定資料の用語差であり一括置換しない。',reason='S67はモダリティの別称としてムードを挙げつつ、ムードを述語形態に限る用法も注記。両語が登場すること自体を表記ゆれの誤りとはしない。'),prior_dispositions_revalidated=39,revalidation='全500問の設問・全肢・既存正答・全解説が前稿と同一。第200・201の文脈照合理由は維持。T3対象を含む全段落はこの用語集1箇所を除き同一。',total_disposed_warnings=40,remaining_unreviewed_warning_instances=119,remaining_codes={'P1':119},docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),render_pages=count,visually_reviewed_pages=pages,page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch202_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
report=f'''\n\n## 第202バッチ 2026-10-20\n\n用語集の「モダリティ（ムード）」をS67原資料の範囲に合わせ1箇所改訂。全18頁PDFを再取得し、印刷133～135頁の本文を精読。モダリティを話し手の判断および発話・伝達態度の意味として説明し、ムードと呼ぶ場合がある一方、ムードを述語形態に限る用法もあると留保を追加した。Q_5_059・060で資料体系を指定した既存の改訂とも整合。用語を一括置換せず、V1の警告自体は残す。\n\n累積493問4315箇所（今回の追加は問題ではなく用語集）。全500問の設問・4肢・正答・全解説が前稿と完全同一、decisions・台帳も不変を比較。第200・201で処置した39警告の対象文脈は全て維持。今回のV1と合わせ40件処置済み、処置点検残119件（P1）。生警告は159件を隠さず保持。v8ハッシュ不変、キー・タグ・早見表・リンク等の既存構造検査を再実施。\n\n完全CJK・非CJK代替収録を検査後、新規{count}頁描画の用語集改訂文字列を検出し、影響{pages}頁を直接画像確認。最終全頁画像QAではない。原資料のハッシュ、原稿の全問不変比較、描画証跡はevidence/batch202_review.json。前付け・用語集他項目等の横断点検、改頁調整、119警告の処置、全頁最終QAは継続中。最終v9未制作、出版不可。\n'''
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第202バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第202バッチ S67用語集への適用\n\n[井上優「モダリティ」](https://www2.ninjal.ac.jp/takoni/DGG/09_modarityi.pdf)全18頁を2026-10-20再取得。印刷133～135頁の全本文を精読し、モダリティの二群とムードの別称／形態への限定用法を用語集へ反映。全学説共通の唯一の定義にはしない。取得バイト・SHA256はevidence/batch202_review.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('493問4314箇所','493問4315箇所')+'\n第202バッチ：用語集のモダリティ／ムードをS67本文の留保に合わせ1箇所改訂。500問の本文・正答・判定は不変。機械警告の処置は累計40件、未処置119件（全てP1）。直前の120件は第201時点の履歴。新規描画の用語集影響頁を確認したが、全頁最終QA・他の横断点検は未完了。\n')
print('Glossary clarified; 119 warnings remain; 500 question bodies unchanged.')
