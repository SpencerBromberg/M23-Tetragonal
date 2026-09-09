#!/usr/bin/env python3
"""Band-law proposition, numeric side: the valuation bound
   m_j >= ceil((397 - 19j)/23)
reproduces the certified seven-band lower boundary and j-caps exactly,
and the exact adjoints H1, H2 meet it.

Inputs: the exact integer adjoints (v92 files).
Checks:
  V1. ceil((397-19j)/23) equals the band minimum r_min(j) = d_min(j) - j
      with d_min per the caps (d=18 for j<=4; 19 for 5<=j<=10; 20 for
      11<=j<=15; 21 for 16<=j<=21).
  V2. For j >= 16 the bound 21-j exceeds the maximal odd digit 20-j:
      the forbidden odd triangle is forced (a_j even in t for j>=16).
  V3. For H1 and H2: ord_q(a_j) >= ceil((397-19j)/23) for every j, with
      equality at some j (the differential vanishes to order exactly 1).
Marker: M23_BAND_LAW_NUMERIC_PASS
"""
import math, pathlib
import sympy as sp

def rmin(j):
    if j <= 4: return 18 - j
    if j <= 10: return 19 - j
    if j <= 15: return 20 - j
    return 21 - j

for j in range(22):
    c = math.ceil((397 - 19*j)/23)
    assert c == rmin(j), (j, c, rmin(j))
print("V1: ceil((397-19j)/23) = certified band minimum r_min(j) for all "
      "j = 0..21 (caps 4, 10, 15, 21 reproduced): PASS")
for j in range(16, 22):
    assert rmin(j) == 21 - j and 21 - j > 20 - j
print("V2: for j >= 16, minimal digit 21-j exceeds the top odd digit "
      "20-j: forbidden odd triangle forced: PASS")

BASE = pathlib.Path(__file__).resolve().parent
T, V = sp.symbols('t v')
q = sp.Poly(T**2 + 23, T, domain=sp.ZZ)
tight = False
for name in ('M23_H1_integer_v91.txt', 'M23_H2_integer_v91.txt'):
    e = sp.sympify((BASE/name).read_text(),
                   locals={'t': T, 'v': V})
    H = sp.Poly(e, V, domain=sp.ZZ[T])
    for j in range(22):
        cj = sp.Poly(H.nth(j) if j <= H.degree() else 0, T, domain=sp.ZZ)
        if j <= 18:
            aj = cj * q**(18-j)
        else:
            quo, rem = sp.div(cj, q**(j-18), domain=sp.QQ)
            assert sp.Poly(rem, T).is_zero
            aj = sp.Poly(quo, T, domain=sp.QQ)
        if aj.is_zero:
            continue
        m = 0
        cur = aj
        while True:
            quo, rem = sp.div(cur, q, domain=sp.QQ)
            if not sp.Poly(rem, T).is_zero:
                break
            m += 1; cur = sp.Poly(quo, T, domain=sp.QQ)
        bound = math.ceil((397 - 19*j)/23)
        assert m >= bound, (name, j, m, bound)
        if m == bound:
            tight = True
assert tight
print("V3: exact adjoints satisfy ord_q(a_j) >= ceil((397-19j)/23) for "
      "all j, with equality attained: PASS")
print("M23_BAND_LAW_NUMERIC_PASS")
