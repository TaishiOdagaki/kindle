"""One-time checkpoint after full four-question and changed-page review."""
from pathlib import Path
import json,hashlib,subprocess,re,io,csv
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/77d0d0a1a222');render=root/'batch90-restored-qa';targets={f'Q_2_{n:03}' for n in range(14,18)}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');r=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(r)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':232,'修正必要':56,'要追加確認':212}
cs=json.loads((p/'changes_batch90.json').read_text());assert len(cs)==40 and sum(bool(x.get('remove_paragraph')) for x in cs)==4
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f');n=len(pages)-1
matches={str((c['id'],c['field'],c['index'])):[i+1 for i,t in enumerate(pages) if re.sub(r'\s+','',c['after']) in re.sub(r'\s+','',t)] for c in cs if c['after']};assert all(matches.values())
reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:Image.open(render/f'review-{x}.png').verify()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));assert machine['issues']==prior['issues'] and len(machine['issues'])==57
f=p/'README.md';s=f.read_text()
for a,b in [('| 確認済み | 228問','| 確認済み | 232問'),('| 要追加確認 | 216問','| 要追加確認 | 212問'),('要追加確認216問','要追加確認212問'),('241問1990箇所','245問2030箇所'),('241問を','245問を')]:s=s.replace(a,b)
f.write_text(s)
report=f'''

## 第90バッチ（2026-10-15）

最新HEAD 07c71bc1918d5b2742c92a3ee59a1e9f6d1352d8を取得して継続。作業環境の切替後にGitHub正本から作業場を復元し、未保存だった本バッチを再構成した。未保存版や旧描画を完了扱いにせず、別の新規出力先batch90-restored-qaの画像で検証。S149原論文も再取得して同一SHA256を確認した。前バッチで取得したS149原論文印刷26〜29頁（PDF12〜13頁）と表5を用い、関連するQ_2_014〜017の設問・全4肢・独立正答・全4解説まで照合して改訂した。原論文の本人らの分類に限定し、引用先の原著を取得したとは扱わない。

問14は「魚のホテル」を目標言語に存在しない造語と断定した旧条件の曖昧さを除き、原論文の造語・迂言・近接語の例を使って分類を明示。原論文にない日本語の語彙史や英語表現の独自調査を承認したものではない。問15は直接・間接援助要求、相手への反復要求、自己修正、回避を区別し、聞き返しを一律に明確化要求とした旧解説を訂正。援助要求の頻度から動機・能力を一律判定する未照合主張を撤回。

問16は非言語的手段の分類を問う条件を明示し、ジェスチャーの認知促進効果、母語話者の使用頻度、首振りの文化普遍性に関する未取得実証研究の主張を残さない。問17は意図した語と発話事実を明示した分類用の架空会話に改稿し、原論文の迂言の例に対応させた。表情・間だけから一義的に援助要求や心的状態を判定せず、単発の意思疎通を長期の言語習得効果と同一視しない。

4問40箇所（36フィールドと問17の旧継続4段落の明示削除）改訂。独立正答は2・2・1・2で既存番号を維持。確認済み232・修正必要56・要追加確認212、残件268。累積245問2030箇所。全500問・500解説、正答番号・影響外本文・元v8ハッシュを維持。台帳原文はv8スナップショットで、改訂はchangesと作業稿を参照。

全問機械検査・公開可否回帰8条件に合格。警告57件は前回と同一。documentsのrender_docx.pyで日本語フォント適用QAコピーを{n}頁描画し、変更文字列のある対象{ '・'.join(map(str,reviewed)) }頁を完成PDFから150dpi再描画・直接目視。36変更文字列、全4肢・正誤タグ、日本語表示を確認。全{n}頁の最終目視は未了、最終v9は未制作。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第90バッチ' not in f.read_text();f.write_text(f.read_text()+report)
url='https://b9f19ceb-f720-4252-a2be-ccde56c0821f.filesusr.com/ugd/ba734f_1c905f1db74f488d924e158afdb63986.pdf?index=true'
f=p/'sources.md';f.write_text(f.read_text()+f'''

## 第90バッチ S149の関連4問追加照合（2026-10-15）

[Celce-Murcia・Dörnyei・Thurrell1995原論文]({url})印刷26〜29頁と表5（PDF12〜13頁）をQ_2_014〜017の設問・全4肢・4解説に適用して照合。問14の原論文例、問15の直接・間接援助要求と反復要求・自己修正の区分、問16の非言語的手段の分類、問17の明示した架空会話と迂言の対応を確認。旧稿の造語の不存在断定、能力・動機の一律判定、ジェスチャーの認知促進や使用頻度、文化普遍性の未取得研究を承認せず撤回。架空会話を原論文の実験結果とはしない。URL・ハッシュ・範囲はevidence/batch90_review.jsonにも記録。
''')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第90バッチ\n日本語フォント適用QAコピーを{n}頁描画。対象'+ '・'.join(map(str,reviewed))+f'頁を完成PDFから150dpiで再描画・直接目視。36変更文字列・全4正誤タグを確認。採用画像PIL検査済み。全{n}頁の最終目視は未了。\n')
e={'batch':90,'base_commit':'07c71bc1918d5b2742c92a3ee59a1e9f6d1352d8','fully_rejudged':sorted(targets),'edits':40,'explicit_old_stem_removals':4,'status_counts':m['status_counts'],'remaining':268,'independent_answers':dict(zip(sorted(targets),[2,2,1,2])),'sources':{'S149':{'url':url,'sha256':sha(root/'celce89.pdf'),'pdf_pages':16,'body_and_image_verified_page_map':{'26–27':12,'28–29':13},'limit':'Original authors classification only; not full cited originals or gesture cognition/frequency/cultural universality studies'}},'fictional_scenario':'Q_2_017 original invented classroom example; not an observed study outcome','machine_warnings':57,'new_machine_warnings':[],'readiness_gate':'8 cases passed','render_pages':n,'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP Static Regular400 QA copy only','docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['pagination_followup']='Q_2_015 stem on28/options on29; explanations split226–227. Final keep-together tuning pending; no clipped text or missing tags.'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;f.write_text(f.read_text()+'\n第90バッチ改頁調整候補：問15の設問と選択肢が28〜29頁、解説が226〜227頁に分かれる。欠字・切れはないが最終版の改頁調整は未了。\n')
(p/'evidence/batch90_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded4fullreviews/40edits;232confirmed/268remaining;pages',reviewed)
