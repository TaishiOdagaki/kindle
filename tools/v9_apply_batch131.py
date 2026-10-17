"""One-time business Japanese audit; all four alternatives independently checked."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2815
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_M_036';ak='A_M_036'
assert d[k]['status']=='修正必要' and a[ak]['ans']=='4'
stem='外国人社員が職場の相手や場面に応じて日本語でやり取りする力を育てるコースで、目標に合う学習内容を一つ選べ。'
opts=['文学作品の読解と文学史の知識の確認に限定し、職場でのやり取りは扱わない。','旅行先での観光客としての会話に限定し、職場の相手とのやり取りは扱わない。','あいさつ表現を暗記するだけにとどめ、職場での相手や場面に応じた使い分けは扱わない。','職場の相手や場面を踏まえ、あいさつや商品の紹介などで使う表現を選ぶ練習をする。']
exps=['文学や文学史を学ぶこと自体を否定するものではありません。ただし、それだけに限定して職場でのやり取りを除く内容は、設問の目標に合いません。','旅行会話にも学習価値はありますが、観光客としての会話だけに限定し、職場の相手とのやり取りを除く内容は、設問の目標に合いません。','あいさつもビジネス日本語の学習対象です。ここで不適切なのは、暗記だけに限定し、職場での相手や場面に応じた使い分けを扱わない点です。','BJTの公開例では取引先へのあいさつや商品の紹介を扱い、相手と場面を踏まえた表現の選択が求められます。これを練習に取り入れる内容は、設問の目標に合います。']
reason='BJT実施団体の特徴説明および聴解サンプルの発言聴解セクション2の設問・解説本文を取得・照合。あいさつを初級生活場面に限ってビジネス日本語から排除した説明を撤回。職場の相手・場面に応じたやり取りという目標を明示し、文学・旅行・暗記そのものの価値を否定せず、目標に必要な練習を除くという限定で誤答を確定。試験が産出技能を直接測る、練習で必ず上達する、全職種に同一内容が必須、という主張はしない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S194'],applied=True,before_version='第130バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S194'],reason=reason,option_verdicts=['誤：職場のやり取りを除外','誤：観光客の会話に限定し職場のやり取りを除外','誤：あいさつ自体ではなく相手・場面の使い分けの除外が不適切','正：相手・場面に応じた業務上の表現選択'],stem_review='コースの目標を条件として明示し全4肢を独立判定。全ビジネス日本語コースの普遍的必須事項とはしない。',explanation_review='全4解説を目標との適合性と実施団体本文に照合。あいさつの排除を撤回。',unresolved='',multiple_correct_risk='なし：明示目標に合う4のみ',no_correct_risk='なし：独立正答4')
for name,obj in [('changes.json',cs+extra),('changes_batch131.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];e=[]
for filename,url in [('bjt-features.html','https://www.kanken.or.jp/bjt/about/feature_merit.html'),('bjt-sample.html','https://www.kanken.or.jp/bjt/sample/sample01.html')]:
 raw=(root/filename).read_bytes();raw.decode('utf-8');e.append(dict(source_id='S194',url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-17',scope='Features introductory business communication definition; sample section 2 written prompts and complete published explanations. Embedded audio/images not reviewed; no immigration, employment effects, or direct productive-skill measurement approval.',full_source_redistributed=False))
(b.OUT/'evidence/batch131_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
