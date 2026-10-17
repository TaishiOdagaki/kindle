"""One-time role-play/safety rejudgments; keep Barnga rules unverified."""
import json,html,hashlib
from pathlib import Path
from docx import Document
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==3071
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_4_098':dict(key=1,sources=['S214'],
 stem='欧州評議会の人権教育手引きCompassのRole-playing節に照らし、ロールプレイを実施するときの配慮に合うものを一つ選べ。',
 opts=['演じた人物像が実際の人々に当てはまるかを問い直し、活動の終わりには役から離れる時間を確保する。','参加者本人や家族の事情に触れる内容であっても、本人が望まない経験の開示を演技のために強いる。','演技で傷ついた人が出ても、その受け止めを取り上げず、進行の都合だけを優先する。','ロールプレイは全ての台詞を正確に暗記して再現する形式であり、即興で演じることを含まないと説明する。'],
 exps=['手引きは、活動の終わりに役から離れる時間を確保することと、固定観念に注意することを挙げています。演じた人々は本当にそのような人か、人物像の情報はどこから得たかを振り返る問いを提案しています。','手引きは、参加者自身や身近な人の事情にも配慮し、本人が望まない形でさらされたり、疎外されたりしないよう求めています。開示を強いる対応は、その配慮に反します。','手引きは、傷ついたり、望まない形でさらされたりすることが起きたら真剣に受け止め、謝罪して説明するよう述べています。受け止めを無視して進行だけを優先する方針ではありません。','手引きは、参加者の経験も利用する一方、ロールプレイは主に即興で演じられるものと説明しています。全て暗記した台詞の再現に限定する定義ではありません。'],
 verdicts=['正：役から離れる時間と人物像・情報の批判的な振り返りに対応','誤：本人の望まない露出や疎外を避ける配慮と反対','誤：傷つき等を真剣に扱い謝罪・説明する方針と反対','誤：主に即興という説明を、暗記のみへ限定する'],
 reason='S214を再取得しDrama・Role-playing・Simulationsの全本文を連続して精読。従来の役割交換による視点取得の効果を一律に高めるという説明は、この資料で実証されたとは扱わず、同じロールプレイ学習の実施条件を問う設問へ改訂。役から離れる時間、参加者と身近な人への配慮、傷つき等への真剣な対応、主に即興という記述、人物像と情報源の振り返りを4肢・4解説へ照合。相手の内面を正確に再現できること、役割交換という特定技法の効果、全活動への必然的効果を承認していない。'),
'Q_4_104':dict(key=2,sources=['S214','S216'],
 stem='異文化の出来事をロールプレイで検討する学習を計画している。欧州評議会刊行のDeveloping intercultural competence through education（2014）第5章とCompassの説明に照らし、指導者の配慮に合うものを一つ選べ。',
 opts=['演じた人物像について参加者が振り返る機会を設けず、互いの解釈を検討する話合いを禁止する。','演じた人物像が特定集団の固定観念になっていないか、情報の根拠は何かを問い直し、過度の一般化を避ける。','言葉遣いや規範が自分と違う人は人間としての価値が低いと結論づける。','演じた人物像は同じ集団の全員に当てはまるものとして教え、その一般化を疑う必要はないとする。'],
 exps=['2014年刊行書41頁は、ロールプレイ後に起きたことや発見、人物像が本物らしいか固定観念かを話し合い、振り返ることを重視します。この学習でその検討を禁止する方針は合いません。ただし、あらゆる学習で集団討議が唯一不可欠だという一般論ではありません。','2014年刊行書41頁は、他集団への過度の一般化や固定観念の強化を避け、現れた固定観念を問い直すよう述べています。Compassも、演じた人物像とその情報の出所を批判的に振り返る問いを提案しています。','2014年刊行書41頁は、視線や言葉遣い、規範などに違いがあっても、人間としての価値が低くなるわけではないと説明します。違いを価値の上下へ直結させる説明は逆です。','両資料は、人物像や他集団についての固定観念、過度の一般化を振り返って問い直す方向を示します。演じた一人の像を集団全体へ確定的に広げる説明ではありません。'],
 verdicts=['誤：当該の活動後の検討と振り返りを禁止する','正：41頁の過度一般化・固定観念への注意とCompassの情報源の確認に対応','誤：文化的な違いが人間的価値を下げないという本文に反する','誤：批判的に問い直すべき人物像を集団全員の事実として扱う'],
 reason='S216の表紙・著者表示・著作権表示と第5章37–46頁を通読、41頁の全体を画像でも精読。S214のRole-playing全文と合わせ、全4肢・4解説を照合。文化事例を扱う指導で固定観念を強めないという学習領域を保ち、取得本文が直接扱うロールプレイでの検討を明示した。旧解説の全ての多視点学習に他参加者との討議が不可欠という一般化、未取得のクリティカル・インシデント法の普遍的定義を承認しない。2014年刊行書は著者の見解であり、欧州評議会の公式政策そのものと同一視しない。実証研究の効果を個別検証したものではない。')}
ps=[p.text for p in Document(b.DST).paragraphs];extra=[]
for k,v in items.items():
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and q[k]['stem'] in ps and a[ak]['ans']==str(v['key'])
 for field,olds,news in [('stem',[q[k]['stem']],[v['stem']]),('options',q[k]['opts'],v['opts']),('explanations',a[ak]['txt'],v['exps'])]:
  for i,(old,new) in enumerate(zip(olds,news)):
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=v['reason'],sources=v['sources'],applied=True,before_version='第151バッチ反映後',block_context=ak if field=='explanations' else k)
   if field=='options':c['stem_context']=v['stem']
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==v['key'] else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=v['key'],fixes_applied=True,sources=v['sources'],reason=v['reason'],option_verdicts=v['verdicts'],candidate_answers=[],stem_review='取得本文で扱うロールプレイと指導上の配慮に対象を明示し、全4肢を独立判定。未取得の技法の定義や効果は承認しない。',explanation_review='全4解説を本文の条件と対照。参加者の安全・情報の批判的な振り返り・一般化の限界を保ち、普遍的な必然性を追加しない。',unresolved='',multiple_correct_risk='なし：指定した資料の説明に合うのは独立正答のみ',no_correct_risk='なし：独立正答'+str(v['key']))
# Partial Barnga announcement is not a substitute for the unavailable manual.
v=d['Q_4_094'];assert v['status']=='要追加確認'
v.update(sources=['S215'],reason=v['reason']+' 第152バッチで開発者側の2006年紹介記事全文の該当節を取得したが、これは完全な実施規則ではない。目的の概略は記述されているものの、言語禁止・筆談・移動・異なるルール等の全主張は承認しない。',unresolved='紹介記事のみ取得。完全な実施・振り返りマニュアルは未取得。リンク先thiagi.com/barngaと旧archiveの候補は今回取得できず、全4肢・4解説の手順・目的・効果の根拠照合が未了。原稿は修正・承認せず要追加確認を維持。')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch152.json',extra),('decisions.json',d)]:(b.OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2]
def meta(name):
 raw=(root/name).read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
e=[dict(source_id='S214',url='https://www.coe.int/en/web/compass/using-compass-for-human-rights-education',title='Compass — Using Compass for human rights education',read_scope='再取得。Drama・Role-playing・Simulations節の全本文を連続して精読。全書・全ウェブページの通読ではない。',**meta('compass152.html')),dict(source_id='S215',url='https://thiagi.net/archive/www/pfp/IE4H/august2006.html',title='THIAGI GAMELETTER August 2006 — Barnga: 25th Anniversary Edition',read_scope='Game Announcementの見出しからOther Details節末までを全て精読。著者側の紹介記事であり、実施マニュアルではない。',limitations='Q_4_094は要追加確認のまま。全文取得した紹介記事を完全な原著マニュアルの代わりにしない。',**meta('thiagi152.html')),dict(source_id='S216',url='https://rm.coe.int/16808ce258',title='Developing intercultural competence through education',editors='Josef Huber and Christopher Reynolds',contributors=['Martyn Barrett','Michael Byram','Ildikó Lázár','Pascale Mompoint-Gaillard','Stavroula Philippou'],publisher='Council of Europe Publishing',year=2014,isbn='978-92-871-7745-2',pdf_pages=132,read_scope='PDF2–4頁の標題・著者・著作権・目次、第5章印刷37–46頁（PDF38–47頁）の全本文を通読。印刷41頁（PDF42頁）を全頁画像照合。英仏合冊全132頁精読ではない。',limitations='著者の見解であり公式政策と同一視しない。引用先の実証研究を個別取得した効果評価ではない。旧coe.int/t/dg4/.../Pestalozzi3.pdfはプログラム入口HTMLへ転送されるためPDFとして使用せず、公式rm.coe.intのPDFを別取得。',**meta('intercultural152b.pdf'))]
for x in e:x.update(retrieved='2026-10-18',full_source_redistributed=False)
(b.OUT/'evidence/batch152_sources.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('2 questions confirmed / 18 edits; Barnga remains unverified')
