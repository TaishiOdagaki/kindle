"""Barnga: primary implementation report, not a universal efficacy claim."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3381
d=json.loads((p/'decisions.json').read_text());k='Q_4_094';ak='A_4_094';assert d[k]['status']=='要追加確認'
_,q,a=qa.audit(str(b.DST));assert a[ak]['ans']=='4'
stem='異文化コミュニケーションを扱うバーンガ（Barnga）について、ニューハンプシャー大学Institute on Disabilityの2019年2月19日付実施報告に合う手順と振り返りの説明を一つ選べ。'
opts=[
'各卓が同じルールであることを全員に確認させ、他の卓へ移動せずに最後まで同じ相手と競技した。',
'特定の国のマナーを暗記するクイズを行い、振り返りでは文化や言語の違いを話題にしなかった。',
'ルールを学んだ後も、対戦中は口頭で互いのルールを説明し合い、違いを言葉で解決しながら進めた。',
'話さずにカードゲームを行い、勝者が別の卓へ移って対戦を続けた。後の振り返りで、言語や文化の違いと、違いに直面したときの感情について話し合った。']
exps=[
'報告では、対戦の途中で勝者が別の卓へ移り、異なる相手と対戦を続けています。何巡かの後で、自分たちと他の卓とではルールが違うのではないかと参加者が疑い始めたとあります。最初から同一ルールを確認し、卓も相手も固定したという説明とは合いません。',
'報告されているのはカードゲームと、その体験を振り返る活動です。振り返りでは言語・文化の違いや、それに直面する人の気持ちを扱っています。特定国の知識の暗記クイズだけを行い、違いを扱わなかったという説明ではありません。',
'報告では、ルールを学んだ後は話さずにゲームをし、別の卓に移った後も話さず対戦を続けています。対戦中に口頭でルールを説明し合う手順とは異なります。これは対戦中の制約であり、後の振り返りまで対話を禁じるという意味ではありません。',
'報告の手順と振り返りの内容に一致します。開発者側の2006年の紹介も、異なる解釈に気づき、その違いを理解・調整することをバーンガのねらいとして説明します。ただし、この実施報告は全参加者の感情が同じだったという測定結果でも、長期的な異文化適応力の向上を実証した研究でもありません。']
reason='S228実施機関UNHの2019年の一次実施報告本文全体と、S229開発者側Gameletter2006年8月のBarnga紹介全節を取得して照合。旧稿の筆談を含む言語使用の一律禁止、葛藤・心理ストレスの必然的生起、普遍的教育効果を取得資料だけで承認せず撤回。対戦中の無言と振り返りの対話を区別。同じバーンガ領域の具体的実施記録へ限定。原マニュアル全冊・統制研究は未取得。'
extra=[]
for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
 for i,(old,new) in enumerate(zip(olds,news)):
  kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==3 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
  extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S228','S229'],applied=True,before_version='第170バッチ後',block_context=ak if field=='explanations' else k,**kw))
assert len(extra)==9
d[k].update(status='確認済み',independent_answer=4,fixes_applied=True,sources=['S228','S229'],reason=reason,option_verdicts=['誤：同一ルール確認・卓と相手の固定は記録と異なる','誤：活動を暗記クイズとし振り返りの内容を否定','誤：対戦中の無言制約を口頭説明に逆転','正：無言の対戦・勝者移動と違いを扱う振り返り'],candidate_answers=[],stem_review='実施主体・報告日を指定し、その手順と振り返りの理解を問う。バーンガ全版の唯一手順や特定参加者感情の診断とはしない。',explanation_review='全4解説を一次実施報告の本文へ照合し、開発者側紹介の目的も区別して照合。筆談禁止・全員同一感情・長期的効果の主張は承認しない。',unresolved='',multiple_correct_risk='なし：4のみ対象の実施記録に一致',no_correct_risk='なし：4が手順・振り返りの記録と一致')
for n,obj in [('changes.json',cs+extra),('changes_batch171.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [('S228','unh171.html','https://iod.unh.edu/blog/2019/02/barnga-simulation-game-cultural-clashes','2019-02-19付UNH Institute on Disabilityの実施報告本文全体。記録された手順と振り返りであり統制研究ではない。リンク先Michigan旧URLは404、マニュアル全冊未取得。'),('S229','thiagi171.html','https://thiagi.net/archive/www/pfp/IE4H/august2006.html','2006年8月Gameletterの編集者名とGame Announcement Barnga:25th Anniversary Edition全節。目的、改訂版・振り返りガイドの存在。ゲーム原マニュアル本文自体の取得とは区別。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-18',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch171_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
