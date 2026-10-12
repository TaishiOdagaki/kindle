#!/usr/bin/env python3
"""Repair Chinese-origin vocabulary claims and indirect-request example."""
import json, html
import v9_apply_batch1 as b
import quiz_audit as qa

prior = json.loads((b.OUT / 'changes.json').read_text())
assert len(prior) == 316
_, Q, A = qa.audit(str(b.DST))
extra = []

def record(k, field, index, new, reason, sources):
    if field == 'stem': old = Q[k]['stem']
    elif field == 'options': old = Q[k]['opts'][index]
    else: old = A['A_' + k[2:]]['txt'][index]
    old = html.unescape(old)
    if old != new:
        extra.append(dict(id=k, field=field, index=index, before=old, after=new,
                          reason=reason, sources=sources, applied=True,
                          before_version='第15修正バッチ作業稿'))

why46 = ('「経済」「文化」を一律に明治期の新造語とする旧解説を撤去。国立国語研究所の語種説明と'
         '文化庁資料に合わせ、中国語由来の漢語と、日本で漢字音を用いて作られた漢語を区別し、'
         '個別語史を断定しなくても単一正答になる選択肢へ全面改稿。')
opts46 = [
    '漢語とは、日本語が成立する以前から日本に固有だった語だけを指し、中国語から取り入れた語は含まない。',
    '漢語には、主として古代中国語から取り入れた語に加え、日本で漢字音を用いて作られた語も含まれる。',
    '漢語とは、現代中国語から近年取り入れた語だけを指し、古くから日本語に定着した語は含まない。',
    '漢語の構成要素は造語に利用できず、明治期にも西洋の概念を表す翻訳語の形成には使われなかった。'
]
exp46 = [
    '日本固有の語は和語です。漢語には、古代中国語から取り入れられた語を基盤とする語群が含まれます。',
    '国立国語研究所は語種を和語・漢語・外来語などに分け、漢語を古代中国語に対応する語群として説明しています。日本で漢字音を用いて作られた漢語もあります。',
    '漢語を近年の現代中国語由来の語だけに限定する説明は誤りです。日本語は古くから中国語の影響を受け、多くの語を取り入れてきました。',
    '漢字・漢語の構成要素は造語に用いられ、明治期には西洋の事物や概念を表す翻訳語にも漢語が使われました。'
]
for i,t in enumerate(opts46): record('Q_5_046','options',i,t,why46,['S51'])
for i,t in enumerate(exp46): record('Q_5_046','explanations',i,t,why46,['S51'])

why75 = ('「寒い」という発話だけでは依頼の解釈が確定しないため、開いた窓、話者の様子、聞き手の'
         '行為可能性を明示。旧解説の「エアコンを強める」は冷房・暖房の別がなく逆効果にもなるので撤去。'
         'Searleの間接発話行為論と大学公開の意味論・語用論解説に照合。')
record('Q_5_075','options',0,
       '開いた窓のそばで寒そうにしている話し手が、窓を閉められる聞き手に「ここは寒いですね」と述べると、気温への言及に加えて、窓を閉めてほしいという間接的な依頼として解釈されることがある。',
       why75,['S52'])
record('Q_5_075','explanations',0,
       '発話は文字どおりには寒さへの言及ですが、提示した状況と共有知識の下では、窓を閉めるよう求める間接的発話行為として理解されることがあります。文脈を無視して常に依頼になるわけではありません。',
       why75,['S52'])
record('Q_5_075','explanations',1,
       '言語表現が持つ比較的安定した意味を扱うのは主に意味論です。語用論では、文脈、共有知識、話し手の意図などを考慮して発話を解釈します。',
       why75,['S52'])
record('Q_5_075','explanations',2,
       '語や文の意味が分かっても、文脈における意図や適切性を常に理解できるとは限りません。このため、語用論的な理解を一律に不要とする説明は適切ではありません。',
       why75,['S52'])
record('Q_5_075','explanations',3,
       '説明が逆です。意味論は言語表現の意味を扱い、語用論は文脈や共有知識を用いた発話解釈を扱います。両者の境界には理論上の議論がありますが、この選択肢の対応は逆転しています。',
       why75,['S52'])

(b.OUT/'changes_batch16.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D['Q_5_046'].update(status='確認済み',fixes_applied=True,independent_answer=2,sources=['S51'],
    option_verdicts=['日本固有語は和語であり誤り','中国語由来と日本での漢字音による造語を含み正しい','近年の現代中国語由来だけに限定して誤り','漢語の造語・翻訳語形成を否定して誤り'],
    stem_review='個別語の語史を問わず、語種としての漢語の由来と造語を問う形に限定。',
    explanation_review='国立国語研究所の語種説明と文化庁の漢語造語資料に全4肢・4解説を照合。',
    multiple_correct_risk='なし：正答2以外は和語との混同、時代限定、造語否定',no_correct_risk='なし：独立正答2',unresolved='')
D['Q_5_075'].update(status='確認済み',fixes_applied=True,independent_answer=1,sources=['S52'],
    option_verdicts=['文脈を明示した間接的依頼の可能性で正しい','意味論と語用論を取り違えて誤り','語用論的理解を不要とするため誤り','意味論と語用論の対象を逆転して誤り'],
    stem_review='間接依頼の成立を無条件にせず、共有知識と行為可能性が分かる状況を明示。',
    explanation_review='Searle原典の間接発話行為の定義・推論条件と大学公開論文の意味論／語用論の区別に照合。',
    multiple_correct_risk='なし：1のみ提示文脈で成立し得る説明',no_correct_risk='なし：独立正答1',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md'
p.write_text(p.read_text()+
 '\n| S51 | 国立国語研究所 [特集 コーパスで知る日本語史](https://kotoba.ninjal.ac.jp/digest/03/d-03-04/)、[中国語にとりいれられた日本語](https://kotoba.ninjal.ac.jp/qa/yokuaru/qa-169/)、文化庁 [第11期国語審議会審議経過](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kakuki/11/tosin01/04.html) | 国研本文で和語・漢語・外来語と古代中国語との対応、明治期に漢語を翻訳語へ用いた背景を確認。文化庁本文で漢字の造語力と漢語形成を確認。個別語「経済」「文化」の成立時期は本問から撤去し、承認対象外とした。 | Q_5_046 |\n'
 '| S52 | John R. Searle (1979), [Expression and Meaning](https://altexploit.files.wordpress.com/2019/10/john-r.-searle-expression-and-meaning-_-studies-in-the-theory-of-speech-acts-1979.pdf), Chapter 2 “Indirect Speech Acts”; 東京外国語大学学術成果コレクション [語の意味論](https://tufs.repo.nii.ac.jp/record/6188/files/acs055001.pdf) | Searle原典pp.30–49（PDF43–63頁）で、一つの発話内行為を別の行為を通じて間接的に行う定義、共有背景情報と推論、依頼例を確認。大学公開論文で意味論と、文脈・人間関係・話者の使用を扱う語用論の区別を確認。 | Q_5_075 |\n')
print('Recorded',len(extra),'repairs.')
