"""One-time historical procedure review; preserve two unverified questions."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1963
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));k='Q_4_032';assert d[k]['status']=='要追加確認' and a['A_4_032']['ans']=='4'
stem='Richards（2006）『Communicative Language Teaching Today』7頁が示す、典型的なオーディオリンガルの授業手順に対応する説明を一つ選びなさい。歴史的な授業の記述を問うのであり、現在の全授業への推奨ではない。'
opts=[
'最初のモデル対話の反復段階から学習者が教科書を参照し、対話の各行を聞いて繰り返す活動を行わない。',
'対話や型練習を始める前の長い文法規則の説明を授業の中心に置き、説明は最小限にするという制限を設けない。',
'モデル対話の反復段階では、発音や文法の誤りを直接その場で訂正することを避ける。',
'モデル対話を聞いて各行を繰り返し、対話を少しずつ暗記し、語句を替えた対話や主要構造の型練習へ進む。']
exps=[
'同頁の手順1は、対話を聞いて各行を個別・一斉に反復し、この段階では教科書を参照しないとしています。後続の手順4で教科書の参照や読み書き等の活動を認めることとは区別します。',
'同頁の手順3は、対話から主要な構造を選んで型練習を行い、その時点で文法説明を加える場合も最小限にするとしています。先に長い説明を中心に据えるという肢とは一致しません。',
'同頁の手順1は、発音や文法の誤りへの訂正を直接・即時と記述しています。設問はその歴史的な手順を問うもので、現在のあらゆる活動で発話を即座に遮るべきという推奨ではありません。',
'同頁の手順1〜3に対応します。モデルの聴取と各行の反復、段階的な暗記、語句を替えた対話、主要構造の型練習という流れです。全教授法がこの順序を守るという意味ではありません。']
reason='S144著者公開冊子印刷7頁（PDF11頁）の全五手順を本文・画像照合。歴史的な典型授業の著者記述に限定し、母語使用の全面排除や全指導への即時訂正の推奨を撤回。引用元Richards/Rodgers2001著書全体の取得とは扱わない。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_4_032']['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S144'],applied=True,before_version='第87バッチ反映後の累積作業稿',block_context='A_4_032' if field=='explanations' else k)
  if field=='options':e['stem_context']=stem
  if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==3 else '誤')+'）'
  extra.append(e)
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S144'],reason=reason,option_verdicts=['誤：最初の反復段階の教科書参照条件と反復の有無が逆','誤：手順3の説明の時点・最小限という条件と逆','誤：手順1の直接・即時訂正という歴史記述と逆','正：手順1〜3の流れに対応'],stem_review='著者・冊子・頁と歴史的説明であることを指定し全4肢を独立判定。',explanation_review='S144印刷7頁の全五手順を本文と150dpi画像で読み、全4解説と照合。2001年共著の全文取得・現代の効果検証とはしない。',unresolved='',multiple_correct_risk='なし：指定手順に対応するのは4のみ',no_correct_risk='なし：独立正答4')
# A publisher page and search citations are not original-body verification.
for key in ['Q_2_013','Q_2_018']:
 e=d[key];assert e['status']=='要追加確認'
 e['unresolved']+=' 2026-10-15追加取得試行：Canale/Swain1980の出版社ページは有料アクセス表示、UEfAP公開候補は404、ResearchGate本文リンクは404。検索引用・他論文の要約だけで原著本文取得と扱わず未確認を維持。'
assert len(extra)==9
for name,obj in [('changes.json',c+extra),('changes_batch88.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('1 full review /9 edits;2 original-source access attempts not approved')
