import batch5 as _b
def _r(q, n, old, new):
    t = _b.B[q][n]; assert old in t, (q, old); return t.replace(old, new, 1)
B = {'Q_5_102': {4: _r('Q_5_102',4,'適切とされる。','適切とされ、これに反する反応は聞き手の無作法とみなされる。')}}
