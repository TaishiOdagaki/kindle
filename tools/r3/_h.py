# 元docx(v5)の選択肢本文に対する置換パッチ用ヘルパ。R(q,n,old,new) は原文中の old を new に置き換えた全文を返す。
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import quiz_audit as qa
SRC = os.environ.get('R3_SRC', os.path.join(os.path.dirname(__file__), '..', '..', '登録日本語教員試験決定版問題集_v5_修正版.docx'))
_Q = qa.audit(SRC)[1]
def R(q, n, old, new):
    t = _Q[q]['opts'][n - 1]; assert old in t, (q, n, old); return t.replace(old, new, 1)
def A(q, n, add):
    """元の選択肢末尾(句点があればその前)に add を足した全文を返す。"""
    t = _Q[q]['opts'][n - 1]
    return t[:-1] + add + '。' if t.endswith('。') else t + add
