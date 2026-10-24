import json,hashlib
from pathlib import Path
from collections import Counter
from audit_2027_epub import read_epub
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit'
D={
'Q_1_040':(1,'S141',[5,6,25,26,49],['相互理解と課題遂行・異文化理解の両能力','拘束力のある全国統制とは説明しない','体験記録と成果も構成要素','共有できるという説明と逆']),
'Q_1_041':(3,'S141',[14,18,19],['活動能力の例示で知識量だけでない','汎言語的と日本語場面の関係が逆','汎言語的なCEFRと具体場面のJFの区別','例示であり網羅ではない']),
'Q_4_050':(4,'S141',[14,18],['知識項目を網羅する一覧でない','言語材料準備は必要','複数を見比べるという注意と逆','比較し現場に応じ材料を準備']),
'Q_4_055':(4,'S141',[25,26],['振り返りを誤排除','三構成要素のうち二つを誤排除','学習者本人の選定と振り返りを誤排除','評価表・体験・成果を振り返りへ利用']),
'Q_O_009':(4,'S141',[18,49],['学習者との共有という利点と逆','本人の自己評価は不要にならない','言語材料の準備は不要にならない','目標・評価内容を共有しやすくする']),
'Q_M_031':(1,'S141',[26,49],['本人ができることを参照し自己評価','教師のみの記入は本人の自己評価でない','他者順位だけでは項目達成を振り返らない','収集だけでは自己評価にならない']),
'Q_2_022':(3,'S245',[311,312,313,317],['仲間意識はポジティブ','非言語を含み敬語形式だけで決まらない','自由への干渉を抑えるネガティブ','自己像否定はポジティブの定義でない']),
'Q_2_026':(4,'S245',[312,313,314],['欲求の定義は合うが主な脅威の分類が違う','行動自由の欲求はネガティブ','承認欲求はポジティブ','依頼は将来行為に圧力をかけ自由を脅かす']),
'Q_2_027':(4,'S245',[316,317],['仲間意識はポジティブ','緊急性等の文脈を除外した常時最高判定は不可','図で別枝、慣習的間接性はオンレコードもある','仲間や友人として欲求共有を示す方策']),
'Q_4_106':(3,'S245',[311,312,317,319,320,321],['自己像の承認と行動自由の混同','仲間と欲求共有を誤排除','距離・力・負担と文化状況個人の評価差','国籍だけで方策の受取りは確定しない']),
'Q_O_057':(4,'S245',[313,316,317],['明示依頼にも配慮を添えられる','明示された負担配慮を仲間意識だけに誤限定','依頼の存在や負担検討は消えない','干渉の謝罪緩和という観点を適用']),
'Q_O_058':(2,'S245',[316,319,320,321],['形式だけで負担を固定できない','直接行為の条件に緊急性等を含む','直接的で配慮を添えない方策も図にある','間接形式だけで成功を保証できない']),
'Q_O_059':(2,'S245',[313,317,319,320,321],['距離力関係の評価を誤排除','三要因と文脈評価をケース比較へ適用','謝罪緩和慣習間接性は扱われる','依頼は聞き手への脅威の例に含まれる']),
'Q_O_060':(4,'S245',[311,312,317,320,321],['具体的内容の文化差を著者は認める','フェイスは国籍別性格でなく欲求','理論的分類から実際の好意的反応は未確定','枠組みと文化状況個人差および実際の受取りを区別']),
}
rows=json.loads((O/'ledger_500.json').read_text());_,_,qs,_,_=read_epub(O/'working/2027_independent_working.epub');qmap={q['id']:q for q in qs}
for r in rows:
 if r['id'] not in D:continue
 key,src,pages,rs=D[r['id']];assert not r['reviewed_this_pass'];assert key==qmap[r['id']]['answer']
 r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=[src],printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(rs,1)],all_four_explanations_reviewed=True,explanation_finding='設問・四肢・四解説とケース12本文を再読し、原資料のページ画像で分類・条件・制約を対照。追加修正不要。',multiple_correct=False,no_correct=False,manuscript_change_required=False,scope='指定ガイドブックまたはBrown/Levinson著者本文の再録を確認。理論への批判文献全体や個々の指導効果を検証した意味ではない。')
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
s=json.loads((O/'source_manifest.json').read_text());L=R.parent/'sources'
for id,url,pages in [('S141','https://www.jfstandard.jpf.go.jp/pdf/limited/3_JFS_guidebook.pdf',[5,6,14,18,19,25,26,49]),('S245','https://pure.mpg.de/rest/items/item_64421/component/file_2225570/content',list(range(311,322)))]:
 s.append(dict(id=id,url=url,retrieved='prior checkpoint local PDF; fresh image reading 2026-10-24',sha256=hashlib.sha256((L/f'{id}.pdf').read_bytes()).hexdigest(),printed_pages_read=pages,printed_images_read=pages,scope='S141本文は文字抽出が乱れるため全指定頁を画像精読。S245著者再録本文311〜321頁を画像精読。編集者の読書課題を著者本文の根拠にしない。'))
(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');p=json.loads((O/'PROGRESS.json').read_text());n=sum(r['reviewed_this_pass'] for r in rows);p.update(freshly_reviewed=n,remaining=500-n,status_counts=dict(Counter(r['status'] for r in rows)),latest_batch=10);(O/'PROGRESS.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');print(n,500-n)
