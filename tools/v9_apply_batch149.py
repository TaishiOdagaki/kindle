"""One-time error-analysis and intercultural interpretation repair."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3012
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_O_032':dict(key=4,sources=['S118'],
 stem='Corder（1967）の議論に照らし、このケースの表現を誤用かどうか検討する際の考え方として、最も適当なものを一つ選べ。',
 opts=['表面上は文法に違反していなければ、状況との意味の対応を調べずに、誤用ではないと結論する。','学習者の誤用はすべて母語の体系に関係すると考え、ほかの可能性は検討しない。','学習者の誤用は母語の体系と一切関係しないと考え、母語との関係は検討しない。','表現がその状況で何を意味するかを確かめ、表面的な形だけで誤用かどうかを判断しない。'],
 exps=['原論文168頁は、表面上は逸脱していない発話でも、状況との意味の対応が必要だと述べています。表面的な形だけを判断根拠とする説明は、この議論に合いません。','原論文168頁は、多くの誤用が母語の体系に関係する一方、すべてではないと述べています。母語だけで説明できるという立場ではありません。','原論文168頁は、多くの誤用と母語の体系との関係を認めています。一切関係しないと排除する説明は、著者の立場に合いません。','著者は、発話が誤用かどうかを判断する際に状況文脈を考慮します。このケースでも、本人がどのような意味で表現したかを確かめるという適用が考えられます。この選択だけで、誤用の有無や母語の影響という個別の原因を確定したことにはなりません。'],
 verdicts=['誤：原論文が必要とする状況との意味の対応を省く','誤：多くは関係するがすべてではないという限定を落とす','誤：多くの誤用と母語の体系の関係を一律排除','正：表面的な形と状況文脈を区別する原論文の議論に一致'],
 reason='S118原論文全12頁をERICから再取得。原誌166–169頁を精読し、168頁全体を画像でも照合。状況文脈と意味の対応、母語との関係は多くにあるが全てではないという限定を全4肢・解説へ照合。母語対照のみを正答とし、日本語の当該文をなお文法的誤用と認定していた旧解説を撤回。Corderの当時の議論に対象を明示し、個別日本語例文の誤用・原因を原論文で実証したとは扱わない。'),
'Q_4_103':dict(key=3,sources=['S213'],
 stem='Cさんが日本語学習者Bさんに「日曜日の引っ越し、もしよかったら手伝いに行きましょうか」と申し出た。Bさんは「あ、大丈夫です。ありがとうございます」と答え、Cさんは「そうですか。じゃあ、気をつけてね」と応じた。当日Cさんが来ず、Bさんは不満を抱いた。欧州評議会のRFCDC（2018）が述べる異文化への開放性や曖昧さへの寛容性を踏まえ、この事例の背景を検討する対応として最も適切なものを一つ選べ。',
 opts=['Bさんの語彙の記憶違いだけが原因だと決め、本人への確認を省く。','Bさんは悪意をもってCさんを混乱させたのだと、発言だけから断定する。','二人が発言に込めた意味や期待した応答を確認し、複数の解釈を検討してから判断する。','Bさんの出身文化の人は全員同じ応答を期待すると考え、出身だけで原因を決める。'],
 exps=['語句をどう理解したかは確認する対象になり得ますが、この記録だけで記憶違いだけが原因だと確定する根拠はありません。判断を保留し、利用できる証拠を確かめる方針と合いません。','悪意があったという情報は示されていません。根拠なく悪意を断定するより、相手の考えや期待を理解し、別の解釈も検討する必要があります。','RFCDCは、他者について判断を保留する態度、状況に複数の解釈があり得ることの認識、相手の視点を理解する技能を述べています。それらをこの仮想事例の確認・検討へ適用した対応です。会話の原因が特定の文化規範だと実証されたという意味ではありません。','出身だけを根拠に個人の期待を確定しており、複数の解釈や本人の視点を検討していません。自分の前提を点検し、証拠に基づいて判断するという方針にも反します。'],
 verdicts=['誤：語彙理解の可能性の検討を、根拠のない単一原因の確定に替える','誤：会話記録にない悪意を断定する','正：判断保留・複数解釈・相手の視点と証拠の確認に対応','誤：出身だけで本人の期待を確定し、他の解釈を排除'],
 reason='S213欧州評議会RFCDC Volume1（2018）全89頁PDFを公式サイトから取得。印刷41–50頁の本文・注記を精読し、41・45・48頁を画像照合。開放性の判断保留、曖昧さへの寛容性の複数解釈、批判的思考の証拠と前提の点検、共感の視点取得を4肢・全解説へ照合。語彙誤解の可能性を誤答として排除し、未特定の母文化の形式的辞退を原因と断定した旧問題を撤回。同じ異文化事例の解釈・背景検討の学習領域を保ち、根拠に基づく対応へ改訂。カルチャー・アシミレーターという方法の原著を取得・承認したものではなく、この仮想会話の原因を資料が実証したものでもない。')}
ps=Document(b.DST).paragraphs
extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']!='確認済み' and a[ak]['ans']==str(v['key'])
 oldstem=q[k]['stem']
 tails=[]
 if k=='Q_4_103':
  i=next(i for i,p in enumerate(ps) if 'Bさん（Y国出身）' in p.text)
  oldstem=ps[i].text;tails=[p.text for p in ps[i+1:i+5]]
  assert q[k]['stem']==' '.join([oldstem]+tails)
 for field,olds,news in [('stem',[oldstem],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   assert html.unescape(old)!=new
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=v['sources'],applied=True,before_version='第148バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 for old in tails:
  extra.append(dict(id=k,field='stem_continuation',index=None,before=old,after='',reason='複数段落に分かれていた旧設問の場面説明を新しい設問段落に統合したため、旧4段落を明示的に削除し二重掲載を防ぐ。'+v['reason'],sources=v['sources'],applied=True,before_version='第148バッチ反映後',block_context=k,remove_paragraph=True))
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=v['sources'],reason=v['reason'],option_verdicts=v['verdicts'],stem_review='取得した原論文・公式枠組みの該当記述に対象を明示。事例から個別原因を断定しない条件で4肢を独立判定。',explanation_review='全4解説を根拠本文へ照合。仮想事例への適用と資料自体の実証を区別し、未確認な単一原因や文化規範の帰属を残さない。',unresolved='',multiple_correct_risk='なし：設問の条件と根拠本文に一致するのは独立正答のみ',no_correct_risk='なし：独立正答'+str(v['key']))
assert len(extra)==22
for n,obj in [('changes.json',cs+extra),('changes_batch149.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2]
def meta(name):
 raw=(root/name).read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
e=[dict(source_id='S118',title="The Significance of Learner’s Errors",author='S. P. Corder',year=1967,url='https://files.eric.ed.gov/fulltext/ED019903.pdf',pdf_pages=12,read_scope='原誌166–169頁本文全体を再精読。168頁（PDF10頁）全体を画像でも照合。全12頁精読ではない。',limitations='当時の著者の立場に限定。個別日本語例文の誤用や原因を直接実証した資料ではない。従来のsources.mdの母語との関連を述べる頁の169（PDF11）という誤記は168（PDF10）へ訂正。',**meta('corder149.pdf')),dict(source_id='S213',title='Reference Framework of Competences for Democratic Culture Volume 1 Context, concepts and model',institution='Council of Europe',year=2018,url='https://rm.coe.int/prems-008318-gbr-2508-reference-framework-of-competences-vol-1-8573-co/16807bc66c',pdf_pages=89,read_scope='印刷41–50頁（PDF43–52頁）本文と注記を全て精読。印刷41・45・48頁（PDF43・47・50頁）を画像照合。全89頁精読ではない。',limitations='態度・技能の枠組みを仮想事例の対応へ適用したもので、原因の実証・国別慣習の実証・カルチャーアシミレーターの原著承認ではない。',**meta('rfcdc150.pdf'))]
for v in e:v.update(retrieved='2026-10-18',full_source_redistributed=False)
(b.OUT/'evidence/batch149_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions / 22 edits including 4 removed old stem paragraphs')
