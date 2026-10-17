"""One-time historical quality-assurance audit from MEXT's full historical account."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2847
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_1_027';ak='A_1_027'
assert d[k]['status']=='修正必要' and a[ak]['ans']=='2'
stem='1980年代末から1990年にかけての、日本語教育施設の質的向上に関する制度整備の経緯として、適切なものを一つ選べ。'
opts=['日本語教育施設の運営に関する基準が1988年12月にまとまる前から、日本語教育振興協会は財団法人として設立されていた。','1989年5月、日本語教育振興協会が任意団体として発足し、日本語教育施設の審査・認定事業を開始した。','1988年12月にまとまった基準は授業料の額だけを対象とし、修業期間や教員の資格要件は対象としなかった。','日本語教育振興協会は、1989年5月の発足時から、文部省・法務省・外務省の三省共管の財団法人だった。']
exps=['運営基準の取りまとめは1988年12月、協会の任意団体としての発足は1989年5月です。財団法人の許可は1990年2月であり、順序が逆です。','文部省の学制百二十年史は、1989年5月の任意団体としての発足と、審査・認定事業の開始を記しています。','基準は修業期間、教員数、教員の資格要件、施設・設備などを扱っています。授業料の額だけを対象にしたという説明は誤りです。','1989年5月は任意団体としての発足です。文部省・法務省による財団法人の許可は1990年2月、外務省を加えた三省共管は同年11月です。']
reason='文科省公開の学制百二十年史「日本語教育施設の質的向上」の本文全2段落を取得・精読。1988年12月の基準、1989年5月の任意団体発足・審査認定開始、1990年2月の財団法人許可と11月の三省共管を照合。質保証史という学習領域を維持し、原問の留学生10万人計画の対象範囲や教師需要の爆発的増加等の未照合主張を撤回して、取得本文で確定できる制度整備の経緯へ改訂。歴史上の審査・認定を現在の日本語教育機関認定制度や法的な認可と同一視しない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S198'],applied=True,before_version='第135バッチ反映後',block_context=ak if field=='explanations' else k)
  if field=='options':c['stem_context']=stem
  if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==1 else '誤')+'）'
  extra.append(c)
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=2,fixes_applied=True,sources=['S198'],reason=reason,option_verdicts=['誤：財団法人許可は基準取りまとめより後','正：1989年5月の任意発足と審査認定開始','誤：修業期間や教員資格・設備も基準の対象','誤：財団法人許可と三省共管はいずれも1990年'],stem_review='1988–1990年の制度整備史に範囲を限定。任意発足、財団法人許可、三省共管の段階を区別し全4肢を独立照合。',explanation_review='全4解説を史料本文全2段落へ照合。未取得の留学生政策の対象範囲や需要の因果・増加幅は承認しない。',unresolved='',multiple_correct_risk='なし：独立正答2のみ史料に合う',no_correct_risk='なし：独立正答2')
for name,obj in [('changes.json',cs+extra),('changes_batch136.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(Path(__file__).resolve().parents[2]/'mext-history.html').read_bytes();assert '日本語教育施設'.encode() in raw
(b.OUT/'evidence/batch136_sources.json').write_text(json.dumps(dict(source_id='S198',url='https://www.mext.go.jp/b_menu/hakusho/html/others/detail/1318583.htm',title='学制百二十年史 三 日本語教育施設の質的向上',retrieved='2026-10-17',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),read_scope='Complete two-paragraph historical account; no current accreditation-law approval.',full_source_redistributed=False),ensure_ascii=False,indent=2)+'\n')
print('1 question / 9 edits')
