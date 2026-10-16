"""One-time primary-source revision of regional coordination and information."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2650
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,sources,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=sources,applied=True,before_version='第120バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=sources,reason=reason,option_verdicts=verdicts,stem_review='設問と全4肢を公表主体による役割・事業目的・改訂プラン抜粋の本文に独立照合。資料内の定義と一般的語義、担当する役割と全業務の独任を区別。',explanation_review='全4解説を照合。学習目標から試験を全面排除せず、情報提供に全世界の言語を要求せず、地域の実情を検討する条件を維持。',unresolved='',multiple_correct_risk='なし：独立正答'+str(key)+'のみ適切',no_correct_risk='なし：独立正答'+str(key))
k='Q_1_019';opts=q[k]['opts'].copy();exps=a['A_1_019']['txt'].copy()
opts[0]='地域日本語教育コーディネーターには、地域の現状や課題、教育資源を把握し、関係者の連携・協働や、生活者としての外国人に適したプログラムの実践に向けた方法の開発を進める役割が示されている。'
opts[1]='国の地域日本語教育の体制づくりへの支援は、地方公共団体と関係機関の連携を排除し、民間語学機関だけが単独で教育を行うことを目的としている。'
opts[2]='研修案内が示す役割は、地域の現状や課題を把握せず、すべての地域で日本語能力試験N1の合格だけを一律の学習目標に設定することである。'
exps[0]='研修案内は、現状把握・課題設定、資源の把握・活用、課題解決の推進、連携、方法の開発を役割として示しています。地域コーディネーターがすべての運営業務を一人で総括すると決めつけず、関係者との協働を捉える説明です。'
exps[2]='研修案内は地域の状況と課題を把握し、生活者としての外国人に適したプログラムの実践に向けて方法を開発するとしています。地域差を無視してN1合格だけを一律に設定する説明とは異なります。試験合格を学習目標に含めること自体を全面的に否定する趣旨ではありません。'
exps[3]='研修案内は、組織内外の調整や人・組織・地域をつなぐ協働を役割に含めています。自ら直接教えることがあっても、それだけで他機関との連携を含まないとする肢は不適切です。国の支援事業でも、総括コーディネーターと地域コーディネーターの設置・配置等が区別して挙げられています。'
review(k,'文部科学省が公開する研修案内に示された地域日本語教育コーディネーターの役割と、地域日本語教育の体制づくりへの国の支援について、最も適切なものを一つ選びなさい。',opts,exps,1,['S186','S187','S06'],'文科省公開の研修案内冒頭の5役割と支援事業の目的・対象取組を本文照合。総括担当と地域担当の混同を避け、架空の指針へのN1一律義務帰属を除去。試験合格を一切目標としないという断定も撤回。既に正しかった2024年4月の所管移管の解説は保持し、新発見と数えない。',['正：現状・課題・資源把握と連携・方法開発を示す','誤：国の支援目的は地方公共団体と関係機関の連携を排除しない','誤：現状把握を否定しN1のみを地域一律とする','誤：組織内外の連携・調整を役割から除外する'])
k='Q_M_004';opts=q[k]['opts'].copy()
opts[0]='受け手や地域の実情にかかわらず、情報提供を日本語の紙媒体のみに限定し、他の言語や電子媒体を用いる方法を検討しないこと'
opts[3]='地域で必要とされる言語を検討せず、特定の一言語に固定し、他の言語での情報提供を一切扱わないこと'
review(k,'総務省の改訂プラン説明資料に示された「行政・生活情報の多言語化、相談体制の整備」に沿う取組として、最も適切なものを一つ選びなさい。',opts,[
'資料は、多言語・やさしい日本語に加え、多様な媒体や伝達経路、SNSの活用を挙げています。地域や受け手の実情にかかわらず、日本語の紙媒体だけに固定して他の方法を検討しない方針とは異なります。',
'資料は、外国人住民が行政・生活情報を入手し、地域生活上の問題を相談できる体制づくりを示しています。情報提供そのものをやめる取組は、この方向と矛盾します。',
'この資料は「多言語」にやさしい日本語を含むと明記し、その枠組みで行政・生活情報の提供を示しています。一般の語義で日本語を複数の言語と数えるという意味ではありません。対応する言語は地域の実情に応じて検討します。',
'資料は地域の実情に応じて対応する言語を検討するとしています。必要性を検討せず一言語に固定する肢は合いません。あらゆる情報を全世界の言語に訳す義務や、特定言語向けの提供が常に誤りだという説明ではありません。'],3,['S188'],'総務省自治行政局国際室の改訂プラン説明資料PDF14頁（印刷13頁）本文・画像を取得照合。同資料が多言語にやさしい日本語を含むと明示しており、元正答3の内容を誤りとせず資料内定義へ範囲限定。全地域一律の実施状況を推測せず、地域の実情に応じる言語・媒体検討を保持。単一言語提供を常に誤りとする解説を条件付きに修正。',['誤：多様な媒体等の検討を実情にかかわらず排除する','誤：入手・相談のための情報提供そのものを廃止する','正：資料は多言語にやさしい日本語を含め情報提供を示す','誤：地域で必要な言語を検討せず一言語へ固定する'])
assert len(extra)==14,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch121.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];meta=[]
for sid,name,url,scope in [('S186','coordinator.html','https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/coordinator_kenshu/','main introduction and all five roles; historical training notice, not current-year admissions or all linked practice studies'),('S187','local_support.html','https://www.mext.go.jp/a_menu/nihongo_kyoiku/mext_02998.html','purpose and funded activities; distinguishes general and regional coordinator; budgets, grant details and deadlines outside approval'),('S188','tabunka.pdf','https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/taikai/r02/pdf/92746701_03.pdf','author on PDF1 and full PDF14/printed13 text+images; multilingual including easy Japanese, regional needs, media, access/counseling; other59 pages not fully approved')]:
 raw=(root/name).read_bytes();meta.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_read_scope=scope,retrieved='2026-10-16',full_source_redistributed=False))
(b.OUT/'evidence/batch121_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('2 questions/14 edits')
