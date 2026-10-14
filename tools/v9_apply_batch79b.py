"""One-time wording correction after batch79 visual review."""
import json
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1703
old='同書16頁の区別は、意味理解を必ずしも要するか、意味に即した選択を求めるかという活動の条件に着目しています。参加人数だけによる分類ではありません。'
new='同書16頁の区別は、意味を理解せずに遂行できるか、意味に即した選択が必要かという活動の条件に着目しています。参加人数だけによる分類ではありません。'
e=dict(id='Q_4_066',field='explanations',index=0,before=old,after=new,reason='画像精読後、必ずしもの係り先が曖昧な表現を修正。意味理解なしの遂行可能性と、意味ある選択の必要性を明示。',sources=['S144'],applied=True,before_version='第79バッチ45箇所反映後の累積作業稿',block_context='A_4_066',paragraph_prefix='1（誤）')
for name,obj in [('changes.json',c+[e]),('changes_batch79b.json',[e])]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
