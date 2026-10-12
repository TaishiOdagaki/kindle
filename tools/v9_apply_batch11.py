#!/usr/bin/env python3
"""Replace unspecified rubric level with a verified CEFR scale."""
import html,json
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==240
_,Q,A=qa.audit(str(b.DST));k='Q_4_054';extra=[]
stem='CEFR補遺版（2020年）の「文法的正確さ（Grammatical accuracy）」の尺度におけるB1の記述に最もよく対応するものはどれか。'
opts=['あらゆる場面で文法・語彙の誤りが一切なく、母語話者と同じように話すことが要求される。','どの場面でも意図が全く理解できず、文法的に破綻した発話しか行えない。','身近な場面である程度の正確さで伝達できる。誤りはあるが、何を表現しようとしているかは分かる。','発音・アクセントだけによって水準を決め、文法形式の使用の正確さは評価しない。']
exps=['B1のこの尺度は、あらゆる場面で誤りが一切ないことや、母語話者と同じ発話をすることを要求していません。身近な場面での伝達と、誤りがあっても意図が分かるという条件を確認します。','B1の記述では、誤りがあっても何を表現しようとしているかは明らかだとされています。意図が全く理解できないという説明は一致しません。','この記述は、身近な文脈でのある程度の正確さと、誤りがあっても表現したいことが分かるというB1の説明に対応します。','文法的正確さは文法形式の使用を扱う尺度です。発音・アクセントなどを扱う音韻的な尺度とは区別され、発音だけで文法的正確さの水準を決めるという説明は誤りです。']
for f,old,new in [('stem',[Q[k]['stem']],[stem]),('options',Q[k]['opts'],opts),('explanations',A['A_'+k[2:]]['txt'],exps)]:
 for i,(x,y) in enumerate(zip(old,new)):
  x=html.unescape(x)
  if x!=y:extra.append(dict(id=k,field=f,index=None if f=='stem' else i,before=x,after=y,reason='尺度も段階数もないレベル3は一意に判断できない。CEFR補遺2020の文法的正確さB1へ基準を明示し、最高水準は誤り皆無という旧一般化も撤回。',sources=['S45'],applied=True,before_version='第10修正バッチ作業稿'))
(b.OUT/'changes_batch11.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n');(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text());D[k].update(status='確認済み',fixes_applied=True,independent_answer=3,sources=['S45'],option_verdicts=['B1に誤り皆無/母語話者同等を要求しており不一致','意図が分かるというB1記述と矛盾','B1の該当尺度の記述に一致','文法的正確さと音韻的制御の尺度を混同'],stem_review='CEFR補遺2020の特定尺度・B1を明示して4肢を独立再判定。',explanation_review='原資料印刷頁130・132の尺度の区別と文法的正確さ表を4解説に照合。表のB1行は版面画像でも確認。',multiple_correct_risk='なし：明示された尺度で4肢を判定',no_correct_risk='なし：独立正答3',unresolved='');(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Recorded',len(extra),'repairs.')
