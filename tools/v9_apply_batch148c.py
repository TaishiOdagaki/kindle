"""One-time shared case summary consistency repair after non-error finding."""
import json
from docx import Document
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3011
old='教師はこれらの誤用を記録し、クラス全体でよく見られる誤用のパターンを整理することにした。'
new='教師は、表現ごとの確認内容や判断根拠を記録し、誤用と判断できたものについて、クラスで見られるパターンを整理することにした。'
assert sum(old in p.text for p in Document(b.DST).paragraphs)==1
c=dict(id='CASE_O_07',field='case_text',index=None,before=old,after=new,reason='過去経験用法を踏まえて誤用断定を撤回した第148バッチ148bに合わせ、ケース末尾のこれらの誤用という一律の認定も撤回。文境界の別例と、Q_O_034・035の系統的誤用の分析と課題対応の条件は保つ。',sources=['S211','S212'],applied=True,before_version='第148バッチ148b追加照合後')
for n,obj in [('changes.json',cs+[c]),('changes_batch148c.json',[c])]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('1 shared-case consistency edit')
