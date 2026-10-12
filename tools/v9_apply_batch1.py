#!/usr/bin/env python3
"""Apply individually documented corrections to a separate, explicitly unfinished draft."""
import hashlib, html, json, sys, zipfile
from pathlib import Path
from docx import Document
sys.path.insert(0,str(Path(__file__).parent))
import quiz_audit as qa
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit/v9'
SRC=ROOT/'登録日本語教員試験決定版問題集_v8_修正版.docx'
DST=OUT/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'
EXPECTED='4aef79631da7096e5837dd31473978d40d4932ba3cf8473c52138662a843d498'
ROWS={r['id']:r for r in json.loads((OUT/'ledger.json').read_text())}
CHANGES=[]

def change(key,field,index,new,reason,sources):
    old=ROWS[key][field][index] if index is not None else ROWS[key][field]
    CHANGES.append({'id':key,'field':field,'index':index,'before':old,'after':new,'reason':reason,'sources':sources,'state':'作業稿に適用。全問監査完了を意味しない。'})

change('Q_1_006','explanations',2,'伊沢修二は、台湾語や漢字漢文を媒介として日本語の意味を理解させる「対訳法」を推進しました。台湾の初期日本語教育における対訳法と、後に山口喜一郎らが実践したグアン法を区別する必要があります。','伊沢の対訳法と山口らのグアン法を混同していた。',['S01'])
change('Q_1_013','stem',None,'高度人材ポイント制による在留資格「高度専門職1号」に関する記述として、最も適切なものを一つ選びなさい。','5年が付与される1号と無期限の2号を区別。ポイント制の対象を明示。',['S02'])
change('Q_1_013','options',2,'学歴・職歴・年収などを評価する高度人材ポイント制により認定され、「高度専門職1号」では5年の在留期間の付与や、所定の要件を満たす場合の永住許可要件の緩和などの優遇措置がある。','全活動区分に同じ年収下限を課す読みと、2号も5年とする読みを避ける。',['S02'])
change('Q_1_013','explanations',2,'高度人材ポイント制では、活動区分に応じた学歴・職歴・年収などの評価により、所定の基準を満たす外国人に優遇措置が認められます。「高度専門職1号」の在留期間は5年です。一方、「高度専門職2号」は在留期間が無期限となる別の区分です。永住許可は自動的に得られるものではなく、別途その要件を満たす必要があります。','対象区分と永住の条件を分ける。現行申請要件の完全な照合は継続。',['S02'])
change('Q_1_019','stem',None,'地域日本語教育の推進に関する国の施策、および「地域日本語教育コーディネーター」の役割に関する記述として、最も適切なものを一つ選びなさい。','2024年4月の文部科学省への移管を反映。',['S06'])
change('Q_1_019','explanations',1,'国は、自治体等と連携した地域日本語教育の体制整備を支援しています。日本語教育の所管は、2024年4月に文化庁から文部科学省へ移管しました。地域の実情に応じた取組を自治体が進めることは、地域日本語教育の推進に重要です。','現在の所管と旧資料の作成主体を区別する。',['S06'])
change('Q_1_023','options',2,'伊沢修二が推進した初期の日本語教授法は、台湾語や漢字漢文を媒介として用いることを禁止し、日本語だけを用いて教える方法であった。','架空・不明確な名称によって対訳法を誤答化せず、誤りの所在を明確にする。',['S01'])
change('Q_1_023','options',3,'1895年に台北郊外に設立された芝山巌学堂では、現地住民への組織的な日本語教育が始まり、後の国語伝習所や公学校での日本語教育へとつながった。','直接教えるを直接法と誤読させない。',['S01'])
change('Q_1_023','explanations',0,'伊沢修二は、台湾語や漢字漢文を媒介とする対訳法を推進しました。現地の言語を一切排除したという記述は誤りです。後の山口喜一郎らによるグアン法の実践と区別して理解する必要があります。','対訳法と直接法の混同を修正。',['S01'])
change('Q_1_023','explanations',2,'初期の日本語教育で用いられた対訳法は、台湾語や漢字漢文を日本語の意味理解に利用する方法でした。媒介語を禁止し、日本語だけを用いたという選択肢の説明は、この方法と一致しません。','新しい誤答の内容と対応させる。',['S01'])
change('Q_1_027','explanations',1,'1983年の「留学生10万人計画」以後、留学生の受入れ拡大に伴い、日本語教育機関の質を確保する仕組みの整備が進みました。日本語教育振興協会の沿革には、1989年の設立と、日本語教育施設の審査・認定事業の開始が記載されています。','確認できない審査・昇格基準という名称を、協会が公表する審査・認定事業に修正。',['S07'])
change('Q_1_032','options',1,'本法律は、日本語教育の推進に関する施策を総合的かつ効果的に推進し、多様な文化を尊重した共生社会の実現や、諸外国との交流の促進に寄与することを目的としている。','第1条の目的と第3条の基本理念を区別。',['S03'])
change('Q_1_032','explanations',0,'第11条では、地方公共団体が政府の基本方針を参酌し、地域の実情に応じて、日本語教育の推進に関する施策の基本的な方針を定めるよう努めることが規定されています。策定を禁止した規定ではありません。','法文の基本的な方針と自治体が独自に用いる計画名を区別。',['S03'])
change('Q_1_032','explanations',1,'共生社会の実現や諸外国との交流の促進は、第1条の目的に掲げられています。第3条は、日本語教育を希望する外国人等の学習機会の確保など、日本語教育の推進に当たっての基本理念を定めています。','目的条項と理念条項の帰属を正確にする。',['S03'])
change('Q_1_032','explanations',2,'第8条は、政府が日本語教育の推進に関する施策を実施するために必要な法制上または財政上の措置その他の措置を講じなければならないと定めています。学習者本人にすべての費用を負担させる規定ではありません。','政府の措置義務を国・地方双方の努力義務と取り違えていた。',['S03'])
change('Q_1_032','explanations',3,'本法律の第2条にいう「外国人等」には、日本語に通じない外国人に加え、日本の国籍を有する者も含まれます。海外の大学留学生だけに対象を限定した法律ではありません。','法の対象に日本国籍者も含まれる。',['S03'])
change('Q_1_033','explanations',0,'第4条は、国が日本語教育の推進に関する施策を総合的に策定・実施する責務を定めています。第5条は、地方公共団体が国との適切な役割分担を踏まえ、地域の状況に応じた施策を策定・実施する責務を定めています。','国と地方の条文上の責務をそれぞれ記述。',['S03'])
change('Q_1_036','explanations',2,'OPIは、初級（Novice）、中級（Intermediate）、上級（Advanced）、超級（Superior）などのACTFLの尺度で発話能力を評価する面接です。初級・中級・上級にはLow・Mid・Highの下位区分がありますが、超級を同様に3分割するわけではありません。「N1〜N5」はJLPTのレベル表記です。','超級までHigh/Mid/Lowに分割すると読める説明を修正。',['S08'])
change('Q_2_008','explanations',3,'日本国憲法第1条は天皇の地位等について定めた条文であり、日本語を唯一の公用語・国家語とする規定ではありません。一方、裁判所法第74条には、裁判所では日本語を用いる旨の規定があります。国全体の公用語の指定と、特定の公的領域で使用する言語の規定は区別する必要があります。','日本語使用を直接定める法律は存在しないという全面否定を修正。',['S09'])
change('Q_2_021','explanations',2,'二重敬語は、一つの語に同じ種類の敬語を重ねることです。一つの文で異なる人物に尊敬語と謙譲語を使うこと自体は二重敬語ではありません。また、同じ動詞に重ねる二重敬語と、別々の動詞を敬語にして「て」で結ぶ敬語連結は区別されます。敬語連結は、それぞれの敬語の使い方と意味のつながりが適切であれば許容されます。','敬語連結を慣用的二重敬語の例として説明していた。',['S04'])
change('Q_2_023','options',2,'「持って参りました」の「参る」は、学習者側の動作を聞き手に丁重に述べる謙譲語Ⅱである。「ご覧になってください」は教師の動作に尊敬語を用いた表現であり、より控えめに確認を依頼したい場面では「ご覧いただけますか」などを選ぶこともできる。','てくださいが目上には一律不適切という設問の前提を撤回し、敬語形式と場面に応じた選択を問う。',['S04'])
change('Q_2_023','explanations',1,'「ご覧になる」は尊敬語ですが、あらゆる場面で最高の敬意を表す完璧な依頼表現とすることはできません。相手との関係や依頼の内容に応じて、表現を選ぶ必要があります。','敬語形式の正しさと、唯一最適・最高という断定を区別。',['S04'])
change('Q_2_023','explanations',2,'「参る」は謙譲語Ⅱであり、学習者側の動作を教師に丁重に述べています。後半の「ご覧になる」は教師の動作を立てる尊敬語です。依頼の適切さは相手との関係や負担にもよるため、「〜てください」を一律に誤用とせず、必要に応じて「ご覧いただけますか」などの疑問形を選ぶことができます。','語用上の選択を文法的誤用と混同しない。',['S04'])
change('Q_2_023','explanations',3,'「持って参りました」の「参る」は、学習者側の動作を話し相手に丁重に述べる謙譲語Ⅱです。教師の動作を高める尊敬語を自分に用いたものではないため、この理由で誤用とすることはできません。','後半のてくださいに必ず問題があるという解説を削除。',['S04'])
change('Q_2_025','options',0,'社外の顧客に自社の社長の動作を述べる場合は、社長が話し手より目上であることだけを理由に、必ず尊敬語を用いて社長を高めなければならない。','会社内外の条件がない元の誤答は、社長が参るが適切な文脈でも成立し得た。',['S04'])
change('Q_2_025','explanations',0,'社外の顧客に自社の社長の動作を述べる場合、社長を話し手側の人物として扱い、尊敬語を用いずに述べることがあります。「参る」は謙譲語Ⅱであり、話し手側の社長の動作を顧客に丁重に述べる場合にも使えます。社長だから必ず尊敬語とすることはできません。','社長の動作に参るは常に誤りとする断定を修正。',['S04'])
change('Q_4_123','options',1,'営利を目的として設置されていない学校その他の教育機関で、教員や授業を受ける者は、授業の過程での利用に必要な限度で公表された著作物を複製・公衆送信できる。ただし、著作権者の利益を不当に害する場合は除かれ、公衆送信には原則として補償金の支払いが必要である。','非営利・但書・公衆送信補償金の重要条件を補う。',['S10'])
change('Q_4_123','explanations',1,'第35条第1項は、営利目的で設置された機関を除く学校その他の教育機関で、教員や授業を受ける者が授業の過程で利用する場合を対象とします。利用は必要な限度に限られ、著作権者の利益を不当に害する場合は認められません。公衆送信には第2項による補償金の支払いが原則として必要で、第3項の例外もあります。','本文の要件と補償金を落とさない。',['S10'])
change('Q_4_123','explanations',3,'第35条第1項の対象となる非営利の教育機関で、授業の過程での利用に必要な限度の複製は、著作権者の許諾なしに行える場合があります。ただし、著作権者の利益を不当に害する場合は認められません。どのような紙の複製でも必ず個別の許諾が必要という説明は誤りです。','必要な範囲だけで無条件に複製可とはしない。',['S10'])

def replace_paragraph(paragraph,old,new):
    # Preserve existing runs, bookmark anchors and tag colors. The replacement
    # is inserted only in the first run that overlaps the old body text.
    txt=''.join(r.text for r in paragraph.runs)
    start=txt.find(old)
    if start<0: return False
    assert txt.count(old)==1
    end=start+len(old); position=0; inserted=False
    for run in paragraph.runs:
        s=run.text; a=position; b=a+len(s); position=b
        if b<=start or a>=end: continue
        prefix=s[:max(0,start-a)]; suffix=s[max(0,end-a):] if end<b else ''
        run.text=prefix+(new if not inserted else '')+suffix
        inserted=True
    assert inserted and old not in paragraph.text
    return True

def main():
    assert hashlib.sha256(SRC.read_bytes()).hexdigest()==EXPECTED
    doc=Document(SRC)
    for c in CHANGES:
        matched=[p for p in doc.paragraphs if c['before'] in p.text]
        assert len(matched)==1,(c['id'],c['field'],len(matched))
        assert replace_paragraph(matched[0],c['before'],c['after'])
    doc.save(DST)
    assert hashlib.sha256(SRC.read_bytes()).hexdigest()==EXPECTED
    assert zipfile.ZipFile(DST).testzip() is None
    before,q0,a0=qa.audit(str(SRC)); after,q1,a1=qa.audit(str(DST))
    assert set(q0)==set(q1) and set(a0)==set(a1) and len(q1)==500
    assert all(a0[k]['ans']==a1[k]['ans'] for k in a0)
    changed_ids={c['id'] for c in CHANGES}
    def normalized(value):
        if isinstance(value,str): return html.unescape(value)
        if isinstance(value,list): return [normalized(x) for x in value]
        if isinstance(value,dict): return {k:normalized(v) for k,v in value.items()}
        return value
    assert all(normalized(q0[k])==normalized(q1[k]) and normalized(a0['A_'+k[2:]])==normalized(a1['A_'+k[2:]]) for k in q0 if k not in changed_ids)
    fatal={'S1','S3','S4','S5','S6','N1','N2'}
    assert not [i for i in after if i[0] in fatal]
    (OUT/'changes.json').write_text(json.dumps(CHANGES,ensure_ascii=False,indent=2)+'\n')
    (OUT/'changes.md').write_text('# 修正前後の比較（第1バッチ・監査作業中）\n\n適用済みは出典による再判定や全問監査完了を意味しない。\n\n| ID | 対象 | 修正前 | 修正後 | 理由 | 根拠 |\n|---|---|---|---|---|---|\n'+''.join(f"| {c['id']} | {c['field']} {'' if c['index'] is None else c['index']+1} | {c['before'].replace('|','／')} | {c['after'].replace('|','／')} | {c['reason']} | {', '.join(c['sources'])} |\n" for c in CHANGES))
    validation={'questions':len(q1),'answers':len(a1),'v8_unchanged':True,'answers_unchanged':True,'unmodified_questions_unchanged':True,'changed_questions':len(changed_ids),'replacements':len(CHANGES),'issues':after,'statistics':qa.stats(q1,a1),'full_visual_qa_completed':False,'release_ready':False}
    (OUT/'postfix_machine.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
    d=json.loads((OUT/'decisions.json').read_text())
    for key in changed_ids:
        d[key]['fixes_applied']=True
        d[key]['sources']=sorted({s for c in CHANGES if c['id']==key for s in c['sources']})
        d[key]['unresolved']='作業稿へ修正済み。関連する全選択肢・解説の残存主張を原資料と照合し、最終再判定・全頁目視検査が必要。'
    (OUT/'decisions.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in validation.items() if k not in ('issues','statistics')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
