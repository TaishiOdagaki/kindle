"""One-time CC BY 4.0 / public-video follow-up, preserving prior decisions."""
import json,html,gzip,re,xml.etree.ElementTree as E
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==2312
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));qb,_=qa.blocks(qa.load(str(b.DST))[0])
items={
'Q_4_121':(3,['S162'],'有効なCC BY 4.0（表示4.0国際）で提供された教材を改変して共有する。パブリックドメインや法定の例外ではなく、このライセンス上の権利に基づく利用について、適切な説明を一つ選べ。',[
'このライセンスでは非営利目的の利用だけが認められ、営利目的での共有は禁止される。',
'このライセンスでは元の教材をそのまま共有できるだけで、翻案した教材の作成・共有は認められない。',
'提供されたクレジット情報等を保持し、ライセンス情報や改変の表示など、共有に適用される条件を満たす必要がある。',
'原作者の氏名を示せば、ライセンスに関する表示や改変したことの表示など、他の条件を省略してよい。'],[
'CC BY 4.0の第2条a項1号は、非営利目的だけに限らず、複製・共有や翻案物の作成・共有を許諾します。非営利限定の別ライセンスと混同しないようにします。',
'第2条a項1号Bは翻案物の作成・複製・共有を認めています。改変禁止とする肢は誤りです。ただし、共有には第3条の条件が適用され、あらゆる権利が許諾されるという意味ではありません。',
'第3条a項1号は、提供された作者等の表示・著作権表示・ライセンスへの言及・免責表示・実行可能な範囲の資料へのリンク等の保持、改変した旨と従前の改変表示の保持、ライセンスの適用とその本文又はURI・リンクの提供を定めています。表示方法は媒体等に応じ合理的に満たせます。人格権・プライバシー等まで一律に許諾する規定ではありません。',
'作者名だけで第3条の条件をすべて満たすとはいえません。共有時のライセンス情報や改変の表示も確認します。第4.0版の条件を問う本問から、他のCCライセンスやすべてのOERへ条件を一般化しません。'],[
'誤：営利目的の利用を一律禁止していない（第2条a項1号）',
'誤：翻案物の作成・共有も許諾の対象（第2条a項1号B）',
'正：提供情報の保持とライセンス・改変表示等の条件に対応（第3条a項）',
'誤：作者名のみで他の条件を省略できない（第3条a項1号）']),
'Q_4_127':(2,['S26'],'教員が誰でも視聴できる文法解説動画を制作・配信する。各素材は公表済みで創作性があり、著作権の保護期間内とする。選択肢2以外では、著作権者からの許諾・利用許諾も、引用その他の権利制限が適用される事情もない。著作権について適切な対応を一つ選べ。',[
'他人の楽曲を動画のBGMとして収録し、その動画を公衆送信した。',
'自分の文法解説と明確に区別して小説の短い一節を引用し、公正な慣行と引用目的上正当な範囲の要件を満たし、出所・著者名も適切に示した。',
'他人の教科書にある創作的な会話文をそのまま朗読・録音し、動画に収録して公衆送信した。',
'他人の創作的なイラストを、視聴者の関心を引くために複製し、動画のサムネイル画像として公衆送信した。'],[
'設問では許諾や権利制限による根拠がないため、他人の楽曲の収録という複製と公衆送信は、第21条・第23条の権利に抵触します。本問は楽曲の著作権を対象とし、市販音源の権利処理まで一括して判断するものではありません。',
'第32条第1項は、公表された著作物の引用について、公正な慣行に合致し、引用目的上正当な範囲で行うことを求めます。本肢はこれらを満たすと明示し、第48条の出所・著作者名の表示にも対応しています。短いことや著者名の表示だけで引用の全要件を満たすとは扱いません。',
'第2条第1項第15号の複製には録音も含まれます。本肢の創作的な会話文の録音・収録と公衆送信には、第21条・第23条に関する根拠が必要です。第24条の公の口述と、録音を作成して配信する行為を混同しません。',
'本肢は保護されるイラストを複製・公衆送信し、許諾や権利制限の根拠もないという設問の条件から不適切です。公開動画や無許諾の画像利用が、別の事情でも常に侵害になると一般化する説明ではありません。'],[
'誤：設問条件では楽曲の複製・公衆送信の根拠がない（第21・23条）',
'正：公表済み・公正慣行・目的上正当な範囲と適切な出所表示を明示（第32・48条）',
'誤：録音・収録及び配信の権利処理の根拠がない（第2条第1項第15号・第21・23条）',
'誤：設問条件ではイラストの複製・公衆送信の根拠がない（第21・23条）'])}
extra=[]
for k,(ans,ss,stem,opts,exps,verdicts) in items.items():
 assert d[k]['status']=='修正必要' and int(a['A_'+k[2:]]['ans'])==ans
 reason=('公式CC BY 4.0リーガルコード全文を取得し第2・3条を中心に照合。作者名だけで足りるという説明を撤回し、他ライセンス・OER一般・人格権等への過度な一般化を避けた。' if k=='Q_4_121' else '保存済みe-Gov本則第2条第1項第15号・第21・23・24・32・48条を照合。引用要件と出所表示を区別し、無許諾公開利用は常に違法という一般化、市販音源の実在事実、口述と録音配信の混同を避けた。')
 parts=[html.unescape(x['t']) for x in qb[k][1:-1] if not x['ind']];assert html.unescape(q[k]['stem'])==' '.join(parts)
 for field,olds,news in [('stem',[parts[0]],[stem]),('options',q[k]['opts'],opts),('explanations',a['A_'+k[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   e=dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=ss,applied=True,before_version='第102バッチ反映後の保存済み稿',block_context='A_'+k[2:] if field=='explanations' else k)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
   if field=='stem':
    for t in parts[1:]:extra.append(dict(e,field='stem_continuation',before=t,after='',remove_paragraph=True,reason='旧設問継続段落を明示削除。'+reason))
 d[k].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=ss,reason=reason,option_verdicts=verdicts,stem_review='設問に対象ライセンス又は保護・許諾・例外の条件を明記し、全4肢を根拠本文から独立判定。既存正答番号は判定の前提としない。',explanation_review='全4解説を根拠本文に照合。CCでは第2条の許諾範囲と他の権利の留保、第3条の条件を区別。引用では第32条の実体要件と第48条の出所表示を区別し、短さだけで成立を承認しない。',unresolved='',multiple_correct_risk='なし：指定した利用根拠と条件に対応する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
assert len(extra)==18
for name,obj in [('changes.json',c+extra),('changes_batch103.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
r=E.fromstring(gzip.decompress((b.OUT/'evidence/egov_batch101.xml.gz').read_bytes()))
(b.OUT/'evidence/egov_batch103_excerpts.txt').write_text('第101バッチ保存済み原応答の追加照合（新規取得ではない）。\n\n'+'\n\n'.join(re.sub(r'\s+',' ',''.join(e.itertext())).strip() for e in r.findall('.//MainProvision//Article') if e.get('Num') in ['2','21','23','24','32','48'])+'\n')
print('2 full reviews /18 edits')
