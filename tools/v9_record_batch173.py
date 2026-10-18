"""Persist independently checked theory boundaries and current visual QA."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from pypdf import PdfReader
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa173';keys={'Q_3_033':1,'Q_3_035':3}
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
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':405,'修正必要':2,'要追加確認':93} and not m['release_ready']
cs=json.loads((p/'changes_batch173.json').read_text());assert len(cs)==18 and json.loads((p/'changes.json').read_text())==json.loads(old('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(old('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==set(keys)
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
for k,v in keys.items():assert a['A_'+k[2:]]['ans']==str(v)
for c in cs:
 k=c['id'];got=q[k]['stem'] if c['field']=='stem' else (q[k]['opts'] if c['field']=='options' else a['A_'+k[2:]]['txt'])[c['index']]
 assert html.unescape(got)==c['after']
matches=json.loads((r/'matches173.json').read_text());assert len(matches)==18 and all(matches.values());pages=sorted({v for ns in matches.values() for v in ns})
machine=json.loads((p/'postfix_machine.json').read_text());pre=json.loads(old('postfix_machine.json'));warnings=[x for x in machine['issues'] if x not in pre['issues']]
assert len(machine['issues'])==125 and len(warnings)==1 and warnings[0][1]=='Q_3_033' and all(x in machine['issues'] for x in pre['issues'])
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pagecount=len(PdfReader(r/'qa.pdf').pages)
text='''

## 第173バッチ 2026-10-19

Q_3_033・035の設問・各4肢・各4解説を18件改訂、独立正答1・3、キー変更なし。確認済み405・修正必要2・要追加確認93、残95問。累積400問3435件、500問維持。

S233 Berry1997原論文の大学教材サイト公開スキャン30頁を取得。印刷5～7・9～12・24～25頁本文、10頁図1と本文画像を確認。保持／接触・参加の分類と、集団や個人の自由な選択が社会から制約される条件を照合。「統合が最も健康的」という全状況への保証を撤回し、支配的社会側の開放性と双方の調整を解説に加えた。著者の研究総括に統合と良好な適応の関連はあるが、全個人の健康保証や統合選択だけの因果効果とはしない。周縁化を本人が自由に好む孤立とだけ扱わず、分離と強制的隔離を区別した。引用研究各原著は未取得。

S234 Bennett2017の著者本文8頁を提唱者の所属研究所から取得、PDF1～7頁本文と4～5頁画像を確認。6段階は連続体上の位置であり、進行は必然ではない。受容は相手の全価値観への同意ではなく、防衛には他文化優位に逆転する型もある。統合は異なる文化的世界観へ出入りする動きを自己に含める説明であり、自己喪失や単一文脈への固定ではない。Berryの文化変容方略の統合と同義にしない。提唱者自身の2017年説明の照合であり、1986原著、尺度全項目、批判・実証研究の全原著を確認したとはしていない。

v8原本不変、全500問、キー・正誤タグ・早見表・リンク、影響外の問題不変を再検査。公開判定回帰8条件・置換回帰4条件通過。機械警告124→125件。新規P1は、統合の条件を限定した正答解説の否定語尾と、誤肢解説が分類上の正しい名称を示すことによる誤検出。既存124件は保持。台帳原文はv8スナップショット、改訂本文はchangesと作業稿を参照。
'''
text+=f'\n完全版Noto Sans CJK JPと同梱Noto Serifを検査し{pagecount}頁を新規描画。18文字列全件を検出、'+ '・'.join(map(str,pages))+'頁の1800px画像を直接確認。改訂箇所に欠字・重なり・切れを認めず。複数頁にまたがる問題・解説は最終組版で調整する。全頁最終QAと残95問は未完了。最終版ではなく出版不可。\n'
for n in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/n;assert '## 第173バッチ' not in f.read_text();f.write_text(f.read_text()+text)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第173バッチ S233 S234 2026-10-19

- S233 [Berry1997 Immigration Acculturation and Adaptation 原論文](https://peda.net/jyu/ktk/educationalleadership/moemalm/efitic/s1itiaic/lectures/l1ita/l1ita/berry-pdf%3Afile/download/87dd958cb50d15350cc101aff1e0fb29ee3f7cdd/Berry.pdf)。Applied Psychology46(1)原論文の第三者公開スキャン30頁。印刷5～7・9～12・24～25頁本文、10頁図1・本文画像。2軸の4方略、自由選択と社会的制約、相互調整、適応の関連を総括する著者の留保。引用実証研究の各原著は未取得。
- S234 [Bennett2017 DMIS 著者本文](https://www.idrinstitute.org/wp-content/uploads/2019/02/DMIS-IDRI.pdf)。著者研究所が2017年百科事典項目として公開する8頁PDF。1～7頁本文、4～5頁画像。連続体上の6位置、非必然的進行、受容と同意の区別、防衛の逆転型、統合の自己のあり方、測定・批判の記述。1986原著・IDI全項目・全引用先の確認ではない。

Q_3_033・035の全肢全解説に対応。原バイトSHA256と精読範囲はevidence/batch173_sources.json。原資料全体非転載。
''')
f=p/'README.md';f.write_text(f.read_text().replace('403問','405問').replace('95問','93問').replace('398問3417箇所','400問3435箇所').replace('398問を部分修正','400問を部分修正').replace('第172バッチの最新描画は353頁',f'第173バッチの最新描画は{pagecount}頁'))
e=dict(batch=173,base_remote_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),fully_rejudged=list(keys),edits=18,independent_answers=keys,sources=['S233','S234'],status_counts=m['status_counts'],remaining=95,machine_warnings=125,new_warnings=warnings,regressions='readiness8; replacement4',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),font_sha256=sha(root/'NotoSansCJKjp-VF.ttf'),page_sha256={str(n):sha(r/f'review-{n:03}.png') for n in pages},full_visual_qa_completed=False,release_ready=False)
(p/'evidence/batch173_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
