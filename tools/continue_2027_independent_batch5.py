import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';rows=json.loads((O/'ledger_500.json').read_text());D={
'Q_1_001':(1,[73],['自文化の尺度と自集団優位','文化放棄の過程でなく評価の見方','他文化優位は方向が逆','相手の基準を使う姿勢で自文化中心でない']),
'Q_1_002':(4,[41,42],['背景を聞かず優劣を逆転','全面放棄を求め権利を尊重しない','発言だけで心理状態は確定しない','本人の経験を尋ね判断を留保し権利を尊重']),
'Q_1_003':(1,[29,30],['複数所属と主観的重要性の変動','国家民族だけに限定','不可逆固定は変動性と逆','以前の所属喪失は同時複数所属と逆']),
'Q_2_031':(3,[48],['語句以外の観察を排除','言語非言語の不一致への注意を排除','話し方身体動作と社会的文脈へ注意','同状況の反応の類似相違の比較を排除']),
'Q_3_034':(4,[29,30],['家族や趣味等を除外','集団内部の資源と意味づけの個人差を否定','所属の主観的重要性の変動を否定','複数所属と場面時間による変化の適用']),
'Q_4_099':(1,[41,42,73],['主要文化を基準に他を評価','尊重と全採用の区別を無視','自分の当然さを問い直す姿勢と逆','人権侵害等への尊重の限界を無視']),
'Q_4_103':(3,[41,45,47,48],['記憶違いのみを断定する証拠なし','悪意の断定は根拠なし','本人の視点と複数解釈を検討','出身による一律判断は個人の視点を除外']),
'Q_O_005':(3,[47,52,53],['経験が浅いことは省察不要の理由でない','誤用と決めず訂正の根拠を点検する必要','発話記録と自己の前提判断を照合','将来の変更を一律に拒否']),
'Q_O_016':(2,[52],['文法誤用を示す本文なし','順序決定の前提差が本文にある','音声問題を示す本文なし','語彙不足を示す本文なし']),
'Q_O_017':(2,[51,52],['くじ引き自体の一律禁止でない','相互理解と合意形成の機会がない','機会欠如を最善とする根拠なし','事情を聞くこと自体は原典に沿う']),
'Q_O_018':(2,[51,52],['一方だけ採用し受入可能な解決を探らない','背景と視点を共有し一緒に検討','対立内容を扱わず解決を探らない','一時休止と永久分離は区別']),
'Q_O_019':(1,[30,51],['意見表明と合意形成を行う機会','国籍による対立傾向は本文から不明','教師のみ決定で学習者の合意機会なし','共有活動の協働の機会を除外']),
'Q_O_020':(3,[52,53],['本人が述べた背景も一括除外','能動的振り返りを不要とする','前提偏りと判断の関係を点検','再発しないとする情報なし']),
'Q_O_063':(2,[52],['文法差だけの原因を示す情報なし','本人の発言にある進め方の重視点の相違','本文に対立理由が明示','発音差の情報なし']),
'Q_O_064':(3,[30,51],['学習者の話合い機会を除外','国籍だけでは意見交換機会にならない','ルールの話合いが合意形成の機会','意見交換の機会を縮小']),
'Q_O_065':(2,[52],['発音だけでは本文の目標と異なる','視点理解と受入可能な解決探究','文法語彙だけでは本文の目標と異なる','特定言語の使用だけでは目標を満たさない']),
'Q_M_038':(2,[48,49,73],['情動伝染のみでなく技能を位置付ける','自己から距離を取り相手視点を理解','情動面の視点取得を除外','sympathyを一形態として含める']),
'Q_MO_004':(3,[52,53],['自分の前提を検討しない','一度の助言で振り返り終了とは定義されない','反応と見立ての差から判断の限界を点検','原因再検討と変更を一律拒否']),
}
for r in rows:
 if r['id'] not in D:continue
 key,pages,rs=D[r['id']];r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=['S213'],printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(rs,1)],all_four_explanations_reviewed=True,explanation_finding='現在の全肢・全解説と指定本文・注記を再照合。ケース1/4/13およびオンライン聴解の前提も再読。原典内の説明と架空例の適用を区別しており追加修正不要。',multiple_correct=False,no_correct=False,manuscript_change_required=False,scope='RFCDC自身の概念枠組み。国籍による心理診断・因果効果・別理論の独立確認へ拡張しない。')
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');s=json.loads((O/'source_manifest.json').read_text());s.append(dict(id='S213',url='https://rm.coe.int/16807bc66c',retrieved_from='https://wergelandcentre.org/content/uploads/2020/02/Reference-Framework-of-competences-Vol-1-1.pdf',retrieved='2026-10-24',bytes=4154359,pdf_pages=89,sha256='a93866bccc575a825b4cc9e9b5f25c115d7c1ffd29dc677a1acc0aa226daa612',identical_to_prior_official_pdf='audit/v9/evidence/batch156_sources.json',printed_pages_read=[29,30,41,42,45,47,48,49,51,52,53,73],printed_images_read=[30,41,42,48,49,51,52,53,73],pdf_page_one_based_offset=2));(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');limits=json.loads((O/'retrieval_limits.json').read_text());limits[0].update(status='解消：別公開先のPDFが既取得公式原本とSHA256・バイト数一致。本文と画像を再精読し18問を確認。TKI主根拠のQ_O_062は別途確認。');limits[1]['status']='解消：第2バッチでS147の7頁本文・図を取得再確認済み';(O/'retrieval_limits.json').write_text(json.dumps(limits,ensure_ascii=False,indent=2)+'\n');print('Fresh total81/500')
