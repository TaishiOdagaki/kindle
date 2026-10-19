"""Record batch182 after fresh render and all affected-page image inspection."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa182';keys={'Q_2_022':3,'Q_2_026':4,'Q_2_027':4,'Q_4_106':3,'Q_O_057':4,'Q_O_058':2,'Q_O_059':2,'Q_O_060':4}
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in keys else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':433,'修正必要':0,'要追加確認':67} and not m['release_ready']
cs=json.loads((p/'changes_batch182.json').read_text());assert len(cs)==72 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches182.json').read_text());assert len(matches)==72 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in pre['issues']];removed=[x for x in pre['issues'] if x not in machine['issues']]
assert len(machine['issues'])==138 and len(added)==4 and all(x[0]=='P1' for x in added) and {x[1] for x in added}=={'Q_2_022','Q_2_026','Q_O_057','Q_O_059'} and len(removed)==1 and removed[0][:2]==['P1','Q_O_058']
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第182バッチ 2026-10-19

Q_2_022・Q_2_026・Q_2_027・Q_4_106・Q_O_057～060の8問、設問・各4肢・各4解説を72件改訂。独立正答3・4・4・3・4・2・2・4、キー変更なし。確認済み433・修正必要0・要追加確認67、残67問。累積426問3687件、500問維持。

S245 Brown・Levinson1987 Politeness: Some Universals in Language Usageの原著からThe Discourse Reader第2版Chapter22へ再録された抜粋を、公開リポジトリの通常直接ダウンロードで取得。1374070バイト、スキャン14頁。Web openは403だったが同一URLへの通常直接取得は成功、認証・保護回避なし。原PDFに抽出可能な文字がないためOCRを補助に使い、著者本文のPDF1～12（再録掲載311～322頁冒頭）を全頁画像で精読。PDF12～13のEditors appendixと著者本文を区別し、PDF14の標題でThe Discourse Reader第二版、編者Adam Jaworski・Nikolas Coupland、Routledgeを確認した。原著全巻、原著1987版の元の頁番号、後続の批判文献、別章Linguistic Politenessの取得とはしない。編集者付録のGrice格率分類等を原著の主張として承認しない。初回画像／OCRが失敗した4・8・12頁は別描画で確認。

311～312頁のフェイス二側面、313～315頁のFTA分類と重複・話者側の脅威、316頁図22.1と直接性の条件、317頁の二方策と慣習化した間接性、318～321頁の三要因・当事者の認識・文化状況個人の評価差を照合。オフレコードをネガティブ・ポライトネス寄りと混同する旧解説を撤回し、図の別枝とオンレコードの関係を明記。言いさしという形式だけでオフレコードと断定せず、意図が一つに確定できないという条件で出題する。相手を褒めれば必ず成功するとの含みも撤回。原著314頁は称賛が負担となる面も挙げるため、ポジティブの設問は仲間として扱い欲求共有を示すという定義へ限定した。

直接依頼を形式だけで常に低配慮・不適切とする説明を撤回し、緊急性・効率性・相手の利益・関係の検討を明記。文化だけを誤解の原因とし国籍から受け取り方を確定する説明を撤回。Q_4_106は距離・力・負担の三要因と評価差を問う。ケース12全文も照合し、Q_O_057は負担配慮の意図を設問で指定、実際の負担軽減や発話者の内心を観察済みとはしない。Q_O_059・060は理論を比較検討に応用する案で、指導効果の実証や全日本語場面での普遍的妥当性の承認とは区別した。個別批判原典を取得していないことを、批判を検証済みという記述で隠さない。

v8不変、500問、全正答番号・正誤タグ・早見表・リンク・改訂外問題不変を検査。公開判定回帰8条件・置換回帰4条件・block-context回帰通過。機械警告135→138件（P1追加4、解消1）。追加はQ_2_022の否定的感情の意味ではない、Q_2_026の常に一方だけではない、Q_O_057の実際の負担軽減確認ではない、Q_O_059の学習効果実証ではない、という限定文末による誤検出。全肢・全解説・タグの対応を原著と再確認。Q_O_058の旧P1は改訂により消滅。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPの既知SHA256一致と同梱Noto Serifの文字収録を検査して{pagecount}頁を新規描画。72改訂文字列を全件検出し、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に日本語欠字・重なり・切れを認めず。全頁最終QA・改頁調整・残67問は未完了。作業稿は出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第182バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第182バッチ S245 2026-10-19

[Brown・Levinson1987原著の再録抜粋公開PDF](https://pure.mpg.de/rest/items/item_64421/component/file_2225570/content)。The Discourse Reader第2版Chapter22、再録本文311～322頁冒頭、編集者付録322～323頁、標題頁を含む14頁スキャン。全頁画像・OCR補助で精読。8問の全肢全解説を著者本文のフェイス定義、FTA、図22.1、直接性の条件、慣習化した間接性、三要因と評価差へ対応。ケース12は分析の適用であり内心・反応・教育効果の実証でない。編集者付録と原著本文を区別し、付録のGrice分類等は今回の承認根拠に使わない。原著全巻や後続批判原典は未取得。原資料サイズ・SHA256・範囲はevidence/batch182_sources.json。Web open403と通常直接取得成功の区別、別章の403はbatch182_source_attempts.json。原PDF・OCR全文は非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('425問','433問').replace('75問','67問').replace('418問3615箇所','426問3687箇所').replace('418問を部分修正','426問を部分修正').replace('第181バッチの最新描画は354頁',f'第182バッチの最新描画は{pagecount}頁'))
e=dict(batch=182,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=72,independent_answers=keys,sources=['S245'],status_counts=m['status_counts'],remaining=67,machine_warnings=138,added_warnings=added,removed_warnings=removed,regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
retry_files={136:'retry-136.png',257:'ppm-257.png',319:'jpeg-319.jpg'}
e['image_retry']={'reason':'PNG表示失敗又は部分欠落を認めたため再描画。319頁はPNGでは部分欠落が残り、JPEGで全文表示を直接確認。文書の欠字とは区別した。','actual_review_files':retry_files}
for n,name in retry_files.items():e['page_sha256'][str(n)]=sha(r/name)
for n in ['visual_qa.md','interim_report.md']:
 f=p/n;f.write_text(f.read_text()+'\n第182バッチ画像再確認: 136頁はpdftocairo PNG、257頁はpdftoppm PNG、319頁はpdftoppm JPEGを実際に閲覧。PNG表示の部分欠落を文書の欠字として扱わず、全字表示を確認した代替画像のSHA256を記録。\n')
(p/'evidence/batch182_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
