"""Save reconstructed batch186 after direct changed-page review."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa186'
BASE='bdff7d52fb2a6de503b9fcc62e81929caac83b0e';keys={'Q_2_028':2,'Q_2_029':4,'Q_4_105':2,'Q_M_011':1}
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
def old(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rows(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
new=dict(rows((p/'ledger.csv').read_bytes()));(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in keys else raw for k,raw in rows(old('ledger.csv'))).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':446,'修正必要':0,'要追加確認':54} and not m['release_ready']
cs=json.loads((p/'changes_batch186.json').read_text());assert len(cs)==36 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches186.json').read_text());assert len(matches)==36 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());assert machine['issues']==json.loads(old('postfix_machine.json'))['issues'] and len(machine['issues'])==140
specs=[('S253','Edward T Hall Beyond Culture 原著スキャン','https://monoskop.org/images/6/60/Hall_Edward_T_Beyond_Culture.pdf','hall186-retry.pdf','8f4ee47a460e40231f067a474a531afc5a6e0213637ceb1e0fd56f72d7268a9a',316,'初版1976、取得版は著作権1976・1981、Anchor Books editions 1977・1989と記載。標題・著作権頁PDF7～8、本文90～93頁PDF106～109を画像精読。原著全316頁精読ではない。高低の定義・連続体・前提の共有と情報の過不足を照合。他の文字史・芸術・政治や現在の各国の全成員の性質を承認していない。'),('S254','Sacks Schegloff Jefferson 1974 A Simplest Systematics for the Organization of Turn Taking for Conversation 原論文','https://www.conversationanalysis.org/wp-content/uploads/2019/06/04_Sacks_Schegloff_Jefferson_A_simplest_systematics_fir_the_organization_of_turn-taking_for_conversation_Language_.pdf','sacks186-isca.pdf','589f90cd2bf83dc37ae8b609d42954b2b891c8df950ec0c5f32bbe69ab7641ab',40,'Language50(4)696～735頁。取得40頁、696・702～704頁（PDF1・7～9）の本文・脚注・会話例を画像精読しOCR補助。順番構成・配分と規則1a～c・2の条件を確認。全論文精読や全言語・全場面の普遍則の承認ではない。')]
sources=[]
for sid,title,url,name,expected,total,scope in specs:
 f=root/name;assert sha(f)==expected and len(PdfReader(f).pages)==total
 sources.append(dict(source_id=sid,title=title,url=url,retrieved_again='2026-10-20',body_review='2026-10-19の画像精読と一致する原バイトを再取得、ハッシュ検証',bytes=f.stat().st_size,sha256=sha(f),pages=total,body_read=scope,full_source_redistributed=False))
(p/'evidence/batch186_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch186_source_attempts.json').write_text(json.dumps([dict(result='前回の未保存作業を最新GitHub HEADから再構成。初回Hall再取得ファイル30728192バイトは構造不正・既知ハッシュ不一致で不採用。別名への通常再取得で30783366バイト・316頁・既知ハッシュ一致を確認。破損ファイルは本文判定・画像QAに使用しない。'),dict(result='前回Hall Web openはrestricted URLで失敗、通常直接取得で成功。学内名義の要約PDF、検索抜粋、無関係なHall検索結果は承認根拠に不採用。SacksのColumbia41頁版も取得したが本バッチはISCA40頁版を使用。原資料全体とOCR全文は非転載。')],ensure_ascii=False,indent=2)+'\n')
pagecount=len(PdfReader(r/'qa.pdf').pages)
text=f'''

## 第186バッチ 2026-10-20保存

Q_2_028・Q_2_029・Q_4_105・Q_M_011の設問・全4肢・全4解説を36件改訂。10月19日の未保存判断を最新HEADから再構成し、原典の同一ハッシュを再取得検証。独立正答2・4・2・1、キー変更なし。確認済み446・修正必要0・要追加確認54。累積439問3804件、500問維持。

S253 Hall原著Beyond Cultureスキャン316頁を取得。初版1976、取得版の著作権1976・1981、Anchor版1977・1989の記載を確認。原著90～93頁（PDF106～109）・標題・著作権頁を画像精読。Q_2_028は高低の情報配分、Q_4_105は連続体と「片方の極だけに存在する文化はない」という留保を反映。旧稿の未照合の国別・言語別一覧、出身文化から個人の内心を推測する一般化を撤回。Q_2_029は前提未共有の場合の相手の既有知識と明示情報の過不足を検討する問題へ改訂。原著90・92～93頁の場面への適用であり指導効果の実証ではない。全巻精読、原著の文字史・芸術・政治、現在の全国民の性質を承認したものではない。

S254 Sacks・Schegloff・Jefferson1974原論文40頁を取得。696・702～704頁（PDF1・7～9）を本文・脚注・会話例の画像で精読、OCR補助。Q_M_011は名称だけから、次話者選定・自己選択・現在話者継続の条件を問う判断へ改訂。旧誤答の臨界期・言語シフト・コード切替の各原典未取得で承認せず、同じ話者交替領域へ差替え。会話モデルを全言語・全制度的場面の普遍則に拡大しない。全論文精読ではない。

全500問構造・タグ・早見表・リンク・改訂外不変、v8 SHA256不変を安全再構成で確認。公開判定8条件、置換4条件、block-context回帰通過。機械警告140件、増減なし。台帳の原文はv8スナップショットで、改訂後はchangesと作業稿を参照。

完全版Noto Sans CJK JPの既知ハッシュと全文CJK・非CJK代替フォント収録を検査。{pagecount}頁を新規描画し、36改訂文字列を全件検出。影響{pages}頁の1800px画像を直接確認。改訂箇所の欠字・重なり・切れなし。最終改頁調整・全頁最終画像QAと残54問は未完了。作業稿は出版不可。
'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第186バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第186バッチ S253 S254 2026-10-20保存\n\n'+'\n\n'.join(f'{s[0]} [{s[1]}]({s[2]})。{s[6]}' for s in specs)+'\n\n原PDF・OCR全文非転載。取得ハッシュと精読範囲はevidence/batch186_sources.json、再構成・破損ファイル不採用はbatch186_source_attempts.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('442問','446問').replace('58問','54問').replace('435問3768箇所','439問3804箇所').replace('435問を部分修正','439問を部分修正').replace('第185バッチの最新描画は355頁',f'第186バッチの最新描画は{pagecount}頁'))
e=dict(batch=186,base_remote_commit=BASE,fully_rejudged=list(keys),edits=36,independent_answers=keys,sources=['S253','S254'],status_counts=m['status_counts'],remaining=54,machine_warnings=140,added_warnings=[],removed_warnings=[],regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/('retry-328.jpg' if n==328 else f'review-{n:03}.png')) for n in pages},image_retry='328頁PNG読込失敗後、同一PDFから1800px JPEGを再生成し直接目視確認',full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch186_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
