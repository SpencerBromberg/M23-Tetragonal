#!/usr/bin/env python3
"""Exact certificate for global PGL2(Q) height minimality.

This extends the global translate/GL2(Z)-unimodular certificate.  It proves
that any primitive integral matrix representing a rational Mobius change and
producing primitive height <= B has determinant 1 or 2 in absolute value,
then exhausts determinant 2 exactly.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd, comb, isqrt
import json, runpy, sympy as sp

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'global_height_minimality' / 'verify_global_height_minimality.py'
# Re-run the already retained exact certificate.  This certifies the root
# geometry, Julia box, Hutz-Stoll constant, all translates, and determinant 1.
G = runpy.run_path(str(BASE))

f = G['f_asc']; g = G['g_asc']; N = G['N']; B = G['HMIN']
assert N == 23 and B == 1_938_799_398
x = sp.symbols('x')
fpoly = sp.Poly(sum(sp.Integer(c)*x**i for i,c in enumerate(f)), x)

# ---------------------------------------------------------------------------
# 1. Determinant/content cutoff.
# ---------------------------------------------------------------------------
Delta = abs(int(sp.discriminant(fpoly.as_expr(), x)))
R2 = abs(int(sp.resultant(fpoly.as_expr(), sp.diff(fpoly.as_expr(), x, 2), x)))
triple_gcd = gcd(Delta, R2)
assert triple_gcd == (2**44) * (23**23)
print('TRIPLE_ROOT_EXCEPTION_GCD = 2^44 * 23^23 PASS')

# Special-prime value bounds used in the local content lemma.
# At p=2, f(r) == 2 mod 4 for every 2-adic integer r (four residue classes).
assert [int(fpoly.eval(r)) % 4 for r in range(4)] == [2,2,2,2]
print('P2_VALUE_VALUATION_ONE_ALL_RESIDUES_MOD4 PASS')
# At p=23, f mod 23 = x^23-1=(x-1)^23.  On the unique root class,
# f(1)=23*8 mod 23^2 and f'(1)=0 mod 23, so every r=1 mod23 has v23(f(r))=1.
mods = [int(c) % 23 for c in f]
assert mods[0] == 22 and mods[-1] == 1 and all(v == 0 for v in mods[1:-1])
assert int(fpoly.eval(1)) % (23**2) == 184
assert int(fpoly.diff().eval(1)) % 23 == 0
print('P23_UNIQUE_ROOT_CLASS_VALUE_VALUATION_ONE PASS')

# Self-contained Hadamard bound for the discriminant of any degree-23
# primitive polynomial of coefficient height <= B.  Squaring avoids radicals.
S2 = N*(N+1)*(2*N+1)//6
rowF2 = (N+1) * B * B
rowD2 = S2 * B * B
had_sq = (rowF2**(N-1)) * (rowD2**N)
# If C is the content of F o M and D=|det M|, q=D^23/C^2 is an integer
# by the local content estimates in PROOF.md.  Then Delta^2*q^44 <= had_sq.
def iroot(z,k):
    lo,hi=0,1
    while hi**k <= z: hi *= 2
    while hi-lo > 1:
        m=(lo+hi)//2
        if m**k <= z: lo=m
        else: hi=m
    return lo
QMAX = iroot(had_sq // (Delta*Delta), 2*(N-1))
assert QMAX == 76_032_571
assert (Delta*Delta) * (QMAX**44) <= had_sq
assert (Delta*Delta) * ((QMAX+1)**44) > had_sq
assert 3**19 > QMAX
assert 23**21 > QMAX
assert 2**44 > QMAX
print('DISCRIMINANT_HADAMARD_QMAX', QMAX, 'PASS')
print('DETERMINANT_SUPPORT_CUTOFF |det| in {1,2} PASS')

# ---------------------------------------------------------------------------
# 2. Determinant 2.  Hutz-Stoll applies to N/sqrt(2) in SL2(R).
# The retained determinant-1 certificate gives cosh distance < 600,000,000.
# Since u>2, c^2+d^2 < 2*cosh_bound.
# ---------------------------------------------------------------------------
COSH = G['COSH_BOUND']
assert COSH == 600_000_000
BOTTOM = isqrt(2*COSH - 1)
assert BOTTOM == 34_641 and BOTTOM**2 < 2*COSH <= (BOTTOM+1)**2
print('DET2_BOTTOM_ROW_BOUND', BOTTOM, 'PASS')

F_eval = G['F_eval']; small = G['small']; outer = G['outer']; crit = G['crit']; piv = G['piv']
threshold = Q(2*B, 5**N)
# For c>=5, |F(a,c)|<=2B implies a/c lies in one of the certified tiny
# real-root intervals.  Check all possible extrema of the complement exactly.
for S,O in zip(small,outer):
    for e in (S[0],S[1],O[0],O[1]):
        val = Q(abs(F_eval(e.numerator,e.denominator)), e.denominator**N)
        assert val > threshold
for Cc in crit:
    V = piv(f,Cc)
    assert V[1] < -threshold or V[0] > threshold
for e in (Q(-8),Q(8)):
    val = Q(abs(F_eval(e.numerator,e.denominator)), e.denominator**N)
    assert val > 2*B
fp=fpoly.diff()
assert fp.eval(8)>0 and fp.eval(-8)>0 and fpoly.eval(8)>2*B and fpoly.eval(-8)<-2*B
print('DET2_THUE_REGION_REDUCTION PASS')

# Enumerate every possible column (a,c), canonicalized by c>=0, satisfying
# |F(a,c)|<=2B and the forced bottom-coordinate bound.  No gcd condition is
# imposed: determinant-2 primitive matrices can have nonprimitive columns.
cols=set()
# c=0: F(a,0)=a^23.  Derive the exact finite range rather than hard-code it.
aamax=0
while (aamax+1)**N <= 2*B: aamax += 1
assert aamax == 2
for a in range(-aamax,aamax+1):
    if a and abs(F_eval(a,0)) <= 2*B: cols.add((a,0))
for c in range(1,5):
    for a in range(-8*c,8*c+1):
        if abs(F_eval(a,c)) <= 2*B: cols.add((a,c))
for c in range(5,BOTTOM+1):
    for lo,hi in small:
        L=lo*c; U=hi*c
        amin=L.numerator//L.denominator-1
        amax=U.numerator//U.denominator+2
        for a in range(amin,amax+1):
            if lo <= Q(a,c) <= hi and abs(F_eval(a,c)) <= 2*B:
                cols.add((a,c))
cols=sorted(cols)
expected_cols=[(-2,0),(-1,0),(0,1),(1,0),(1,1),(2,0),(2,1)]
assert cols == expected_cols
print('DET2_COLUMN_SOLUTIONS', cols)

# Exact binary substitution.
def compose(M):
    a,b,c,d=M; out=[0]*(N+1)
    for i,fi in enumerate(f):
        if not fi: continue
        p1=[comb(i,k)*a**k*b**(i-k) for k in range(i+1)]
        p2=[comb(N-i,k)*c**k*d**(N-i-k) for k in range(N-i+1)]
        for k1,v1 in enumerate(p1):
            if not v1: continue
            for k2,v2 in enumerate(p2):
                if v2: out[k1+k2] += fi*v1*v2
    return out

signed=set()
for a,c in cols:
    signed.add((a,c)); signed.add((-a,-c))
matrices=[]; below=[]; equal=[]; minH=None; minimizers=[]
for a,c in signed:
    for b,d in signed:
        if abs(a*d-b*c) != 2: continue
        if gcd(gcd(abs(a),abs(b)),gcd(abs(c),abs(d))) != 1: continue
        M=(a,b,c,d); raw=compose(M)
        ct=0
        for z in raw: ct=gcd(ct,abs(z))
        assert ct in (1,2)
        prim=[z//ct for z in raw]
        H=max(abs(z) for z in prim)
        matrices.append((M,ct,H))
        if H < B: below.append((M,ct,H))
        if H == B: equal.append((M,ct,H))
        if minH is None or H < minH: minH=H; minimizers=[(M,ct,H)]
        elif H == minH: minimizers.append((M,ct,H))
assert len(matrices) == 32
assert not below and not equal
assert minH == 372_261_710_848
assert all(ct == 2 for _,ct,_ in matrices)
print('DET2_PRIMITIVE_MATRICES_TESTED', len(matrices))
print('DET2_MINIMUM_HEIGHT', minH)
print('DET2_NO_TIE_OR_IMPROVEMENT PASS')

print('M23_GLOBAL_PGL2Q_HEIGHT_MINIMALITY_PASS')
