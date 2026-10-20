"""One-time revision of a writing feedback question; CEFR 2020 pp140-141."""
import html,json
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT
cs=json.loads((p/'changes.json').read_text()); assert len(cs)==3885
d=json.loads((p/'decisions.json').read_text())
_,q,a=qa.audit(str(b.DST))
k='Q_5_094'; ak='A_5_094'; assert d[k]['status']=='要追加確認' and a[ak]['ans']=='1'
stem='【事例】身近な経験を読み手に伝える作文で、出来事の順序を保ちながら、文のつなぎ方を広げることを今回の目標とする。学習者Bさんは次のように書いた。「昨日、私は友達と映画を見に行きました。映画はとても面白かったです。それから、レストランでラーメンを食べました。ラーメンはとても美味しかったです。それから、家に帰りました。」CEFR補遺版（2020）の主題展開と結束性の観点を参考に、この目標に合う指導を一つ選べ。'
opts=[
'「それから」で順序を示せている点を認めた上で、意味を保ちながら「〜て」などで文をつなぐ別の書き方を試し、元の文と読み比べる。',
'文法上の誤りが目立たないことを理由に、今回の目標についても達成済みとし、文のつなぎ方を検討する活動は行わない。',
'この作文だけで語彙の意味を理解していないと断定し、辞書的定義の暗記だけを行って、文のつなぎ方は扱わない。',
'今回の目標を、日常の経験を伝えることから論文の文体を模倣することへ変え、出来事の関係を検討せず硬い表現へ置き換える。']
exps=[
'提示文にも順序を示す接続表現があります。CEFR補遺版140〜141頁は時系列の明示と文を結ぶ手段を扱います。これを参考に、既にできている点を認めて別のつなぎ方を試す活動は、指定された目標に合います。',
'文法上の誤りの少なさと、文のつなぎ方の選択肢を広げるという今回の目標は同じではありません。この肢では目標に沿う検討を行いません。',
'この短い作文から、語彙を理解していないとは断定できません。また、辞書的定義の暗記だけでは、指定された文のつなぎ方を検討する活動になりません。',
'この設問では、経験を伝えながら文のつなぎ方を広げることが目標です。論文の文体の模倣へ目標を変える対応は合いません。硬い表現自体を一律に誤りとする判断ではありません。']
reason='S45 CEFR補遺版2020の印刷140〜141頁（公式PDF139〜140、0始まり）の主題展開・結束性本文と尺度をWeb経由で取得・精読。原文の「それから」による時系列の結び付きを認め、結束性不足・幼さ・最適指導の断定を撤回。架空課題の目標を明示し、指導案との整合性を全肢全解説で判定。短文から語彙理解全般を診断しない。「〜て」は本設問の例示で、CEFRの日本語指定形式や介入の実証効果とはしない。因果を加える「〜ので」の無条件追加は削除。BさんのCEFRレベル判定ではない。'
extra=[]
prompt='CEFR補遺版（2020）の主題展開と結束性の観点を参考に、この目標に合う指導を一つ選べ。'
intro='【事例】身近な経験を読み手に伝える作文で、出来事の順序を保ちながら、文のつなぎ方を広げることを今回の目標とする。学習者Bさんは次のように書いた。'
oldstems=['【事例】以下は、中級の日本語学習者Bさんが作文（書面パフォーマンス）で書いた文章である。','Bさんの作文に対する分析と指導方針として、最も適切なものはどれか。']
for field,olds,news in [('stem',oldstems,[intro,prompt]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==0 else '誤')+'）'} if field=='explanations' else ({'stem_context':prompt} if field=='options' else {})
  extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S45'],applied=True,before_version='第190バッチ後',block_context=ak if field=='explanations' else k,**kw))
d[k].update(status='確認済み',independent_answer=1,fixes_applied=True,sources=['S45'],reason=reason,option_verdicts=['正：既存の時系列接続を認め目標に沿って別の接続を試す','誤：文法上の誤りの少なさを別の課題目標の達成と同一視','誤：語彙理解を断定し目標の活動を行わない','誤：指定された作文目標を別の目標に変更'],candidate_answers=[],stem_review='架空課題の目標を明示。提示文の接続を認める。',explanation_review='全4解説を原文観察・指定目標・S45の主題展開と結束性の範囲へ照合。最適指導や指導効果、CEFRレベル、内的語彙知識を断定しない。',unresolved='',multiple_correct_risk='なし：指定目標に合うのは1のみ',no_correct_risk='なし：1は既存の接続を認めた上で目標の活動を行う')
assert len(extra)==10
for name,obj in [('changes.json',cs+extra),('changes_batch191.json',extra),('decisions.json',d)]:
 (p/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
