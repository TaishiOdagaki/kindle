#!/usr/bin/env python3
"""Verify orthographic policy against Cabinet-notice texts on Bunka's site."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==570
_,Q,A=qa.audit(str(b.DST));extra=[];D=json.loads((b.OUT/'decisions.json').read_text())
def item(k,stem,opts,exps,ans,why,sources,verdicts,scope):
 for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
  for i,new in enumerate(vs):
   old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][i] if field=='options' else A['A_'+k[2:]]['txt'][i]
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=sources,applied=True,before_version='第32修正バッチ作業稿'))
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=sources,option_verdicts=verdicts,reason=why,stem_review='告示本文の範囲を明示。未照合の政策原因や他制度の数値を採用内容から撤去。',explanation_review=scope,unresolved='',multiple_correct_risk=f'なし：{ans}のみ告示の記述に一致',no_correct_risk=f'なし：独立正答{ans}')
item('Q_5_033','常用漢字表（平成22年11月30日内閣告示）の前書きと表の構成について、適切な説明はどれか。',
 ['一般の社会生活における漢字使用の目安を示す表で、本表には2,136字が掲げられている。','科学・技術・芸術などの専門分野や個々人の表記も、すべて例外なく同じ扱いで対象とする。','すべての固有名詞を、例外なくこの表の対象とする。','過去の著作や文書の漢字使用を否定し、必ず現在の表の字体へ書き換えるよう求めている。'],
 ['前書きは一般の社会生活での漢字使用の目安という位置付けを示し、表の見方は本表の字種を2,136字としています。','前書きは、専門分野や個々人の表記にまで及ぼそうとするものではないとしています。ただし、社会生活と密接に関連する専門語では参考とすることが望ましいと述べており、全部を一律に対象とする説明ではありません。','前書きは、都道府県名に使う漢字とそれに準じる漢字を除き、固有名詞を対象としないとしています。すべての固有名詞を対象とする説明は誤りです。','前書きは、過去の著作や文書での漢字使用を否定しないとしています。必ず現在の表へ書き換えることを求める説明とは逆です。'],1,
 'IT機器・スマートフォンによる改定原因や別の教育漢字制度の未照合説明を撤去。告示自身の目安・適用範囲・字種に限定して確定した。',['S72'],
 ['告示の目安と本表字種に一致して正しい','専門分野・個人の適用範囲を過大にし誤り','固有名詞の除外を否定して誤り','過去の表記を否定しないという記述と逆で誤り'],
 '文化庁掲載の常用漢字表PDF第1頁、前書き1–5・表の見方及び使い方1–2を全肢・全解説へ照合。')
item('Q_5_035','現代仮名遣い（昭和61年内閣告示）の原則と表記の慣習による特例について、適切な説明はどれか。',
 ['現代語の音韻を基準とせず、すべて歴史的仮名遣いと同じに書くことを原則とする。','現代語の音韻を基準に書くことを原則とし、表記の慣習を踏まえて特例も設けている。','助詞の「は」「へ」「を」も、現代の音に合わせて必ず「わ」「え」「お」に書き換える。','同音の連呼の「ちぢむ」や二語の連合の「はなぢ」も、必ず「ちじむ」「はなじ」に書き換える。'],
 ['前書きは現代語の音韻に従って書くことを原則としています。歴史的仮名遣いを尊重する記述はありますが、すべて同じに書く原則とはしていません。','前書きの原則に一致します。本文第2は、助詞のは・へ・をなど、表記の慣習による特例を示しています。','本文第2は、それぞれ助詞のは・へ・ををその仮名で書くとしています。音に合わせてわ・え・おへ必ず書き換える説明は誤りです。','本文第2の5は、同音の連呼としてちぢむ、二語の連合としてはなぢ（鼻血）を挙げています。この例をすべてじへ直す説明は誤りです。なお、これとは別に二語へ分解しにくい語等の本則・許容の扱いもあり、複合語全体へ一律には広げません。'],2,
 'はなぢを同音連呼とした誤分類と花＋血という旧解説の誤りを撤去。告示の原則を現代語の音韻とし、例語の範囲を明示。',['S71'],
 ['現代語音韻による原則を否定して誤り','前書きの原則と特例に一致して正しい','本文第2の助詞表記と逆で誤り','本文第2の連呼・二語連合の用例と逆で誤り'],
 '文化庁掲載の現代仮名遣い前書き1・8と本文第2の1–3・5(1)(2)・なお以下を全肢・全解説へ照合。')
(b.OUT/'changes_batch33.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S71 | 文化庁 [現代仮名遣い 前書き](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/gendaikana/maegaki.html)、[本文第2](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/gendaikana/honbun_dai2.html) | 2026-10-12本文取得。前書き1・8、助詞1–3、5(1)(2)となお以下。ちぢむの同音連呼、はなぢ（鼻血）の二語連合を照合し、全部の複合語へ一般化しない。 | Q_5_035 |\n| S72 | 文化庁 [常用漢字表（平成22年11月30日内閣告示）](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf) | 2026-10-12本文取得。PDF第1頁の前書き1–5、表の見方1–2を照合。目安、専門分野・個人・固有名詞の範囲、過去表記の非否定、本表2,136字。改定原因と教育漢字制度は本問から撤去。 | Q_5_033 |\n')
print('Recorded',len(extra),'repairs')
