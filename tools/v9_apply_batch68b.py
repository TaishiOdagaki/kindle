"""Align the distractor's temporal condition exactly with its cited examples."""
import json
import v9_apply_batch1 as b
c=json.loads((b.OUT/'changes.json').read_text());assert len(c)==1359
e=dict(id='Q_5_102',field='options',index=3,before='話し手がフィラーを発している間に聞き手が「はい」などと応答する例は、この研究の対話データには存在しない。',after='話し手のフィラーの後に、聞き手が「はい」などと応答する例は、この研究の対話データには存在しない。',reason='例8・9と解説が扱う時間条件はフィラーの後である。初回改訂の間という条件を本文に合わせ、誤答判定の根拠を一致させる。',sources=['S132'],applied=True,before_version='第68バッチ反映後の累積作業稿',stem_context='水上・山下（2007）が分析した図形説明課題対話の、聞き手の発話に関する記述として、最も適当なものを一つ選べ。')
for name,obj in [('changes.json',c+[e]),('changes_batch68b.json',[e])]:
 (b.OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
