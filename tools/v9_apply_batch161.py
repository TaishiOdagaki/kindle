"""Independent source-limited Praat item audit; no learning-effect approval."""
import json,html,hashlib
from pathlib import Path
from lxml import html as lh
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3218
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_120';ak='A_4_120'
assert d[k]['status']=='要追加確認' and a[ak]['ans']=='2'
reason='S218 Praat開発者の公式マニュアルIntro2.2・4.1・4.2の全本文とSoundのInside a Sound・Limitations本文を取得して精読。波形の振幅の時系列と、解析で求めるピッチ曲線を区別し、解析範囲と表示範囲、話者差、選択区間再生を全4肢へ照合。旧問のMALLの最大の利点、録音のメタ認知効果、視覚提示で発音を修正できるという効果、ASRと聴感評価の一致や教師不要という広範な主張を撤回し、同じICT音声指導領域で公式仕様に限定した分析の読み方へ改訂。これらの旧主張の実験的な否定・肯定や、特定の授業効果を検証したものではない。'
stem='発音指導の資料として学習者の録音をPraatで調べる。公式マニュアルの波形・ピッチ曲線と解析設定の説明に合うものを一つ選べ。'
opts=['波形は推定された基本周波数そのものの時間変化なので、波形を表示すればピッチ解析を別に行う必要はない。',
'波形とピッチ曲線は別の表示であり、ピッチ解析では話者の声の高さの範囲に合う設定かを確かめる。',
'ピッチの解析範囲を変更しても計算される曲線は変わらないため、表示範囲だけを変える操作と常に同じである。',
'波形やピッチ曲線を表示すると録音の選択区間は再生できなくなるため、音を聞きながら該当区間を確かめることはできない。']
exps=['Soundの内部データは時間に対応したサンプルと振幅を含み、Intro2.2は波形とその下の解析表示を区別しています。Intro4.1のピッチ曲線は時間に沿ったピッチの表示であり、波形を表示しただけで同じ値を得たことにはなりません。',
'Intro2.2と4.1は波形とピッチ曲線を別に説明しています。4.2は、話者により声の高さの範囲が大きく異なること、下限などの設定が解析や時間分解能に関わることを示します。図の一致だけで発音の正誤や習得を確定する説明ではなく、分析条件を確かめる必要があります。',
'Intro4.2は、ピッチ範囲を変えると解析範囲も変わり、曲線自体が変わる場合があると説明しています。解析範囲を変えず表示だけを拡大するにはView rangeを用いるため、二つの操作は常に同じではありません。',
'Intro2.2は、SoundEditorで波形や解析を表示し、区間を選択して再生する操作を説明しています。表示すると選択区間を再生できなくなるという肢は、この機能に反します。再生して聞けることと、発音学習の効果を実証したことは別です。']
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S218'],applied=True,before_version='第160バッチ反映後',block_context=ak if field=='explanations' else k)
  assert c['before']!=new
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S218'],reason=reason,option_verdicts=['誤：振幅の時系列とピッチ解析を同一視','正：別表示と話者差に応じた解析範囲の確認に一致','誤：解析範囲とView rangeを同一視し曲線不変と断定','誤：選択区間再生ができるというIntro2.2の操作に反する'],candidate_answers=[],stem_review='設問と全4肢を公式マニュアル本文の機能・解析制約へ独立照合。製品仕様を学習効果へ拡張しない。',explanation_review='全4解説をIntro2.2・4.1・4.2、Sound内部データ本文へ照合。ピッチと波形の混同を撤回し、旧MALL・メタ認知・ASR等の未照合の補助的主張を残さない。',unresolved='',multiple_correct_risk='なし：指定仕様に合うのは2のみ',no_correct_risk='なし：独立正答2')
for name,obj in [('changes.json',cs+extra),('changes_batch161.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2]
pages=[('view','Intro_2_2__Viewing_and_editing_a_sound.html','Intro 2.2. Viewing and editing a sound','20230202'),('pitch','Intro_4_1__Viewing_a_pitch_contour.html','Intro 4.1. Viewing a pitch contour','20110128'),('config','Intro_4_2__Configuring_the_pitch_contour.html','Intro 4.2. Configuring the pitch contour','20231115'),('sound','Sound.html','Sound','2016-10-13')]
e=[]
for local,path,title,version in pages:
 p=root/f'praat161-{local}.html';raw=p.read_bytes();t=lh.fromstring(raw).text_content();assert title in t
 e.append(dict(source_id='S218',url='https://www.fon.hum.uva.nl/praat/manual/'+path,title=title,retrieved='2026-10-18',manual_page_revision=version,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope='Intro2.2・4.1・4.2は全本文。Soundは内部データと制限の本文（コマンドのリンク先全頁は未読）。Web本文とも照合。',limitations='開発者公式の機能・解析制約を確認。ソフト実行試験や授業介入、メタ認知効果、ASR性能、発音習得の実証研究ではない。原HTML非転載。',full_source_redistributed=False))
(b.OUT/'evidence/batch161_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Q_4_120 /9edits /key2')
