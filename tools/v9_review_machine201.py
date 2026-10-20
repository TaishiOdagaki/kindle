"""Record manually read warnings, bound to the exact unedited batch199 draft."""
import hashlib,json,subprocess
from pathlib import Path
import quiz_audit as qa
p=Path('audit/v9');doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'
BASE='355a3eeaa4d1b2e3a38222914fdf1e79008102c5'
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
digest=hashlib.sha256(doc.read_bytes()).hexdigest()
assert digest=='d0555e5ffe001b76dec74b5e152e54b152d1a441fe86b4af4175eb2e542b673a'
issues,q,a=qa.audit(str(doc));saved=json.loads((p/'postfix_machine.json').read_text())
assert [list(i) for i in issues]==saved['issues'] and len(issues)==159
reasons={
'Q_1_003':'正答1は複数帰属と重要さの変化を肯定し、末尾は頻度測定ではないとの根拠の射程の留保。誤答2は国家・民族への限定、3は幼少期固定、4は旧帰属の全喪失を反証。正答の内容を否定していない。',
'Q_1_006':'正答4は場所・対象・教授内容を肯定、末尾は政策全体の評価を問わないという設問範囲の留保。誤答1は提案と最終選定、2は台湾語研究等の排除、3は日本からの学生限定をそれぞれ反証。',
'Q_1_008':'正答1はEJUの目的を肯定し、全受験者の全科目受験は意味しないと留保。誤答2はBJTの点数と6段階、3はJLPTに会話試験がないこと、4はOPI口頭面接を説明して反証。',
'Q_1_009':'正答3は身分等の資格の活動制限なしを肯定し、職業免許の免除ではないと留保。誤答1は本人申請不能、2は無許可40時間、4は留学の休業例外を家族滞在へ広げる点を反証。',
'Q_1_010':'正答4は制度目的と運用開始日を肯定し、現時点で全面運用済みとの取り違えを防ぐ。誤答1は人材確保の除外、2は公布と開始の混同、3は旧制度と目的同一を反証。',
'Q_1_013':'正答3は外務省査証申請ページの滞在期間と注2を肯定し、高度専門職2号や国内手続へ一律適用しないと留保。誤答1は家族等への不交付、2は国籍別追加書類なし、4は紙原本限定を反証。',
'Q_1_018':'正答1は一文一内容・対象者に応じた語彙等を肯定し、一律の試験級への制限ではないと留保。誤答2は災害限定、3は外来語の無条件多用、4は二重否定等の多用を反証。',
'Q_1_021':'正答3は多言語とやさしい日本語の使分け・視覚補助・確認を肯定し、全場面の理解保証や翻訳廃止ではないと留保。誤答1は絵等の一律禁止、2は英語限定、4は対象者等の確認工程省略を反証。',
'Q_1_022':'正答4は静岡県の対話交流型の説明を肯定し、全地域同一運営や効果保証ではないと留保。誤答1は学ぶ側の固定、2は初期教室との不両立、3は交流を一方向講義へ置換する点を反証。',
'Q_1_026':'正答3は設立年・所管・組織変化の日付を肯定し、日本語普及政策全史の説明ではないと留保。誤答1は設立時独法、2は1983年初設、4は変更方向の逆を反証。',
'Q_1_036':'正答4は面接と全般的評価を肯定し、全レベルに段落単位の発話を要求しないと留保。誤答1は筆記機械採点、2は文法のみ、3はN1～N5という評価区分を反証。',
'Q_1_037':'正答3は同じ採点基準で判断差を抑える条件を肯定し、処理ミスや全測定誤差の消滅は保証しないと留保。誤答1は熟達度の誤定義、2は妥当性と信頼性の混同、4はテスター訓練不要を反証。',
'Q_1_039':'正答4はA1～C2の3領域6段階を肯定し、下位区分や調整の禁止ではないと留保。誤答1は母語話者唯一目標、2はCan-doを性格判定限定、3は文法語彙量だけへの限定を反証。',
'Q_2_002':'正答2は宜蘭の接触・再編と世代にまたがる担い手を肯定し、全クレオール成立史の普遍過程ではないと留保。誤答1は台湾日本語との同一視、3は高年層限定、4は日本語上層の例の存在否定を反証。',
'Q_2_003':'正答2は言語能力水準の媒介を肯定し、個人の思考能力不足の診断基準ではないと留保。誤答1は閾値固定、3と4は加算・減算名称の逆を反証。',
'Q_2_004':'正答3は会話の流暢さと学習上の言語能力の混同回避を肯定し、全児童の共通習得期限ではないと留保。誤答1と4はBICS/CALPの逆、2は二分類で全能力を説明し尽くす点を反証。',
'Q_2_010':'正答3は紹介される8言語の一覧を肯定し、危機言語がその8つに尽きるとの主張ではないと留保。誤答1はアイヌ語除外、2は沖縄県内限定、4は保存継承の取組なしを反証。',
'Q_2_022':'正答3はネガティブ・フェイスへの配慮を肯定し、否定的感情を意味しないと留保。誤答1はポジティブとの逆、2は敬語形式限定、4は自己像否定を定義とする点を反証。',
'Q_2_026':'正答4は依頼等の圧力とネガティブ・フェイスを肯定し、両方のフェイスを脅かす場合もあると留保。誤答1は脅威最大化、2と3はフェイスの名称逆を反証。',
'Q_2_034':'正答3は宣言第4条3・4項の機会と可能な限りの条件を肯定し、教育効果の普遍的実証ではないと留保。誤答1は母語と社会知識機会の排他化、2は少数者文化等の措置なし、4は全機関全科目母語のみを反証。',
'Q_2_036':'正答3は全言語レパートリーと経験の活用機会を肯定し、全員への学習効果の因果保証ではないと留保。誤答1は家庭言語禁止、2は他言語経験の全除外、4は職業翻訳者限定を反証。'
}
entries=[]
for k,reason in reasons.items():
 found=[list(i) for i in issues if i[0]=='P1' and i[1]==k];assert len(found)==1
 snapshot={'question':q[k],'answer':a['A_'+k[2:]]}
 entries.append(dict(issue=found[0],result='正誤タグ取り違えなし',reason=reason,content_sha256=hashlib.sha256(json.dumps(snapshot,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
extra=[
('S2','Q_O_073','どの群の例か。という選択肢の群名を尋ねる問いがあり、全4肢は方略分類名。QMARKは選べ・どれか等を列挙するが、どの群の例かを認識しない。問いの欠落ではない。'),
('S2','Q_M_015','何と呼ぶか。でモデル全体の名称を尋ね、全4肢は名称。QMARKは何と呼ぶかを認識しない。問いの欠落ではない。'),
('A1','Q_3_001','ABSの常には、正答3の非常に少ないの一部に一致する。語認識が非常に少ない場合に理解できないことがあるという条件・可能性の記述で、常にとの断定ではない。他3肢は処理の逆定義や併用否定を述べ、正答は3のまま。'),
('A1','Q_3_004','必ずは架空学習者が持つ支払順序の思い込みの引用内容。全飲食店の客観的規則として著者が断定していない。語句・文は理解し、経験の期待と順序が食い違う設定が正答3。他肢は語彙・接続語・読みの未知。'),
('A1','Q_4_066','正答4の必ずしも要さずは意味理解の必要性を否定する限定表現。意味理解が常に不要だという断定ではない。1は人数だけ、2は個人情報の一切排除、3は意味選択の排除であり、4の原著分類の対比と整合しない。'),
('A1','Q_5_011','正答4のすべてではなくは母語起因を全称化しない限定。1は母語だけ、2は妨げだけ、3は初期限定・必ず消失で、4はそれらを避けた説明。断定語があるとの表層検出を誤答の証拠にしない。'),
('A1','Q_O_036','正答1は四つの柱すべての実践を確認したことにはならないと記録の不足を指摘する限定。2は動画指示だけで全柱実践を認定、3は教師支援排除、4は動画以外禁止で、1の記録に即した範囲と異なる。')]
for code,k,reason in extra:
 found=[list(i) for i in issues if i[0]==code and i[1]==k];assert len(found)==1
 snapshot={'question':q[k],'answer':a['A_'+k[2:]]}
 entries.append(dict(issue=found[0],result='文脈を直接対照し修正不要',reason=reason,content_sha256=hashlib.sha256(json.dumps(snapshot,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
t3=[list(i) for i in issues if i[0]=='T3'];assert len(t3)==1
paras,_=qa.load(str(doc));texts=[x['t'] for x in paras if x['t'].startswith(t3[0][1])];assert len(texts)==1 and 'もともと' in texts[0]
entries.append(dict(issue=t3[0],result='誤植ではない',reason='A_3_036の解説1にある、もともと内発的に楽しんで行っている、という副詞。もともとを同句反復の正規表現が検出したもので、語句の重複入力ではない。',paragraph_sha256=hashlib.sha256(texts[0].encode()).hexdigest()))
assert len(entries)==29
prior=json.loads((p/'evidence/machine_correspondence_review_200.json').read_text());assert prior['docx_sha256']==digest
done={(code,r['id']) for r in prior['dispositions'] for code in r['codes']}
done|={(r['issue'][0],r['issue'][1]) for r in entries};assert len(done)==39
remaining=[list(i) for i in issues if (i[0],i[1]) not in done];assert len(remaining)==120
obj=dict(batch=201,base_remote_commit=BASE,docx_sha256=digest,scope='機械警告の文脈と正誤タグ・設問の対応点検。学術資料の新規承認や再取得はしない。',source_question_status_counts=json.loads((p/'manifest.json').read_text())['status_counts'],raw_machine_issues=len(issues),reviewed_this_batch=29,total_disposed=39,dispositions=entries,remaining_unreviewed_warning_instances=120,remaining_issues=remaining,glossary_followup='APPENDIX_GLOSSARYのモダリティ（ムード）の同一視は出典・定義範囲の横断点検を要する。V1は未処置のまま保持。',draft_text_changed=False,full_visual_qa_completed=False,release_ready=False)
(p/'evidence/machine_review_batch201.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
assert hashlib.sha256(doc.read_bytes()).hexdigest()==digest
report='''\n\n## 第201バッチ 2026-10-20\n\n機械警告29件を文脈と全4肢・全4解説に直接対照。P1は第1・2章の21件で、正答の肯定に続く一般化・因果保証・適用範囲の留保を否定文として検出したもの。S2の2件は「どの群の例か」「何と呼ぶか」を検出式が認識しない。A1の5件は「非常に」内の「常に」部分一致、架空学習者の思い込みの記述、「必ずしも」「すべてではなく」等の限定。T3の1件は「もともと」という副詞。正答・正誤タグ・設問・解説の追加改訂は不要と判定し、生警告159件は削除しない。\n\n第200の10件と合わせ39件の個別処置を記録、処置点検残120件（P1 119、V1 1）。根拠となる原稿・問題本文のハッシュと各警告の個別理由はevidence/machine_review_batch201.json。用語集の「モダリティ（ムード）」の同一視は横断点検を要し、V1を解決済みにしない。既存の500問学術判定、493問4314箇所の累積改訂、作業DOCX、v8、台帳、changesは変更なし。対象DOCXのSHA256はd0555e5ffe001b76dec74b5e152e54b152d1a441fe86b4af4175eb2e542b673a。\n\n新しい原稿描画は不要な読取り検査のみ。最終改頁・全頁画像QA・前付け等の横断根拠点検・残警告処置は未完了。最終v9としての納品、公開、KDP配信、元ブランチへのマージは行わない。\n'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第201バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'README.md';f.write_text(f.read_text()+'\n第201バッチ：機械警告29件を追加処置。生警告159件中39件の確認理由を記録し、処置点検残120件（P1 119・V1 1）。用語集のモダリティ／ムードを横断点検残件として保持。原稿・台帳・個別学術判定は変更なし、最終検査は継続中。詳細 evidence/machine_review_batch201.json。\n')
print('29 warnings reviewed; 120 remain; manuscript bytes unchanged.')
