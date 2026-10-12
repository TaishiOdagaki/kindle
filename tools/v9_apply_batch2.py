#!/usr/bin/env python3
"""Rebuild cumulative unfinished draft from immutable v8 and explicit corrections."""
import hashlib,html,json,zipfile
from docx import Document
import v9_apply_batch1 as b
import quiz_audit as qa
ROWS=b.ROWS
extra=[]
def change(k,f,i,t,r,s):
 old=ROWS[k][f] if i is None else ROWS[k][f][i]
 assert old!=t
 extra.append(dict(id=k,field=f,index=i,before=html.unescape(old),after=t,reason=r,sources=s,applied=True))
change('Q_3_040','explanations',1,'Horwitzら（1986）は、外国語不安を考えるための関連概念として、コミュニケーション不安、テスト不安、否定的評価への恐れを論じました。ただし、外国語不安はこの3種の不安の単純な組合せではなく、教室での外国語学習に特有の自己認識・信念・感情・行動の複合体とされています。これらをFLCASの確定した3下位尺度と同一視することは避ける必要があります。','関連概念と尺度の下位構造を混同していた。原著印刷頁127–130に基づき修正。',['S17'])
change('Q_4_068','stem',None,'学習者の発話に対し、教師が次のように応答した。学習者：「昨日、図書館へ行って、勉強しなかったでした。」教師：「勉強しなかった……？」学習者：「あ、勉強しませんでした！」このやり取りにおける教師の行動の説明として、最も適切なものはどれか。','なかったですは許容される過去否定である。誤用例をなかったでしたへ置き換え、発話のどこを繰り返したか明確にする。',['S18'])
change('Q_4_068','options',2,'誤りを含む部分を繰り返して語調で注意を促し、正しい形を直接与えずに学習者の自己修正を促した。','新しい会話例の実際の教師行動に対応させる。',['S18'])
change('Q_4_068','explanations',0,'教師は「勉強しませんでした」という正しい形を直接提示しておらず、それを模倣するように求めてもいません。','正しい形の提示を常に模倣要求と一括しない。',['S18'])
change('Q_4_068','explanations',2,'教師は「勉強しなかった……？」と発話の一部を疑問調で繰り返し、学習者が自分で形を直す機会を与えています。この例では、教師による正しい形の直接提示はありません。なお、「勉強しなかったです」自体は過去否定の表現として使われるため、それを一律に誤用と扱ってはなりません。','エリシテーションとの曖昧な名称混同を避け、観察できる行動を説明する。',['S18'])
change('Q_4_086','explanations',0,'この文章題では、15－6＝9で正解になります。ただし、キーワードだけで演算を選ぶ方法では、比較の向きが逆の問題に対応できない場合があります。例えば「あおいさんは15枚持っています。あおいさんはあきらさんより6枚少ないです。あきらさんは何枚持っていますか」なら、正解は15＋6＝21です。「少ない」という語だけを見て15－6とするのは誤りになります。','逆比較の15＋6＝21を誤用と呼んでいた計算上の誤りを修正。外部資料に依存しない代入検算を実施。',[])
assert 15-6==9 and (15+6)-6==15
all_changes=b.CHANGES+extra
def norm(x):
 if isinstance(x,str):return html.unescape(x)
 if isinstance(x,list):return [norm(t) for t in x]
 if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
 return x
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
doc=Document(b.SRC)
for c in all_changes:
 ps=[p for p in doc.paragraphs if c['before'] in p.text]
 assert len(ps)==1,(c['id'],c['field'],len(ps))
 assert b.replace_paragraph(ps[0],c['before'],c['after'])
doc.save(b.DST)
assert zipfile.ZipFile(b.DST).testzip() is None
issues,q,a=qa.audit(str(b.DST)); _,q0,a0=qa.audit(str(b.SRC))
assert len(q)==len(a)==500 and set(q)==set(q0) and set(a)==set(a0)
assert all(a[k]['ans']==a0[k]['ans'] for k in a)
modified={c['id'] for c in all_changes}
assert all(norm(q[k])==norm(q0[k]) and norm(a['A_'+k[2:]])==norm(a0['A_'+k[2:]]) for k in q if k not in modified)
assert not [i for i in issues if i[0] in {'S1','S3','S4','S5','S6','N1','N2'}]
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
for filename,changes in [('changes_batch2.json',extra),('changes.json',all_changes)]:
 (b.OUT/filename).write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.md').write_text('# 修正前後の比較（累積・監査作業中）\n\n部分修正の適用は問題全体の最終承認を意味しない。\n\n| ID | 対象 | 修正前 | 修正後 | 理由 | 根拠 |\n|---|---|---|---|---|---|\n'+''.join(f"| {c['id']} | {c['field']} {'' if c['index'] is None else c['index']+1} | {c['before'].replace('|','／')} | {c['after'].replace('|','／')} | {c['reason']} | {', '.join(c['sources']) or '算術・具体例の代入検算'} |\n" for c in all_changes))
(b.OUT/'postfix_machine.json').write_text(json.dumps(dict(questions=500,answers=500,v8_unchanged=True,answers_unchanged=True,unmodified_questions_unchanged=True,changed_questions=len(modified),replacements=len(all_changes),issues=issues,statistics=qa.stats(q,a),full_visual_qa_completed=False,release_ready=False),ensure_ascii=False,indent=2)+'\n')
d=json.loads((b.OUT/'decisions.json').read_text())
for k in {c['id'] for c in extra}:
 d[k]['fixes_applied']=True
 d[k]['unresolved']='第2修正バッチを作業稿へ適用。その他の選択肢・解説の出典照合と修正後再判定、表示検査は未了。'
(b.OUT/'decisions.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(f'Cumulative {len(modified)} questions / {len(all_changes)} replacements; all 500 mechanical checks rerun; v8 immutable.')
