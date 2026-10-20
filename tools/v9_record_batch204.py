"""Record primary-source glossary repair and verify all question text unchanged."""
import json,hashlib,subprocess,tempfile
from pathlib import Path
from docx import Document
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');r=Path('../qa204');BASE='d4e474b203953293aaa3d0402cf93a7f9561b16c'
def old(n):return subprocess.check_output(['git','show',BASE+':audit/v9/'+n])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';cs=json.loads((p/'changes_batch204.json').read_text());assert len(cs)==1
assert json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
with tempfile.TemporaryDirectory(prefix='v9-204-') as t:
 f=Path(t)/'before.docx';f.write_bytes(old(doc.name));_,q0,a0=qa.audit(str(f));paras0,_=qa.load(str(f))
_,q,a=qa.audit(str(doc));paras,_=qa.load(str(doc));assert q==q0 and a==a0 and len(q)==len(a)==500
assert [x['t'] for x in paras]==[x['t'].replace(cs[0]['before'],cs[0]['after']) for x in paras0]
assert (p/'decisions.json').read_bytes()==old('decisions.json') and (p/'ledger.json').read_bytes()==old('ledger.json')
assert sha(Path('登録日本語教員試験決定版問題集_v8_修正版.docx'))=='4aef79631da7096e5837dd31473978d40d4932ba3cf8473c52138662a843d498'
rs=[z for x in Document(doc).paragraphs if x.text==cs[0]['after'] for z in x.runs if z.text]
assert len(rs)==2 and rs[0].text==cs[0]['glossary_head'] and rs[0].bold is True and rs[1].bold is False
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(old('postfix_machine.json'))['issues'] and len(machine['issues'])==159
matches=json.loads((r/'matches204.json').read_text());assert len(matches)==1 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns});count=len(PdfReader(r/'qa.pdf').pages)
s=Path('../standards204.pdf');assert len(PdfReader(s).pages)==240 and sha(s)=='78182353e8cd877535f6f3c8967da52d4d3af64725146c08606d38825941ac61'
failed=[]
for name in ['kinsui204.pdf','kinsui204-complete.pdf','kinsui204-alt.pdf','kinsui204-range.part']:
 f=Path('..')/name;failed.append(dict(file=name,bytes=f.stat().st_size,sha256=sha(f),body_used=False))
e=dict(batch=204,base_remote_commit=BASE,source=dict(id='S142',url='https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf',retrieved='2026-10-20',bytes=s.stat().st_size,sha256=sha(s),pages=240,body_read='印刷11と33～34頁の全本文。11・33頁は直接原画像も確認。全書全主張の承認ではない。'),source_retry_failure=dict(id='S201',url='https://www.jstage.jst.go.jp/article/nihongokyoiku/150/0/150_34/_pdf/-char/ja',failure='HTTP/2 stream INTERNAL_ERROR、HTTP/1.1 outstanding read data、Web timeout。PDF xrefとpagesが破損。Range要求にも200で全体を返し再切断。過去保存済み3390457バイト/SHA3987f263…とも一致しないため使用しない。アクセス権の拒否ではない通信切断。',attempts=failed,glossary_role_language_still_pending=True),edited_block='APPENDIX_GLOSSARY',edits=1,total_edits=4316,all_500_questions_answers_unchanged=True,decisions_and_ledger_unchanged=True,raw_machine_issues=159,prior_dispositions_revalidated=51,remaining_unreviewed_warning_instances=108,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),render_pages=count,visually_reviewed_pages=pages,page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},font_sha256=sha(Path('../NotoSansCJKjp-VF.ttf')),glossary_style_checked={'head_bold':True,'explanation_bold':False},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch204_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
report=f'''\n\n## 第204バッチ 2026-10-20\n\n用語集の妥当性／信頼性1箇所を、S142の2014年版Testing Standards印刷11・33～34頁に照合して改訂。用途別の得点解釈を証拠と理論が支持する程度という妥当性の定義と、手続反復時の一貫性・課題／時点／採点者の変動という信頼性・精度の説明を明示。既存改訂問Q_1_037等の定義と整合させた。公式全240頁を再取得し、本文3頁と画像2頁を直接照合、原バイトは過去取得と同じSHA256。最新版や全研究者の唯一の定義とはしない。\n\n累積493問4316箇所。今回の追加は用語集であり、全500問の設問・全肢・正答・解説、台帳とdecisionsは前稿と完全同一。生警告159件不変、既処置51件の対象文脈は保持、未処置108件。見出しだけ太字、説明は通常字の書式を検査。CJK全字と代替収録を確認して新規{count}頁を描画し、影響{pages}頁の画像を直接確認。最終全頁QAではない。v8不変と構造・キー・タグ等の検査を再実施。\n\n役割語のS201原論文再取得はHTTP/2とHTTP/1.1の途中切断、Web timeoutで失敗。4取得ファイルのいずれも既知の全3390457バイト・ハッシュに一致せず、PDF解析で破損を検出した。Range要求も200応答で全体を返した後に切断するため、部分ファイルを継ぎ合わせたり修復推測したりせず、根拠に使用しない。用語集の役割語は未改訂の横断残件として保留。原資料取得の障害・ファイルハッシュ・新稿の画像証跡はevidence/batch204_review.json。\n\n原稿は作業中。役割語などの横断点検、機械警告処置、改頁調整、全頁最終画像QAは未完了。最終v9未制作、公開・KDP配信・元ブランチへのマージは行わない。\n'''
for name in ['critical_findings.md','interim_report.md','visual_qa.md']:
 f=p/name;assert '## 第204バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第204バッチ S142用語集への適用\n\n[Testing Standards 2014公式全文](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf)全240頁を2026-10-20再取得、印刷11・33～34頁本文と11・33頁画像を精読し、用語集の妥当性／信頼性を改訂。S201の再取得は切断・破損のため使用せず、役割語の用語集改訂は保留。原バイトと障害の詳細はevidence/batch204_review.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('493問4315箇所','493問4316箇所')+'\n第204バッチ：S142本文により用語集の妥当性／信頼性1箇所を改訂し画像確認。500問本文・正答・台帳・判定は不変。S201原論文の再取得は途中切断・破損のため使わず、役割語の用語集修正は保留。警告未処置108件。全頁最終QA・改頁調整・横断点検は継続中。\n')
print('Glossary validity/reliability repaired; 500 question bodies unchanged.')
