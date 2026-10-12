#!/usr/bin/env python3
"""Source-gate intransitive and possessive passives without unverified historical facts."""
import json,html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text());assert len(prior)==470
_,Q,A=qa.audit(str(b.DST));extra=[];D=json.loads((b.OUT/'decisions.json').read_text())
def item(k,stem,opts,exps,ans,why,verdicts):
 for field,vs in [('stem',[stem]),('options',opts),('explanations',exps)]:
  for i,new in enumerate(vs):
   old=Q[k]['stem'] if field=='stem' else Q[k]['opts'][i] if field=='options' else A['A_'+k[2:]]['txt'][i]
   extra.append(dict(id=k,field=field,index=None if field=='stem' else i,before=html.unescape(old),after=new,reason=why,sources=['S65'],applied=True,before_version='第26修正バッチ作業稿'))
 D[k].update(status='確認済み',fixes_applied=True,independent_answer=ans,sources=['S65'],option_verdicts=verdicts,reason=why,stem_review='同じ自動詞の能動・使役・受身の区別、所有受身の主語と所有物の格関係を明示。',explanation_review='国際交流基金2014年7月受身文の所有受身の基本形と自動詞受身の本文に全4肢・4解説を照合。',unresolved='',multiple_correct_risk=f'なし：{ans}のみ提示条件に一致',no_correct_risk=f'なし：独立正答{ans}')
item('Q_5_055','子供が泣いたことによって私が困ったことを、自動詞「泣く」の受身で表す文はどれか。',
 ['子供が泣いて、私は困った。','私は子供を泣かせた。','私は子供に泣かれて困った。','子供が泣いている。'],
 ['子供が泣いたことと私が困ったことを述べる文として成立しますが、「泣く」は能動の形であり、設問が求める受身ではありません。','私が子供を泣かせるという使役の文です。子供の泣く行為によって私が困るという自動詞受身の文ではありません。','自動詞「泣く」の受身「泣かれる」を用い、子供が泣くことによって私が困ったことを、私を主語として表しています。','子供が泣いていることを能動の形で述べています。設問が求める、私が困ることを表す自動詞受身ではありません。'],3,
 '迷惑受身と間接受身を無条件に同義として分類する旧設問を撤去。文脈と自動詞受身の形を明示し、能動の言い換えも誤用とは扱わない。',['意味は成立するが能動形で誤答','使役であり受身でなく誤答','自動詞受身で主語の迷惑を述べ正しい','能動のテイルで受身でなく誤答'])
item('Q_5_067','「私は子供にカメラをこわされた」のような所有受身について、適切な説明はどれか。',
 ['所有者を主語として、所有物を「を」で示し、その所有物に及んだ影響を述べる。','所有受身は必ず被害だけを表すため、「先生に作文をほめられた」は所有受身として扱えない。','この文では、カメラが主語で、私はカメラをこわした動作主である。','日本語では自動詞の受身を作ることができず、「子供に泣かれて困った」は受身として成立しない。'],
 ['この文では私が所有者・主語、子供が動作主、カメラが影響を受けた所有物です。所有物を「を」で示す所有受身の基本形に合います。','所有受身には被害・迷惑以外の例もあります。国際交流基金は「先生に作文をほめられた」も所有受身の例に挙げています。','文の役割を取り違えています。主語は私で、カメラは「を」で示された所有物です。こわした動作主は「に」で示された子供です。','国際交流基金の解説には「子供に泣かれて困った」などの自動詞受身があります。自動詞から受身を一切作れないという説明は誤りです。'],1,
 '法隆寺の建造者という未確認の歴史的断定を撤去。所有受身の主語・所有物・動作主を公的教材の例で問う。所有受身が被害だけとは限らないことも反映。',['所有受身の主語と所有物の格で正しい','被害だけに限定して誤り','所有物と主語と動作主を逆転して誤り','自動詞受身を全否定して誤り'])
(b.OUT/'changes_batch27.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md';p.write_text(p.read_text()+'\n| S65 | 国際交流基金 [文法を楽しく 受身文](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/201407.html) | 本文と例1–3、質問3–4への説明を取得・精読。所有者を主語・所有物をヲ格とする基本形、作文をほめられる非被害例、自動詞泣くの受身と能動での言い換えも成立する点を確認。歴史的建造者の断定や全受身分類体系は本問から撤去。 | Q_5_055、067 |\n')
print('Recorded',len(extra),'repairs')
