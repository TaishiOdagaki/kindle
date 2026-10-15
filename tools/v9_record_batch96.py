"""Record only after direct inspection of the batch96 completed page images."""
import json,hashlib,subprocess,re,io,csv,bisect
from pathlib import Path
from PIL import Image
p=Path('audit/v9');root=Path('/workspace/scratch/697c245d9771');render=root/'batch96-qa';targets={'Q_M_053','Q_M_054','Q_M_056'}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def records(data):
 s=io.StringIO(data.decode('utf-8-sig'),newline='');r=csv.reader(s);out=[]
 while True:
  start=s.tell()
  try:row=next(r)
  except StopIteration:break
  out.append((row[0],s.getvalue()[start:s.tell()]))
 return out
old=records(subprocess.check_output(['git','show','HEAD:audit/v9/ledger.csv']));new=dict(records((p/'ledger.csv').read_bytes()))
(p/'ledger.csv').write_bytes(b'\xef\xbb\xbf'+''.join(new[k].replace('\r\n','\n') if k in targets else raw for k,raw in old).encode())
m=json.loads((p/'manifest.json').read_text());assert m['status_counts']=={'確認済み':248,'修正必要':52,'要追加確認':200}
cs=json.loads((p/'changes_batch96.json').read_text());assert len(cs)==27
pages=subprocess.check_output(['pdftotext','-layout',str(render/'qa.pdf'),'-']).decode().split('\f')[:-1];norm=[re.sub(r'\s+','',t) for t in pages];whole=''.join(norm);bounds=[0]
for t in norm:bounds.append(bounds[-1]+len(t))
matches={}
for c in cs:
 needle=re.sub(r'\s+','',c['after']);start=0;found=set()
 while (at:=whole.find(needle,start))>=0:
  found.update(range(bisect.bisect_right(bounds,at),bisect.bisect_right(bounds,at+len(needle)-1)+1));start=at+1
 matches[str((c['id'],c['field'],c['index']))]=sorted(found)
assert all(matches.values());reviewed=sorted({x for v in matches.values() for x in v})
for x in reviewed:
 with Image.open(render/f'review-{x}.png') as im:im.load()
machine=json.loads((p/'postfix_machine.json').read_text());prior=json.loads(subprocess.check_output(['git','show','HEAD:audit/v9/postfix_machine.json']));added=[i for i in machine['issues'] if i not in prior['issues']];removed=[i for i in prior['issues'] if i not in machine['issues']]
assert added==[['V1','表記ゆれ',"{'モダリティ': 7, 'ムード': 3}"]]
assert removed==[['V1','表記ゆれ',"{'モダリティ': 10, 'ムード': 3}"]]
assert len(machine['issues'])==60
f=p/'README.md';s=f.read_text()
for a,b in [('245問','248問'),('53問','52問'),('202問','200問'),('258問2148箇所','261問2175箇所'),('258問を','261問を')]:s=s.replace(a,b)
f.write_text(s)
sources={
'S154':{'url':'https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/052.html','title':'助詞とは 解説','scope':'全84行を本文取得・精読。17〜73行の格助詞・接続助詞・副助詞・終助詞の4分類。','targets':['Q_M_053']},
'S155':{'url':'https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/095.html','title':'副助詞 解説','scope':'全250行を本文取得・精読。15行の名称併記、54〜99行の「も」の並立・付加と「だけ」の限定、193〜204行の「さえ」の添加・最低条件も確認。改訂問はだけ・もに限定。','targets':['Q_M_053']},
'S156':{'url':'https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/079.html','title':'V＋N 解説','scope':'全88行を本文取得・精読。17〜43行の名詞に先行する修飾部分、60〜68行の連体修飾節と「こわれたコンピューター」。85行の内外の関係への留保も読み、全修飾節に同じ意味関係を課さない。','targets':['Q_M_054']},
'S157':{'url':'https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/076.html','title':'～かもしれません・～にちがいありません 解説','scope':'全212行を本文取得・精読。68〜100行「はずです」の根拠に基づく推論、推論と現実の不一致、直感的確信との区別。後半のそうだ・ようだ・らしい全用法や確率尺度は対象の承認に流用しない。','targets':['Q_M_056']}}
for k,v in sources.items():v.update(sha256=sha(root/f'{k}-96.html'),retrieved='2026-10-16 JST',acquisition='Full public HTML body, not search snippet',limits='指定教材の分類と用例の説明に限定。全学説・全話者の普遍的判断や指導の因果効果を承認しない。')
report=f'''

## 第96バッチ（2026-10-16）

最新GitHub HEAD d2683a89c1290a5630523507e58896bb92035e44をfetchし、専用の新規作業場へ復元。README・manifest・decisions・changes・sources・postfix_machineを引き継ぎ、初期生成スクリプトは再実行していない。

東京外国語大学言語モジュール「助詞とは」「副助詞」「V＋N」「～かもしれません・～にちがいありません」のHTML全文を取得し、設問・全4肢・独立正答・全4解説を照合した。Q_M_053は「だけ」「も」に例を限定し、副助詞・取り立て助詞という指定教材の名称を明記。他分類との対応を教材本文で確認し、全学説の同一性は仮定しない。Q_M_054は「節＝必ず複数語」という旧解説の誤りを撤回し、述語を含むまとまりが後続名詞を修飾する関係を問う。Q_M_056は予定表と変更なしという根拠を与えた模式例に改訂。「はずだ」の推論を、直接観察済みの事実、根拠のない直感、結果の保証と区別する。語句の使用頻度や教授効果の保証を根拠なしに追加しない。

3問27箇所、独立正答3・4・3で番号変更なし。確認済み248・修正必要52・要追加確認200、残件252。累積261問2175箇所。全500問・解説500件、元v8のSHA256、影響外本文、リンク・正解表・正誤タグを機械検査し維持。公開可否回帰8条件に合格。機械警告は60件で、V1「モダリティ／ムード」の出現数だけが10／3から7／3に変わり、他59件は不変。新種の構造警告はない。台帳の原文はv8スナップショットで、改訂はchangesと作業稿を参照する。

documents手順でNoto Sans JPを適用したQAコピーを{len(pages)}頁描画し、変更文字列のある{'・'.join(map(str,reviewed))}頁を150dpi Cairo画像で直接目視。27変更文字列は改頁をまたぐ場合も含めてPDF中で検出した。全頁最終目視と残252問の根拠照合は未了。作業稿は最終v9ではなく出版不可。
'''
for name in ['interim_report.md','critical_findings.md']:
 f=p/name;assert '## 第96バッチ' not in f.read_text();f.write_text(f.read_text()+report)
f=p/'sources.md';s=f.read_text()+'\n\n## 第96バッチ 大学公開文法教材（2026-10-16）\n\n| ID | 資料 | 取得範囲・限界 | 対象 |\n|---|---|---|---|\n'
for k,v in sources.items():
 assert '| '+k+' |' not in s
 s+='| '+k+' | 東京外国語大学 ['+v['title']+']('+v['url']+') | '+v['scope']+' '+v['limits']+' | '+'・'.join(v['targets'])+' |\n'
f.write_text(s+'\n上記は公開HTML本文であり検索抜粋のみの承認ではない。作成・更新日の表示が明確でないため刊年を推定しない。取得原バイトのハッシュはevidence/batch96_review.jsonへ記録し、本文全文は転載しない。\n')
f=p/'visual_qa.md';f.write_text(f.read_text()+f'\n\n## 第96バッチ\nNoto Sans JP適用コピー{len(pages)}頁を描画し、27変更文字列のある'+ '・'.join(map(str,reviewed))+f'頁を150dpi Cairo画像で直接目視。全頁最終目視は未了。\n')
e={'batch':96,'base_commit':'d2683a89c1290a5630523507e58896bb92035e44','fully_rejudged':sorted(targets),'edits':27,'status_counts':m['status_counts'],'remaining':252,'independent_answers':{'Q_M_053':3,'Q_M_054':4,'Q_M_056':3},'sources':sources,'machine_warnings':60,'new_machine_warnings':added,'removed_machine_warnings':removed,'readiness_gate':'8 cases passed','render_pages':len(pages),'visually_reviewed_pages':reviewed,'review_image_dpi':150,'all_changed_strings_found_in_pdf':matches,'full_visual_qa_completed':False,'font':'Noto Sans JP QA copy only','font_sha256':sha(root/'NotoSansJP94.ttf'),'docx_sha256':sha(p/'登録日本語教員試験決定版問題集_v9_監査作業中.docx'),'pdf_sha256':sha(render/'qa.pdf'),'page_sha256':{str(x):sha(render/f'review-{x}.png') for x in reviewed},'release_ready':False}
e['machine_delta_review']='V1の用語出現数のみ10/3から7/3へ更新。他59件は同一。新たな構造不良ではない。'
e['pagination_followup']='対象3問の設問・4選択肢・各4解説はそれぞれ同一頁内に収まり、欠字・重なり・本文クリッピングなし。Q_M_054の戻るリンクだけは次頁へ分離しており最終組版で再確認する。'
(p/'evidence/batch96_review.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('Recorded3 fullreviews/27 edits;248 confirmed/252 remaining;pages',reviewed)
