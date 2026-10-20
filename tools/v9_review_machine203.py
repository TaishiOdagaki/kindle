"""Manual P1 chapter3 dispositions, bound to the exact batch202 manuscript."""
import json,hashlib,subprocess,sys
from pathlib import Path
import quiz_audit as qa
p=Path('audit/v9');BASE=sys.argv[1];assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==BASE
doc=p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx';digest=hashlib.sha256(doc.read_bytes()).hexdigest()
assert digest=='fbcc7c5c8d2e588baf24fe84c51ba5af820568d0748c6f1c56e9db8f496203e5'
issues,q,a=qa.audit(str(doc));assert [list(i) for i in issues]==json.loads((p/'postfix_machine.json').read_text())['issues']
reasons={
'Q_3_004':'正答3は経験からの支払順序の期待と物語の順序の不一致を肯定。末尾は国民全体の慣習の例ではないとの限定で、事例を否定していない。誤答1・2・4はそれぞれ語義・接続表現・漢字読みの未知であり、スキーマとの食違いの事例ではない。',
'Q_3_009':'正答4は宣言的解釈から手続的遂行への知識コンパイルを肯定し、あらゆる課題の無意識・無誤り遂行という過大な保証を否定。誤答1は表象形式の逆、2は宣言的知識の一律消去、3は手続き化後の学習停止を反証。',
'Q_3_022':'正答2は独力と成人支援下の二水準を肯定し、一回の課題完成でその後の独力習得まで確定しないと留保。誤答1は支援してもできない、3は既に独力でできる、4は支援自体がないという設問条件との不一致。',
'Q_3_028':'正答3は記憶と認知の分類例を肯定し、実際の活動での併用を認めて完全な排他性を否定。誤答1は語彙学習の全認知化、2は迂言と分析・要約の分類逆、4は計画・不安調整の分類逆を反証。',
'Q_3_030':'正答4は滞在先の第2段階の説明を肯定し、個人差を残して全員の順序・期間・症状の診断基準ではないと留保。誤答1は蜜月を帰国後へ移す、2は自分の生活様式の全放棄、3は第4段階の帰国後限定を反証。',
'Q_3_032':'正答1は慣れた合図・手掛かり喪失による不安を肯定し、個人の症状をこの一文で診断しないと留保。誤答2は文法規則限定、3は不満を客観評価の証拠とする点、4は元の行動様式の全喪失を反証。',
'Q_3_033':'正答1は文化保持と社会参加の両方を肯定し、本人の希望だけで参加機会が保証されるとはしない。誤答2は周縁化、3は同化、4は分離という別の組合せをそれぞれ説明して反証。肯定的な別分類の説明は正答タグの付け替えを要しない。',
'Q_3_034':'正答4は事例の複数所属と文脈に応じた重要性の変化を肯定し、特定症状や不適応の診断ではないと留保。誤答1は国家限定、2は全員同じ資源・意味づけ、3は重要性不変を反証。',
'Q_3_038':'正答1は活動自体の面白さという本人の発言を肯定し、時間を忘れることだけを判定基準にしないと留保。誤答2は承認、3は奨学金、4はPCという活動から分離可能な結果を理由としており、活動自体への興味とは異なる。',
'Q_3_039':'正答4は二つの将来自己の指針に加えたL2学習経験を肯定し、自己像と現状の差だけで必ず意欲が生じるという保証をしない。誤答1は将来像限定、2は二要素限定、3は運動能力から言語能力への移転だけという誤定義を反証。',
'Q_3_041':'正答2は不安の可能性を調べ、本人の負担・訂正法・反応を見直す対応を肯定し、特定活動の効果を保証しない。誤答1は経済理由だけ、3は全訂正と順位で必ず解決、4は知識不足だけとの断定であり、設問の検討条件と異なる。'
}
assert len(reasons)==11
entries=[]
for k,reason in reasons.items():
 found=[list(i) for i in issues if i[0]=='P1' and i[1]==k];assert len(found)==1
 snapshot={'question':q[k],'answer':a['A_'+k[2:]]}
 entries.append(dict(issue=found[0],result='正誤タグ取り違えなし',reason=reason,content_sha256=hashlib.sha256(json.dumps(snapshot,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
done={(code,x['id']) for x in json.loads((p/'evidence/machine_correspondence_review_200.json').read_text())['dispositions'] for code in x['codes']}
done|={(x['issue'][0],x['issue'][1]) for x in json.loads((p/'evidence/machine_review_batch201.json').read_text())['dispositions']}
done.add(('V1','表記ゆれ'));done|={(x['issue'][0],x['issue'][1]) for x in entries}
remaining=[list(i) for i in issues if (i[0],i[1]) not in done];assert len(done)==51 and len(remaining)==108 and all(x[0]=='P1' for x in remaining)
e=dict(batch=203,base_remote_commit=BASE,docx_sha256=digest,scope='機械警告P1の正誤タグと文脈の対応点検。原典の追加取得や全主張の新規承認ではない。',reviewed_this_batch=11,dispositions=entries,raw_machine_issues=159,total_disposed=51,remaining_unreviewed_warning_instances=108,remaining_issues=remaining,draft_text_changed=False,full_visual_qa_completed=False,release_ready=False)
e['cross_section_followup']=[{'block':'APPENDIX_GLOSSARY','term':'役割語','current_text':'特定のキャラクター像を想起させる、フィクション上の特徴的な話し方。','question':'Q_M_010','existing_source':'S201','finding':'用語集のフィクション上という範囲が、既存改訂問のフィクションに限らない説明と食い違う読みを生む。S201の原論文本文を再取得し、用語集の人物像と言葉遣いの定義と範囲を改訂する。現時点では未改訂。'},{'block':'APPENDIX_GLOSSARY','term':'妥当性／信頼性','finding':'測定したいものを正しく測れているか／結果の安定性という用語集の簡略説明と、得点解釈・用途の根拠を扱うQ_1_037等との説明範囲を既存原典で横断照合する。未確認のまま最終承認しない。'}]
(p/'evidence/machine_review_batch203.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
report='\n\n## 第203バッチ 2026-10-20\n\n第3章のP1警告11件を設問・全4肢・全4解説と直接照合し、正誤タグの取り違えなしと判定。正答を肯定した後の、国民全体の慣習・無誤り遂行・習得の確定・因果保証・症状診断などへの一般化を防ぐ留保に検出式が反応している。別の分類や概念を肯定的に説明する誤答解説も、その肢の誤りを反証しているか確認。個別理由と問題本文ハッシュはevidence/machine_review_batch203.json。\n\n生警告159件は保持し、処置済み累計51件、点検残108件（P1）。用語集改訂後の原稿SHA256 fbcc7c5c8d2e588baf24fe84c51ba5af820568d0748c6f1c56e9db8f496203e5を対象とし、本文・判定・台帳・正答・書式・作業DOCXは変更しない。再描画を要する編集はない。最終全頁QA、改頁調整、前付け・ケース・他の用語集項目などの横断点検、残警告処置は未完了。最終v9ではなく出版不可。\n'
report+='\n横断点検の具体的残件：用語集の役割語の「フィクション上」という範囲は、S201本文に基づきフィクション限定を撤回したQ_M_010と食い違う読みを生む。S201原論文を再取得し、人物像と言葉遣いの定義と範囲を修正する。用語集の妥当性／信頼性の簡略説明も、得点解釈・用途を扱う改訂問と原典で照合する。両項目とも現時点では未改訂・横断点検未完了。\n'
for n in ['interim_report.md','critical_findings.md']:
 f=p/n;assert '## 第203バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'README.md';f.write_text(f.read_text()+'\n第203バッチ：第3章のP1警告11件を追加点検。機械警告159件中51件の個別処置理由を記録し、点検残108件（P1）。119件は第202時点の履歴。作業DOCX・500問の本文・正答・判定は変更なし。最終全頁QA・横断点検・改頁調整は未完了。\n')
print('11 additional warnings disposed; 108 remain; no document edits.')
