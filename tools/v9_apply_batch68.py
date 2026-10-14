"""Use the filler study's own interactional findings and limitations."""
import json,html
import quiz_audit as qa
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1341
d=json.loads((b.OUT/'decisions.json').read_text());_,q,a=qa.audit(str(b.DST));extra=[]
items={
'Q_5_093':(4,
'水上・山下（2007）「対話におけるフィラーの発話権保持機能の検証」の考察に合う記述を一つ選べ。',
['フィラーの後に話し手の発話が続いた割合が高ければ、それだけでフィラーが発話継続の原因になったと証明できる。','フィラーの後に聞き手が発話を始めた例は、相づちや助け舟を含め、すべて発話権保持の失敗である。','図形説明課題対話で得られた知見は、追加検討をせずに、あらゆる日常対話にそのまま適用できる。','フィラーは発話を続ける意思と生成作業中であることを示し、場合によっては聞き手の支援を促すものと考察されている。'],
['原論文5.1節は、発話が継続したという事実だけでは、フィラーの発話権保持機能の証拠にならないと注意しています。割合の高さだけから因果関係を結論づけることはできません。','原論文は、聞き手の相づちや助け舟が、話し手の発話継続を支える場合を区別しています。聞き手が発話したという事実だけで失敗と判定していません。','原論文の結語は、対象が図形説明課題対話であることを明示し、日常対話などへの適用可能性には追加の検討が必要だとしています。','原論文5.2節は、フィラーを、話し手が発話を続ける意思をもち、内容を生成していることを示すものと考察しています。発話権の保持が必ず成功するという意味ではありません。'],
['誤：著者が区別する記述的割合と機能の証拠を混同','誤：相づち・助け舟などの分類を無視','誤：結語の課題依存性への留保を無視','正：5.2節の考察に一致'],
'自己修正を必ず中間言語再構築の証拠とする旧解説や、フィラーの普遍的な評価・指導効果を除去。原研究の機能と限定を問う。'),
'Q_5_102':(1,
'水上・山下（2007）が分析した図形説明課題対話の、聞き手の発話に関する記述として、最も適当なものを一つ選べ。',
['聞き手の短い相づちや復唱は、話し手が発話を続けようとする意思を前提に、その継続を促す働きをすることがある。','聞き手が話し手の発話を先取りして完成させる行為は、どのような経緯でも必ず適切な支援になる。','フィラーの後に聞き手が発話を始めたら、その聞き手は常に話し手の継続意思を理解していない。','話し手がフィラーを発している間に聞き手が「はい」などと応答する例は、この研究の対話データには存在しない。'],
['原論文4.2.1節I-3は、聞き手の短い相づちや復唱を、話し手の発話継続の意思を前提として発話を促す行為として分析しています。','原論文は、話し手が言葉探しに窮したときの助け舟と、求められていない先取りの支援を区別しています。先取りを無条件に適切とはしていません。','原論文は、聞き手が話し手の継続意思を察したうえで、その先を言わせないように介入したと考えられる例も分析しています。','原論文の例8・9などには、フィラーの後の聞き手の「はい」「うん」があります。そうした応答を一律に発話権の奪取と扱う説明ではありません。'],
['正：4.2.1節I-3の分析に一致','誤：助け舟と求められない先取りを区別していない','誤：継続意思を察したからこその介入の分析と不一致','誤：例8・9の存在と不一致'],
'あいづち・協働的構築を常に好意的な配慮とする一般化と、未照合の言語間頻度比較・終助詞の補助主張を撤去。文脈に応じた聞き手の支援を問う。')}
for key,(ans,stem,opts,exps,verdicts,reason) in items.items():
 for field,olds,news in [('stem',[q[key]['stem']],[stem]),('options',q[key]['opts'],opts),('explanations',a['A_'+key[2:]]['txt'],exps)]:
  for i,(old,new) in enumerate(zip(olds,news)):
   if html.unescape(old)==new:continue
   e=dict(id=key,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=reason,sources=['S132'],applied=True,before_version='第67バッチ反映後の累積作業稿')
   if field=='options':e['stem_context']=stem
   if field=='explanations':e['paragraph_prefix']=str(i+1)+'（'+('正' if i+1==ans else '誤')+'）'
   extra.append(e)
 d[key].update(status='確認済み',independent_answer=ans,fixes_applied=True,sources=['S132'],option_verdicts=verdicts,reason=reason,stem_review='指定した原研究の対象と考察の範囲で全4肢を独立判定。',explanation_review='4.2.1節I-3、4.2.2節、5.1・5.2節、結語に全4解説を本文照合。原稿601–602頁の画像でも限定を確認。',unresolved='',multiple_correct_risk='なし：原研究の分析と限定に一致する肢は一つ',no_correct_risk='なし：独立正答'+str(ans))
for name,obj in [('changes.json',c+extra),('changes_batch68.json',extra),('decisions.json',d)]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(len(extra),'edits')
