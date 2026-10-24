import json,hashlib,sys
from pathlib import Path
from collections import Counter
from audit_2027_epub import read_epub
R=Path(__file__).resolve().parents[1];O=R/'publishing/2027/independent_audit'
D={
'Q_3_018':(3,'S29',[3,6],['母語転移だけへの限定が誤り','目標言語内の経験を誤除外','他の目標言語構造の経験から逸脱形を形成','経験に基づく規則形成を誤否定']),
'Q_3_019':(4,'S29',[6,9],['見るの正しいタ形','閉めるの正しいタ形','来るの正しいタ形','既習く→いたを例外の行くに適用した架空例']),
'Q_3_020':(2,'S29',[6,9],['食べるの正しいテ形','既習く→いてを例外の行くに適用した架空例','来るの正しいテ形','見るの正しいテ形']),
'Q_4_073':(3,'S29',[3,6],['目標言語の経験を誤除外','待遇上の文体切替で指定定義でない','既習構造の適用範囲を越えた非目標形','使用言語の切替で指定定義でない']),
'Q_5_008':(1,'S29',[2,3,4,6],['母語影響と目標言語内要因を検討','母語のみへの誤限定','異なる母語にも共通する記述に反する','対照だけで全原因を確定できない']),
'Q_3_001':(3,'S99',[],['背景予測はトップダウン','音声解読はボトムアップ','語の認識が乏しい場合の限界','別々の練習と実際の併用は両立']),
'Q_3_002':(1,'S99',[],['話題場面の知識から事前予測','単語分割と計数は音声解読','単語境界の確認は音声解読','予測を明示的に除外']),
'Q_5_088':(2,'S99',[],['音声理解が乏しい場合の限界を誤否定','文脈知識と音声解読を併用','トップダウンとボトムアップを逆対応','ボトムアップとトップダウンを逆対応']),
'Q_MO_001':(4,'S99',[],['ケースから形式単独原因を確定不能','教材無問題とも学習者単独原因とも確定不能','初級のみで全聴解を排除できない','語彙知識と連続音声での認識を区別して確認']),
'Q_MO_003':(2,'S99',[],['背景知識活性化という明示目的と異なる','料理写真から場面知識を活性化して予測','著作権の適法性は設問で未判定','背景知識予測を文法分析だけに誤限定']),
'Q_MO_005':(4,'S99',[],['実態を考慮せず上級へ一律化','オンラインを理由に支援を誤排除','聴解継続の設問条件に反する','実態に応じて背景予測と語認識を検討']),
'Q_4_085':(1,'S23',[],['教科と言語の支援を統合し学習参加を育成','固定した文法項目配列の最優先を誤主張','教科から完全分離した初期指導だけに誤限定','母語母文化の支えを誤排除']),
'Q_O_042':(4,'S23',[],['母語だけへ切替という事実はケースにない','教科と日本語を関連づける明示方針に反する','日本語表現練習という事実に反する','算数と言語の関連づけで全課程実施の認定ではない']),
'Q_O_043':(4,'S23',[],['実態把握を除外して一律化','効果低下はケースに示されていない','教科と言語の関係を誤否定','理解と表現両面の情報共有による検討']),
'Q_O_044':(3,'S23',[],['母語母文化の支えを誤排除','教科固有の表現支援を誤排除','他教科の固有の表現も実態に応じ検討','所属学級参加を除外し常時分離']),
'Q_O_045':(1,'S23',[],['理解と参加を継続把握し見直しへ用いる','理解確認と評価を誤排除','教師指導者の理解把握を誤排除','開始後の継続確認を誤排除']),
}
rows=json.loads((O/'ledger_500.json').read_text());_,_,qs,_,_=read_epub(O/'working/2027_independent_working.epub');qmap={q['id']:q for q in qs}
for r in rows:
 if r['id'] not in D:continue
 key,src,pages,rs=D[r['id']];assert not r['reviewed_this_pass'];assert key==qmap[r['id']]['answer'];assert len(rs)==4
 r.update(status='再確認済み',reviewed_this_pass=True,independent_answer=key,source_ids=[src],printed_pages=pages,option_verdicts=[dict(option=i,correct=i==key,reason=v) for i,v in enumerate(rs,1)],all_four_explanations_reviewed=True,explanation_finding='現行の設問・全肢・全解説を指定本文と対照。架空例・ケースの条件、原因未確定、支援効果の非保証を維持。',multiple_correct=False,no_correct=False,manuscript_change_required=False,scope='S29の1970会議稿、S99署名記事、S23公式報告の記載と適用。引用先の全原著や因果効果を独立実証した意味ではない。')
(O/'ledger_500.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
s=json.loads((O/'source_manifest.json').read_text());L=R.parent/'independent_sources'
for id,file,url,pages,imgs,scope in [
 ('S29','S29.pdf','https://files.eric.ed.gov/fulltext/ED037721.pdf',[2,3,4,5,6,7,8,9,10,11,12],[3,6,9],'1970年会議稿の書誌・序論・1節・3.1〜3.2節。日本語のタ形・テ形は架空適用として確認。'),
 ('S23','S23a.html','https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/001.htm',[],[],'基本構想全文、評価、サポート・システム、所属学級支援。TLS検証失敗後に公開資料のみ検証無効で取得し公式web本文とも照合。'),
 ('S23','S23b.html','https://www.mext.go.jp/a_menu/shotou/clarinet/003/001/008/006.htm',[],[],'教科志向型1〜2.3。個々の支援と日本語で学ぶ力、学習参加。')]:
 s.append(dict(id=id,url=url,retrieved='2026-10-24',sha256=hashlib.sha256((L/file).read_bytes()).hexdigest(),printed_pages_read=pages,printed_images_read=imgs,scope=scope))
s.append(dict(id='S99',url='https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/listening-top-down-and-bottom',retrieved='2026-10-24',sha256=None,access='web tool official HTML text, no local original bytes; local download timed out',sections_read=['署名','Top-down vs. bottom-up listening','Listening in the classroom','Top-down listening activities','Bottom-up listening activities','Conclusion'],scope='Catherine Morley記事本文全体。参考文献原著の全検証や特定活動の効果量の確認ではない。'))
(O/'source_manifest.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
p=json.loads((O/'PROGRESS.json').read_text());n=sum(r['reviewed_this_pass'] for r in rows);p.update(freshly_reviewed=n,remaining=500-n,status_counts=dict(Counter(r['status'] for r in rows)),latest_batch=9);(O/'PROGRESS.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');print(n,500-n)
