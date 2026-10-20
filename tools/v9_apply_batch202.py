"""One-time glossary clarification, no question or answer edits."""
import json,subprocess
from pathlib import Path
import quiz_audit as qa
p=Path('audit/v9');cs=json.loads((p/'changes.json').read_text());assert len(cs)==4314
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'
paras,_=qa.load(str(doc))
old='モダリティ（ムード）　話し手の判断・推量・意志などを表す文法カテゴリー。'
assert sum(x['t']==old for x in paras)==1
new='モダリティ　井上優「モダリティ」の整理では、命題内容に対する話し手の判断や、発話・伝達の態度に関わる意味をいう。ムードと呼ぶ場合もあるが、ムードを述語の形態に限って用いる場合もある。'
c=dict(id='APPENDIX_GLOSSARY',field='glossary',index=None,before=old,after=new,reason='S67原資料全18PDF頁を再取得し、印刷133～135頁を全文精読。133頁のムードを述語形態に限定する用法の留保と134頁の判断／発話・伝達の二分類を用語集にも反映。両語を常に同一視する読みと、この整理を全研究者に普遍化する読みを避ける。Q_5_059・060の指定資料と整合させ、設問・選択肢・正答・解説は変更しない。',sources=['S67'],applied=True,before_version='第199～201バッチ後')
c['glossary_head']='モダリティ'
(p/'changes.json').write_text(json.dumps(cs+[c],ensure_ascii=False,indent=2)+'\n')
(p/'changes_batch202.json').write_text(json.dumps([c],ensure_ascii=False,indent=2)+'\n')
