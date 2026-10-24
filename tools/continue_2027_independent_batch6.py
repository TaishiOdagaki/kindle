import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit';rows=json.loads((O/'ledger_500.json').read_text());D={
'Q_4_117':(4,['S173'],{'S173':[1,2]},['動画以外の教材も示す','継続観察と形成的評価を除外できない','集団の相互作用と教師支援を除外する誤り','直接指導を個人へ移し集団を相互作用の場へ']),
'Q_O_036':(1,['S173'],{'S173':[1,2]},['事前学習と教室活動の記録だけで全柱実践は不明','動画指示だけで全柱は確認できない','観察と支援も柱の指標にある','動画以外の教材を禁止していない']),
'Q_O_037':(4,['S173'],{'S173':[2]},['成績不算入だけでは形成的利用でない','小テストで事前学習不要とはならない','P2が形成的評価を明示','観察記録を次の指導に生かす']),
'Q_O_038':(4,['S173'],{'S173':[2]},['観察とアクセス配慮を放棄','偶然だけと断定する情報なし','未視聴の記録と矛盾','理由と環境を確かめアクセスを検討']),
'Q_O_039':(3,['S173'],{'S173':[2]},['必要に応じた支援を全放棄','確認せず調整しない方針','観察結果に応じ補足とフィードバック','参加支援の条件に反して完全排除']),
'Q_O_040':(3,['S173'],{'S173':[2]},['全時間を反復で使い切り応用に接続しない','再試行という条件と異なる','事情確認とアクセス・活動接続の見直し','理解状況を確認しない一律対応']),
'Q_2_004':(3,['S190'],{'S190':[2,3,5]},['CALPとBICSを逆にする','概念的区別を全能力理論と誤解','会話だけで教科言語を判断しない','BICSとCALPの定義を取り違える']),
'Q_4_037':(1,['S190','S191'],{'S190':[2,3,5],'S191':[9,10,11]},['内容思考と言語の支援を関連付ける','全言語習得後に内容という原則でない','既有知識と文脈的支援を無視して思考全廃','CALPは口頭も含む']),
'Q_4_084':(3,['S190'],{'S190':[2,3,5]},['会話流暢さだけで教科学習支援を排除','口頭を除外する定義は誤り','教科の理解表現を確かめ支援を検討','課題の要求と支えは学習者による']),
'Q_O_008':(1,['S190'],{'S190':[2,3]},['講義の概念要点理解と記録が不安に対応','発音だけでは理解記録を含まない','会話だけで講義理解を保証しない','挨拶のみでは講義理解記録を含まない']),
'Q_O_041':(2,['S190'],{'S190':[2,3,5]},['会話と教科学習の同一視','困難な表現内容を確かめる','文章題に時間を要するだけで認知不足と診断不可','CALPは口頭説明の理解も含み得る']),
'Q_O_066':(1,['S191'],{'S191':[9,10,11]},['内容目標と必要な言語を統合','内容理解を除外','必要な言語の学習を除外','内容言語の二重焦点を否定']),
'Q_O_067':(4,['S191'],{'S191':[10]},['Contentは四要素の一つ','Cognitionは四要素の一つ','Communicationは四要素の一つ','CompetitionでなくCulture']),
'Q_O_068':(2,['S191'],{'S191':[9,10,11]},['内容目標を除き量だけに限定','内容思考と意味伝達の機会','内容相手の考えを除く反復だけに限定','内容意味を問わず発音だけに限定']),
'Q_O_069':(3,['S191','S192'],{'S191':[9,10,11],'S192':[15]},['目標の内容理解を評価しない','運用目標を正確さだけで判断','目標基準に応じ内容と言語を全体で評価','感想だけで両目標の達成は不明']),
'Q_O_070':(3,['S191','S192'],{'S191':[9,10,11],'S192':[14,15]},['名称だけで普遍的効果保証はない','日本語を用いた実践も記述','内容思考と言語を結び支援と負担を検討','言語と手順の支援を全除外']),
}
for r in rows:
 if r['id'] not in D:continue
 key,src,pages,rs=D[r['id']];r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=src,source_page_map=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(rs,1)],all_four_explanations_reviewed=True,explanation_finding='指定された概念・指標・ケース条件と全解説を本文・図へ再照合。概念的区別と因果効果、単元全体と各課題の評価焦点を区別。追加修正不要。',multiple_correct=False,no_correct=False,manuscript_change_required=False)
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');s=json.loads((O/'source_manifest.json').read_text())
for id,url,sha,pages,images,offset in [('S173','https://flippedlearning.org/wp-content/uploads/2016/07/FLIP_handout_FNL_Web.pdf','8710b0c0f1a34f9ca2df143876659a96fb5d0e4795bdaf6d055ce5b21d09aa2e',[1,2],[1,2],0),('S190','https://eclass.upatras.gr/modules/document/file.php/PDE1535/CumminsBICSCALPSpringer2007.pdf','a1e7a83e8540631dccb79d7a23d1222e8d535cf2de6e7094b0b7ed58568a6151',[1,2,3,5],[2,3,5],None),('S191','https://assets.cambridge.org/97811087/29734/excerpt/9781108729734_excerpt.pdf','fb242ad4c4cec5ef59e0e25564ff0c28cc6e55993ccb58be3eca4904be49017e',[9,10,11],[9,10,11],-1),('S192','https://www.cambridgeenglish.org/Images/22191-tkt-clil-handbook.pdf','1a8d64343ddf539351efc2ff8a4d048e8d44d8c3a090095e0171902abdabafda',[14,15],[14,15],1)]:s.append(dict(id=id,url=url,retrieved='2026-10-24',sha256=sha,pages_read=pages,page_images_read=images,pdf_page_one_based_offset=offset,page_numbering='PDF pages' if id=='S190' else 'Printed pages',scope='指定頁の記述とケース適用。引用先研究全体の追試・未取得書籍全文・普遍的介入効果は承認しない。'))
(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print('Fresh total',sum(x['reviewed_this_pass'] for x in rows))
