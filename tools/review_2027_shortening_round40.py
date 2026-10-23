import json,csv,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/round40'
B={q['id']:q for q in json.loads((R/'publishing/2027/round37_baseline/corpus_500.json').read_text())}
M={q['id']:q for q in json.loads((R/'audit/v9/academic_master_500_20261022.json').read_text())['questions']}
import sys
sys.path.insert(0,str(R/'tools'));from audit_2027_epub import read_epub
_,_,qs,_,qa=read_epub(O/'2027_review_manuscript.epub');N={q['id']:q for q in qs}
reasons={
'Q_1_024':'二学科の対象と言語、学校設置の目的を保持。学科と対象の誤対応は生じない。',
'Q_1_029':'設置日・設置先・四審議会等の統合と国語分科会の事務を保持。詳細な四名称は解説にある。',
'Q_2_009':'言語的少数民族に属する者という対象を保持。条文全体の逐語引用ではなく、自己の言語の使用権を問う設問内の要約。行政言語の義務へ拡張しない解説も維持。',
'Q_2_012':'必要に応じた意味の説明を正答にも復元した。',
'Q_2_023':'参るとご覧になるの分類および負担・場面への配慮を保持。動作の主体と待遇の対象は設問と解説で明示。',
'Q_2_025':'「行為者など」「自分側の行為など」と、話や文章の相手という限定を復元済み。',
'Q_3_004':'食後払いの既有知識と食前払いの文章との不一致、語句の理解という条件を保持。国民性への一般化はしていない。',
'Q_3_011':'感覚登録器から選ばれた情報という選択過程を復元済み。',
'Q_3_017':'同じ学習者・特定の助詞・同じ意味文脈・複数年の観察を保持。使用歴15年の削除は永久的化石化の確定を避ける設問条件を変えない。',
'Q_3_021':'仲間の有能さが学習者に対する比較であることを復元した。',
'Q_3_039':'二つの将来の自己と現在の学習経験を保持。教師等の環境要素も残り、正答の構成要素は欠けない。',
'Q_4_072':'安定化の観察と永久性の判断を区別する条件を保持。単回の正用・誤用で確定しない全解説も維持。',
'Q_4_089':'問い・結論・調査の出所方法対象と根拠／考察の区別を保持。接続語だけの置換を十分としない。',
'Q_4_094':'無言の対戦・勝者の卓移動・振り返りの順序を保持。複数回の移動は解説で確認できる。普遍的な効果や感情は断定しない。',
'Q_4_125':'引用の対象と公正な慣行・目的上正当な範囲・複製引用時の出所表示を保持。設問が第32条第1項を指定し、解説が第48条の方法・程度と著作者名の例外を示す。',
'Q_5_015':'見る／切るの分類と実際のない形が一致。切るの一般的規則の説明を省いても、設問で指定された対比は維持される。',
'Q_5_027':'音の高低という内容は保持し、設問を日本語発音教材の範囲へ限定した。',
'Q_5_028':'英語seaとの違い、sheとの近似と円唇化しすぎない注意を保持。促音欠落や有声化の誤答との区別も一意。',
'Q_5_061':'様態の一用法であることを復元し、予測だけの定義という誤読を防いだ。',
'Q_5_079':'行為を妨げられたくない欲求と一部の他者に欲求を望ましく思われたい欲求を保持。名称の逆転はない。',
'Q_5_084':'格率衝突・協調拒否・欺きではないという条件と、含意が生じうるという可能性を保持。全ての不遵守への必然的効果ではない。',
'Q_5_092':'有限容量、他条件一定、側面間の遂行低下の可能性を保持。複雑さ等の同時向上が不可能とはしていない。',
'Q_5_100':'依頼の聞き手ネガティブ、謝罪の話し手ポジティブという対応を保持。設問・解説とも原著の分類内に限定され、排他的な唯一の効果とはしていない。',
'Q_5_101':'応答が記録された問いと未記録の問いを区別し、協力姿勢全体を断定しない条件を保持。',
'Q_O_030':'利用目的・必要な許可・保管・共通基準・複数の教師の再確認をすべて保持。記録だけで妥当性が保証されるとはしていない。',
'Q_O_031':'過去の経験も表すという可能性と文脈確認を保持。ケースでの来日前という理由だけの誤用断定を避ける。',
'Q_O_063':'ケース本文で双方が示した意思決定方法の相違に対応。多数決の文言をケース実文で再確認し、国籍を原因としない。',
'Q_M_002':'設問自体に公式紹介と2026-10-20確認が明記され、2027年事業の全対象国・全研修を断定する文ではない。対象・約6か月・初級から中級は保持。',
'Q_M_007':'2014年記事という条件、言語的支援・社会との橋渡し、専門家助言の正確な通訳を保持。通訳者が法的助言を代行するとはしない。',
'Q_M_032':'実施後の振り返り・配分見直し・将来の改善を保持。成果向上の必然性は全解説で否定。',
'Q_M_055':'許可・恩恵についての事実または気持ちという条件を復元した。',
'Q_MO_005':'語彙・聴解の実態、背景知識と音声中の語認識の双方を保持。特定の方法による一律改善は保証していない。'}
assert len(reasons)==32
rows=[]
for id,reason in reasons.items():
 q=N[id];k=q['answer']-1
 rows.append(dict(id=id,original_choice=M[id]['options'][k],baseline_choice=B[id]['options'][k],current_choice=q['options'][k],answer=q['answer'],reason=reason,decision='restored_canonical_qualification' if q['options'][k]==M[id]['options'][k] else 'retain_contextually_equivalent_shortening',review_scope='Read complete current stem/4 options/4 explanations and original correct choice; source evidence inherited except explicitly renewed sources in round40',scholarly_source_ids=M[id]['academic_review']['sources']))
(O/'shortening_decisions_32.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
# No wholesale resetting of the historic independent scholarly decisions.
changed38={x['id'] for x in json.loads((R/'publishing/2027/round38/revisions_14.json').read_text())['edits']};changed40={x['id'] for x in json.loads((O/'revisions_and_regression.json').read_text())['changes']}
ledger=[]
for q in qs:
 id=q['id'];rev=M[id]['academic_review'];assert rev['status']=='確認済み' and len(rev['option_verdicts'])==4 and rev['independent_answer']==q['answer'] and not rev['unresolved']
 ledger.append(dict(id=id,answer=q['answer'],academic_base_status=rev['status'],academic_base_sources=rev['sources'],current_adoption='round40_precision_review' if id in changed40 else 'round38_rewrite_review' if id in changed38 else 'shortening_context_review' if id in reasons else 'inherit_unchanged_academic_content_and_supplemental_decisions',current_full_fields_extracted=True,word_epub_consistency=True,unresolved_content_difference=False,new_independent_full_source_audit=False))
(O/'adoption_ledger_500.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
manifest=[]
for fn in ['Schon1983.pdf','Keigo.pdf']:
 p=Path('work/sources')/fn;manifest.append(dict(file=fn,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,scope='Schön printed61–62 / Keigo printed40, respectively; whole books not rereviewed'))
(O/'renewed_sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Adoption ledger500; historical shortening32 contextual decisions; cumulative20 questions revised')
