"""One-time clarification of Presentation versus Production before save."""
import json
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1704
old='同書8頁のProductionは、提示・練習した新形式を異なる文脈で使う段階です。無関係な未習形式の初提示という説明はPresentationともProductionとも対応しません。'
new='同書8頁のProductionは、提示・練習した新形式を異なる文脈で使う段階です。新形式の初提示はPresentationの説明であり、Productionとする記述は対応しません。'
e=dict(id='Q_4_064',field='explanations',index=3,before=old,after=new,reason='新形式の初提示はPresentationの説明であることを明示し、Productionとの段階区別を曖昧にしない。',sources=['S144'],applied=True,before_version='第79バッチ46箇所反映後の累積作業稿',block_context='A_4_064',paragraph_prefix='4（誤）')
for name,obj in [('changes.json',c+[e]),('changes_batch79c.json',[e])]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
