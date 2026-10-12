#!/usr/bin/env python3
"""Adopt an explicitly identified IPAL classification for Q5-073."""
import json, html
import v9_apply_batch1 as b
import quiz_audit as qa
prior=json.loads((b.OUT/'changes.json').read_text())
assert len(prior)==337
_,Q,A=qa.audit(str(b.DST))
extra=[]
why='旧稿の顔の身体分類と比喩三分類の一括帰属を撤去。IPAL解説編の類似性・隣接性・カテゴリ包摂の区別を明示して全肢を再構成。'
def record(field,index,new):
    old=Q['Q_5_073']['stem'] if field=='stem' else Q['Q_5_073']['opts'][index] if field=='options' else A['A_5_073']['txt'][index]
    extra.append(dict(id='Q_5_073',field=field,index=index,before=html.unescape(old),after=new,reason=why,sources=['S54'],applied=True,before_version='第17修正バッチ作業稿'))
record('stem',None,'『計算機用日本語基本名詞辞書 IPAL 解説編』（1996）の分類における比喩的な意味拡張について、適切な説明はどれか。')
opts=['形状や機能などの類似に基づく拡張をメトニミーという。','容器でその中身を指すような隣接関係による拡張をメタファーという。','形状や性質などの類似に基づく拡張をメタファーという。','カテゴリ全体でその一部を指す包摂関係による拡張をメタファーという。']
exps=['同資料では、形状や性質、機能、状況などの類似による拡張はメタファー（隠喩）です。メトニミー（換喩）ではありません。','同資料では、容器から中身へなど、隣接関係による拡張はメトニミー（換喩）です。メタファー（隠喩）ではありません。','同資料では、形状や性質などが似ていることに基づく拡張をメタファー（隠喩）とします。類似性と隣接性を区別するこの分類に一致します。','同資料では、カテゴリ全体とその一部という包摂関係による拡張はシネクドキー（提喩）です。また、カテゴリの包摂関係と、物の全体部分関係とを区別しています。']
for i,t in enumerate(opts):record('options',i,t)
for i,t in enumerate(exps):record('explanations',i,t)
(b.OUT/'changes_batch18.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
(b.OUT/'changes.json').write_text(json.dumps(prior+extra,ensure_ascii=False,indent=2)+'\n')
D=json.loads((b.OUT/'decisions.json').read_text())
D['Q_5_073'].update(status='確認済み',fixes_applied=True,independent_answer=3,sources=['S54'],option_verdicts=['類似性を換喩とするため誤り','隣接性を隠喩とするため誤り','類似性による隠喩の定義で正しい','カテゴリ包摂を隠喩とするため誤り'],stem_review='採用資料と分類体系を明記し、未照合の個別例を撤去。',explanation_review='IPAL解説編印刷頁212–214の定義・注意事項に全4肢・4解説を照合。',reason=why,multiple_correct_risk='なし：指定体系で3のみ正しい',no_correct_risk='なし：独立正答3',unresolved='')
(b.OUT/'decisions.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
p=b.OUT/'sources.md'
p.write_text(p.read_text()+'\n| S54 | 情報処理振興事業協会技術センター（1996）[IPAL基本名詞辞書 解説編](https://www2.ninjal.ac.jp/dictionaries/IPALBN/IPALBN_manual.pdf) | 国立国語研究所公開版。印刷頁212–214（PDF223–225頁）の本文を取得・精読。類似性の隠喩、隣接性の換喩、カテゴリ包摂の提喩を区別。物理的全体部分関係とカテゴリ包摂を混同しない注意も確認。顔が広いの個別帰属は承認せず撤去。 | Q_5_073 |\n')
for name in ['README.md','interim_report.md']:
 p=b.OUT/name;t=p.read_text();t=t.replace('66問337箇所','67問346箇所').replace('66問を部分修正','67問を部分修正')
 if name=='README.md':t=t.replace('| 38問 |','| 39問 |').replace('| 129問 |','| 128問 |').replace('修正必要129問','修正必要128問')
 else:t=t.replace('66問・337箇所','67問・346箇所').replace('修正必要129問','修正必要128問')
 p.write_text(t)
for name in ['interim_report.md','critical_findings.md']:
 p=b.OUT/name;p.write_text(p.read_text()+'\n## 第18バッチ（2026-10-12）\n\nQ_5_073の旧稿にあった顔の身体分類と比喩三分類の一括帰属を撤去。IPAL解説編の分類体系を指定した定義問題へ設問・全4肢・全4解説を改訂し、独立正答3を確定。確認済み39・修正必要128・要追加確認333、累積67問346箇所。\n')
print('Recorded',len(extra),'repairs')
