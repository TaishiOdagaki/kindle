#!/usr/bin/env python3
"""Explicit legal, institutional, and teaching corrections; rebuild from immutable v8."""
import json,html,hashlib,zipfile
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
OUT=b.OUT
prior=json.loads((OUT/'changes.json').read_text())
# Prior cumulative history must be the batch-2 checkpoint for a fresh execution.
assert len(prior)==35,'Run the saved cumulative manifest, not this one-time recording again.'
_,Q,A=qa.audit(str(b.DST))
extra=[]
def change(k,f,i,new,why,sources):
 old=Q[k]['stem'] if f=='stem' else Q[k]['opts'][i] if f=='options' else A['A_'+k[2:]]['txt'][i]
 old=html.unescape(old)
 if old==new:return
 extra.append(dict(id=k,field=f,index=i,before=old,after=new,reason=why,sources=sources,applied=True,before_version='第2修正バッチ作業稿'))
def full(k,stem,opts,exps,why,sources):
 assert len(opts)==len(exps)==4
 change(k,'stem',None,stem,why,sources)
 for f,arr in [('options',opts),('explanations',exps)]:
  for i,t in enumerate(arr):change(k,f,i,t,why,sources)
# National and local duties are responsibility, distinct from employers' efforts.
change('Q_1_033','options',0,'国は日本語教育の推進に関する施策を総合的に策定・実施する責務を有し、地方公共団体は国との適切な役割分担を踏まえ、地域の状況に応じた施策を策定・実施する責務を有する。','国・地方の責務と事業主の努力義務を条文に沿って区別。',['S27'])
change('Q_1_033','explanations',2,'本法律は、日本語教師に一律の無報酬活動を義務付けていません。第4条、第5条、第6条は、それぞれ国、地方公共団体、外国人等を雇用する事業主の責務について定めています。','本法律と別法の資格制度の説明を混在させない。',['S27'])
change('Q_1_033','explanations',3,'第6条は、外国人等を雇用する事業主が、国・地方の施策に協力するとともに、雇用する外国人等とその家族に学習機会の提供その他の学習支援を行うよう努める旨を定めています。日本語学習を全面的に禁止した規定ではありません。','条文の外国人等と学習支援の努力義務を正確に述べる。',['S27'])
full('Q_4_126','著作権法第36条による試験問題への著作物の利用について、正しいものはどれか。',[
'公表された著作物を試験・検定の目的上必要な限度で問題として複製・公衆送信できる。営利目的の場合には通常の使用料相当額の補償金が必要であり、同条第1項の但書にも従う。',
'第36条を利用して試験問題にした著作物は、試験後に市販の過去問題集へ載せる場合にも、利用目的や分量を問わず自動的に自由利用できる。',
'第36条の対象は未公表の著作物だけであり、すでに出版された小説や論説文を試験問題に使うことは同条によって認められない。',
'営利目的の試験・検定では、第36条による利用は一切認められず、補償金を支払って利用する仕組みも存在しない。'],[
'第36条第1項は、公表された著作物を、試験・検定の目的上必要な限度で、その問題として複製・公衆送信する場合を対象とします。但書は、著作物の種類・用途や公衆送信の態様に照らし、著作権者の利益を不当に害する場合を除きます。営利目的の複製・送信には、第2項の補償金が必要です。',
'第36条は試験・検定の問題としての利用を対象とします。その後の市販問題集への掲載を、条件なしに認める規定ではありません。許諾や、適用可能な別の権利制限などの根拠を改めて検討する必要があります。',
'第36条第1項は、公表された著作物を対象としており、未公表の著作物だけを対象とする規定ではありません。',
'第36条第2項は、営利を目的として第1項の複製・公衆送信を行う者について、通常の使用料相当額の補償金を支払うことを定めています。営利目的だから同条の利用が一切禁止されるわけではありません。'],
'第36条の但書と第2項を明示。ひらがな化・難易度調整が自動的に許されるとの不確かな改変説明を撤去。',['S26'])
change('Q_4_122','explanations',1,'第51条では、別段の定めがある場合を除き、著作権は著作者の死後70年を経過するまで存続するとされています。保護期間が満了した後も、第60条による著作者の死後の人格的利益の保護などに留意が必要です。死後50年という情報だけで、常に遺族の許諾が必要とも、直ちに自由利用できるとも判断できません。','死後の人格的利益保護と存続期間、例外を分ける。',['S26'])
change('Q_4_122','explanations',2,'第17条第2項は、著作者人格権・著作権の享有に方式の履行を必要としないと定めています。権利の発生に登録申請を要求する説明は誤りです。','無方式主義を現行法の根拠条項で説明。',['S26'])
change('Q_O_048','explanations',1,'第35条第1項の対象となる非営利設置の教育機関で、授業の過程に必要な限度の公衆送信を行う場合、第2項の補償金が原則として必要です。第3項の例外は、対面で著作物を提示等して行う授業を、別の場所で同時に受ける者へ送信する等の所定の場合です。すべてのリアルタイム送信が免除されるわけではありません。','同時中継ならすべて免除という誤読を除く。',['S26'])
change('Q_MO_011','options',1,'オンデマンド配信は公衆送信に当たり、第35条第1項を適用する場合でも原則として第2項の補償金が必要になるため。','非同期と同期の単純な区分でなく条文上の要件を示す。',['S26'])
change('Q_MO_011','explanations',1,'第35条第1項による授業目的の公衆送信には、第2項に基づく補償金の支払いが原則として必要です。第3項は、対面授業の場で提示等した著作物を、その授業を別の場所で同時に受ける者に送信する等の所定の場合を例外とします。録画した授業のオンデマンド配信は、この同時受講の例外とは区別して確認します。','公衆送信補償金の例外の適用条件を正確にする。',['S26'])
change('Q_MO_013','explanations',2,'第10条第2項は、事実の伝達にすぎない雑報・時事の報道を、言語の著作物から除いています。一方、創作的な表現を含む新聞の論説・コラム等は著作物になり得ます。新聞に載っているというだけで、すべて著作権がないとする説明は誤りです。','すべての新聞記事が著作物という断定を修正。',['S26'])
change('Q_O_049','options',1,'権利関係を確認した上で、必要な範囲の利用に絞る、権利者の許諾を得る、または既存の創作的表現を流用しない自作教材へ置き換えることを検討する。','要約すれば権利問題を回避できるという誤解を防ぐ。',['S26'])
change('Q_O_049','explanations',1,'文章を要約しても、元の創作的な表現を引き継ぐ場合には翻案等の権利が関わり得ます。第35条・第47条の6等の要件を満たす利用か、許諾が必要かを確認し、必要に応じて既存の表現を流用しない自作教材へ置き換えます。「要約だから自由」とは扱いません。','要約と自作を一括した権利回避の説明を修正。',['S26'])
change('Q_4_127','stem',None,'教員Hさんが、誰でも視聴できる文法解説動画を配信する。選択肢2以外の素材については、権利者の許諾・利用許諾を得ておらず、引用その他の権利制限が適用される事情もないものとする。著作権法上、適切なものはどれか。','権利者が許諾した素材等なら誤答も成立するため利用条件を明示。',['S26'])
change('Q_4_127','explanations',2,'この設問の条件では、教科書の創作的な会話文を録音して動画へ収録する複製と、その動画の公衆送信について、権利者の許諾その他の根拠が必要です。録音の収録・配信と、聴衆の前で公に口述する行為は区別して考えます。','録音配信を口述権の行使と一括する権利区分の誤りを修正。',['S26'])
full('Q_5_034','2025年12月22日の内閣告示第4号「ローマ字のつづり方」に関する記述として、正しいものはどれか。',[
'新しい告示では、「し・ち・つ・ふ」を必ずsi・ti・tu・huと書くものとし、shi・chi・tsu・fuは本表から除かれた。',
'本表では「し・ち・つ・ふ」をshi・chi・tsu・fuと書く。長音には母音字の上に符号を付ける方法のほか、現代仮名遣いに沿って母音字を並べる方法も示されている。',
'新しい告示は、過去の著作や文書に使われた別の方式をすべて誤りとし、さかのぼって書き直すことを要求している。',
'新しい告示は、科学・技術・芸術の専門分野と個々人の表記にも、例外なく同じ方式を強制する。'],[
'本表にはshi・chi・tsu・fuが示されています。si・ti・tu・huだけを採用したという説明は誤りです。',
'告示の本表と添え書き3に対応する記述です。長音は原則として母音字の上のマクロンで表し、必要な場合にはサーカムフレックスも使用できます。また、現代仮名遣いと同様に母音字を並べる書き方も認められています。',
'前書き3は、過去の著作や文書のつづり方を否定するものではないとしています。旧方式の資料を一律にさかのぼって修正する趣旨ではありません。',
'前書き2は、科学・技術・芸術その他の専門分野や個々人の表記にまで及ぼそうとするものではないとしています。一般の社会生活で現代の国語をローマ字表記する際のよりどころです。'],
'現行内閣告示に全面改稿し、学校・旅券の独自ルールと古い告示の混同を除く。',['S20'])
full('Q_3_020','学習者が「書く→書いて」というテ形の規則を学んだ。次のうち、学んだ規則を適用範囲外にも広げた過剰般化の例はどれか。',[
'「食べる」のテ形を「食べて」と正しく言った。',
'「行く」のテ形にも「く→いて」を適用し、「行いて」と言った。',
'「来る」のテ形を「来て（きて）」と正しく言った。',
'「見る」のテ形を「見て」と正しく言った。'],[
'「食べる→食べて」はグループ2の正しいテ形です。適用範囲外への拡張による誤りの例ではありません。',
'「行く」のテ形は「行って」です。「書く→書いて」の規則を例外の「行く」にも広げて「行いて」とした事例は、この設問でいう過剰般化に当たります。',
'「来る→来て（きて）」はグループ3の正しいテ形です。過剰般化による誤りではありません。',
'「見る→見て」はグループ2の正しいテ形です。過剰般化による誤りではありません。'],
'食べるないも過剰般化として成立する競合を除き、全誤答を出典で確認した正用に変更。正用に付いた非文記号も撤去。',['S28','S29'])
change('Q_3_038','explanations',1,'他者の評価や承認を目指すため、活動そのものの興味とは異なる外発的な動機づけの例です。ただし、この発言だけでは、外的な要求に応じた外的調節なのか、罪悪感の回避や自尊心の維持による取入的調節なのかまでは特定できません。','承認目的だけで取入的調節と決めつけない。',['S14'])
change('Q_M_020','explanations',1,'活動そのものが興味深い、楽しいという理由から取り組む動機づけが内発的動機づけです。外発的動機づけは活動と分離可能な結果を目指すもので、報酬・要求による外的調節だけでなく、本人が目的の重要性を認める同一化的調節なども含みます。','外発的動機づけを外部要因だけに限定しない。',['S14'])
change('Q_M_026','stem',None,'まとまった文章を聞きながらメモを取り、そのメモや記憶を基にペア・グループで話し合って元の内容を文章に再構成する活動を指す用語として、最も適当なものを選べ。','そのまま全文書取りとメモによる再構成を区別。',['S24'])
change('Q_M_027','explanations',1,'ディクトグロスは、文章を聞いて取ったメモや記憶を基に、ペア・グループで文章を再構成する活動です。聞いた音声を声に出して追うシャドーイングとは異なります。','ディクトグロスの全文書取りという誤解を除く。',['S24'])
change('Q_O_036','stem',None,'授業前に動画で基本的な説明を学び、教室ではその内容を用いる活動に時間を充てる授業設計を、最も具体的に指す用語を選べ。','反転はブレンディッドの上位分類にも属するため最も具体的な用語を指定。',['S25'])
# Track unchanged source separately, apply exact ordered replacements.
changes=prior+extra
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
doc=Document(b.SRC)
for c in changes:
 matches=[p for p in doc.paragraphs if html.unescape(c['before']) in p.text]
 assert len(matches)==1,(c['id'],c['field'],len(matches))
 assert b.replace_paragraph(matches[0],html.unescape(c['before']),c['after'])
doc.save(b.DST)
assert zipfile.ZipFile(b.DST).testzip() is None
issues,q,a=qa.audit(str(b.DST));_,q0,a0=qa.audit(str(b.SRC))
assert len(q)==len(a)==500 and set(q)==set(q0) and set(a)==set(a0)
assert all(a[k]['ans']==a0[k]['ans'] for k in a)
assert not [i for i in issues if i[0] in {'S1','S3','S4','S5','S6','N1','N2'}]
modified={c['id'] for c in changes}
def norm(x):
 if isinstance(x,str):return html.unescape(x)
 if isinstance(x,list):return [norm(y) for y in x]
 if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
 return x
assert all(norm(q[k])==norm(q0[k]) and norm(a['A_'+k[2:]])==norm(a0['A_'+k[2:]]) for k in q if k not in modified)
assert hashlib.sha256(b.SRC.read_bytes()).hexdigest()==b.EXPECTED
for fn,c in [('changes_batch3.json',extra),('changes.json',changes)]:
 (OUT/fn).write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
(OUT/'postfix_machine.json').write_text(json.dumps(dict(questions=500,answers=500,v8_unchanged=True,answers_unchanged=True,unmodified_questions_unchanged=True,changed_questions=len(modified),replacements=len(changes),issues=issues,statistics=qa.stats(q,a),full_visual_qa_completed=False,release_ready=False),ensure_ascii=False,indent=2)+'\n')
D=json.loads((OUT/'decisions.json').read_text())
for k in {c['id'] for c in extra}:
 D[k]['fixes_applied']=True
 D[k]['sources']=sorted(set(D[k]['sources'])|{s for c in extra if c['id']==k for s in c['sources']})
 D[k]['unresolved']='第3修正バッチを作業稿へ適用。問題全体の再判定が未記録の箇所は承認しない。'
# These complete rewrites were independently compared with all relevant source clauses.
for k,v,verdicts in [
 ('Q_4_126',1,['第36条1・2項に一致','試験目的外の無条件利用は第36条で保証されず誤り','公表された著作物の規定なので誤り','第2項が営利目的の補償金を規定しており誤り']),
 ('Q_5_034',2,['本表のshi/chi/tsu/fuに反する','本表と添え書き3に一致','前書き3に反する','前書き2に反する']),
 ('Q_3_020',2,['グループ2の正用なので過剰般化ではない','学習規則を例外に拡張する誤用なので正しい','グループ3の正用なので過剰般化ではない','グループ2の正用なので過剰般化ではない'])]:
 D[k].update(status='確認済み',independent_answer=v,option_verdicts=verdicts,unresolved='',multiple_correct_risk='なし：4選択肢の再判定記録を参照',no_correct_risk='なし：独立正答が存在',stem_review='改訂した設問条件を原資料と照合済み。',explanation_review='改訂後の4解説の全主張を記録した根拠箇所と照合済み。')
(OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print(f'Applied {len(extra)} new replacements; cumulative {len(modified)} questions / {len(changes)} replacements. Rechecked all 500 mechanically.')
