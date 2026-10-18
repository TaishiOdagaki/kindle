"""One-time methods and issuer-defined plurilingualism audit."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3534
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_4_034',4,'S242',
'Larsen-FreemanとAnderson（2011）『Techniques and Principles in Language Teaching』第3版の直接法の説明に合うものを一つ選べ。',
['新出語句は必ず学習者の母語に翻訳し、目標言語と意味を直接結び付けることを避ける。',
'文法規則を初めに明示することを原則とし、例から学習者が規則を考える帰納的な学習は行わない。',
'授業開始から数か月間は読む・書く活動を一切認めず、文字を提示することを全面的に禁止する。',
'実物、絵、身振りなどで語句の意味を示し、母語への翻訳を介さずに目標言語と意味を結び付ける。'],
['第3章は、母語への翻訳ではなく、実演や視覚的な補助を使って目標言語で意味を伝えると説明しています。母語への翻訳を必須とする説明とは逆です。',
'同章の原則3は、例から規則や一般化を考える帰納的な文法学習を説明しています。規則の明示を常に先行させるという説明は合いません。',
'同章の原則7は、口頭でのコミュニケーションを基礎としつつ、読む・書く・話す・聞くの四技能を初めから扱うとしています。数か月間の文字活動の全面禁止とは異なります。',
'同章の導入と原則3に対応します。実物や絵、身振りを利用して、目標言語と意味の直接の結び付きを図る方法として説明されています。'],
'S242著者2名の2011年第3版原著本文を大学公開PDFで取得。PDF46・52～54頁の直接法の導入・全10原則・技法冒頭を精読、52～53頁画像照合。数か月間の文字禁止をALM一般に帰属する旧解説を撤回。著者の整理に範囲を明示し、Berlitz原典・全教授法史・日本語授業の効果を検証したとはしない。',
['誤：母語への翻訳必須とする','誤：帰納的文法学習を否定','誤：開始時の四技能を文字禁止に変える','正：実物等による意味の直接提示']),
('Q_O_051',1,'S242',
'ケース11のA教師の練習をオーディオリンガル・メソッドの特徴と比較する。Larsen-FreemanとAnderson（2011）の同メソッドの理論的基盤の説明に合うものを一つ選べ。',
['構造主義言語学の原理を背景とし、発展の過程で行動主義心理学の原理が取り入れられ、刺激への反応と強化による習慣形成を考える。',
'母語への翻訳と明示的な文法規則の説明だけを基盤とし、対話文の模倣・反復は授業から排除する。',
'新しい言語習慣の形成を否定し、正しい反応への強化も行わないという立場を基盤とする。',
'読む・書く活動を常に先行させ、その後で初めて聞く・話す活動を導入するという順序を基盤とする。'],
['第4章の導入は、構造主義言語学の原理の応用に続き、行動主義心理学の原理が取り入れられたと説明しています。ケースの置換練習・暗唱は原則3で示される練習と比較できますが、手順だけからA教師本人の理論的信念を確定するものではありません。',
'同章の原則3は、対話文の模倣・反復と各種ドリルを挙げ、文法は例から帰納的に扱うと説明しています。模倣や反復を排除し、翻訳と規則説明だけを基盤とする説明は合いません。',
'同章の導入は新しい言語習慣の形成を説明し、原則3は成功した反応への肯定的な強化を挙げています。両方を否定する説明とは逆です。',
'同章の原則7は、聞く・話す・読む・書くの提示順序と、口頭で扱った内容に基づく書く活動を説明しています。読む・書く活動を常に先行させるという説明とは異なります。'],
'S242第4章導入PDF59頁・原則PDF70～72頁本文、59頁画像を照合。ケース11のA教師本文も照合。練習手順から本人の理論的信念を断定する問いを撤回し、著者が説明するALMの理論と特徴の比較へ限定。Skinner・Fries等の引用先原典、他理論の基盤の包括的分類、習得効果は承認しない。',
['正：同書の理論的基盤と習慣形成に対応','誤：対話文の模倣・反復を排除','誤：習慣形成と強化を否定','誤：提示順序を逆転']),
('Q_2_032',3,'S243',
'欧州評議会のCEFR公式解説「Plurilingualism and pluriculturalism」の本文に照らし、複言語・複文化主義の説明に合うものを一つ選べ。',
['個人の言語・文化的な資源は活用せず、既習言語の知識や経験を全て切り離すことを目指す。',
'言語や文化についての部分的な能力や気づきには価値を認めず、それらを個人の資源から排除する。',
'個人の言語・文化的な資源を相互に関連するものとして捉え、社会的状況で複数の言語や変種、文化的な知識・経験を動的に活用する。',
'複言語・複文化主義と多言語・多文化主義には区別がなく、いずれも言語と文化を分離した静的なものとしてだけ捉える。'],
['公式解説は、個人が言語・文化の多様な資源を用い、さらに発展させると説明しています。既習の資源を全て切り離すという説明は合いません。',
'本文は、部分的な能力や気づきにも価値を認めています。部分的であることを理由に排除する説明とは逆です。',
'本文の、個人の資源の全体性、言語・文化間の関連、社会的状況での動的な活用という説明に対応します。',
'本文は両者を区別し、多言語・多文化主義の側では言語と文化を社会又は個人内に共存する別個のものとして捉えると説明しています。両者を区別しない説明は合いません。'],
'S243欧州評議会CEFR公式ページの概念説明本文3段落をWeb openで全体取得・精読。検索抜粋でなくページ本文。全肢全解説をこの定義本文へ照合。多言語主義を社会レベルだけとする旧単純化、トランスランゲージングの別理論や全母語活用教授法の推奨を撤回。原バイトHTMLとCEFR2020PDFは直接取得403のため未取得と区別し、CEFR2001/2020全原典の確認とはしない。',
['誤：既有の言語文化資源を排除','誤：部分的な能力を排除','正：相互関連と動的活用','誤：二つの概念の区別を否定'])]
extra=[]
for k,key,sid,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第178バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='対象著作又は発表機関の定義本文を指定し、全4肢を独立照合。活動から教師の信念を断定しない。',explanation_review='全4解説を取得本文へ照合。段階条件・部分的能力・相互関連を確認し、別原典・効果の一般化を撤回。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定本文に一致',no_correct_risk=f'なし：{key}の根拠本文取得済み')
assert len(extra)==27
for n,obj in [('changes.json',cs+extra),('changes_batch179.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'methods179.pdf').read_bytes()
entries=[dict(source_id='S242',url='https://elearning.usm.md/pluginfile.php/190241/mod_resource/content/2/Larsen-freeman%203rd%20ed_techniques-in-language-teaching.pdf',title='Diane Larsen-Freeman and Marti Anderson Techniques and Principles in Language Teaching third edition 2011',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope='著者・奥付PDF3～4頁、直接法46・52～54頁、ALM59・70～72頁。52・53・59頁画像。318頁の電子的再組版PDFで印刷版の頁を推定しない。全書籍・引用先原典の精読ではない。',full_source_redistributed=False),dict(source_id='S243',url='https://www.coe.int/en/web/common-european-framework-reference-languages/plurilingualism-and-pluriculturalism',checked='2026-10-19',retrieval='Web open によるページ本文取得。turn662view0 L128～132 の概念説明3段落全体。動画・別文献は未取得。',raw_bytes_obtained=False,raw_sha256=None,read_scope='公式機関自身の概念説明の全文。検索抜粋・抄録ではない。CEFR2001/2020原PDFの独立取得とはしない。',full_source_redistributed=False)]
(p/'evidence/batch179_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
(p/'evidence/batch179_source_attempts.json').write_text(json.dumps([dict(url=u,result='urllib直接取得HTTP403。迂回取得せず。CEFR2020原PDF取得成功とはしない。HTMLは別にWeb openで本文3段落を取得。') for u in ['https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4','https://www.coe.int/en/web/common-european-framework-reference-languages/plurilingualism-and-pluriculturalism']],ensure_ascii=False,indent=2)+'\n')
