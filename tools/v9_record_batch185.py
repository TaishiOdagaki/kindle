"""Record batch185 once, after direct review of all matched page images."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa185'
BASE='26cc964671d749a73bfdafa06b58ba2d882b4466'
keys={'Q_4_018':3,'Q_M_023':2,'Q_M_022':1}
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':442,'修正必要':0,'要追加確認':58} and not m['release_ready']
cs=json.loads((p/'changes_batch185.json').read_text());assert len(cs)==27 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches185.json').read_text());assert len(matches)==27 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));added=[x for x in machine['issues'] if x not in pre['issues']];removed=[x for x in pre['issues'] if x not in machine['issues']]
assert len(machine['issues'])==140 and len(added)==1 and added[0][:2]==['P1','Q_M_023'] and not removed
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
specs=[
 ('S250','Yale Poorvu Center Classroom Seating Arrangements','https://poorvucenter.yale.edu/teaching/teaching-resource-library/classroom-seating-arrangements','yale185.html','271712843c59126764f27a9ede457a08463677fe7457e00c3d029ce38d31c6e0','本文の各配置、活動と目標への整合、固定席での隣同士の活動。参照研究の原著未取得で因果効果・語学授業効果を実証したとの承認ではない。仮想教室の節も読んだがZoom現行仕様の根拠にしない。'),
 ('S251','ASQ Plan Do Check Act Cycle','https://asq.org/quality-resources/pdca-cycle','asq185.html','edddb4313595615ccc7a7eeffef5615fb556024616b07e01513455191d433a40','本文の4段階と継続的反復、Checkの分析と学び、Actの学びの活用を照合。Pearl River事例は読んだが全教育プログラムへの効果保証にしない。The Quality Toolbox原著全文未取得。'),
 ('S252','The W Edwards Deming Institute PDSA Cycle','https://deming.org/explore/pdsa/','deming185.html','c06956c4bf62724a2bd57fda4de941a0439eb0f4f4ac50dbae061669f00f6bac','本文のPlan Do Study ActとPDSA and PDCA節。StudyをCheckと同一展開語にせず、ASQのCheckにも分析と学びがある説明を保持。Deming本人の原著全文やリンク先論文は今回未取得で起源史を承認しない。')]
sources=[]
for sid,title,url,name,expected,scope in specs:
 f=root/name;assert sha(f)==expected
 sources.append(dict(source_id=sid,title=title,url=url,checked='2026-10-19',bytes=f.stat().st_size,sha256=sha(f),body_read=scope,full_source_redistributed=False))
(p/'evidence/batch185_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
text=f'''

## 第185バッチ 2026-10-19

Q_4_018・Q_M_023・Q_M_022の設問・各4選択肢・各4解説を27件改訂。独立正答3・2・1、キー変更なし。確認済み442・修正必要0・要追加確認58、残58問。累積435問3768件、全500問を維持。

S250 Yale Poorvu Center公式ガイド本文を取得精読。Q_4_018は配置が必ず心理効果を生むとの一般化を外し、列型・円卓型・グループ／ペア型・U字型の用途を指定ガイドに照らして問う形へ改訂。円形配置で緊張が和らぎラポール形成が進むとの旧解説、島型が前方への集中を削ぐとの未取得の実証的主張を今回承認しない。Q_M_023は前方に教材を投影して全体で議論するという活動を指定し、U字型・半円型を検討する判断へ限定。固定席であっても隣同士のThink-Pair-Share等は可能という推奨を反映。特定機器の効果・現行仕様や全授業の効果を保証しない。ガイド引用の各研究原著は未取得で、原著全文を照合済みとはしない。

S251 ASQのPDCA手順本文とS252 Deming InstituteのPDSA説明本文を取得精読。Q_M_022は名称だけから4段階と反復の判断へ改訂。ASQのCheckにも試行結果の検討・分析と学びがあることを保持し、Actでは結果に応じた別計画や広い変更へ学びを生かす点を照合。PDSAのSはStudyと区別する。PDCAは学びを含まないという一律の二分法を作らない。Deming本人の原著全文、発祥史、ASQが挙げた原著全文は未取得であり承認しない。旧誤答のCLIL・PPP・TBLTを今回の資料だけで承認せず、同じ改善サイクル領域内の判断へ差替え。

全500問の構造・正答タグ・早見表・リンクと改訂外不変を安全再構成で検査。v8 SHA256不変。公開判定8条件、置換4条件、block-context回帰通過。機械警告139→140件、新規P1はQ_M_023正答解説の「特定機器の導入効果を保証する判断ではありません」という限定の誤検出。全肢・タグ・解説と本文を再照合し、キー不整合ではないと確認。台帳の原文はv8スナップショット、改訂後はchangesと作業稿を参照する。

完全版Noto Sans CJK JPの既知SHA256一致、全CJK収録と非CJK代替フォント収録を描画前に検査。{pagecount}頁を新規描画し、全27改訂文字列を検出。影響{pages}頁の1800px画像を直接確認し、改訂箇所に欠字・重なり・切れなし。設問・選択肢・解説の頁またぎを含む最終改頁調整と全頁最終QAは未完了。作業稿は最終版ではなく出版不可。
'''
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第185バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'\n\n## 第185バッチ S250 S251 S252 2026-10-19\n\n'+'\n\n'.join(f'{s[0]} [{s[1]}]({s[2]})。{s[5]}' for s in specs)+'\n\n各公式ページ本文を取得・精読し、Q_4_018・Q_M_023とQ_M_022の全肢全解説へ照合。検索抜粋だけの承認ではない。原資料全体非転載。サイズ・SHA256・範囲はevidence/batch185_sources.json。\n')
f=p/'README.md';f.write_text(f.read_text().replace('439問','442問').replace('61問','58問').replace('432問3741箇所','435問3768箇所').replace('432問を部分修正','435問を部分修正').replace('第184バッチの最新描画は355頁',f'第185バッチの最新描画は{pagecount}頁'))
e=dict(batch=185,base_remote_commit=BASE,fully_rejudged=list(keys),edits=27,independent_answers=keys,sources=['S250','S251','S252'],status_counts=m['status_counts'],remaining=58,machine_warnings=140,added_warnings=added,removed_warnings=removed,regressions='readiness8; replacement4; block-context',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch185_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
