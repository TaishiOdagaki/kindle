"""Two distinct meanings of integration, bounded by author texts."""
import json,html,hashlib
from pathlib import Path
import quiz_audit as qa
import v9_apply_batch1 as b
p=b.OUT;cs=json.loads((p/'changes.json').read_text());assert len(cs)==3417
d=json.loads((p/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
data=[
('Q_3_033',1,'S233',
'ベリー（1997）「Immigration, Acculturation, and Adaptation」が、非支配的集団の立場から説明する文化変容方略のうち、「統合」に合うものを一つ選べ。',
[
'自らの文化的アイデンティティや特徴を保つことを重視し、同時に他の集団との日常的な関わりや、より大きな社会への参加も求める。',
'自らの文化を保つ可能性や関心が乏しく、他の集団との関係にも関心が乏しい。文化の喪失や排除が背景にある場合も含む。',
'自らの文化的アイデンティティを保とうとはせず、他の文化の人々との日常的な関わりを求める。',
'自らの文化を保つことを重視し、他の集団との関わりを避けたいと考える。'],
[
'9頁の「統合」の説明に一致します。ただし10～11頁では、統合を自由に選び実現するには、支配的社会が文化的多様性に開かれ、双方が調整することも必要としています。本人の希望だけで参加機会が必ず保障されるという意味ではありません。',
'9～10頁の「周縁化」に対応する説明です。著者は、文化の強制的な喪失、排除や差別によってこの状態になる場合も挙げています。誰もが自由に選ぶ孤立の好みとしてだけ扱うことはできません。',
'9頁で「同化」と呼ばれる組合せです。文化的アイデンティティの保持を求めず、他の文化との関わりを求める点が、保持と参加の両方を求める統合と異なります。全ての人の文化的特徴が一度に完全消去されるという主張ではありません。',
'9頁の非支配的集団が選ぶ「分離」に対応します。10頁では、支配的社会から関係の分離を強制される場合を「隔離」と区別しています。本人が関わりを避けたいという志向と、社会から排除される条件を混同しないことが必要です。'],
'S233原論文9～12頁、図1、24～25頁本文を取得照合。自文化保持と他集団との接触・参加の2軸、選択と強制・排除の違いを明示。「統合が最も健康的」という普遍的評価は撤回し、相互調整・社会側の包摂条件を残す。著者の適応研究の総括を個々人の健康保証・因果効果とは扱わない。',
['正：保持と接触・参加の両方を求める','誤：両方が乏しい周縁化の説明','誤：保持を求めず接触を求める同化','誤：保持を求め接触を避ける分離']),
('Q_3_035',3,'S234',
'ベネット（2017）「Developmental Model of Intercultural Sensitivity」による異文化感受性発達モデル（DMIS）の説明に合うものを一つ選べ。',
[
'「受容」は、相違を認めるだけでは足りず、相手の価値観に全て同意し、その行動をどの場面でも実践することを意味する。',
'「防衛」では、異なる文化の存在や関連性をほとんど知覚できず、自文化と他文化を対比するカテゴリーも形成されていない。',
'否定・防衛・最小化を自文化中心的、受容・適応・統合を文化相対的な側に位置づける。ただし、段階を進むことは必然ではない。',
'最終の「統合」は、文化的な自己のあり方を一つに固定し、異なる文化的世界観の間を移動できなくなることを意味する。'],
[
'PDF4頁の受容の説明は、相違を認めることと同意することを区別しています。また、受容の段階では異なる文脈へ行動を容易に調整できるとは限りません。他文化の全価値観への同意や常時実践を要求する説明は合いません。',
'PDF3頁では、防衛は「自分たち／彼ら」という二分的な捉え方であり、他者は否定よりも明瞭に知覚される一方、固定的に捉えられやすいと説明されます。存在や関連性を知覚しにくいという否定の説明と区別します。',
'PDF3頁に示された6段階の位置づけと、進行が必然ではないという留保に対応します。PDF1頁の段階は連続体上の位置であり、切り離された状態ではないという説明にも注意が必要です。全員が必ず同じ速度で到達する自然法則として扱いません。',
'PDF5頁では、統合は異なる文化的世界観へ出入りする動きを自己の経験に含める状態として説明されます。自己を一つの文脈に固定して移動できなくなるという意味ではありません。これはDMIS内の概念であり、ベリーの文化変容方略の統合とは枠組みが異なります。'],
'S234提唱者の所属研究所が公開する2017年著者本文PDF1～7頁を取得照合、4～5頁画像確認。段階は連続体上の位置、進行は必然でない、受容は同意ではないことを明示。防衛の逆転型もあるため自文化優位だけを必要条件としない。統合を自己喪失やベリーの方略と同義にしない。1986原著・測定尺度全項目を取得したとはしない。',
['誤：受容を全同意・常時実践とする','誤：防衛を否定の知覚構造と取り違える','正：6段階の位置づけと非必然性','誤：統合を文脈間移動の不能とする'])]
extra=[]
for k,key,sid,stem,opts,exps,reason,verdicts in data:
 ak='A_'+k[2:];assert d[k]['status']=='要追加確認' and a[ak]['ans']==str(key)
 for field,olds,news in [('stem',[q[k]['stem']],[stem]),('options',q[k]['opts'],opts),('explanations',a[ak]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   kw={'paragraph_prefix':str(i+1)+'（'+('正' if i==key-1 else '誤')+'）'} if field=='explanations' else ({'stem_context':stem} if field=='options' else {})
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=[sid],applied=True,before_version='第172バッチ後',block_context=ak if field=='explanations' else k,**kw))
 d[k].update(status='確認済み',independent_answer=key,fixes_applied=True,sources=[sid],reason=reason,option_verdicts=verdicts,candidate_answers=[],stem_review='著者と対象本文を明示し、その枠組み内で独立に4肢を比較。個人の健康・段階を診断する問題とはしない。',explanation_review='設問・全4肢・全4解説を著者本文へ照合。理論内分類、自由選択の社会条件、段階の非必然性を保持。批判・後続実証の全原著の承認とは区別する。',unresolved='',multiple_correct_risk=f'なし：{key}のみ指定した枠組みの説明に整合',no_correct_risk=f'なし：{key}を著者本文に照合')
assert len(extra)==18
for n,obj in [('changes.json',cs+extra),('changes_batch173.json',extra),('decisions.json',d)]:(p/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
root=Path(__file__).resolve().parents[2];entries=[]
for sid,fn,url,scope in [
 ('S233','berry173.pdf','https://peda.net/jyu/ktk/educationalleadership/moemalm/efitic/s1itiaic/lectures/l1ita/l1ita/berry-pdf%3Afile/download/87dd958cb50d15350cc101aff1e0fb29ee3f7cdd/Berry.pdf','Berry1997原論文第三者公開スキャン30頁。印刷5～7・9～12・24～25頁本文、10頁図1と本文画像。保持／参加、自由選択の制約、双方の調整、適応との関連を総括する著者の留保。引用研究各原著は未取得。'),
 ('S234','bennett173.pdf','https://www.idrinstitute.org/wp-content/uploads/2019/02/DMIS-IDRI.pdf','Bennett2017著者本文8頁を著者研究所から取得。PDF1～7頁本文、4～5頁画像。連続体と6段階、非必然性、受容と同意、防衛の逆転型、適応と統合、測定と批判の記述。1986原著、引用原著、IDI全項目の独立検証ではない。')]:
 raw=(root/fn).read_bytes();entries.append(dict(source_id=sid,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),checked='2026-10-19',read_scope=scope,full_source_redistributed=False))
(p/'evidence/batch173_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
