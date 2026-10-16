"""One-time review of three easy-Japanese questions against 2020 official guide."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
cs=json.loads((b.OUT/'changes.json').read_text());assert len(cs)==2664
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
def review(k,stem,opts,exps,key,reason,verdicts):
 assert d[k]['status']!='確認済み' and a['A_'+k[2:]]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   c=dict(id=k,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S189'],applied=True,before_version='第121バッチ反映後',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':c['stem_context']=stem
   if field=='explanations':c['paragraph_prefix']=str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'
   extra.append(c)
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=['S189'],reason=reason,option_verdicts=verdicts,stem_review='2020年8月の出入国在留管理庁・文化庁ガイドライン印刷3・5〜10頁の本文と画像に設問・全4肢を独立照合。書き言葉中心の提案と読み手に応じた調節を範囲条件とする。',explanation_review='全4解説を同本文に照合。旧試験の級への一律限定、未照合の語源分類・原著や効果の一般化を承認しない。具体的作成提案と効果の保証を区別。',unresolved='',multiple_correct_risk='なし：独立正答'+str(key)+'のみ適切',no_correct_risk='なし：独立正答'+str(key))
prefix='出入国在留管理庁・文化庁の2020年版「在留支援のためのやさしい日本語ガイドライン」に基づき、'
k='Q_1_005';opts=q[k]['opts'].copy()
opts[1]='書き換えでは、元の文章の一言一句を必ずそのまま対応させ、伝える情報の取捨選択や、不足する情報の補足を行ってはならない。'
opts[3]='読みやすさよりも敬意の高さを優先し、文末に尊敬語や謙譲語を多用することが、このガイドラインの作成方針である。'
review(k,prefix+'書き言葉の作成について最も適切なものを一つ選びなさい。',opts,[
'ガイドラインは、難しい言葉を対象者に合わせてわかりやすくし、外来語にも注意するよう求めています。原語と意味や発音が異なる場合もあり、日常的な和製英語ならわかりやすいと一律に置き換える方針ではありません。',
'必要な情報に絞る一方、不足している情報は補うという提案です。元の文の一言一句への対応を必須とする肢とは異なります。意味や必要な条件を落としてよいということでもありません。',
'同書は一文で伝える内容を一つにして短くし、文末を「です」「ます」に統一するという作成上のポイントを示しています。ただし、読み手の言語背景や日本語能力に応じて柔軟に調節することも求め、厳密な一律基準は設けていません。',
'このガイドラインでは、尊敬語・謙譲語ではなく丁寧語を使い、文末を「です」「ます」にすることを示しています。敬意の高さを理由に複雑な敬語を多用する方針とは合いません。'],3,'2020公式ガイドライン印刷5〜10頁を本文・画像照合。正答の短文・ですますは同資料の提案として維持し全場面の絶対規則にしない。未取得の結論先置・オノマトペ規則を根拠にせず、情報整理と敬語という取得本文に明示された誤答へ改訂。和製英語の一律推奨を認めない。',['誤：和製英語への一律置換を基本とする','誤：情報の取捨選択・補足を禁じる','正：同資料の短文・文末統一の提案に対応','誤：尊敬語・謙譲語の多用を方針とする'])
k='Q_1_018';opts=q[k]['opts'].copy()
opts[0]='一文で伝える内容を一つにして短くし、難しい言葉を読み手に合わせてわかりやすくする。漢字の量やふりがなにも配慮し、必要な重要語は説明を添えて残すことがある。'
opts[1]='このガイドラインは災害発生時の緊急情報だけを対象としており、平時の行政のお知らせや学校・企業での情報発信は想定していない。'
opts[2]='外来語なら外国人全員になじみがあるため、原語との意味や発音の違いに注意せず、難しい言葉をできるだけ外来語に換えることを勧めている。'
review(k,prefix+'読み手への配慮と表現の工夫として最も適切なものを一つ選びなさい。',opts,[
'一文で伝える内容を絞ること、対象者に応じた語彙、漢字の量とふりがなへの配慮が示されています。知っておくとよい災害用語や日常の重要語は、説明を添えて残す提案もあります。特定の試験の級に全語彙・文法を一律に制限する説明ではありません。',
'同書は国や地方公共団体のお知らせを中心に、学校や企業での活用も想定しています。災害時だけを対象とし、平時の情報発信を対象外とする説明ではありません。',
'外来語には原語と意味や発音が異なるものもあると注意を促しています。バス・ガス・テレビのような語も挙げており、外来語を無条件に多用することとも、すべての外来語を使用禁止にすることとも異なります。',
'同書は二重否定を避け、受身形や使役表現もできる限り使わないよう示しています。行動の主体などをわかりやすくするための提案であり、多用して複雑にする肢は合いません。意味の正確さを犠牲にして、あらゆる文を機械的に能動文へ直す趣旨ではありません。'],1,'2020公式ガイドライン印刷5〜10頁を本文・画像照合。旧3〜4級/N4〜N5相当へ全語彙文法を限定する説明を撤回し、同書が厳密な基準を置かず対象者に応じて調節すると明記する点へ整合。未照合の和製英語事例分類や成立史ではなく、当該文書の用途と明示的な表現提案に限定。重要語を残し説明を添える点、外来語・受身等の条件を保持。',['正：短文・対象者別語彙・ふりがな・重要語説明に対応','誤：行政・学校・企業等の平時用途を排除','誤：外来語の意味・発音の違いへの注意を排除','誤：二重否定・受身・使役の多用を勧める'])
k='Q_1_021';opts=q[k]['opts'].copy()
opts[2]='外国人住民への情報提供では、多言語による翻訳・通訳とやさしい日本語を、内容や相手に応じて使い分ける。イラスト等も活用し、伝わるかどうかを確かめる。'
opts[3]='やさしい日本語の文案は担当職員だけで完成させ、日本語教師や対象となる外国人にわかりやすさを確認してもらう工程は設けない。'
review(k,prefix+'外国人住民へ情報を伝える取組として最も適切なものを一つ選びなさい。',opts,[
'同書は、イラスト・写真・図・記号を使って視覚的にわかりやすくする提案をしています。一切使うべきでないという肢は合いません。ただし、どの記号でも誰にでも自動的に通じると保証するものではありません。',
'同書は多言語での翻訳・通訳に加え、やさしい日本語を活用することを示しています。英語への翻訳だけに情報支援を限定し、日本語や他の言語を除く説明とは異なります。',
'やさしい日本語と多言語の資料を内容に応じて使い分けること、視覚的な補助や、読み手に伝わるかの確認が示されています。やさしい日本語だけで全員・全場面の理解を保証したり、必要な翻訳・通訳を廃止したりする説明ではありません。',
'同書の作成手順の最後は、日本語教師や外国人にわかりやすさや伝わり方を確認してもらう工程です。職員だけで完成とし、その確認を設けない方針とは一致しません。読み手の背景や能力に応じる柔軟な調節も必要です。'],3,'2020公式ガイドライン印刷3・5〜10頁を本文・画像照合。多言語とやさしい日本語の使い分け、視覚支援、相手の確認を公的提案として説明し、全外国人・全障害種別に同じ配慮が常に有効という一般化を除去。JIS/国際規格の個別仕様や未取得の実証効果は承認せず、取得本文に明示された作成手順を問う。',['誤：視覚的補助を一切排除','誤：英語翻訳だけに限定し他言語・日本語支援を除外','正：内容・相手別の使い分けと補助・確認に対応','誤：作成の最終工程である対象者等の確認を除外'])
assert len(extra)==22,len(extra)
for name,obj in [('changes.json',cs+extra),('changes_batch122.json',extra),('decisions.json',d)]:(b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];raw=(root/'easy.pdf').read_bytes()
(b.OUT/'evidence/batch122_sources.json').write_text(json.dumps([dict(source_id='S189',url='https://www.mext.go.jp/a_menu/nihongo_kyoiku/kyoiku/pdf/92484001_01.pdf',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),retrieved='2026-10-16',body_read_scope='2020-08 official guideline printed3 and5-10/PDF4 and6-11, full text+images; printed4 additional text only, statistics primary studies and linked tools not approved',full_source_redistributed=False)],ensure_ascii=False,indent=2)+'\n')
print('3 questions/22 edits')
