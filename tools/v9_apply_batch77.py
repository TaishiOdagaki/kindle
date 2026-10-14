"""One-time continuation of the JF2017 full-guide review."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1577
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST))
items={
'Q_1_041':(3,'国際交流基金の2017年版ガイドブックにおける、CEFR Can-doとJF Can-doの関係の説明として、最も適切なものを一つ選びなさい。',[
'CEFR Can-doとJF Can-doは、どちらも文法項目や漢字を何個暗記したかという知識量だけを記述する。',
'CEFR Can-doは日本語だけの使用場面を記述し、JF Can-doは日本語の使用場面を一切想定しない。',
'CEFR Can-doの記述は汎言語的で抽象性・包括性が高く、JF Can-doは日本語の使用場面を想定した具体的な言語活動を例示する。',
'JF Can-doはあらゆる日本語の言語活動を網羅しているので、各教育現場に合ったCan-doを新たに作る必要はない。'],[
'ガイドブック14頁は、知識項目の個数とは異なる捉え方として、できる言語活動や持っている言語能力の例を示しています。知識量だけの記述ではありません。',
'ガイドブック19頁の説明と逆です。CEFR Can-doは汎言語的で、JF Can-doは日本語の使用場面を想定しています。',
'ガイドブック19頁の両者の役割の説明に対応します。ここでは同書の説明を問い、別の分類名称をこの区別と無条件に同一視しません。',
'ガイドブック18頁は、Can-doは例示であり、すべてを網羅していないと説明します。各現場に合ったCan-doを作る必要を否定する記述は逆です。']),
'Q_4_050':(4,'国際交流基金の2017年版ガイドブックで説明されるCan-doと、その利用上の留意点について、最も適切なものを一つ選びなさい。',[
'Can-doは、知っている文法項目や漢字の個数だけで熟達度を示す文である。',
'Can-doを設定すれば、目標達成に必要な語彙や文法項目などの言語材料を準備する必要はない。',
'一つのCan-doを見れば十分なので、異なるレベルやカテゴリーの記述を見比べてはならない。',
'Can-doは、ある熟達段階でできる言語活動や持っている言語能力を例示するものであり、現場で必要な言語材料なども別に準備する。'],[
'ガイドブック14頁は、文法や単語・漢字の知識量とは異なる捉え方として、できる活動や能力の例を示しています。個数だけで熟達度を示す文という説明は誤りです。',
'ガイドブック18頁は、実際の教育活動に必要な語彙や文法項目などの言語材料の準備を求めています。Can-doを設定することと、その準備が不要になることは同じではありません。',
'ガイドブック18頁は、複数のCan-doをレベルやカテゴリーをまたいで見比べることを重視しています。見比べてはならないという記述は逆です。',
'ガイドブック14・18頁の説明に対応します。Can-doによる例示と、各現場の目的・ニーズに応じた言語材料や記述されていない能力の検討を併せて行います。']),
'Q_O_009':(4,'国際交流基金の2017年版ガイドブックに沿って、Can-doを使った「学習目標一覧」と「自己評価チェックリスト」を作る意義として最も適切なものを一つ選びなさい。',[
'学習内容や評価内容を学習者から隠し、教師だけが知るためである。',
'目標一覧を作るだけで、学習者による達成度の振り返りは実施しなくてよくなる。',
'Can-doだけで目標設定や評価の準備が完結するので、語彙や文法項目などの言語材料を準備しなくてよい。',
'学習内容や評価内容をイメージしやすくし、教師と学習者が共有しやすくする。'],[
'ガイドブック49頁は、教師と学習者の共有を利点として示しています。学習者から隠すためという説明は逆です。',
'ガイドブック18頁は、Can-doを自己評価チェックリストに利用し、現段階や授業後に何ができるかを見る方法を示しています。一覧の作成だけで本人の振り返りが不要になるとはしません。',
'ガイドブック18頁は、Can-doだけでは目標設定や評価は行えず、必要な言語材料などを準備すると明記しています。準備が完結するという説明は誤りです。',
'ガイドブック49頁の説明に対応します。目標を意識し、学習・評価内容を共有するための利用であり、記述形式を変えるだけで実際の能力向上が保証されるという意味ではありません。'])}
extra=[]
for key,(ans,stem,opts,exps) in items.items():
 assert int(a['A_'+key[2:]]['ans'])==ans
 reason='JF2017公式ガイド全文の14・18・19・49頁へ限定。出典未照合の分類二分法や大まかなレベル対応を、CEFR/JFの役割、Can-doの例示性と利用上の準備・共有へ改訂。'
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   old=html.unescape(old)
   if old==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=old,after=new,reason=reason,sources=['S141'],applied=True,before_version='第76バッチ反映後の累積作業稿',block_context='A_'+key[2:] if field=='explanations' else key)
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i==ans-1 else '誤')+'）'
   extra.append(e)
 verdicts={
 'Q_1_041':['誤：知識量だけに限定','誤：汎言語的記述と日本語使用場面の対応を逆転','正：同書19頁の両者の役割に対応','誤：例示を網羅と取り違える'],
 'Q_4_050':['誤：知識項目の個数だけに限定','誤：必要な言語材料の準備を排除','誤：複数記述の比較を禁止','正：例示と現場での準備を併せる'],
 'Q_O_009':['誤：共有を秘匿と取り違える','誤：一覧作成だけで本人の振り返り不要とはならない','誤：Can-doだけでは目標設定や評価の準備は完結しない','正：学習・評価内容の具体化と共有に対応']}
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S141'],option_verdicts=verdicts[key],reason=reason,stem_review='2017年版ガイドを明示。全4肢を同じ資料の枠組みと手続きへ照合し、独立正答を確定。',explanation_review='全92頁公式PDFを取得。印刷14・18・19・49頁（PDF18・22・23・53頁）の本文と画像を照合。熟達度Can-do/課題Can-doの二分法とCEFR/JFの区別を無条件に同一視せず、学術論文読解と学会論争の一括レベル判定も承認範囲から外す。Can-doがすべての能力を網羅する、語彙文法の準備や評価が不要になる、形式だけで能力向上が保証されるという推論を認めない。',unresolved='',multiple_correct_risk='なし：設問に対応するのは'+str(ans)+'のみ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch77.json',extra),('decisions.json',d)]: (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
