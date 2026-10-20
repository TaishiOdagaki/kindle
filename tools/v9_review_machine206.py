"""One-time manual disposition of the remaining P1 warnings, without manuscript edits."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import quiz_audit as qa

p = Path('audit/v9')
BASE = sys.argv[1]
assert subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == BASE
doc = p / '登録日本語教員試験決定版問題集_v9_監査作業中.docx'
digest = hashlib.sha256(doc.read_bytes()).hexdigest()
assert digest == json.loads((p/'evidence/machine_review_batch205.json').read_text())['docx_sha256']
issues, q, a = qa.audit(str(doc))
issues = [list(i) for i in issues]
assert issues == json.loads((p/'postfix_machine.json').read_text())['issues']
reasons = {
'Q_M_002':'正答1は公式事業の対象・約6か月・初中級を肯定し、EPA全送出国・全段階の説明ではないと留保。誤答2は教育機会なし、3は学習不要の上級者限定、4は旅行者限定をそれぞれ反証。',
'Q_M_005':'正答1は2,899,208÷3,794,714=約76.4%の分布を肯定し、近さによる因果説明はしない。誤答2は地域同数、3は両アフリカ区分ゼロ、4は西欧東欧限定を原表の対例で反証。',
'Q_M_010':'正答3は人物像と言葉遣いの双方向の連想を肯定し、フィクション限定を否定。誤答1は音量のみ、2はマンガアニメのみ、4は全高齢者の実使用調査との混同を反証。用語集のフィクション限定という別残件は閉じない。',
'Q_M_018':'正答4は帰国後までのWカーブを肯定し、全員の経過の予測保証はしない。誤答1は滞在中だけ、2は語数だけ、3は語順比較で、指定された適応過程に不一致。',
'Q_M_019':'正答4は職業上の現象・非疾患という位置付けを肯定し、個人診断とはしない。誤答1は全生活領域と疾患への拡大、2は短時間の疲労だけ、3は三側面を疲弊だけに縮減する点を反証。',
'Q_M_023':'正答2は投影と議論に応じたU字型等の候補を肯定し、機器の効果保証はしない。誤答1は目標除外、3は議論妨害という目的逆、4は固定席なら隣同士の活動も不可とする拡大を反証。',
'Q_M_024':'正答2はDELTA三モジュールと任意順序・組合せを肯定し、申込条件不要とはしない。誤答1は一科目不可分、3は逆順義務、4は全部同時開始限定を反証。',
'Q_M_028':'正答1は状況・目的に応じた選択と評価を肯定し、無条件混合とはしない。誤答2は無作為、3は唯一法の普遍的優越、4は選択結果評価不要を反証。1987年論考の射程の留保も正答否定ではない。',
'Q_M_032':'正答1は実施後の省察と時間見積りの見直しを肯定し、成果向上を保証しない。誤答2は変更禁止、3は毎回無作為、4は計画・自己点検との無関係という判断を反証。',
'Q_M_041':'正答4は年齢・プライバシー・人間による検討を肯定し、製品適法性や効果を保証しない。誤答1は年齢不問、2は倫理検討なし、3は個人情報保護無関係を反証。',
'Q_M_042':'正答4は引用の条件と合理的出所明示の併存を肯定し、表示だけの適法性保証を否定。誤答1は引用表示で無制限全文、2は著作物利用でない、3は出所表示で他条件免除を反証。短作品全引用や著作者名の例外の補足は肢の付替えを要しない。',
'Q_M_044':'正答2は指定解説の日本語混用と中国語の対比を肯定し、全文章の文字種固定とはしない。誤答1は漢字なし、3は中国語が全てひらがな、4はローマ字一切なしを反証。D2の以前の対応確認とも矛盾しない。',
'Q_M_045':'正答3は状態変化と結果への着目を肯定し、頻度・教授効果の実証とはしない。誤答1はしますとの対比逆、2は背の変化の否定、4は名詞型の存在否定を反証。',
'Q_M_047':'正答4は指定教材の語中[g]/[ŋ]と意味不変を肯定し、全話者等の使用率の固定とはしない。誤答1は[ŋ]のみ、2は意味が変わる、3は[ŋ]不存在であり、それぞれ対比と逆。',
'Q_M_049':'正答4は読み手に応じた常用漢字語への振り仮名を肯定し、改変の適法性判断とはしない。誤答1は常用漢字一律禁止、2は固有名詞限定、3は非母語話者への配慮否定を反証。',
'Q_M_055':'正答4は許可・恩恵の基本条件を肯定し、見立てや個人差を残して形式だけの一律判断はしない。誤答1は頻用なら常時適切、2はいただくが非敬語、3は許可恩恵無関係を反証。',
'Q_MO_004':'正答3は前提と判断限界の共同点検を肯定し、相談や変更の効果を保証しない。誤答1は前提除外、2は助言一度で見直し不要、4は再考と今後変更の拒否。オンライン教材のケース前提とも対応する。',
'Q_MO_006':'正答1は現場の指示・注意喚起の理解を肯定し、日本語指導だけの安全保証はしない。誤答2は文学、3は伝統文化、4は大学レポートで、ケースの主目的と異なる。別の進学ニーズの可能性を認めても主目的の単一性は崩れない。',
'Q_MO_007':'正答3は写真・イラストによる物や状況の理解支援を肯定し、理解保証はしない。誤答1は著作権対象外、2は理解確認不要、4は日本語学習不要を反証。安全な模擬場面・法定教育の代替でないケース条件も確認。',
'Q_O_009':'正答4は目標・評価内容の共有を肯定し、形式変更だけの能力向上保証はしない。誤答1は隠す、2は一覧だけで振返り不要、3は言語材料準備不要を反証。',
'Q_O_012':'正答2は聞き手との関係に応じた表現選択を肯定し、本人への引用の一律誤用判定はしない。誤答1は活用のみ、3は発音のみ、4は正書法のみで、同部長の社内外報告という指定焦点と異なる。',
'Q_O_014':'正答4は同部長の社内外報告の場面比較を肯定し、本人の在席不在だけで判断しない。誤答1は活用だけで場面なし、2は非文法なら扱わない、3は待遇表現を除外し、設問の気づきの目標に不一致。',
'Q_O_015':'正答2は敬語の仕組み・複数例・選択・実践機会を肯定し、指導効果の保証はしない。誤答1は場面選択除外、3は唯一表現固定、4は経験のみで意図的学習なしを反証。改頁の別残件は閉じない。',
'Q_O_017':'正答2は事情聴取後に相互理解の時間を設けない過程を指摘し、日本全体の慣習の事実承認はしない。誤答1はくじ引き自体の全面禁止、3は最望ましいとの無問題評価、4は事情聴取自体を問題とする焦点逆。',
'Q_O_018':'正答2は背景共有と共同の決定を肯定し、全員納得の保証はしない。誤答1は一方に従わせる、3は内容を無視、4は永久分離であり、受入可能な解決を探る過程を欠く。一時休止の補足は永久分離の肯定ではない。',
'Q_O_019':'正答1はルールの事前話合いの機会を肯定し、対立防止保証はしない。誤答2は国籍による組合せ排除、3は常に教師のみ、4は個人活動のみ。教師判断や個人活動の価値を否定せず、今回の機会という目的で区別。',
'Q_O_020':'正答3は自分の前提と判断を見直す取組を肯定し、特定理論の定義・改善効果の実証とはしない。誤答1は本人の背景を検討から排除、2は振返り不要、4は再発なしと決めた省察拒否。',
'Q_O_022':'正答4は年中行事の既有知識を使う予測を肯定し、ボトムアップ不在は認定しない。誤答1は形式のみ、2は文構造のみ、3は個語解読のみで、報告に明示された背景知識の使用を説明しない。',
'Q_O_024':'正答4は本文にある根拠箇所を詳しく読む細部確認を肯定し、効果保証はしない。誤答1は未習語彙全排除、2は大意目標を廃止、3は確認せず自習任せで、ケースの目標と方針に不一致。',
'Q_O_025':'正答3は大意・細部の目標に応じた活動と見直しを肯定し、全授業への同一活動強制はしない。誤答1は精読のみ、2は計画不変更、4は全授業で導入省略への根拠のない拡大。',
'Q_O_026':'正答2は観点別・段階別の基準表を肯定し、表だけの妥当性・一致保証はしない。誤答1は学習資料等の蓄積、3は言語データベース、4は学習内容等の計画で、評価との関係を否定せず指定表の名称として区別。',
'Q_O_027':'正答1は事前の基準解釈調整を肯定し、全点数一致は保証しない。誤答2は採点者削減、3は試験時間短縮、4は受験者削減で、会議の明示目的ではない。',
'Q_O_028':'正答1は基準と実発話根拠の対応説明を肯定し、保護者の納得保証はしない。誤答2は根拠不要、3は説明無関係、4は見せるだけで疑問消滅・説明不要を反証。法的説明義務の有無とは別の方針問題。',
'Q_O_033':'正答2は分かりませんでしたの後の句点による二文境界を肯定し、接続表現欠落を唯一分析とはしない。誤答1は読み仮名だけ、3は発音だけ、4は推測可能なら境界不要で、書記上の区切りという焦点と異なる。',
'Q_O_035':'正答3は誤用分析後の残る課題と学習者の必要を指導計画に使うことを肯定し、特定練習の効果保証はしない。誤答1は必要を除外、2はL1/L2順序同一の決め付け、4は体系への手掛かり否定。',
'Q_O_037':'正答4は理解情報による次の活動・支援調整を肯定し、得点だけで視聴や不理解原因は確定しない。誤答1は指導にも情報を反映しない、2は動画不要、3は無関係であり、形成的利用の指定に不一致。',
'Q_O_038':'正答4は未視聴の事情とアクセス方法の検討を肯定し、原因特定や変更効果保証はしない。誤答1は確認も調整もしない、2は偶然だけと断定、3は記録に反する全員視聴・理解の決め付け。',
'Q_O_041':'正答2は会話と学習言語を区別して困難箇所を確認することを肯定し、原因やCALP不足を診断しない。誤答1は会話から全学習言語十分、3は認知能力不足診断、4はCALP書面限定を反証。',
'Q_O_042':'正答4はケースの明示された教科と日本語の統合方針を肯定し、一練習だけで全JSL実施とは認定しない。誤答1は母語のみ、2は教科から完全分離、3は日本語指導なしで、ケースに不一致。取り出し支援一般を誤りとはしない。',
'Q_O_043':'正答4は教科理解と日本語表現の両面の情報共有を肯定し、連携の効果保証はしない。誤答1は全員一律、2は効果低下の無根拠断定、3は両面無関係・共有不要を反証。',
'Q_O_044':'正答3は教科別表現等への実態に応じた支援検討を肯定し、同じ練習の全教科強制はしない。誤答1は母語全禁止、2は他教科全排除、4は常時完全分離を反証。必要な取り出し自体は否定しない。',
'Q_O_045':'正答1は理解・参加の継続把握を見直しに使うことを肯定し、支援だけの因果効果とは確定しない。誤答2は測定不能として未確認、3は保護者のみ、4は開始後確認なしで、教師の継続的把握の目的と異なる。',
'Q_O_047':'正答3は指定された35条1項ただし書の条件を肯定し、許諾や別規定の利用まで否定しない。誤答1は必要限度だけでただし書無視、2は部数等無視、4は教育なら全条件免除を反証。',
'Q_O_050':'正答4は指定2024年資料の必須内容と到達目標を肯定し、確認だけで個別利用の適法性保証はしない。誤答1は事務担当だけ、2は実践無関係で非必須、3は情報資源の理解不要を反証。',
'Q_O_051':'正答1は指定原著の構造主義・行動主義・習慣形成を肯定し、練習手順だけで教師本人の信念は確定しない。誤答2は反復排除、3は習慣・強化否定、4は読書き先行への順序逆。',
'Q_O_052':'正答4は設問で加えた意味伝達と成果、事後の言語整理を肯定し、名称だけのタスク認定や習得保証はしない。誤答1は指定文再生だけ、2は形式事後確認禁止、3はPPP順序との取違え。',
'Q_O_055':'正答3は目標と観察に基づく正確さ・流暢さ活動の関連付けを肯定し、混合だけの効果保証はしない。誤答1は形式練習全廃、2は目標不問の好みのみ、4は正確さ活動が必ず先という固定順序を反証。',
'Q_O_057':'正答4は明示された負担への配慮意図をネガティブ・ポライトネスで分析し、負担感低減の実証とはしない。誤答1はオフレコード限定、2は仲間意識だけ、3は前置きで依頼消滅という取違え。',
'Q_O_059':'正答2は距離・力関係・負担評価を比較に使うことを肯定し、指導効果を原著が実証したとはしない。誤答1は関係除外、3は前置き等を理論から全排除、4は依頼がFTA例でないという否定を反証。',
'Q_O_063':'正答2は早い決定と全員納得という本人の発言を肯定し、国籍文化の単独因果認定はしない。誤答1は文法のみ、3は理由なし、4は発音のみで、記録された対立理由と不一致。',
'Q_O_064':'正答3は意思決定ルールの事前話合いという協働機会を肯定し、対立予防保証はしない。誤答1は教師のみで話合いなし、2は国籍分類だけ、4は交流最小化で、今回の意見交換機会の目的を満たさない。',
'Q_O_065':'正答2は明示された異なる視点の理解と解決探索を肯定し、一授業で習得完了とはしない。誤答1は発音のみ、3は文法語彙のみ、4は特定言語だけで、教師が述べた学習目標と不一致。',
'Q_O_068':'正答2は環境内容と日本語による伝達の二重焦点を肯定し、全員の能力向上保証はしない。誤答1は内容目標除外、3は内容を扱わない型反復のみ、4は発音のみでケースの読解・議論・レポートと不一致。',
'Q_O_069':'正答3は単元全体で両目標を捉える評価を肯定し、全課題で両面同時同重み採点とはしない。誤答1は内容評価排除、2は正確さだけで全目標判断、4は感想のみで成果評価なしを反証。',
}
assert len(reasons) == 54
remaining0 = json.loads((p/'evidence/machine_review_batch205.json').read_text())['remaining_issues']
assert set(reasons) == {i[1] for i in remaining0}
entries = []
for k, reason in reasons.items():
    found = [i for i in issues if i[:2] == ['P1', k]]
    assert len(found) == 1
    snapshot = {'question': q[k], 'answer': a['A_'+k[2:]]}
    h = hashlib.sha256(json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    entries.append(dict(issue=found[0], result='正誤タグ取り違えなし', reason=reason, content_sha256=h))

# Verify all preceding warning records against current content, not just counts.
done = {}
def add(issue, source, reason):
    key = tuple(issue)
    assert key in map(tuple, issues) and key not in done
    done[key] = dict(issue=issue, evidence=source, reason=reason)
e200 = json.loads((p/'evidence/machine_correspondence_review_200.json').read_text())
old_bytes = subprocess.check_output(['git','show',e200['base_remote_commit']+':'+str(doc)])
assert hashlib.sha256(old_bytes).hexdigest() == e200['docx_sha256']
with tempfile.TemporaryDirectory(prefix='v9-warning-206-') as td:
    old = Path(td)/'prior.docx'; old.write_bytes(old_bytes)
    _, oq, oa = qa.audit(str(old))
    assert q == oq and a == oa  # all 500 full question/answer records unchanged
for item in e200['dispositions']:
    for code in item['codes']:
        found = [i for i in issues if i[:2] == [code, item['id']]]
        assert len(found) == 1
        add(found[0], 'machine_correspondence_review_200.json', item['reason'])
paras, _ = qa.load(str(doc))
for batch in [201, 203, 205]:
    name = f'machine_review_batch{batch}.json'
    for item in json.loads((p/'evidence'/name).read_text())['dispositions']:
        ident = item['issue'][1]
        if 'content_sha256' in item:
            h = hashlib.sha256(json.dumps({'question':q[ident], 'answer':a['A_'+ident[2:]]},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
            assert h == item['content_sha256'], (batch, ident)
        if 'paragraph_sha256' in item:
            assert any(hashlib.sha256(x['t'].encode()).hexdigest()==item['paragraph_sha256'] for x in paras)
        add(item['issue'], name, item['reason'])
v1 = json.loads((p/'evidence/batch202_review.json').read_text())['warning_disposition']
assert any('ムードを述語の形態' in x['t'] or ('ムード' in x['t'] and '形態' in x['t']) for x in paras)
found = [i for i in issues if i[0]=='V1']; assert len(found)==1
add(found[0], 'batch202_review.json', v1['reason'])
for item in entries:
    add(item['issue'], 'machine_review_batch206.json', item['reason'])
assert len(done) == len(issues) == 159 and set(done) == set(map(tuple,issues))
baseline_names = ['decisions.json','ledger.json','ledger.csv','ledger.md','changes.json','manifest.json','postfix_machine.json']
unchanged = {}
for name in baseline_names:
    b = (p/name).read_bytes()
    assert b == subprocess.check_output(['git','show',BASE+':'+str(p/name)])
    unchanged[name] = hashlib.sha256(b).hexdigest()
v8 = Path(json.loads((p/'manifest.json').read_text())['source_file'])
assert hashlib.sha256(v8.read_bytes()).hexdigest() == '4aef79631da7096e5837dd31473978d40d4932ba3cf8473c52138662a843d498'
assert digest == hashlib.sha256(doc.read_bytes()).hexdigest()
e = dict(batch=206, review_date='2026-10-21', base_remote_commit=BASE, docx_sha256=digest,
    scope='全4肢・全4解説とケース前提の直接対照。原典の新規取得や全学術主張の再承認ではない。',
    reviewed_this_batch=54, dispositions=entries, raw_machine_issues=159,total_disposed=159,
    remaining_unreviewed_warning_instances=0,remaining_issues=[],
    preceding_question_content_revalidated_against_commit=e200['base_remote_commit'],
    preceding_all_500_question_answer_records_unchanged=True, unchanged_file_sha256=unchanged,
    draft_text_changed=False, v8_unchanged=True, current_warning_disposition_complete=True,
    final_machine_inspection_after_remaining_edits_completed=False, full_visual_qa_completed=False,release_ready=False)
(p/'evidence/machine_review_batch206.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
clearance = dict(review_date='2026-10-21',docx_sha256=digest,raw_issues=issues,
    dispositions=list(done.values()),undisposed_issues=[],raw_warning_count=159,disposed_warning_count=159,
    current_warning_disposition_complete=True,manuscript_unchanged_this_batch=True,
    final_machine_inspection_after_remaining_edits_completed=False,full_visual_qa_completed=False,release_ready=False,
    limitation='現在稿の検出159件の個別処置の完了。横断点検・改頁調整等の後には再検査と根拠の有効性確認を行う。出版準備完了を意味しない。')
(p/'evidence/machine_clearance_checkpoint206.json').write_text(json.dumps(clearance,ensure_ascii=False,indent=2)+'\n')
report='\n\n## 第206バッチ 2026-10-21\n\n残るP1警告54件（応用35・模擬16・模擬応用3）を、設問・全4肢・全4解説と関連ケース前提へ直接照合。正答の肯定後に因果・効果・一般化・法的保証の限界を述べる留保、および誤答が混同した別概念を肯定的に説明する文脈であり、正誤タグの取り違えは認めなかった。個別理由・本文ハッシュはevidence/machine_review_batch206.json。\n\n現在稿の機械検出159件を削除せず、159件全件の個別処置を記録し、処置点検残は0件。第200バッチの対象稿と現在稿の全500問の設問・全肢・正答・全解説が同一であること、第201・203・205バッチの各内容ハッシュとT3段落ハッシュが現稿で有効であることを再検証。V1は第202バッチの用語の範囲の留保を維持。全159検出と処置の一対一対応はevidence/machine_clearance_checkpoint206.json。\n\nこれは現稿の警告処置の完了であり、最終全問機械検査の完了ではない。500問の学術判定・台帳・変更4316箇所・作業DOCX・元v8は変更しない。新規出典取得や原典全主張の再承認を意味しない。役割語の原典正常再取得と用語集修正、他の横断点検、改頁調整、全頁最終画像QAは未了。編集後には機械検査と処置理由の有効性を再確認する。最終v9ではなく出版不可。\n'
for name in ['critical_findings.md','interim_report.md']:
    f=p/name; assert '## 第206バッチ' not in f.read_text(); f.write_text(f.read_text()+report)
f=p/'README.md'; f.write_text(f.read_text()+'\n第206バッチ：残るP1警告54件を全肢・全解説・関連ケースと直接対照し、処置点検残0件。生警告159件は全て保持し159件の個別処置と現稿での有効性を記録。54件は第205時点の履歴。本文・正答・学術判定・台帳・作業DOCXは不変。役割語等の横断点検・改頁調整・編集後の最終機械検査・全頁最終画像QAは未完了。\n')
print('54 warnings individually disposed; all 159 mapped; 0 undisposed; final QA incomplete; manuscript unchanged.')
