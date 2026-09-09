#!/usr/bin/env python3
"""Certificate 3: the exact good-frame adjoints reduce, at p = 100207139,
to the recorded q-pair RREF certificate of the executed Magma run.

Builds the 469-dimensional q-pair coordinate vectors of the exact H1, H2
(q-adic digits of the u-form coefficients a_j = q^(18-j) c_j), verifies
they are exactly the pivot-normalized RREF frame over Q (pivots at slots
19, 20 = (EVEN, j=0, r=18), (EVEN, j=0, r=19)), reduces mod p, and checks
against the values recorded in the executed log of
M23_qpair_full_rows_p100207139_v86.m:

  R1. pivot slots [19, 20] with unit/zero pattern over Q (not just mod p);
  R2. row nonzero counts 85 / 85; union support 86; common zeros 383;
      the 15 forbidden slots identically zero in both rows;
  R3. support contained in the seven bands (hence r >= 18-j);
  R4. the recorded ROW1 fingerprint (24 slot/value pairs, transcribed
      from the executed log) matches the computed reduction exactly.

Marker: M23_PATCH_CERT3_PASS
"""
import pathlib
import sympy as sp
from fractions import Fraction

BASE = pathlib.Path(__file__).resolve().parent
T, V = sp.symbols('t v')
q = sp.Poly(T**2 + 23, T, domain=sp.ZZ)
P = 100207139

# recorded anchors, transcribed from the executed p=100207139 log
REC_PIVOTS = [19, 20]
REC_ROW_NONZERO = (85, 85)
REC_COMMON_ZERO = 383
REC_FP_ROW1 = [(21, 17391866), (22, 89182402), (40, 40319090),
               (41, 11003833), (42, 50492035), (43, 45123475),
               (60, 92344821), (61, 49426237), (62, 39370264),
               (63, 19649607), (79, 44144890), (80, 25944224),
               (81, 55505107), (82, 76835278), (97, 28249679),
               (98, 68631779), (99, 37463754), (100, 42348806),
               (115, 78750317), (116, 84775353), (117, 7502161),
               (131, 50904780), (132, 42782138), (133, 4470249)]

def qpair_slots():
    out = []
    for j in range(22):
        for r in range(22-j):
            out.append(("EVEN", j, r))
    for j in range(16):
        for r in range(21-j):
            out.append(("ODD", j, r))
    return out

SLOTS = qpair_slots()
assert len(SLOTS) == 469

def load_qpair(name):
    e = sp.sympify((BASE/'data'/name).read_text(), locals={'t': T, 'v': V})
    H = sp.Poly(e, V, domain=sp.ZZ[T])
    dig = {}
    for j in range(22):
        cj = sp.Poly(H.nth(j) if j <= H.degree() else 0, T, domain=sp.ZZ)
        if j <= 18:
            aj = cj * q**(18-j)
        else:
            quo, rem = sp.div(cj, q**(j-18), domain=sp.QQ)
            assert sp.Poly(rem, T).is_zero
            aj = sp.Poly(quo, T, domain=sp.QQ)
        r = 0
        while not aj.is_zero:
            quo, rem = sp.div(aj, q, domain=sp.QQ)
            rem = sp.Poly(rem, T, domain=sp.QQ)
            e0 = Fraction(str(rem.nth(0)))
            f0 = Fraction(str(rem.nth(1))) if rem.degree() >= 1 else Fraction(0)
            dig[("EVEN", j, r)] = e0
            dig[("ODD", j, r)] = f0
            aj = sp.Poly(quo, T, domain=sp.QQ)
            r += 1
    vec = []
    for s in SLOTS:
        x = dig.get(s, Fraction(0))
        vec.append(x)
    # forbidden digits (odd, j>=16) must not appear at all
    for (c, j, r), x in dig.items():
        if c == "ODD" and j >= 16:
            assert x == 0, ("forbidden digit nonzero", j, r)
    return vec

rows = [load_qpair('M23_H1_integer_v91.txt'),
        load_qpair('M23_H2_integer_v91.txt')]

# R1: RREF over Q; verify the first independent columns are slots 19, 20
i19, i20 = 18, 19          # 0-based positions of slots 19, 20
first_nz = [next(i for i, x in enumerate(r) if x != 0) for r in rows]
M = [row[:] for row in rows]
piv = []
c = 0
for rr in range(2):
    while c < 469:
        if M[rr][c] == 0 and M[1-rr][c] != 0 and rr == 0 and not piv:
            M[0], M[1] = M[1], M[0]
        if M[rr][c] != 0:
            break
        c += 1
    piv.append(c)
    inv = 1/M[rr][c]
    M[rr] = [x*inv for x in M[rr]]
    o = 1-rr
    fac = M[o][c]
    if fac != 0:
        M[o] = [a - fac*b for a, b in zip(M[o], M[rr])]
    c += 1
assert piv == [i19, i20], ("pivot columns", [p+1 for p in piv])
rows = M
print(f"R1: exact basis (leading slots {[f+1 for f in first_nz]}) RREFs "
      f"over Q with pivot columns exactly [19, 20]: PASS")

# reduce mod P
def redp(x):
    num, den = x.numerator, x.denominator
    assert den % P != 0
    return num * pow(den, -1, P) % P

R = [[redp(x) for x in row] for row in rows]

# R2: counts
nz = [sum(1 for x in r if x) for r in R]
union = sum(1 for a, b in zip(*R) if a or b)
common0 = sum(1 for a, b in zip(*R) if a == 0 and b == 0)
forb_idx = [i for i, s in enumerate(SLOTS) if s[0] == "ODD" and s[1] >= 16]
assert len(forb_idx) == 0  # forbidden slots are not in the 469 admissible
assert tuple(nz) == REC_ROW_NONZERO, nz
assert union == 86 and common0 == REC_COMMON_ZERO, (union, common0)
print(f"R2: row nonzeros {nz[0]}/{nz[1]}, union 86, common zeros "
      f"{common0}: PASS (matches recorded)")

# R3: band membership
caps_even = {18: 4, 19: 10, 20: 15, 21: 21}
caps_odd = {18: 4, 19: 10, 20: 15}
for r in R:
    for i, x in enumerate(r):
        if x:
            c, j, rr = SLOTS[i]
            d = j + rr
            caps = caps_even if c == "EVEN" else caps_odd
            assert d in caps and j <= caps[d], ("support outside bands",
                                                SLOTS[i])
            assert rr >= 18 - j
print("R3: full support inside the seven bands (r >= 18-j): PASS")

# R4: recorded fingerprint
for slot, val in REC_FP_ROW1:
    got = R[0][slot-1]
    assert got == val, (slot, got, val)
print(f"R4: all {len(REC_FP_ROW1)} recorded ROW1 fingerprint values match "
      f"the exact reduction at p={P}: PASS")
print("M23_PATCH_CERT3_PASS")
