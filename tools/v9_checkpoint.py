#!/usr/bin/env python3
"""v8 extraction and evidence-gated audit ledger. Never infers academic approval."""
import csv, hashlib, html, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import quiz_audit as qa

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit/v9'
SRC = ROOT / '登録日本語教員試験決定版問題集_v8_修正版.docx'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def release_ready(ledger, machine):
    """Academic approval alone must never bypass final machine and visual QA."""
    return (len(ledger) == 500 and all(r['status'] == '確認済み' for r in ledger)
            and machine.get('questions') == machine.get('answers') == 500
            and machine.get('full_visual_qa_completed') is True
            and machine.get('release_ready') is True)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    issues, qs, answers = qa.audit(str(SRC))
    assert len(qs) == len(answers) == 500
    versions = {}
    for v in (4,5,6):
        versions[v] = qa.audit(str(ROOT / f'登録日本語教員試験決定版問題集_v{v}_修正版.docx'))[1]
    decisions_path = OUT / 'decisions.json'
    decisions = json.loads(decisions_path.read_text()) if decisions_path.exists() else {}
    ledger = []
    for key, q in qs.items():
        a = answers['A_' + key[2:]]
        changed = {f'v{v-1}→v{v}': [n+1 for n in range(4) if versions[v-1][key]['opts'][n] != versions[v][key]['opts'][n]] for v in (5,6)}
        d = decisions.get(key, {})
        status = d.get('status', '要追加確認')
        assert status in ('確認済み', '修正必要', '要追加確認')
        if status == '確認済み':
            assert d.get('sources') and len(d.get('option_verdicts', [])) == 4 and d.get('explanation_review') and d.get('stem_review')
        ledger.append(dict(id=key, status=status, content_reviewed=d.get('content_reviewed',False),
            source_v8_sha256=digest(SRC), stem=html.unescape(q['stem']), options=[html.unescape(o) for o in q['opts']],
            original_answer=int(a['ans']), explanations=[html.unescape(t) for t in a['txt']],
            priority='重点確認（v5/v6選択肢変更）' if any(changed.values()) else '通常',
            historical_changed_options=changed, structure='構造検査実施済み・学術的判定とは別',
            machine_flags=[list(i) for i in issues if i[1] in (key,'A_'+key[2:])],
            independent_answer=d.get('independent_answer'), option_verdicts=d.get('option_verdicts',[]),
            candidate_answers=d.get('candidate_answers',[]), multiple_correct_risk=d.get('multiple_correct_risk','未判定'),
            no_correct_risk=d.get('no_correct_risk','未判定'), fixes_applied=d.get('fixes_applied',False),
            stem_review=d.get('stem_review','未実施'), explanation_review=d.get('explanation_review','未実施'),
            sources=d.get('sources',[]), reason=d.get('reason','未精読・出典照合未実施。構造検査の合格を学術的確認済みとは扱わない。'),
            unresolved=d.get('unresolved','正答・各誤答・解説を独立に精査し、根拠本文と照合する。')))
    (OUT/'ledger.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+'\n')
    with (OUT/'ledger.csv').open('w', newline='', encoding='utf-8-sig') as f:
        fields=['id','status','content_reviewed','priority','original_answer','independent_answer','stem','options','explanations','option_verdicts','reason','sources','unresolved','historical_changed_options']
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in ledger: w.writerow({k: json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],(dict,list)) else r[k] for k in fields})
    reviewed = sum(r['content_reviewed'] for r in ledger)
    (OUT/'ledger.md').write_text(f'# 全500問監査台帳\n\n内容精読は{reviewed}問で実施済み。「要追加確認」は資料照合等の残件を示す。構造検査と学術的な確認を区別する。ledger.json / ledger.csv の設問・選択肢・解説の原文はv8スナップショット。改訂後の本文はchanges.jsonと累積作業稿を参照。\n\n| 問題ID | 判定 | 内容精読 | 優先度 | 所見 |\n|---|---|---|---|---|\n'+''.join(f"| {r['id']} | {r['status']} | {'済' if r['content_reviewed'] else '未'} | {r['priority']} | {r['reason'].replace('|','／')} |\n" for r in ledger))
    (OUT/'baseline_machine.json').write_text(json.dumps({'issues':issues,'statistics':qa.stats(qs,answers)},ensure_ascii=False,indent=2)+'\n')
    manifest={'base_commit':'367d6488f7e81c78c1a0161c52a7d8db804a5991','source_file':SRC.name,'source_sha256':digest(SRC),'questions':len(qs),'answers':len(answers),'content_reviewed':sum(r['content_reviewed'] for r in ledger),'status_counts':{s:sum(r['status']==s for r in ledger) for s in ('確認済み','修正必要','要追加確認')},'v5_v6_priority_questions':sum(r['priority'].startswith('重点') for r in ledger),'release_ready':all(r['status']=='確認済み' for r in ledger)}
    machine_path = OUT/'postfix_machine.json'
    machine = json.loads(machine_path.read_text()) if machine_path.exists() else {}
    manifest['academic_audit_complete'] = all(r['status']=='確認済み' for r in ledger)
    manifest['full_visual_qa_completed'] = machine.get('full_visual_qa_completed') is True
    manifest['release_ready'] = release_ready(ledger, machine)
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
