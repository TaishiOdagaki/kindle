"""Checkpoint five independent judgments, preserving unchanged CSV bytes."""
import json,hashlib,subprocess,io,csv,html
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from docx import Document
import quiz_audit as qa
p=Path('audit/v9');root=Path(__file__).resolve().parents[2];r=root/'qa161';targets={'Q_4_120'}
def oldfile(n):return subprocess.check_output(['git','show','HEAD:audit/v9/'+n])
def records(raw):
 s=io.StringIO(raw.decode('utf-8-sig'),newline='');rd=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(rd)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(oldfile('ledger.csv'));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':382,'修正必要':2,'要追加確認':116} and not m['release_ready']
machine=json.loads((p/'postfix_machine.json').read_text());before=json.loads(oldfile('postfix_machine.json'))
removed=[x for x in before['issues'] if x not in machine['issues']];newwarnings=[x for x in machine['issues'] if x not in before['issues']]
assert len(machine['issues'])==113 and not removed and not newwarnings
cs=json.loads((p/'changes_batch161.json').read_text());assert len(cs)==9 and json.loads((p/'changes.json').read_text())==json.loads(oldfile('changes.json'))+cs
d=json.loads((p/'decisions.json').read_text());d0=json.loads(oldfile('decisions.json'));assert {k for k in d if d[k]!=d0[k]}==targets
for v in d.values():
 if v['status']=='確認済み':assert len(v['option_verdicts'])==4 and v['sources'] and not v['unresolved']
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';_,q,a=qa.audit(str(doc));assert len(q)==len(a)==500
assert a['A_4_120']['ans']=='2'
paras=[x.text for x in Document(doc).paragraphs]
for c in cs:
 if c['field']=='case_text':assert paras.count(c['after'])==c.get('count',1);continue
 values=q[c['id']] if c['field']!='explanations' else a['A_'+c['id'][2:]]
 actual=values['stem'] if c['field']=='stem' else values['opts' if c['field']=='options' else 'txt'][c['index']]
 assert html.unescape(actual)==c['after']
matches=json.loads((r/'matches.json').read_text());assert len(matches)==9 and all(matches.values());pages=sorted({n for ns in matches.values() for n in ns})
def png(n):return r/f'review-{n:03}.png'
for n in pages:
 with Image.open(png(n)) as im:im.verify()
 with Image.open(png(n)) as im:im.load()
pagecount=len(PdfReader(r/'qa.pdf',strict=True).pages)
f=p/'README.md';s=f.read_text().replace('381問','382問').replace('117問','116問').replace('376問3218箇所','377問3227箇所').replace('376問を部分修正','377問を部分修正');f.write_text(s)
report='''

## 第161バッチ（2026-10-18）

Q_4_120を公式マニュアル本文へ独立照合し、設問・4肢・4解説の9件を改訂。独立正答2を確定しキー変更なし。確認済み382・修正必要2・要追加確認116、残118問。累積377問3227件の変更記録、500問維持。

S218はPraat開発者の公式マニュアルIntro2.2、4.1、4.2、SoundのHTML原バイトを取得し、Intro3頁の全本文とSoundのInside a Sound・Limitations本文を精読。Web取得本文とも照合。Intro4.1は2011年版、4.2は2023年版で掲載される初期設定値が異なるため、古いページの数値を現行の全解析方式の共通値とせず、出題を波形・ピッチ曲線の区別と解析範囲・表示範囲の制約に限定した。原バイトのSHA256・サイズ・URL・取得日・読了範囲をevidence/batch161_sources.jsonへ記録。Soundのリンク先全頁やPraat全マニュアルを読了したとはしない。

旧解説の「イントネーションの波形」はピッチ曲線と音声波形を混同していたため撤回。波形は時間に対応した振幅の表示、ピッチ曲線は解析されたピッチの時間変化として区別。解析範囲を変えると曲線自体が変わる場合があること、解析範囲を変えない表示の拡大にはView rangeを用いること、話者差に応じた解析設定の確認、選択区間を再生できる機能を全4肢へ照合した。

旧問のMALLの「最大の特長」、録音がメタ認知能力を高めるという効果、視覚提示により発音を客観的に認識・修正できるという効果、ASRと人間の聴感評価の一致や教師不要という広い主張を残さず、同じICT音声指導領域の分析図の読み方と機能・制約を問う問題へ限定して改訂。公式マニュアルを学習効果の実証研究の代わりに承認したものではなく、これら旧主張を実験的に否定したという記録にもしていない。ソフト自体の実行試験も未実施であり、仕様本文の照合と区別する。

旧3218件の履歴は不変のまま9件追記。安全な累積再構成・台帳再生成、v8 SHA256不変、500問・キー・正誤タグ・早見表・リンク、公開判定回帰8条件・置換回帰4条件を検査。機械警告113件で増減なし。台帳原文はv8スナップショット、改訂後はchangesと作業稿を参照する。
'''
pagination=['Q_4_120の設問・肢1–3が98頁、肢4が99頁']
report+=f'\nNoto Sans JPで{pagecount}頁を新規描画し、変更後文字列9件を全件検出。'+ '・'.join(map(str,pages))+'頁のPNGをverify・loadし1800px画像を直接目視。日本語の欠字・重なりなし。ただし'+ '、'.join(pagination)+'を改頁調整の残件に記録。未照合118問、既記録の改頁調整と全頁最終QAは未了。最終v9ではなく出版不可。\n'
for name in ['interim_report.md','critical_findings.md','visual_qa.md']:
 f=p/name;assert '## 第161バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';f.write_text(f.read_text()+'''

## 第161バッチ S218（2026-10-18）

S218 Praat開発者公式マニュアル。以下4頁のHTML原バイトを取得。Intro2.2・4.1・4.2の全本文とSoundのInside a Sound・Limitations本文を精読し、Q_4_120の全4肢・4解説を独立照合した。

- [Intro 2.2 Viewing and editing a sound](https://www.fon.hum.uva.nl/praat/manual/Intro_2_2__Viewing_and_editing_a_sound.html) 波形表示・解析表示・区間再生。
- [Intro 4.1 Viewing a pitch contour](https://www.fon.hum.uva.nl/praat/manual/Intro_4_1__Viewing_a_pitch_contour.html) ピッチ曲線の時間変化と青線・点の表示。
- [Intro 4.2 Configuring the pitch contour](https://www.fon.hum.uva.nl/praat/manual/Intro_4_2__Configuring_the_pitch_contour.html) 話者差、下限設定と時間分解能、解析範囲とView rangeの違い。
- [Sound](https://www.fon.hum.uva.nl/praat/manual/Sound.html) 時間・サンプル・振幅の内部データとメモリ制限。コマンドの全リンク先の読了ではない。

版の異なるページの初期値を混ぜず、数値の固定暗記を出題しない。仕様の本文照合であり、ソフト実行、授業効果・メタ認知効果・ASR性能・発音習得を実証したものではない。evidence/batch161_sources.jsonに原バイトSHA256・サイズ・取得日・読了範囲。原HTML非転載。
''')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
e=dict(batch=161,base_remote_commit='4645f8f36902d29f5f6f49ff2561d3196ccb4dd5',fully_rejudged=sorted(targets),edits=9,independent_answers={'Q_4_120':2},sources=['S218'],status_counts=m['status_counts'],remaining=118,machine_warnings=113,new_warnings=newwarnings,removed_warnings=removed,readiness_gate='8 cases passed; replacement regression 4 conditions passed',render_pages=pagecount,visually_reviewed_pages=pages,all_final_changed_strings_found=matches,docx_sha256=sha(doc),pdf_sha256=sha(r/'qa.pdf'),page_sha256={str(n):sha(png(n)) for n in pages},font_sha256=sha(root/'NotoSansJP-retry.ttf'),full_visual_qa_completed=False,release_ready=False)
e['pending_pagination']=pagination
(p/'evidence/batch161_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('382 confirmed /118 remaining',pages)
